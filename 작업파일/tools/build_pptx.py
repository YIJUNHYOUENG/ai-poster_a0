import json, sys, os, copy
from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_MARKER_STYLE, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION
from pptx.enum.dml import MSO_LINE
from pptx.oxml.ns import qn
from lxml import etree

work = sys.argv[1]
out_path = sys.argv[2]
Y_SHIFT = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0   # fraction of line height to nudge text down
d = json.load(open(os.path.join(work, 'layout.json'), encoding='utf-8'))
THEME_ARG = sys.argv[4] if len(sys.argv) > 4 else 'A'
FONT = 'Pretendard' if THEME_ARG in ('A3', 'D') else '맑은 고딕' if THEME_ARG == 'GE' else 'Noto Sans KR'
SLIDE_W, SLIDE_H = 30276000, 42804000           # A0 portrait, 841 x 1189 mm
K = SLIDE_W / d['W']                              # EMU per CSS px

def E(px): return Emu(int(round(px * K)))
def rgb(h): return RGBColor.from_string(h)

prs = Presentation()
prs.slide_width, prs.slide_height = SLIDE_W, SLIDE_H
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid(); slide.background.fill.fore_color.rgb = rgb(d.get('bg', 'FFFFFF'))

# 1-3. rectangles, lines and pictures in document (paint) order
big = Image.open(os.path.join(work, 'poster@2x.png')).convert('RGB')
items = [('rect', r) for r in d['rects']] + [('oval', o) for o in d.get('ovals', [])] + [('line', l) for l in d['lines']] + [('img', im) for im in d['images']]
items.sort(key=lambda it: it[1]['z'])
for i, (kind, o) in enumerate(items):
    if kind == 'rect':
        lw = o.get('lineW', 0) if o.get('line') else 0
        x0, y0, w0, h0 = o['x'] + lw / 2, o['y'] + lw / 2, o['w'] - lw, o['h'] - lw
        rad = o.get('radius', 0)
        s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rad > 0 else MSO_SHAPE.RECTANGLE, E(x0), E(y0), E(w0), E(h0))
        if rad > 0:
            s.adjustments[0] = min(0.5, max(rad - lw / 2, 0) / max(min(w0, h0), 1))
        if o.get('color'):
            s.fill.solid(); s.fill.fore_color.rgb = rgb(o['color'])
        else:
            s.fill.background()
        if lw:
            s.line.color.rgb = rgb(o['line']); s.line.width = Pt(lw * 0.75)
            if o.get('dash'):
                s.line.dash_style = MSO_LINE.DASH
        else:
            s.line.fill.background()
        s.shadow.inherit = False
        s.name = f'면 {i + 1}'
    elif kind == 'oval':
        inset = o['lineW'] / 2 if o['line'] else 0
        s = slide.shapes.add_shape(MSO_SHAPE.OVAL, E(o['x'] + inset), E(o['y'] + inset), E(o['w'] - 2 * inset), E(o['h'] - 2 * inset))
        if o['fill']:
            s.fill.solid(); s.fill.fore_color.rgb = rgb(o['fill'])
        else:
            s.fill.background()
        if o['line']:
            s.line.color.rgb = rgb(o['line']); s.line.width = Pt(o['lineW'] * 0.75)
        else:
            s.line.fill.background()
        s.shadow.inherit = False
        s.name = f'원 {i + 1}'
    elif kind == 'line':
        c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(o['x1']), E(o['y1']), E(o['x2']), E(o['y2']))
        c.line.color.rgb = rgb(o['color']); c.line.width = Pt(o['sw'] * 0.75)
        if o['arrow']:
            ln = c.line._get_or_add_ln()
            tail = etree.SubElement(ln, qn('a:tailEnd')); tail.set('type', 'triangle'); tail.set('w', 'med'); tail.set('len', 'med')
        c.name = f'화살표 {i + 1}' if o['arrow'] else f'선 {i + 1}'
    else:
        pad = 6 if o['kind'] == 'math' else 2
        x0, y0 = o['x'] - pad, o['y'] - pad
        w, h = o['w'] + 2 * pad, o['h'] + 2 * pad
        crop = big.crop((int(x0 * 2), int(y0 * 2), int((x0 + w) * 2), int((y0 + h) * 2)))
        if THEME_ARG == 'GE':   # white → transparent, so formulas sit on the tinted example block
            from PIL import ImageChops, ImageOps
            r_, g_, b_ = crop.split()
            crop = crop.convert('RGBA')
            crop.putalpha(ImageOps.invert(ImageChops.darker(ImageChops.darker(r_, g_), b_)))
        p = os.path.join(work, f'img_{i}.png'); crop.save(p)
        pic = slide.shapes.add_picture(p, E(x0), E(y0), E(w), E(h))
        pic.name = {'math': '수식 ', 'legend': '범례 기호 ', 'icon': '화살촉 '}[o['kind']] + str(i + 1)

