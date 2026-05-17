# -*- coding: utf-8 -*-
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn

NAVY  = RGBColor(0x1F, 0x3B, 0x5B)   # X 自变量
TEAL  = RGBColor(0x1B, 0x7F, 0x79)   # M 中介机制
GREEN = RGBColor(0x2E, 0x7D, 0x32)   # Y-A
RED   = RGBColor(0xB0, 0x3A, 0x2E)   # Y-B
ORANGE= RGBColor(0xC0, 0x5A, 0x16)   # Y (二/三章)
PURPLE= RGBColor(0x6A, 0x3D, 0x9A)   # 调节变量 W
AMBER = RGBColor(0xC8, 0x7F, 0x0A)   # 识别/IV/分解
LAMBER= RGBColor(0xF1, 0xD9, 0xA8)
GREY  = RGBColor(0x6B, 0x76, 0x82)   # 控制变量
BLUE  = RGBColor(0x2E, 0x5E, 0x8C)   # 技术路线步骤
LGREY = RGBColor(0xEC, 0xEF, 0xF3)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK  = RGBColor(0x20, 0x28, 0x33)
LINEC = RGBColor(0x5A, 0x6B, 0x7B)

SW, SH = 13.333, 7.5
FONT = "Microsoft YaHei"

prs = Presentation()
prs.slide_width  = Inches(SW)
prs.slide_height = Inches(SH)


def new_slide(title):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    sp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0),
                            Inches(SW), Inches(0.66))
    sp.fill.solid(); sp.fill.fore_color.rgb = NAVY
    sp.line.fill.background(); sp.shadow.inherit = False
    tf = sp.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = title
    r.font.size = Pt(19); r.font.bold = True
    r.font.color.rgb = WHITE; r.font.name = FONT
    return s


def box(s, x, y, w, h, text, fill, fg=WHITE, size=11, bold=True,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, line=None):
    sp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    sp.line.color.rgb = line if line else fill
    sp.line.width = Pt(1); sp.shadow.inherit = False
    tf = sp.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Pt(4); tf.margin_right = Pt(4)
    tf.margin_top = Pt(2); tf.margin_bottom = Pt(2)
    first = True
    for ln in text.split("\n"):
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = fg; r.font.name = FONT
    return sp


def label(s, x, y, w, h, text, size=10, color=DARK, italic=False,
          bold=False, align=PP_ALIGN.CENTER):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    first = True
    for ln in text.split("\n"):
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.color.rgb = color
        r.font.italic = italic; r.font.bold = bold; r.font.name = FONT
    return tb


def conn(s, p1, p2, color=LINEC, width=1.5, dashed=False, arrow=True):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                               Inches(p1[0]), Inches(p1[1]),
                               Inches(p2[0]), Inches(p2[1]))
    c.line.color.rgb = color; c.line.width = Pt(width)
    c.shadow.inherit = False
    ln = c.line._get_or_add_ln()
    if dashed:
        ln.append(ln.makeelement(qn('a:prstDash'), {'val': 'dash'}))
    if arrow:
        ln.append(ln.makeelement(qn('a:tailEnd'),
                  {'type': 'triangle', 'w': 'med', 'len': 'med'}))
    return c


def bc(s):
    return (s.left + s.width / 2) / 914400, (s.top + s.height) / 914400


def tc(s):
    return (s.left + s.width / 2) / 914400, s.top / 914400


def lc(s):
    return s.left / 914400, (s.top + s.height / 2) / 914400


def rc(s):
    return (s.left + s.width) / 914400, (s.top + s.height / 2) / 914400


def legend(s, items, y=7.05):
    x = 0.3
    for txt, col in items:
        d = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                               Inches(0.22), Inches(0.16))
        d.fill.solid(); d.fill.fore_color.rgb = col
        d.line.fill.background(); d.shadow.inherit = False
        label(s, x + 0.26, y - 0.06, 1.9, 0.3, txt, 9, DARK,
              align=PP_ALIGN.LEFT)
        x += 0.30 + 0.10 + min(1.9, 0.16 * len(txt) + 0.6)


