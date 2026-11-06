"""B안 채택판 — B안(폐루프 중심) 구조에 C안의 디자인을 입힌다.

C안 디자인: 흰 바탕, 먹색 #111111 글자, 회색 #555555 보조 글자, 회색 #F2F2F2 색면,
강조색은 파랑({{blue}}) 하나 — 단계 이름, 제안 구조 값, 51%, 그래프의 제안 구조 선에만 쓴다.
"""
import os, sys, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_c as g

tpl_path, out_path = sys.argv[1], sys.argv[2]
HH = int(sys.argv[3]) if len(sys.argv) > 3 else 1050     # ring row height
INK, MUTED, FIELD, BLUE = "#111111", "#555555", "#F2F2F2", "{{blue}}"
g.INK = INK
g.BLUE = BLUE

W, D, RING = 2953, 860, 18
CX, CY = W // 2, D // 2
R = D // 2 - RING // 2
ZONE = (W - D) // 2 - 100            # width of each side text zone

STAGES = [  # (corner, name, agent, desc, foot, number, unit, number text)
    ("nw", "상황인지", "Monitoring · Diagnosis",
     "Telemetry MCP로 슬라이스별 수요 <i>x</i>를 모으고 상황 <i>s</i>(평시·응급·대형 행사·IoT 급증)를 추론",
     "식 1, 같은 상황 유지 확률 0.98", "47", "/ 47", "자율 판단한 스텝의 상황인지 정확"),
    ("ne", "자원배분 결정", "Planning",
     "이용률 임계값 <i>θ</i>와 용량 <i>C</i>로 목표 배분을 산출해 Orchestrator MCP로 적용하고 수요 압력 <i>P</i>를 계산",
     "식 2, <i>P</i>가 1을 넘으면 배분만으로는 SLA 불가", None, None, None),
    ("se", "자원할당", "Execution",
     "<i>P</i>가 임계값 이상이면 압력을 가장 크게 낮추는 슬라이스의 용량을 마켓플레이스에서 조달",
     "응급 0.8 · 그 밖 1.0, 벤더는 PoC 점수식으로 선택", "22", "/ 22", "용량이 모자란 스텝을 모두 자동 조달"),
    ("sw", "판단검증", "Verification",
     "상황 신뢰도가 0.9 미만일 때만 망관리자에게 질의하고 결과를 Diagnosis로 되돌리며, SLA 충족 여부를 벤더 평판에 반영",
     "신뢰도 = 사후확률 최댓값", "3", "/ 50", "망관리자 질의가 필요했던 스텝"),
]

def node_xy(corner):
    dx, dy = round(R * math.cos(math.radians(35))), round(R * math.sin(math.radians(35)))
    return {"nw": (CX - dx, CY - dy), "ne": (CX + dx, CY - dy), "se": (CX + dx, CY + dy), "sw": (CX - dx, CY + dy)}[corner]

def tri(x, y, direction):
    pts = {"right": [(-20, -24), (26, 0), (-20, 24)], "down": [(-24, -20), (0, 26), (24, -20)],
           "left": [(20, -24), (-26, 0), (20, 24)], "up": [(-24, 20), (0, -26), (24, 20)]}[direction]
    d = "M " + " L ".join(f"{30 + px} {30 + py}" for px, py in pts) + " Z"
    return (f'<svg width="60" height="60" viewBox="0 0 60 60" aria-hidden="true" style="position: absolute; left: {x - 30}px; top: {y - 30}px; '
            f'width: 60px; height: 60px; overflow: visible"><path d="{d}" fill="{BLUE}"></path></svg>')