# 4. text
def set_fonts(run):
    rPr = run._r.get_or_add_rPr()
    for tag in ('a:latin', 'a:ea', 'a:cs'):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set('typeface', FONT)

for i, t in enumerate(d['texts']):
    lines = [[]]
    for rn in t['runs']:
        if rn['text'] == '\n': lines.append([])
        else: lines[-1].append(rn)
    x, y, w, h = t['x'], t['y'], t['w'], t['h']
    if t.get('rot'): t['align'] = 'center'          # turn around the box centre, so keep the text centred in it
    if t['align'] == 'left' and not t['bullet'] and t['textX'] > x + 1:
        w -= t['textX'] - x; x = t['textX']
    slack = max(24, w * 0.06)
    if t['align'] == 'center': x -= slack / 2; w += slack
    elif t['align'] == 'right': x -= slack; w += slack
    else: w += slack
    bullet_indent = 42 if t['bullet'] else 0
    x -= bullet_indent; w += bullet_indent
    y += t['lh'] * Y_SHIFT
    lh = t['lh']
    big = max([r['size'] for line in lines for r in line] or [lh])
    if len(lines) == 1 and lh < big * 1.15:
        # PowerPoint lifts glyphs when exact spacing is tighter than the font; give single lines room instead
        y -= (big * 1.15 - lh) / 2; lh = big * 1.15
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(max(h, lh)))
    if t.get('rot'): tb.rotation = t['rot'] % 360
    tb.name = '텍스트 ' + (''.join(r['text'] for r in t['runs'] if r['text'] != '\n')[:20])
    tf = tb.text_frame
    tf.word_wrap = False; tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE if t['middle'] else MSO_ANCHOR.TOP
    p = tf.paragraphs[0]
    p.alignment = {'center': PP_ALIGN.CENTER, 'right': PP_ALIGN.RIGHT}.get(t['align'], PP_ALIGN.LEFT)
    p.line_spacing = Pt(lh * 0.75)
    pPr = p._p.get_or_add_pPr()
    if t['bullet']:
        pPr.set('marL', str(int(round(bullet_indent * K)))); pPr.set('indent', str(-int(round(bullet_indent * K))))
        bf = etree.SubElement(pPr, qn('a:buFont')); bf.set('typeface', 'Arial')
        bc = etree.SubElement(pPr, qn('a:buChar')); bc.set('char', '•')
    else:
        etree.SubElement(pPr, qn('a:buNone'))
    for li, line in enumerate(lines):
        if li > 0: p.add_line_break()
        for rn in line:
            r = p.add_run(); r.text = rn['text']
            f = r.font
            f.size = Pt(round(rn['size'] * 0.75 * 2) / 2)
            f.bold = rn['bold']; f.italic = rn['italic']
            f.color.rgb = rgb(rn['color'])
            set_fonts(r)
            rPr = r._r.get_or_add_rPr()
            if rn['ls']: rPr.set('spc', str(int(round(rn['ls'] * 0.75 * 100))))
            if rn['va'] == 'sub': rPr.set('baseline', '-25000')
            if rn['va'] == 'sup': rPr.set('baseline', '30000')