def footer(s, text):
    box(s, 0.3, 6.62, SW - 0.6, 0.42, text, NAVY, WHITE, 10.5, True,
        MSO_SHAPE.RECTANGLE)


# ============================================================ Slide 1
s = new_slide("总框架·模型技术路线图  X → 双机制 → 双刃Y → 三层识别")
X  = box(s, 4.267, 0.86, 4.8, 0.56, "X｜LLM 大模型接入·数字信贷触达升级", NAVY, size=14)
M1 = box(s, 2.467, 1.66, 3.6, 0.52, "机制① 意向识别能力 ↑", TEAL, size=12)
M2 = box(s, 7.267, 1.66, 3.6, 0.52, "机制② 个性化劝说力 ↑", TEAL, size=12)
YA = box(s, 0.45, 2.50, 3.5, 0.74, "Y-A 信贷可得性 ↑\n更多人·更易借到", GREEN, size=12)
YB = box(s, 9.383, 2.50, 3.5, 0.74, "Y-B 金融脆弱性 ↑\n重复借贷·多头·逾期违约", RED, size=12)
label(s, 5.0, 2.18, 3.333, 0.30, "—— 双刃张力 ——", 12, RGBColor(0x8A,0x4B,0x08), True, True)
conn(s, rc(YA), lc(YB), RGBColor(0x8A,0x4B,0x08), 1.5, dashed=True, arrow=False)
DM = box(s, 5.717, 3.46, 1.9, 0.95, "脆弱性\n来源分解", AMBER, size=11,
         shape=MSO_SHAPE.DIAMOND)
C1 = box(s, 3.55, 4.62, 2.9, 0.58, "组成·外延\n更脆弱人群被卷入", LAMBER, DARK, 11)
C2 = box(s, 6.883, 4.62, 2.9, 0.58, "行为·内涵\n同类人借贷恶化", LAMBER, DARK, 11)
B1 = box(s, 0.52, 5.40, 3.95, 0.74, "第一章·微观 马消客户级\nStacked RD-in-time + DFL分解", BLUE, size=11)
B2 = box(s, 4.69, 5.40, 3.95, 0.74, "第二章·中观 裁判文书+扩散\n双向FE + Bartik IV", BLUE, size=11)
B3 = box(s, 8.86, 5.40, 3.95, 0.74, "第三章·宏观 CHFS/CFPS\n监管DDD + 2SLS", BLUE, size=11)
conn(s, bc(X), tc(M1)); conn(s, bc(X), tc(M2))
conn(s, bc(M1), tc(YA)); conn(s, bc(M2), tc(YB))
conn(s, bc(M1), (rc(YB)[0]-0.25, tc(YB)[1]), RGBColor(0x9A,0xA7,0xB2), 1.0)
conn(s, bc(M2), (lc(YA)[0]+0.25, tc(YA)[1]), RGBColor(0x9A,0xA7,0xB2), 1.0)
conn(s, bc(YB), tc(DM)); conn(s, bc(DM), tc(C1)); conn(s, bc(DM), tc(C2))
conn(s, bc(YA), (tc(B1)[0]-0.4, tc(B1)[1]))
conn(s, bc(C1), tc(B1)); conn(s, bc(C2), (tc(B1)[0]+0.4, tc(B1)[1]))
conn(s, rc(B1), lc(B2)); conn(s, rc(B2), lc(B3))
footer(s, "结论与政策：智能信贷触达让更多人借到钱——是否也让更多人陷进去？  金融AI消费者保护 · 共债治理")
s.notes_slide.notes_text_frame.text = (
    "1. X 是 LLM 接入这一可识别技术冲击；2. 双机制：识别↑、劝说↑；"
    "3. 落脚双刃而非转化率；4. 关键：脆弱性升来自组成 vs 行为；"
    "5. 微观/中观/宏观三套数据各识别一遍，收口政策。")

