---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 22px;
    background: #ffffff;
  }
  h1 { color: #1a3a5c; font-size: 2em; margin-bottom: 0.2em; }
  h2 { color: #2563a8; font-size: 1.4em; border-bottom: 2px solid #2563a8; padding-bottom: 4px; }
  table { width: 100%; border-collapse: collapse; font-size: 0.85em; }
  th { background: #2563a8; color: white; padding: 6px 10px; }
  td { padding: 5px 10px; border: 1px solid #ddd; }
  tr:nth-child(even) { background: #f0f4ff; }
  .highlight { color: #d97706; font-weight: bold; }
  code { background: #f1f5f9; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }
  pre { background: #1e293b; color: #e2e8f0; padding: 12px; border-radius: 6px; }
  .lead { font-size: 0.9em; color: #555; }
---

# Hackology II — Team 08
## Detektor produktów na półkach sklepowych

**mAP@0.5 (public) = 0.7420** · +130% vs baseline

*Illia Bahlai · Hackology 2026*

---

## 1. Problem i dane

**Zadanie:** automatyczna detekcja i klasyfikacja produktów na zdjęciach półek sklepowych

| | Wartość |
|---|---|
| Kategorie | **369** (brand × typ × pojemność) |
| Obrazy train | ~2 000 (real + synthetic SIDG) |
| Obrazy test | **481** (~3024 × 4032 px) |
| Metryka | mAP@0.5 (COCO, maxDets=100/img) |

**Wyzwania domenowe**
- Gęste upakowanie: do 150+ produktów na jednym zdjęciu
- Wizualne podobieństwo wariantów (np. Pepsi 0.33L vs 0.5L)
- Niezbalansowanie klas — rzadkie kategorie mają <5 próbek

---

## 2. Pipeline treningu

Trzy iteracje — każda buduje na poprzedniej:

```
[YOLOv11l baseline]  →  [Killer fine-tune]  →  [Pseudo-labeling ×2]
    mAP 0.32               mAP 0.65              mAP 0.73+
```

**Etap 1 — Baseline fine-tuning**
`YOLOv11l` na danych train + synthetic, `imgsz=640`, conf sweep → 0.32 public

**Etap 2 — Killer pipeline**
Agresywny augmentation, mosaic, mixup, copy-paste → `yolov11l_killer` → 0.65 public

**Etap 3 — Pseudo-labeling loop**
1. Najlepszy model etykietuje public test (silver labels)
2. Retrenujemy na real + pseudo → `pseudo_v1`, `pseudo_refit`
3. Drugi round → **`opus_pseudo`** (val 0.881 single-model best)

---

## 3. Kluczowy insight — skala inferencji

Model trenowany na **640 px**, ale zdjęcia mają ~3024 × 4032 px.

**Sweep val mAP@0.5 przy różnych imgsz:**

```
imgsz:  640   768   960   1280  1600
mAP:   0.80  0.83  0.83  0.79  0.75
              ^^^^  ^^^^
             OPTIMUM
```

**Dlaczego 768–960 > 1280?**
- Przy 960 px: typowy produkt (~200 px na oryginale) → ~60 px w sieci → w zasięgu head
- Przy 1280+: YOLO interpoluje z bardzo dużych resolutionów → szum, alias artefakty
- Przy 640: za mało pikseli na mały produkt w rogu kadru

> Zasada: `imgsz_optymalne ≈ training_imgsz × 1.5`

---

## 4. WBF Ensemble — 5 źródeł z TTA

**Weighted Box Fusion** (WBF) zamiast NMS — uśrednia pozycje boxów w klastrach

### Konfiguracja finalna (public 0.7420)

| Źródło | Skala | Waga | Val mAP (single) |
|--------|-------|------|-----------------|
| `opus_pseudo` | 960 px | **2.0** | 0.8285 |
| `opus_pseudo` | 768 px | 1.0 | 0.8286 |
| `pseudo_v2` | 960 px | **2.0** | 0.8022 |
| `pseudo_v1` | 1280 px | 0.5 | — |
| `dpr_ft` | 1280 px | 0.5 | — |

`iou_wbf=0.7 · TTA (flip+scale) · cap=300/img`

**Kluczowy kompromis odkryty empirycznie:**
8 źródeł → val 0.8676 (**+1.5pp**) → ale public 0.7377 (**−0.4pp**)
Przyczyna: więcej źródeł = więcej low-conf FP w top-100 → gorsza precyzja

---

## 5. Wyniki — progression i porównanie

**Historia publicznego mAP@0.5:**

```
0.32  ──── baseline YOLOv8 ──────────────────────────────────
0.43  ──── pierwsze fine-tuning ────────────────────────────
0.65  ──── killer pipeline ─────────────────────────────────
0.72  ──── single opus_pseudo ───────────────────────────────
0.74  ════ 5-src TTA WBF  ◄ FINAL (0.7420)  ════════════════
```

**Porównanie konfiguracji ensemble:**

| Config | Val mAP | Public mAP | Preds/img |
|--------|---------|------------|-----------|
| **5-src TTA WBF** | 0.8528 | **0.7420** | 57.7 |
| 8-src TTA WBF | 0.8676 | 0.7377 | 65.6 |
| Killer-heavy WBF | 0.8786 | 0.7322 | >100 |
| Single model | 0.8285 | ~0.73 | ~28 |

---

## 6. Analiza błędów i ograniczenia

**Hard ceiling — dense shelves**
55 / 481 obrazów testowych ma >100 produktów → limit `maxDets=100` ucina TP
Nie da się poprawić bez zmiany metryki lub tile inference (SAHI)

**False positives — podobne warianty**
369 kategorii × wizualne podobieństwo = wysokie FP między wariantami tej samej marki
Rozwiązanie: two-stage detect+classify lub hierarchia taksonomii

**Val → public gap (13pp)**
- Val: 0.8528 → Public: 0.7420 (ratio 0.87)
- Public test ma trudniejszą dystrybucję (inne oświetlenie, kąty)
- Overfitting val przez zbyt wiele źródeł (8-src hurt public)

**Czas inferencji**
5-model WBF + TTA ≈ 12 min / 481 img na T4 GPU → mieści się w 30-min limicie

---

## 7. Potencjał wdrożeniowy

**Gotowe do uruchomienia:**
```bash
uv sync --locked
uv run predict --input <dir> --output predictions.json
```
Automatyczne pobieranie wag z HF Hub `L3M0H/hackology-2-detector`

**Reprodukowalność:**
- `uv.lock` locked dependencies
- Versioned weights: `best_{timestamp}_{pipeline}.pt`
- CI/CD: GitHub Actions auto-submit po push do `submissions/`

**Co dalej (poza zakresem hackathonu):**

| Technika | Potencjalny gain | Koszt |
|----------|-----------------|-------|
| SAHI tile inference | +5-10pp dla gęstych półek | 3× wolniej |
| Confidence calibration | lepszy ranking FP/TP | 1-2 dni |
| Hierarchia taksonomii | mniej FP w wariantach | retraining |
| Two-stage detect+classify | +precision | ~1 tydzień |