# 5. native chart for figure 2 (D draws figure 2 as shapes, so it has none)
c = d['chart']
if c is None:
    prs.save(out_path); print('saved', out_path); sys.exit(0)
THEME = sys.argv[4] if len(sys.argv) > 4 else 'A'
if THEME == 'B':   # colour chapters: chart on the grey-green field, ink proposal; the y-axis title is already page text
    NAVY, GRAY, ORANGE, MUTED, GRID, HOLLOW, RIM, YTITLE = '141414', '6B6B6B', 'E07B00', '3D3D3D', 'B5BAB1', 'CFD3CB', 'CFD3CB', False
elif THEME == 'B3':   # loop-centred: teal on paper; the y-axis title is already page text
    NAVY, GRAY, ORANGE, MUTED, GRID, HOLLOW, RIM, YTITLE = '06525C', '8A8F8E', 'E07B00', '3F6F75', 'D5E0DF', 'F7F9F8', 'F7F9F8', False
elif THEME == 'A3':   # spec card layout: legend and y-axis title are drawn inside the figure's own header
    NAVY, GRAY, ORANGE, MUTED, GRID, HOLLOW, RIM, YTITLE = '1F4E79', '8C8C8C', 'E07B00', '444444', 'E1E6EC', 'FFFFFF', 'FFFFFF', False
elif THEME == 'C':   # white page, blue proposal; the y-axis title is already page text
    NAVY, GRAY, ORANGE, MUTED, GRID, HOLLOW, RIM, YTITLE = '1A4BE0', '8C8C8C', 'E07B00', '555555', 'E0E0E0', 'FFFFFF', 'FFFFFF', False
elif THEME == 'GE':   # Gemini colours (anishathalye/gemini): blue proposal, orange edge; the y-axis title is already page text
    NAVY, GRAY, ORANGE, MUTED, GRID, HOLLOW, RIM, YTITLE = '40739E', '8C8C8C', 'E07B00', '555555', 'E0E4EC', 'FFFFFF', 'FFFFFF', False
elif THEME == 'D':   # problem-stage-evidence sheet: ink proposal on paper, vermilion edge; the y-axis title is already page text
    NAVY, GRAY, ORANGE, MUTED, GRID, HOLLOW, RIM, YTITLE = '161616', '948E80', 'E0451F', '6B655A', 'DDD7CB', 'FFFFFF', 'FFFFFF', False
else:
    NAVY, GRAY, ORANGE, MUTED, GRID, HOLLOW, RIM, YTITLE = '1F4E79', '8C8C8C', 'E07B00', '55606B', 'D5DBE1', 'FFFFFF', 'FFFFFF', True
base = [0.897, 1.000, 1.132, 1.503, 1.184, 2.208, 1.259, 1.106, 1.539, 1.614]
prop = [0.741, 0.793, 0.946, 1.060, 1.014, 1.039, 1.028, 0.929, 0.936, 0.864]
buys = {3: 'v1', 4: 'v1', 5: 'v1', 8: 'v3', 9: 'v5'}
cd = CategoryChartData()
cd.categories = [str(i) for i in range(10)]
cd.add_series('기존 PoC (위반 8회)', base)
cd.add_series('제안 구조 (위반 4회)', prop)
cd.add_series('SLA 위반 경계 (부하율 1.0)', [1.0] * 10)
cd.add_series('용량 조달 (v: 벤더)', [round(prop[i] - 0.12, 3) if i in buys else None for i in range(10)])

