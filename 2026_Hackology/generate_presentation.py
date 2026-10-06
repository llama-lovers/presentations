"""Generate Hackology II Team 08 presentation PDF matching the minimal style."""
import math
from fpdf import FPDF
from fpdf.enums import RenderStyle

# ── colours ───────────────────────────────────────────────────────────────────
BG       = (245, 246, 248)
WHITE    = (255, 255, 255)
CARD_BG  = (249, 250, 251)
BORDER   = (220, 224, 230)
BLUE     = (59, 130, 246)
ORANGE   = (245, 158, 11)
GREEN    = (16, 185, 129)
BLACK    = (20, 20, 20)
GRAY     = (107, 114, 128)
DARKGRAY = (55, 65, 81)
BULLET   = BLUE

W, H = 297, 210
MARGIN = 18
FOOTER_Y = H - 12

FONT_DIR = "/Users/Illia/Library/Fonts"
FONT_R = f"{FONT_DIR}/Helvetica.ttf"
FONT_B = f"{FONT_DIR}/Helvetica-Bold.ttf"


class Deck(FPDF):
    def __init__(self):
        super().__init__(orientation="L", unit="mm", format="A4")
        self.set_auto_page_break(False)
        self.set_margins(0, 0, 0)
        self.add_font("Hv", style="",  fname=FONT_R)
        self.add_font("Hv", style="B", fname=FONT_B)

    def slide_bg(self):
        self.set_fill_color(*BG)
        self.rect(0, 0, W, H, "F")

    def footer_line(self, page_n, total):
        self.set_font("Hv", "", 7.5)
        self.set_text_color(*GRAY)
        self.text(MARGIN, FOOTER_Y, "Hackology 2026 · Team 08")
        label = f"{page_n}/{total}"
        self.text(W - MARGIN - self.get_string_width(label), FOOTER_Y, label)

    def card(self, x, y, w, h, fill=None, border=True):
        fill = fill or CARD_BG
        self.set_fill_color(*fill)
        if border:
            self.set_draw_color(*BORDER)
            self.set_line_width(0.25)
        else:
            self.set_draw_color(*fill)
        rs = RenderStyle.DF if border else RenderStyle.F
        self._draw_rounded_rect(x, y, w, h, rs, True, 4)

    def heading(self, title, subtitle="", y_title=14):
        self.set_font("Hv", "B", 28)
        self.set_text_color(*BLACK)
        self.set_xy(MARGIN, y_title)
        self.cell(W - 2*MARGIN, 12, title, ln=True)
        if subtitle:
            self.set_font("Hv", "", 11)
            self.set_text_color(*GRAY)
            self.set_x(MARGIN)
            self.cell(W - 2*MARGIN, 7, subtitle, ln=True)

    def bullet_list(self, items, x, y, w, line_h=6.5, dot_color=BLUE):
        self.set_font("Hv", "", 10)
        self.set_text_color(*DARKGRAY)
        for item in items:
            self.set_fill_color(*dot_color)
            self.ellipse(x + 1.5, y + line_h/2 - 1.75, 3.5, 3.5, "F")
            self.set_xy(x + 8, y)
            self.multi_cell(w - 8, line_h, item, align="L")
            y = self.get_y() + 1.5

    def metric_card(self, x, y, w, h, value, label, color=BLUE):
        self.card(x, y, w, h, fill=WHITE)
        self.set_font("Hv", "B", 38)
        self.set_text_color(*color)
        self.set_xy(x + 6, y + 8)
        self.cell(w - 12, 20, str(value), align="L")
        self.set_font("Hv", "", 10)
        self.set_text_color(*GRAY)
        self.set_xy(x + 6, y + 32)
        self.multi_cell(w - 12, 5, label)

    def info_card(self, x, y, w, h, title, body, title_color=BLACK):
        self.card(x, y, w, h, fill=WHITE)
        self.set_font("Hv", "B", 12)
        self.set_text_color(*title_color)
        self.set_xy(x + 8, y + 8)
        self.cell(w - 16, 7, title)
        self.set_font("Hv", "", 10)
        self.set_text_color(*GRAY)
        self.set_xy(x + 8, y + 17)
        self.multi_cell(w - 16, 5.5, body, align="L")

    def draw_arrow(self, x1, y1, x2, y2):
        self.set_draw_color(*BLUE)
        self.set_line_width(0.6)
        self.line(x1, y1, x2, y2)
        ah, ax = 3, math.radians(28)
        angle = math.atan2(y2 - y1, x2 - x1)
        self.line(x2, y2,
                  x2 - ah * math.cos(angle - ax),
                  y2 - ah * math.sin(angle - ax))
        self.line(x2, y2,
                  x2 - ah * math.cos(angle + ax),
                  y2 - ah * math.sin(angle + ax))

    def tag(self, x, y, label, fill_rgb, text_rgb=(30, 30, 30)):
        self.set_font("Hv", "B", 9)
        tw = self.get_string_width(label)
        pw, ph = tw + 10, 8
        self.set_fill_color(*fill_rgb)
        self.set_draw_color(*fill_rgb)
        self._draw_rounded_rect(x, y, pw, ph, RenderStyle.F, True, 4)
        self.set_text_color(*text_rgb)
        self.text(x + 5, y + ph - 2, label)
        return pw + 5