# ============================================================ Slide 2
s = new_slide("第一章 框架图  X →（中介机制M）→ Y，调节W·控制Z")
LX = 1.85
label(s, 0.18, 1.12, 1.6, 0.5, "自变量\nX", 11, NAVY, bold=True)
label(s, 0.18, 2.55, 1.6, 0.5, "中介机制\nM", 11, TEAL, bold=True)
label(s, 0.18, 3.95, 1.6, 0.5, "因变量\nY（双刃）", 11, RED, bold=True)
X  = box(s, LX, 1.00, 4.4, 0.78,
         "X｜LLM大模型接入·数字信贷触达升级\n剂量梯度：IVR → LLM-v1 → LLM-v2", NAVY, size=11)
M1 = box(s, LX, 2.42, 4.4, 0.56, "M₁ 意向识别能力 ↑", TEAL, size=11)
M2 = box(s, LX, 3.06, 4.4, 0.56, "M₂ 个性化劝说力 ↑", TEAL, size=11)
YA = box(s, 7.05, 1.95, 5.9, 0.78,
         "Y-A 信贷可得性 ↑（H1）\n借款概率·获批·放款规模·授信额度", GREEN, size=11)
YB = box(s, 7.05, 3.55, 5.9, 0.78,
         "Y-B 金融脆弱性 ↑（H2）\n重复借贷·applist多头·DPD30+/违约·脆弱指数", RED, size=11)
label(s, 7.05, 2.80, 5.9, 0.30, "◄—— 双刃张力 ——►", 11, RGBColor(0x8A,0x4B,0x08), True, True)
conn(s, bc(X), tc(M1))
conn(s, bc(M1), tc(M2), arrow=False)
conn(s, rc(M2), lc(YA))
conn(s, rc(M2), lc(YB))
conn(s, rc(M1), (lc(YA)[0], lc(YA)[1]-0.16), RGBColor(0x9A,0xA7,0xB2), 1.0)
DM = box(s, 7.05, 4.55, 1.7, 0.85, "脆弱性\n来源（H3）", AMBER, size=10,
         shape=MSO_SHAPE.DIAMOND)
C1 = box(s, 9.0, 4.52, 1.9, 0.42, "组成·外延 更脆弱人群被卷入", LAMBER, DARK, 9.5)
C2 = box(s, 9.0, 5.00, 1.9, 0.42, "行为·内涵 同类人借贷恶化", LAMBER, DARK, 9.5)
conn(s, bc(YB), tc(DM)); conn(s, rc(DM), lc(C1)); conn(s, rc(DM), lc(C2))
W  = box(s, LX, 5.50, 4.4, 0.78,
         "调节变量 W（H4·异质性）\nIVR→LLM 智能化梯度（剂量响应）｜客户风险类型·征信分", PURPLE, size=10)
conn(s, tc(W), (tc(W)[0], bc(M2)[1]+0.02), PURPLE, 1.3, dashed=True)
footer(s, "控制 Z：征信分·历史多头·负债收入比·年龄·名单来源·活动类型·时段·地域　|　识别：以升级日为外生时点的 Stacked RD-in-time")
legend(s, [("自变量X", NAVY), ("中介机制M", TEAL), ("因变量Y", RED),
           ("调节W", PURPLE), ("分解/识别", AMBER)])

# ============================================================ Slide 3
s = new_slide("第一章 技术路线图  问题 → 数据 → 识别 → 检验 → 结论")
P  = box(s, 3.67, 0.85, 6.0, 0.56,
         "研究问题：LLM接入是否同时抬高信贷可得性与金融脆弱性？", BLUE, size=12)
D  = box(s, 3.67, 1.62, 6.0, 0.56,
         "数据：全量AI拨打 + 每通模型版本 + 用信表 + applist多头", BLUE, size=11)
G  = box(s, 3.67, 2.39, 6.0, 0.56,
         "反推 LLM 接入日 g  +  采用曲线诊断（陡跳 / 灰度爬坡）", BLUE, size=11)