# plot box inside the chart frame, in CSS px: left, top, right margin, height; x-axis title top
PX0, PTOP, PRM, PH, XT = 110, 20, 28, c['h'] - 124, c['h'] - 38
if THEME == 'A3':
    bgc = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, E(c['x']), E(c['y']), E(c['w']), E(c['h']))
    bgc.adjustments[0] = 12 / min(c['w'], c['h']); bgc.fill.solid(); bgc.fill.fore_color.rgb = rgb('FFFFFF'); bgc.line.fill.background(); bgc.name = '그림 2 바탕'
    HEAD = 150   # legend + y-axis title band at the top of the figure, kept as a picture
    crop = Image.open(os.path.join(work, 'poster@2x.png')).convert('RGB').crop((int(c['x'] * 2), int(c['y'] * 2), int((c['x'] + c['w']) * 2), int((c['y'] + HEAD) * 2)))
    hp = os.path.join(work, 'chart_head.png'); crop.save(hp)
    slide.shapes.add_picture(hp, E(c['x']), E(c['y']), E(c['w']), E(HEAD)).name = '그림 2 범례'
    c = {'x': c['x'], 'y': c['y'] + HEAD, 'w': c['w'], 'h': c['h'] - HEAD}
    PX0, PTOP, PRM, PH, XT = 100, 10, 30, 386, 462
top = 0
if YTITLE:
    ytitle = slide.shapes.add_textbox(E(c['x']), E(c['y']), E(c['w']), E(44))
    ytitle.name = '그림 2 세로축 제목'
    tf = ytitle.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.word_wrap = False
    r = tf.paragraphs[0].add_run(); r.text = '최대 슬라이스 부하율 (이용률 ÷ 임계값)'
    r.font.size = Pt(24); r.font.color.rgb = rgb(MUTED); set_fonts(r)
    top = 44

gf = slide.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, E(c['x']), E(c['y'] + top), E(c['w']), E(c['h'] - top), cd)
gf.name = '그림 2 차트'
ch = gf.chart
ch.has_legend = False
ch.font.size = Pt(24); ch.font.name = FONT; ch.font.color.rgb = rgb(MUTED)
va = ch.value_axis
va.minimum_scale = 0.5; va.maximum_scale = 2.3; va.major_unit = 0.5
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = rgb(GRID); va.major_gridlines.format.line.width = Pt(1.5)
va.format.line.fill.background()
va.tick_labels.number_format = '0.0'; va.tick_labels.number_format_is_linked = False
ca = ch.category_axis
ca.format.line.color.rgb = rgb(GRAY); ca.format.line.width = Pt(1.5)
if YTITLE:
    ca.has_title = True
    ca.axis_title.text_frame.text = '스텝 (15분 간격)'
    for para in ca.axis_title.text_frame.paragraphs:
        for rr in para.runs:
            rr.font.size = Pt(24); rr.font.bold = False; rr.font.color.rgb = rgb(MUTED); set_fonts(rr)
else:
    # pinned plot area: the x-axis title sits under the chart as page text, as on the poster
    xt = slide.shapes.add_textbox(E(c['x'] + PX0), E(c['y'] + XT), E(c['w'] - PX0 - PRM), E(44))
    xt.name = '그림 2 가로축 제목'
    tf = xt.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.word_wrap = False
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    rr = tf.paragraphs[0].add_run(); rr.text = '스텝 (15분 간격)'
    rr.font.size = Pt(24); rr.font.color.rgb = rgb(MUTED); set_fonts(rr)
    # points sit on the axis ends (category 0 at the left edge), like the poster's chart
    valAx = ch._chartSpace.chart.plotArea.find(qn('c:valAx'))
    cb = valAx.find(qn('c:crossBetween'))
    if cb is None:
        cb = etree.Element(qn('c:crossBetween'))
        anchor = valAx.find(qn('c:majorUnit'))
        if anchor is not None:
            anchor.addprevious(cb)
        else:
            valAx.find(qn('c:crosses')).addnext(cb)
    cb.set('val', 'midCat')
    # tick labels close to the axis, as on the poster, leaving room for the title text below
    catAx = ch._chartSpace.chart.plotArea.find(qn('c:catAx'))
    lo = catAx.find(qn('c:lblOffset'))
    if lo is None:
        lo = etree.Element(qn('c:lblOffset'))
        nm = catAx.find(qn('c:noMultiLvlLbl'))
        if nm is not None:
            nm.addprevious(lo)
        else:
            catAx.append(lo)
    lo.set('val', '20')