def ring():
    o = [f'<div role="img" aria-label="에이전트 4단계 폐루프: 상황인지, 자원배분 결정, 자원할당, 판단검증을 매 스텝(15분) 반복" '
         f'style="position: relative; width: {W}px; height: {HH}px">',
         '<h2 style="position: absolute; left: 0px; top: 0px; margin: 0">에이전트 4단계 폐루프</h2>']
    for corner, *_ in STAGES:
        nx, ny = node_xy(corner)
        if corner in ("nw", "sw"):
            o.append(g.arrow_svg(ZONE + 24, ny, nx - 30, ny, INK, 4, False))
        else:
            o.append(g.arrow_svg(nx + 30, ny, W - ZONE - 24, ny, INK, 4, False))
    o.append(f'<div style="position: absolute; left: {CX - D // 2}px; top: 0px; width: {D}px; height: {D}px; box-sizing: border-box; '
             f'border: {RING}px solid var(--blue); border-radius: 50%"></div>')
    o.append(tri(CX, CY - R, "right"))
    o.append(tri(CX + R, CY, "down"))
    o.append(tri(CX, CY + R, "left"))
    o.append(tri(CX - R, CY, "up"))
    for corner, *_ in STAGES:
        nx, ny = node_xy(corner)
        o.append(f'<div style="position: absolute; left: {nx - 30}px; top: {ny - 30}px; width: 60px; height: 60px; box-sizing: border-box; '
                 f'border-radius: 50%; border: 14px solid var(--blue); background: {FIELD}"></div>')
    o.append(f'<div style="position: absolute; left: {CX - 340}px; top: {CY - 232}px; width: 680px; text-align: center">'
             f'<p class="mu" style="margin: 0; font-size: 36px; line-height: 1.3; font-weight: 700">매 스텝(15분) 반복</p>'
             f'<p style="margin: 8px 0 0; font-size: 300px; line-height: 0.9; font-weight: 700; letter-spacing: -0.06em; color: var(--blue)">51%</p>'
             f'<p style="margin: 14px 0 0; font-size: 48px; line-height: 1.25; font-weight: 700">SLA 위반 감소</p>'
             f'<p class="mu" style="margin: 2px 0 0; font-size: 40px; line-height: 1.3">(평균 7.8 → 3.8회)</p></div>')
    for corner, name, agent, desc, foot, num, unit, ntext in STAGES:
        nx, ny = node_xy(corner)
        left = 0 if corner in ("nw", "sw") else W - ZONE
        block = [f'<div style="position: absolute; left: {left}px; top: {ny - 35}px; width: {ZONE}px; display: flex; flex-direction: column; gap: 8px">',
                 f'<p style="margin: 0; font-size: 64px; line-height: 1.1; font-weight: 700; color: var(--blue)">{name}<span class="mu" style="font-size: 32px; font-weight: 400; letter-spacing: 0">&nbsp;&nbsp;{agent}</span></p>',
                 f'<p class="tx" style="margin: 6px 0 0">{desc}</p>',
                 f'<p class="tx" style="margin: 4px 0 0; font-weight: 700">{foot}</p>']
        if num:
            block.append('<sc-if value="{{extra}}" hint-placeholder-val="{{ true }}">'
                         f'<div style="margin-top: 14px; display: flex; align-items: center; gap: 28px">'
                         f'<p style="margin: 0; font-size: 120px; line-height: 0.9; font-weight: 700; letter-spacing: -0.05em; white-space: nowrap">{num}'
                         f'<span style="font-size: 0.5em; letter-spacing: -0.02em"> {unit}</span></p>'
                         f'<p class="tx" style="margin: 0">{ntext}</p></div></sc-if>')
        block.append('</div>')
        o.append("".join(block))
    o.append('</div>')
    return "\n".join(o)