R1 = box(s, 1.6, 3.20, 4.6, 0.62, "陡跳 → Stacked RD-in-time（主模型）", TEAL, size=11)
R2 = box(s, 7.1, 3.20, 4.6, 0.62, "爬坡 → Fuzzy RD / 剂量交错DiD", AMBER, size=11)
YY = box(s, 3.67, 4.05, 6.0, 0.56,
         "估计 双结果：Y-A 信贷可得性  &  Y-B 金融脆弱性", GREEN, size=11)
DE = box(s, 3.67, 4.82, 6.0, 0.56,
         "DFL 重加权分解：组成·外延  vs  行为·内涵", AMBER, size=11)
TT = box(s, 3.67, 5.59, 6.0, 0.56,
         "识别检验：密度连续 · 安慰剂升级日 · donut-RD · 机制三角", GREY, size=10.5)
conn(s, bc(P), tc(D)); conn(s, bc(D), tc(G))
conn(s, bc(G), tc(R1)); conn(s, bc(G), tc(R2))
conn(s, bc(R1), (tc(YY)[0]-0.3, tc(YY)[1]))
conn(s, bc(R2), (tc(YY)[0]+0.3, tc(YY)[1]))
conn(s, bc(YY), tc(DE)); conn(s, bc(DE), tc(TT))
footer(s, "结论：信贷可得性与金融脆弱性并存（双刃），并判定脆弱性主驱动＝组成 抑或 行为")

# ============================================================ Slide 4
s = new_slide("第二章 框架图  扩散X →（机制M）→ 区域过度负债Y")
label(s, 0.18, 1.05, 1.6, 0.5, "识别\nIV/冲击", 11, AMBER, bold=True)
label(s, 0.18, 2.45, 1.6, 0.5, "自变量\nX", 11, NAVY, bold=True)
label(s, 0.18, 3.70, 1.6, 0.5, "中介机制\nM", 11, TEAL, bold=True)
label(s, 0.18, 4.95, 1.6, 0.5, "因变量\nY", 11, ORANGE, bold=True)
IV = box(s, 1.85, 0.95, 9.6, 0.56,
         "识别：Bartik 移动份额IV  /  2017现金贷·2020网络小贷监管冲击", AMBER, size=11)
X2 = box(s, 1.85, 2.35, 9.6, 0.56,
         "X｜区域智能外呼·数字营销扩散度（招聘大数据构造 / 数字普惠信贷子项）", NAVY, size=11)
M  = box(s, 1.85, 3.60, 9.6, 0.56,
         "M｜获客技术扩散 → 边际·脆弱客群被开发", TEAL, size=11)
Y2 = box(s, 1.85, 4.85, 9.6, 0.62,
         "Y｜区域金融借款/民间借贷纠纷（人口标准化）· 区域过度负债 ↑", ORANGE, size=11)
conn(s, tc(X2), bc(IV), AMBER, 1.3, dashed=True)  # IV --识别--> X
conn(s, bc(X2), tc(M)); conn(s, bc(M), tc(Y2))
footer(s, "控制 Z：人均GDP·人口·产业结构·传统金融密度　|　单元：城市(或省)×年面板，双向固定效应 μ_r + λ_t")
legend(s, [("识别IV", AMBER), ("自变量X", NAVY), ("中介机制M", TEAL),
           ("因变量Y", ORANGE)])

# ============================================================ Slide 5
s = new_slide("第二章 技术路线图  问题 → 数据 → 识别 → 备择 → 结论")
P  = box(s, 3.67, 1.05, 6.0, 0.62,
         "研究问题：智能外呼扩散是否伴随区域过度负债上升？", BLUE, size=12)
D  = box(s, 3.67, 2.05, 6.0, 0.70,
         "数据：裁判文书面板 + 招聘数据构造扩散代理 + 数字普惠指数", BLUE, size=11)
M  = box(s, 3.67, 3.13, 6.0, 0.62,
         "基准：双向固定效应  +  Bartik 移动份额 IV", TEAL, size=11)
RB = box(s, 3.67, 4.05, 6.0, 0.70,
         "备择识别：2017/2020 监管冲击 DiD/DDD  +  事件研究前趋势检验", AMBER, size=11)
