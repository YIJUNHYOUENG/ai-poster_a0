"""Aragon 템플릿 슬라이드 준비 — build_aragon.py가 쓴다.

- 템플릿의 빈 본문 자리 표시자는 지운다(내용은 도형·글상자로 따로 넣는다).
- 제목·저자·소속 자리 표시자를 채우고 제목 띠 안에 다시 배치한다.
- 섹션 제목 막대는 템플릿의 제목 막대 자리 표시자를 HTML의 h2 막대 위치로 옮겨 쓴다.
  템플릿에는 막대가 6개뿐이라, 7번째는 같은 막대 서식을 복사한 일반 도형으로 만든다.
"""
import copy
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.oxml.ns import qn
from lxml import etree

CM = 360000
BODY_IDX = (10, 26, 28, 30, 96, 155)          # 빈 본문 자리 표시자
BAR_LEFT, BAR_RIGHT = (11, 20, 154), (25, 27, 29)
EA = "맑은 고딕"

TITLE = ["에이젠틱 AI를 이용한 자율망에서", "동적 자원할당 자동화를 위한 구조 및 설계"]
SUBTITLE = "Architecture and Design for Automated Dynamic Resource Allocation in Autonomous Network using Agentic AI"
AUTHORS = "이준형, 김재경, 최윤경, 김양중*"
AUTHOR_NOTE = "  (* 교신저자)"
AFFIL = "한국공학대학교 컴퓨터전자공학과  ·  {ljh040325, 2023531014, dhksejs235, *zeroplus}@tukorea.ac.kr"


def _ea(run):
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", EA)


def _set_lines(tf, lines):
    """lines: [[(text, size_pt, bold or None, color or None), ...], ...] — one paragraph per inner list."""
    tf.clear()
    for i, runs in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        for text, size, bold, color in runs:
            r = p.add_run(); r.text = text
            if size: r.font.size = Pt(size)
            if bold is not None: r.font.bold = bold
            if color: r.font.color.rgb = color
            _ea(r)


def open_template(path, K, bars, bar_texts):
    """bars: [(x, y, w, h) in CSS px] of the HTML section bars; bar_texts: their titles in the same order."""
    prs = Presentation(path)
    slide = prs.slides[0]
    ph = {p.placeholder_format.idx: p for p in slide.placeholders}
    for idx in BODY_IDX:
        if idx in ph:
            el = ph[idx]._element; el.getparent().remove(el)

    def place(shape, x_cm, y_cm, w_cm, h_cm):
        shape.left, shape.top, shape.width, shape.height = Emu(int(x_cm * CM)), Emu(int(y_cm * CM)), Emu(int(w_cm * CM)), Emu(int(h_cm * CM))

    # 제목 띠: 제목 2줄 + 영문 제목, 저자, 소속·이메일
    place(ph[153], 4.0, 0.5, 76.1, 6.2)
    _set_lines(ph[153].text_frame, [[(TITLE[0], 56, True, None)], [(TITLE[1], 56, True, None)], [(SUBTITLE, 28, False, None)]])
    place(ph[151], 4.0, 7.5, 76.1, 1.6)
    _set_lines(ph[151].text_frame, [[(AUTHORS, 36, True, None), (AUTHOR_NOTE, 26, False, None)]])
    place(ph[150], 4.0, 9.25, 76.1, 1.3)
    _set_lines(ph[150].text_frame, [[(AFFIL, 26, False, None)]])

    # 섹션 제목 막대: 왼쪽 단 3개, 오른쪽 단 4개
    order = sorted(range(len(bars)), key=lambda i: (bars[i][0] > 1500, bars[i][1]))
    left = [i for i in order if bars[i][0] < 1500]
    right = [i for i in order if bars[i][0] >= 1500]
    slots = list(zip(left, BAR_LEFT)) + list(zip(right, BAR_RIGHT))
    extra = right[len(BAR_RIGHT):]
    template_bar = ph[BAR_RIGHT[-1]]._element
    for i in extra:                     # 막대 서식을 레이아웃에서 그대로 가져온 일반 도형
        lay = slide.slide_layout
        src = next(s for s in lay.placeholders if s.placeholder_format.idx == BAR_RIGHT[-1])._element
        el = copy.deepcopy(src)
        nv = el.find(qn("p:nvSpPr"))
        nv.find(qn("p:nvPr")).clear()
        nv.find(qn("p:cNvPr")).set("id", str(900 + i)); nv.find(qn("p:cNvPr")).set("name", f"섹션 제목 {bar_texts[i]}")
        nv.find(qn("p:cNvSpPr")).clear()
        template_bar.addnext(el)
    shapes = {s.shape_id: s for s in slide.shapes}
    for i, idx in slots:
        bar_shape = ph[idx]
        x, y, w, h = bars[i]
        bar_shape.left, bar_shape.top, bar_shape.width, bar_shape.height = Emu(int(round(x * K))), Emu(int(round(y * K))), Emu(int(round(w * K))), Emu(int(round(h * K)))
        _set_lines(bar_shape.text_frame, [[(bar_texts[i], None, None, None)]])
    for i in extra:
        bar_shape = shapes[900 + i]
        x, y, w, h = bars[i]
        bar_shape.left, bar_shape.top, bar_shape.width, bar_shape.height = Emu(int(round(x * K))), Emu(int(round(y * K))), Emu(int(round(w * K))), Emu(int(round(h * K)))
        _set_lines(bar_shape.text_frame, [[(bar_texts[i], None, None, None)]])
    return prs, slide
