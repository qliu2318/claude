# -*- coding: utf-8 -*-
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn

NAVY   = RGBColor(0x1F, 0x3B, 0x5B)
BLUE   = RGBColor(0x2E, 0x5E, 0x8C)
TEAL   = RGBColor(0x1B, 0x7F, 0x79)
GREEN  = RGBColor(0x2E, 0x7D, 0x32)
RED    = RGBColor(0xB0, 0x3A, 0x2E)
AMBER  = RGBColor(0xC8, 0x7F, 0x0A)
LAMBER = RGBColor(0xF1, 0xD9, 0xA8)
LGREY  = RGBColor(0xEC, 0xEF, 0xF3)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
DARKTX = RGBColor(0x20, 0x28, 0x33)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank


def box(x, y, w, h, text, fill, fg=WHITE, size=12, bold=True,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, line=None):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    sp.line.color.rgb = line if line else fill
    sp.line.width = Pt(1)
    sp.shadow.inherit = False
    tf = sp.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Pt(4); tf.margin_right = Pt(4)
    tf.margin_top = Pt(2); tf.margin_bottom = Pt(2)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.color.rgb = fg; r.font.name = "Microsoft YaHei"
    return sp


def label(x, y, w, h, text, size=10, color=DARKTX, italic=False, bold=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.color.rgb = color
    r.font.italic = italic; r.font.bold = bold
    r.font.name = "Microsoft YaHei"
    return tb


def conn(p1, p2, color=RGBColor(0x5A, 0x6B, 0x7B), width=1.5, dashed=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                   Inches(p1[0]), Inches(p1[1]),
                                   Inches(p2[0]), Inches(p2[1]))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    c.shadow.inherit = False
    ln = c.line._get_or_add_ln()
    if dashed:
        d = ln.makeelement(qn('a:prstDash'), {'val': 'dash'}); ln.append(d)
    else:
        te = ln.makeelement(qn('a:tailEnd'),
                             {'type': 'triangle', 'w': 'med', 'len': 'med'})
        ln.append(te)
    return c


def bc(s):  # bottom-center (inches)
    return (s.left + s.width / 2) / 914400, (s.top + s.height) / 914400


def tc(s):  # top-center
    return (s.left + s.width / 2) / 914400, s.top / 914400


def lc(s):
    return s.left / 914400, (s.top + s.height / 2) / 914400


def rc(s):
    return (s.left + s.width) / 914400, (s.top + s.height / 2) / 914400


SW = 13.333
# Title band
box(0.3, 0.12, SW - 0.6, 0.60,
    "技术路线图 — LLM 大模型接入对消费者借贷行为的影响",
    NAVY, WHITE, 20, True, MSO_SHAPE.RECTANGLE)

# L0  X
X = box(4.267, 0.92, 4.8, 0.60,
        "X｜LLM 大模型接入·数字信贷触达升级", NAVY, WHITE, 14)

# L1  mechanisms
M1 = box(2.467, 1.78, 3.6, 0.56, "机制①  意向识别能力 ↑", TEAL, WHITE, 12)
M2 = box(7.267, 1.78, 3.6, 0.56, "机制②  个性化劝说力 ↑", TEAL, WHITE, 12)

# L2  dual outcome
YA = box(0.45, 2.66, 3.5, 0.80,
         "Y-A 信贷可得性 ↑\n更多人·更易借到", GREEN, WHITE, 12)
YB = box(9.383, 2.66, 3.5, 0.80,
         "Y-B 金融脆弱性 ↑\n重复借贷·多头·逾期违约", RED, WHITE, 12)
label(5.0, 2.30, 3.333, 0.32, "—— 双刃张力 ——", 12, RGBColor(0x8A, 0x4B, 0x08), True, True)
conn(rc(YA), lc(YB), RGBColor(0x8A, 0x4B, 0x08), 1.5, dashed=True)

# L3  fragility source diamond
DM = box(5.717, 3.66, 1.9, 1.0, "脆弱性\n来源分解", AMBER, WHITE, 11,
         shape=MSO_SHAPE.DIAMOND)

# L3b decomposition
C1 = box(3.55, 4.85, 2.9, 0.62, "组成·外延\n更脆弱人群被卷入",
         LAMBER, DARKTX, 11)
C2 = box(6.883, 4.85, 2.9, 0.62, "行为·内涵\n同类人借贷恶化",
         LAMBER, DARKTX, 11)

# L4 identification chain
B1 = box(0.52, 5.66, 3.95, 0.80,
         "第一章·微观 马消客户级\nStacked RD-in-time + DFL 分解", BLUE, WHITE, 11)
B2 = box(4.69, 5.66, 3.95, 0.80,
         "第二章·中观 裁判文书+扩散代理\n双向FE + Bartik IV", BLUE, WHITE, 11)
B3 = box(8.86, 5.66, 3.95, 0.80,
         "第三章·宏观 CHFS/CFPS\n监管DDD + 2SLS", BLUE, WHITE, 11)

# L5 policy + bottom band (single band)
band = box(0.3, 6.62, SW - 0.6, 0.60,
           "结论与政策：智能信贷触达让更多人借到钱——是否也让更多人陷进去？  "
           "金融AI消费者保护 · 共债治理", NAVY, WHITE, 12, True, MSO_SHAPE.RECTANGLE)

# Connectors
conn(bc(X), tc(M1)); conn(bc(X), tc(M2))
conn(bc(M1), tc(YA)); conn(bc(M2), tc(YB))
conn(bc(M1), (rc(YB)[0]-0.2, tc(YB)[1]), RGBColor(0x9A,0xA7,0xB2), 1.0)
conn(bc(M2), (lc(YA)[0]+0.2, tc(YA)[1]), RGBColor(0x9A,0xA7,0xB2), 1.0)
conn(bc(YB), tc(DM))
conn(bc(DM), tc(C1)); conn(bc(DM), tc(C2))
conn(bc(YA), (tc(B1)[0]-0.4, tc(B1)[1]))
conn(bc(C1), tc(B1)); conn(bc(C2), (tc(B1)[0]+0.4, tc(B1)[1]))
conn(rc(B1), lc(B2)); conn(rc(B2), lc(B3))
conn(bc(B3), (bc(B3)[0], 6.62))

# Speaker notes
notes = slide.notes_slide.notes_text_frame
notes.text = (
    "讲稿：\n"
    "1. 自变量是 LLM 大模型接入这一可识别的技术冲击，非泛泛“AI”。\n"
    "2. 两条机制：模型更会找有意向的人、更会个性化劝说。\n"
    "3. 落脚不在转化率，而在双刃——可得性与脆弱性是否同时上升。\n"
    "4. 关键识别任务：脆弱性上升是“更脆弱的人被卷入”还是“同类人借得更糟”。\n"
    "5. 同一条 X→Y 链在微观/中观/宏观三套数据各识别一遍，互证后收口政策。"
)

out = "/home/user/claude/技术路线图_LLM消费信贷.pptx"
prs.save(out)
print("SAVED", out)