# B안 템플릿(구조)을 그대로 쓰고, 색과 강조만 C안 규칙으로 바꾼다
s = open(tpl_path, encoding="utf-8").read()
P = "제안"
rep = [
    ("<title>A0 포스터 B안 — 폐루프 중심</title>", "<title>A0 포스터 B안 — 폐루프 중심 (C안 디자인)</title>"),
    ("a{color:#06525C}a:hover{color:#3F6F75}", "a{color:#111111}a:hover{color:#555555}"),
    (".lp h2{margin:0 0 20px;font-size:78px;line-height:1.05;font-weight:700;letter-spacing:-0.035em}",
     ".lp h2{margin:0 0 22px;font-size:80px;line-height:1.05;font-weight:700;letter-spacing:-0.03em}"),
    (".lp .mu{color:#3F6F75}", ".lp .mu{color:#555555}"),
    (".lp .fd .mu{color:#C9DCDA}", ""),
    ("border-bottom:2px solid rgba(6,82,92,0.22)", "border-bottom:2px solid #D4D4D4"),
    (".lp table.pt th{font-weight:700;border-bottom:6px solid #06525C}", ".lp table.pt th{font-weight:700;border-bottom:6px solid #111111}"),
    ('<div class="lp" style="width: 3179px;', '<div class="lp" style="--blue: {{blue}}; width: 3179px;'),
    ("background: #F7F9F8; display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); grid-template-rows",
     "background: #FFFFFF; display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); grid-template-rows"),
    ("font-family: 'Pretendard', 'Noto Sans KR', sans-serif; color: #06525C;", "font-family: 'Pretendard', 'Noto Sans KR', sans-serif; color: #111111;"),
    # 비교표: 제안 구조 열은 파랑
    ('<th class="mu" style="border-bottom-color: #8A8F8E">기존 PoC 구조</th><th>제안 구조</th>',
     '<th class="mu" style="border-bottom-color: #8C8C8C">기존 PoC 구조</th><th style="color: var(--blue); border-bottom-color: var(--blue)">제안 구조</th>'),
    # 폐루프 띠: 짙은 청록 → C안의 회색 색면
    ('<section class="fd" style="grid-column: 1 / -1; margin: 48px -113px 0; padding: 48px 113px 44px; background: #06525C; color: #F7F9F8">',
     '<section style="grid-column: 1 / -1; margin: 48px -113px 0; padding: 48px 113px 44px; background: #F2F2F2">'),
    ("border-top: 3px solid #F7F9F8; padding: 4px 8px 0", "border-top: 3px solid #111111; padding: 4px 8px 0"),
    ('<p style="margin: 0; font-size: 32px; font-weight: 700; white-space: nowrap">(식1)</p>',
     '<p style="margin: 0; font-size: 32px; font-weight: 700; white-space: nowrap; color: var(--blue)">(식1)</p>'),
    ('<p style="margin: 0; font-size: 32px; font-weight: 700; white-space: nowrap">(식2)</p>',
     '<p style="margin: 0; font-size: 32px; font-weight: 700; white-space: nowrap; color: var(--blue)">(식2)</p>'),
    ('<tr><td style="font-weight: 700">제안</td><td style="font-weight: 700">에이전트 기반 오케스트레이터',
     '<tr><td style="font-weight: 700">제안</td><td style="font-weight: 700; color: var(--blue)">에이전트 기반 오케스트레이터'),
    # 범례
    ('stroke="#8A8F8E" stroke-width="4" stroke-dasharray="10 7"></line><rect x="22" y="2" width="20" height="20" fill="#F7F9F8" stroke="#8A8F8E"',
     'stroke="#8C8C8C" stroke-width="4" stroke-dasharray="10 7"></line><rect x="22" y="2" width="20" height="20" fill="#FFFFFF" stroke="#8C8C8C"'),
    ('<line x1="2" y1="12" x2="62" y2="12" stroke="#06525C" stroke-width="5"></line><circle cx="32" cy="12" r="10" fill="#06525C" stroke="#F7F9F8" stroke-width="3"></circle>',
     '<line x1="2" y1="12" x2="62" y2="12" stroke="{{blue}}" stroke-width="5"></line><circle cx="32" cy="12" r="10" fill="{{blue}}" stroke="#FFFFFF" stroke-width="3"></circle>'),
    ('<path d="M16 2 L29 24 L3 24 Z" fill="#06525C"></path>', '<path d="M16 2 L29 24 L3 24 Z" fill="{{blue}}"></path>'),
    ('<th style="padding-right: 12px">제안<br>위반(회)</th>', '<th style="padding-right: 12px; color: var(--blue)">제안<br>위반(회)</th>'),
    ("border-bottom: 4px solid #06525C", "border-bottom: 4px solid #111111"),
    ("background: #E6EEED; display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 48px; align-content: start",
     "background: #F2F2F2; display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 48px; align-content: start"),
    ("width: 190px; height: 190px; background: #F7F9F8;", "width: 190px; height: 190px; background: #FFFFFF;"),
    # 지도교수 의견(2026-11-03): 사사는 싣지 않는다
    ('\n<p class="cap" style="margin: 24px 0 0"><b>사사</b> 본 연구는 IITP(정보통신기획평가원)의 ‘Agentic AI 기반 종단간 완전자율형 네트워크 기술을 위한 Cross-SDO 표준 개발(RS-2026-25527078)’ 지원을 받음.</p>', ''),
    ("""data-props='{"showExtra":{"editor":"boolean","default":true},"$preview":{"width":3179,"height":4494}}'""",
     """data-props='{"blue":{"editor":"color","default":"#1A4BE0"},"showExtra":{"editor":"boolean","default":true},"$preview":{"width":3179,"height":4494}}'"""),
    ("    return { extra: extra, noExtra: !extra };", "    return { blue: this.props.blue ?? '#1A4BE0', extra: extra, noExtra: !extra };"),
]
for a, b in rep:
    assert a in s, a[:70]
    s = s.replace(a, b)
# 비교표·시드표의 제안 구조 값
for v in ("HMM 전진 필터로 자동 추론", "수요·잡음·임계값으로 산출", "수요 압력 기준 자동 조달", "신뢰도 0.9 미만일 때만 질의", "결정 근거와 호출 순서까지 기록"):
    a = f'<td style="font-weight: 700">{v}</td>'
    assert a in s, v
    s = s.replace(a, f'<td style="font-weight: 700; color: var(--blue)">{v}</td>')
s = re.sub(r'(<td style="padding-right: 12px; font-weight: 700)(;? ?(?:border-bottom: 4px solid #111111)?">\d</td>)',
           lambda m: m.group(1) + "; color: var(--blue)" + m.group(2), s)
s = s.replace('<td style="padding-right: 12px; font-weight: 700">3.8</td>', '<td style="padding-right: 12px; font-weight: 700; color: var(--blue)">3.8</td>')
# 로고·QR 자리
s = s.replace("background: #E6EEED; display: flex; align-items: center; justify-content: center; text-align: center; font-size: 28px; line-height: 1.3; color: #3F6F75",
              "background: #F2F2F2; display: flex; align-items: center; justify-content: center; text-align: center; font-size: 28px; line-height: 1.3; color: #555555")
s = s.replace("color: #3F6F75", "color: #555555")
left = [h for h in ("#06525C", "#3F6F75", "#E6EEED", "#F7F9F8", "#8A8F8E", "#C9DCDA", "rgba(6,82,92") if h in s]
assert not left, left

s = s.replace("@@DIAGRAM@@", g.diagram(1700, band=FIELD, comp="#FFFFFF", sup=BLUE))
s = s.replace("@@RING@@", ring())
s = s.replace("@@CHART@@", g.chart(960))
open(out_path, "w", encoding="utf-8").write(s)
print("written", len(s))