def build(out_path: str):
    pdf = Deck()
    TOTAL = 7

    # ══════════════════════════════════════════════════════════════════════════
    # Slide 1 — title
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.slide_bg()

    pdf.set_font("Hv", "B", 12)
    pdf.set_text_color(*BLUE)
    pdf.text(MARGIN, 18, "Team 08")

    pdf.set_font("Hv", "B", 36)
    pdf.set_text_color(*BLACK)
    pdf.set_xy(MARGIN, 26)
    pdf.cell(165, 16, "Od modeli YOLO")
    pdf.set_xy(MARGIN, 42)
    pdf.cell(165, 16, "do agregacji predykcji")

    pdf.set_font("Hv", "", 12)
    pdf.set_text_color(*GRAY)
    pdf.text(MARGIN, 66, "Hackology 2026 · Team 08 · YOLOv11l + WBF ensemble · 369 klas · +130% vs baseline")

    # Metric card — matching reference proportions
    cx, cy, cw, ch = 192, 28, 88, 62
    pdf.card(cx, cy, cw, ch, fill=WHITE)
    pdf.set_font("Hv", "B", 44)
    pdf.set_text_color(*BLUE)
    pdf.set_xy(cx + 8, cy + 7)
    pdf.cell(cw - 16, 22, "0.7420")
    pdf.set_font("Hv", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(cx + 8, cy + 44)
    pdf.cell(cw - 16, 6, "najlepszy uzyskany wynik mAP@0.5")

    tags = [
        ("YOLO variants",   (219, 234, 254)),
        ("fine-tuning",     (209, 250, 229)),
        ("pseudo-labeling", (254, 243, 199)),
        ("ensemble",        (220, 238, 255)),
    ]
    tx = MARGIN
    for label, color in tags:
        tx += pdf.tag(tx, 148, label, color)

    pdf.footer_line(1, TOTAL)

    # ══════════════════════════════════════════════════════════════════════════
    # Slide 2 — quick pipeline baseline
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.slide_bg()
    pdf.heading("1. Punkt startowy: szybki pipeline",
                "Najpierw sprawdziliśmy, które warianty YOLO i ustawienia dają sensowny kierunek.")

    card_w, card_h = 56, 45
    usable = W - 2 * MARGIN
    stride = (usable - card_w) / 3
    flow_labels = [
        ("YOLOv8 / YOLO11", "różne rozmiary modeli"),
        ("imgsz",           "640, 768, 960, 1280"),
        ("trening",         "lr, optimizer,\naugmentacje"),
        ("submission",      "mAP@0.5"),
    ]
    cy_flow = 55
    for i, (title, body) in enumerate(flow_labels):
        cx = MARGIN + i * stride
        pdf.info_card(cx, cy_flow, card_w, card_h, title, body, title_color=BLUE)
        if i < 3:
            mid_y = cy_flow + card_h / 2
            pdf.draw_arrow(cx + card_w + 2, mid_y, cx + stride - 3, mid_y)

    # Summary card
    sy = 110
    pdf.card(MARGIN, sy, W - 2*MARGIN, 65, fill=WHITE)
    pdf.set_font("Hv", "B", 11)
    pdf.set_text_color(*BLACK)
    pdf.set_xy(MARGIN + 8, sy + 8)
    pdf.cell(W - 2*MARGIN - 16, 7, "Wniosek z etapu pojedynczych modeli")
    pdf.bullet_list([
        "Pierwszy krok: naiwny fine-tuning YOLO11l na oryginalnych danych (imgsz=640, domyślne "
        "hiperparametry) — wynik mAP@0.5 = 0.3221 i pierwsze miejsce na początku konkursu.",
        "Odkrycie: sweep imgsz inferencji bez retreningu — model trenowany na 640px daje mAP 0.83 "
        "przy 960px vs 0.80 przy 640px. Reguła: imgsz_opt ≈ 1.5x imgsz treningowy.",
        "Postęp iteracyjny: augmentacje (mosaic, mixup) -> 0.65; pseudo-labeling x2 rundy "
        "na zbiorze testowym -> 0.72; WBF z 5 źródeł -> 0.7420 (final tag).",
    ], MARGIN + 8, sy + 17, W - 2*MARGIN - 16)

    pdf.footer_line(2, TOTAL)

    # ══════════════════════════════════════════════════════════════════════════
    # Slide 3 — models in ensemble (clean table, matching reference)
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.slide_bg()
    pdf.heading("2. Co finalnie trafiło do agregacji?",
                "Z logów: 4 unikalne pliki wag oraz 5 źródeł predykcji w ensemble.")

    cols = [("Model / wagi", 79), ("Architektura", 40), ("Trening", 71), ("Użycie w ensemble", 71)]
    tx, ty = MARGIN, 46
    # Header
    pdf.set_fill_color(*CARD_BG)
    pdf.set_draw_color(*BORDER)
    pdf.set_line_width(0.2)
    pdf.set_font("Hv", "B", 9.5)
    pdf.set_text_color(*BLUE)
    rx = tx
    for label, cw in cols:
        pdf.rect(rx, ty, cw, 10, "FD")
        pdf.set_xy(rx + 3, ty + 2)
        pdf.cell(cw - 6, 6, label)
        rx += cw

    rows = [
        ("best_opus_pseudo_ft.pt",   "YOLO11L, 25.6M",   "pseudo-label r2, imgsz 768, AdamW", "960 w=2.0 + 768 w=1.0"),
        ("pseudo_r2_20260524.pt",    "YOLO11L, 25.6M",   "imgsz 1280, lr 0.0001",        "960 w=2.0"),
        ("best_pseudo_refit_v1.pt",  "YOLO11L, 25.6M",   "pseudo-labeling, AdamW",       "1280 w=0.5"),
        ("best_yolo11m_dpr_ft.pt",   "YOLO11M, 20.3M",   "DPR fine-tune, batch 16",      "1280 w=0.5"),
    ]
    pdf.set_font("Hv", "", 9.5)
    pdf.set_text_color(*DARKGRAY)
    for ri, row in enumerate(rows):
        ry = ty + 10 + ri * 11
        fill = WHITE if ri % 2 == 0 else CARD_BG
        rx = tx
        for val, cw in zip(row, [c[1] for c in cols]):
            pdf.set_fill_color(*fill)
            pdf.rect(rx, ry, cw, 11, "FD")
            pdf.set_xy(rx + 3, ry + 3)
            pdf.cell(cw - 6, 5, val)
            rx += cw

    # Plain text note at bottom — matching reference style
    note_y = H - 35
    pdf.set_font("Hv", "", 10.5)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(MARGIN, note_y)
    pdf.multi_cell(W - 2*MARGIN, 6,
        "Idea: zamiast ufać jednemu modelowi, łączymy kilka modeli trenowanych na różnych "
        "wariantach danych i uruchamianych z różną rozdzielczością. "
        "WBF (iou_thr=0.7) uśrednia pozycje boxów zamiast wybierać jeden.")

    pdf.footer_line(3, TOTAL)

    # ══════════════════════════════════════════════════════════════════════════
    # Slide 4 — why ensemble
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.slide_bg()
    pdf.heading("3. Dlaczego uważaliśmy, że agregacja zadziała?",
                "Mieliśmy konkretne powody techniczne — nie zgadywaliśmy.")

    # Left scheme card — matching reference proportions
    lx, ly, lw, lh = MARGIN, 46, 115, 130
    pdf.card(lx, ly, lw, lh, fill=WHITE)

    pdf.set_font("Hv", "B", 13)
    pdf.set_text_color(*BLACK)
    pdf.set_xy(lx + 8, ly + 9)
    pdf.cell(lw - 16, 8, "Schemat")

    sources = ["predykcje modelu A", "predykcje modelu B", "predykcje modelu C"]
    for i, label in enumerate(sources):
        ey = ly + 32 + i * 22
        pdf.set_font("Hv", "", 9.5)
        pdf.set_text_color(*DARKGRAY)
        pdf.text(lx + 8, ey, label)

    # NMS/fusion box
    fx, fy, fw, fh = lx + lw - 34, ly + 40, 26, 20
    pdf.card(fx, fy, fw, fh, fill=CARD_BG)
    pdf.set_font("Hv", "B", 9)
    pdf.set_text_color(*BLUE)
    pdf.set_xy(fx + 2, fy + 5)
    pdf.cell(fw - 4, 5, "NMS /", align="C")
    pdf.set_xy(fx + 2, fy + 11)
    pdf.cell(fw - 4, 5, "fusion", align="C")

    # Lines from labels to fusion box
    pdf.set_draw_color(100, 130, 200)
    pdf.set_line_width(0.5)
    target_y = fy + fh / 2
    for i in range(3):
        ey = ly + 32 + i * 22 - 1
        lw_text = pdf.get_string_width(sources[i])
        pdf.line(lx + 8 + lw_text + 2, ey, fx, target_y)

    # Arrow from NMS to output
    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.8)
    pdf.draw_arrow(fx + fw, fy + fh/2, lx + lw - 4, fy + fh/2)

    # Bottom legend — simple text, matching reference
    pdf.set_font("Hv", "B", 10)
    pdf.set_text_color(*BLACK)
    pdf.text(lx + 8, ly + lh - 22, "Ważone predykcje:")
    pdf.set_font("Hv", "", 9.5)
    pdf.set_text_color(*GRAY)
    pdf.text(lx + 8, ly + lh - 14, "większa waga = większe zaufanie do źródła")

    # Right info cards — NO background (floating on gray, matching reference)
    rx2 = lx + lw + 10
    rw = W - rx2 - MARGIN
    right_items = [
        ("Różne rozdzielczości",
         "960 i 1280 px pomagają inaczej łapać małe oraz większe obiekty na tej samej półce."),
        ("Różne treningi",
         "pseudo-labeling i fine-tuning zmieniają rozkład błędów — inne FP, inne FN."),
        ("Ważenie modeli",
         "mocniejsze źródła (val 0.83) dostają wagę 2x, słabsze (val 0.74) — wagę 0.5."),
        ("Mniej przypadkowości",
         "pojedynczy false positive ma mniejszą szansę przebić się przez agregację WBF."),
    ]
    card_gap = 4
    rh_each = int((lh - card_gap * 3) / 4)
    for i, (title, body) in enumerate(right_items):
        pdf.info_card(rx2, ly + i * (rh_each + card_gap), rw, rh_each, title, body)

    pdf.footer_line(4, TOTAL)

    # ══════════════════════════════════════════════════════════════════════════
    # Slide 5 — results
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.slide_bg()
    pdf.heading("4. Najlepszy wynik i interpretacja",
                "Główna metryka: mAP@0.5 (im wyżej, tym lepiej). Final tag = commit 1693fcb.")

    metrics = [
        ("0.7420", "finalny najlepszy wynik Team 08",      BLUE),
        ("5",      "źródeł predykcji w agregacji",         GREEN),
        ("4",      "unikalne pliki wag",                   ORANGE),
    ]
    mw = (W - 2*MARGIN - 16) / 3
    for i, (val, label, color) in enumerate(metrics):
        pdf.metric_card(MARGIN + i * (mw + 8), 50, mw, 58, val, label, color)

    cy2 = 116
    pdf.card(MARGIN, cy2, W - 2*MARGIN, 76, fill=WHITE)
    pdf.set_font("Hv", "B", 11)
    pdf.set_text_color(*BLACK)
    pdf.set_xy(MARGIN + 8, cy2 + 8)
    pdf.cell(W - 2*MARGIN - 16, 7, "Komentarz do rezultatu")
    pdf.bullet_list([
        "Wynik 0.7420 oznacza, że finalna agregacja WBF była skuteczniejsza niż traktowanie "
        "pojedynczego modelu jako jedynego źródła prawdy (+130% vs naive baseline 0.3221).",
        "Kluczowy kompromis: 8 źródeł poprawiło val mAP (+1.5pp), ale pogorszyło public "
        "(-0.4pp) przez maxDets=100. Wybraliśmy 5 źródeł po analizie tego efektu.",
        "Koszt ensemble: 8.5 min / 481 obrazów (T4) vs ~2 min single model — 4x wolniej. "
        "Mieści się w limicie 30 min; świadomy kompromis: +5pp mAP za dłuższy czas inferencji.",
        "Gap val->public: 0.8528->0.7420 (ratio 0.87). Przy 8 źródłach val +1.5pp, "
        "ale public -0.4pp — maxDets=100 faworyzuje mniej, lecz pewniejsze predykcje.",
    ], MARGIN + 8, cy2 + 17, W - 2*MARGIN - 16)

    pdf.footer_line(5, TOTAL)

    # ══════════════════════════════════════════════════════════════════════════
    # Slide 6 — summary (matching reference slide 6 style)
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.slide_bg()
    pdf.heading("5. Podsumowanie i wnioski",
                "Od naiwnego baseline do komplementarnego ensemble — co zadziałało i dlaczego.")

    # "Najkrócej" card
    pdf.card(MARGIN, 42, W - 2*MARGIN, 36, fill=WHITE)
    pdf.set_font("Hv", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.set_xy(MARGIN + 8, 50)
    pdf.cell(W - 2*MARGIN - 16, 6, "Najkrócej")
    pdf.set_font("Hv", "", 10.5)
    pdf.set_text_color(*DARKGRAY)
    pdf.set_xy(MARGIN + 8, 58)
    pdf.multi_cell(W - 2*MARGIN - 16, 6,
        "Zaczęliśmy od szybkiego baseline (0.3221) żeby sprawdzić, że pipeline działa. "
        "Finalnie najlepszy efekt dała agregacja WBF kilku modeli YOLO z różnymi "
        "ustawieniami, rozdzielczościami i wagami — wynik 0.7420 public mAP@0.5.")

    # 3 column cards
    col_w = (W - 2*MARGIN - 2*8) / 3
    col_data = [
        ("Co działało", BLUE, [
            "fine-tuning YOLO11l",
            "pseudo-labeling (2 rundy)",
            "ensemble WBF zamiast single model",
        ]),
        ("Dlaczego", GREEN, [
            "modele widzą dane inaczej",
            "różne rozdzielczości inferencji",
            "redukcja losowych FP przez agregację",
        ]),
        ("Pułapki i limity", ORANGE, [
            "maxDets=100 tnie recall — gęste półki nierozwiązane",
            "więcej źródeł WBF hurt public przez FP w top-100",
            "val mAP != public mAP — nie optymalizuj val naiwnie",
        ]),
    ]
    cy_cols = 85
    col_h = 72
    for i, (title, color, items) in enumerate(col_data):
        cx = MARGIN + i * (col_w + 8)
        pdf.card(cx, cy_cols, col_w, col_h, fill=WHITE)
        pdf.set_font("Hv", "B", 11)
        pdf.set_text_color(*color)
        pdf.set_xy(cx + 8, cy_cols + 8)
        pdf.cell(col_w - 16, 6, title)
        pdf.bullet_list(items, cx + 8, cy_cols + 17, col_w - 16, line_h=6, dot_color=color)

    # Bold footer text — matching reference
    pdf.set_font("Hv", "B", 10)
    pdf.set_text_color(*BLACK)
    pdf.set_xy(MARGIN, 164)
    pdf.multi_cell(W - 2*MARGIN, 5.5,
        "Finalny przekaz: wynik 0.7420 uzyskano dzięki połączeniu komplementarnych "
        "modeli, a nie przez jedną zmianę hiperparametru.")

    pdf.footer_line(6, TOTAL)

    # ══════════════════════════════════════════════════════════════════════════
    # Slide 7 — możliwości dalszego rozwoju
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.slide_bg()
    pdf.heading("6. Możliwości dalszego rozwoju",
                "Co można poprawić przy więcej czasu lub zasobów obliczeniowych.")

    proposals = [
        ("SAHI tile inference",
         "Sliding window 1280×1280 px dla gęstych półek (>100 produktów/zdjęcie). "
         "Eliminuje hard ceiling maxDets=100 — potencjał +5-10pp dla najtrudniejszych obrazów."),
        ("Confidence calibration per-class",
         "Kalibracja progów confidence dla każdej z 369 klas osobno. "
         "Zmniejsza FP między wariantami tej samej marki (np. Pepsi 0.33L vs 0.5L)."),
        ("Hierarchia taksonomii",
         "Grupowanie 369 klas wg brand + typ + pojemność, potem two-stage detect+classify. "
         "Precyzyjniejsza klasyfikacja wariantów przy zachowaniu szybkości detekcji."),
        ("Więcej danych i pseudo-labeling r3",
         "Dane syntetyczne (SDXL) dla rzadkich klas (<5 próbek). "
         "Trzecia runda pseudo-labelingu na zbiorze rozszerzonym o trudne przypadki."),
    ]
    pw = (W - 2*MARGIN - 8) / 2
    ph = 60
    for i, (title, body) in enumerate(proposals):
        cx = MARGIN + (i % 2) * (pw + 8)
        cy = 46 + (i // 2) * (ph + 6)
        pdf.info_card(cx, cy, pw, ph, title, body, title_color=BLUE)

    pdf.footer_line(7, TOTAL)

    pdf.output(out_path)
    print(f"Saved: {out_path}  ({pdf.page} pages)")


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(__file__), "hackology2_team08.pdf")
    build(out)