plot = ch.plots[0]
s_base, s_prop, s_edge, s_buy = plot.series
for s in plot.series: s.smooth = False
s_base.format.line.color.rgb = rgb(GRAY); s_base.format.line.width = Pt(3); s_base.format.line.dash_style = MSO_LINE.DASH
s_base.marker.style = XL_MARKER_STYLE.SQUARE; s_base.marker.size = 14
s_base.marker.format.fill.solid(); s_base.marker.format.fill.fore_color.rgb = rgb(HOLLOW)
s_base.marker.format.line.color.rgb = rgb(GRAY); s_base.marker.format.line.width = Pt(3)
s_prop.format.line.color.rgb = rgb(NAVY); s_prop.format.line.width = Pt(3.75)
s_prop.marker.style = XL_MARKER_STYLE.CIRCLE; s_prop.marker.size = 16
s_prop.marker.format.fill.solid(); s_prop.marker.format.fill.fore_color.rgb = rgb(NAVY)
s_prop.marker.format.line.color.rgb = rgb(RIM); s_prop.marker.format.line.width = Pt(2)
s_edge.format.line.color.rgb = rgb(ORANGE); s_edge.format.line.width = Pt(3)
s_edge.marker.style = XL_MARKER_STYLE.NONE
s_buy.format.line.fill.background()
s_buy.marker.style = XL_MARKER_STYLE.TRIANGLE; s_buy.marker.size = 16
s_buy.marker.format.fill.solid(); s_buy.marker.format.fill.fore_color.rgb = rgb(NAVY)
s_buy.marker.format.line.color.rgb = rgb(NAVY)
for idx, name in buys.items():
    pt = s_buy.points[idx]
    if idx == 9:
        pt.marker.style = XL_MARKER_STYLE.TRIANGLE; pt.marker.size = 16
        pt.marker.format.fill.solid(); pt.marker.format.fill.fore_color.rgb = rgb(HOLLOW)
        pt.marker.format.line.color.rgb = rgb(NAVY); pt.marker.format.line.width = Pt(2.25)
    dl = pt.data_label
    dl.has_text_frame = True; dl.text_frame.text = name
    dl.position = XL_LABEL_POSITION.RIGHT if idx < 8 else XL_LABEL_POSITION.LEFT
    for para in dl.text_frame.paragraphs:
        for rr in para.runs:
            rr.font.size = Pt(24); rr.font.bold = True; rr.font.color.rgb = rgb(NAVY); set_fonts(rr)
# B/C: pin the plot area to the page chart's own plot box (x 110 .. w-28, y 20 .. h-90 in CSS px)
if not YTITLE:
    plotArea = ch._chartSpace.chart.plotArea
    old = plotArea.find(qn('c:layout'))
    if old is not None:
        plotArea.remove(old)
    lay = etree.Element(qn('c:layout'))
    ml = etree.SubElement(lay, qn('c:manualLayout'))
    for tag, val in (('c:layoutTarget', 'inner'), ('c:xMode', 'edge'), ('c:yMode', 'edge'),
                     ('c:x', PX0 / c['w']), ('c:y', PTOP / c['h']), ('c:w', (c['w'] - PX0 - PRM) / c['w']), ('c:h', PH / c['h'])):
        etree.SubElement(ml, qn(tag)).set('val', str(round(val, 4)) if isinstance(val, float) else val)
    plotArea.insert(0, lay)
# empty cells as gaps so the procurement series has no connecting line
dispBlanks = ch._chartSpace.chart.find(qn('c:dispBlanksAs'))
if dispBlanks is None:
    dispBlanks = etree.SubElement(ch._chartSpace.chart, qn('c:dispBlanksAs'))
dispBlanks.set('val', 'gap')

prs.save(out_path)
print('saved', out_path)