R  = box(s, 3.67, 5.13, 6.0, 0.62,
         "结论：中观扩散 → 区域过度负债 的因果证据", ORANGE, size=11)
conn(s, bc(P), tc(D)); conn(s, bc(D), tc(M))
conn(s, bc(M), tc(RB)); conn(s, bc(RB), tc(R))
footer(s, "工具变量有效性报告：Goldsmith-Pinkham-Sorkin-Swift / Borusyak-Hull-Jaravel 检验")

# ============================================================ Slide 6
s = new_slide("第三章 框架图  数字金融/AI信贷X →（家庭传导M）→ 脆弱性Y")
label(s, 0.18, 1.25, 1.6, 0.5, "自变量\nX", 11, NAVY, bold=True)
label(s, 0.18, 2.65, 1.6, 0.5, "中介机制\nM", 11, TEAL, bold=True)
label(s, 0.18, 3.90, 1.6, 0.5, "因变量\nY", 11, ORANGE, bold=True)
label(s, 0.18, 5.15, 1.6, 0.5, "调节\nW·异质", 11, PURPLE, bold=True)
X3 = box(s, 1.85, 1.15, 9.6, 0.62,
         "X｜数字金融·AI信贷暴露  +  2017/2020 监管冲击（准实验）", NAVY, size=11)
M3 = box(s, 1.85, 2.55, 9.6, 0.56,
         "M｜信贷可得 与 劝说 在家庭层的传导", TEAL, size=11)
Y3 = box(s, 1.85, 3.80, 9.6, 0.62,
         "Y｜负债收入比·偿债比·逾期·无法应急筹款·是否多头", ORANGE, size=11)
W3 = box(s, 1.85, 5.05, 9.6, 0.56,
         "调节 W·异质性：低收入 / 年轻 / 已多头 组效应更强", PURPLE, size=11)
conn(s, bc(X3), tc(M3)); conn(s, bc(M3), tc(Y3))
conn(s, tc(W3), bc(Y3), PURPLE, 1.3, dashed=True)
footer(s, "识别：高/低暴露区 × 前后 三重差分(DDD)　|　稳健：数字普惠指数连续处理 2SLS（到杭州距离/历史银行网点）+ PSM-DID")
legend(s, [("自变量X", NAVY), ("中介机制M", TEAL), ("因变量Y", ORANGE),
           ("调节W", PURPLE)])

# ============================================================ Slide 7
s = new_slide("第三章 技术路线图  问题 → 数据 → 主识别 → 稳健 → 异质 → 政策")
P  = box(s, 3.67, 0.90, 6.0, 0.56,
         "研究问题：家庭金融脆弱性后果与监管含义为何？", BLUE, size=12)
D  = box(s, 3.67, 1.66, 6.0, 0.56,
         "数据：CHFS / CFPS + 数字普惠指数 + 监管事件", BLUE, size=11)
M  = box(s, 3.67, 2.42, 6.0, 0.56,
         "主识别：高/低暴露区 × 前后  三重差分（DDD）", TEAL, size=11)
RB = box(s, 3.67, 3.18, 6.0, 0.62,
         "稳健：数字普惠连续处理 2SLS  +  PSM-DID  +  平行趋势", AMBER, size=11)
H  = box(s, 3.67, 4.02, 6.0, 0.56,
         "异质性：低收入 / 年轻 / 已多头 组应更强", PURPLE, size=11)
R  = box(s, 3.67, 4.78, 6.0, 0.62,
         "结论与政策闭环：金融AI消费者保护 · 共债治理", ORANGE, size=11)
conn(s, bc(P), tc(D)); conn(s, bc(D), tc(M)); conn(s, bc(M), tc(RB))
conn(s, bc(RB), tc(H)); conn(s, bc(H), tc(R))
footer(s, "三章逻辑闭环：微观(公司内组成效应) → 中观(行业/区域扩散) → 宏观(家庭脆弱性与监管)")

out = "/home/user/claude/技术路线图_LLM消费信贷.pptx"
prs.save(out)
print("SAVED", out, "slides=", len(prs.slides._sldIdLst))
