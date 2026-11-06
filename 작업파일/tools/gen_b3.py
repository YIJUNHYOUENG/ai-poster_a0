import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_c as g

tpl_path, out_path = sys.argv[1], sys.argv[2]
HH = int(sys.argv[3]) if len(sys.argv) > 3 else 1160     # ring row height
TEAL, PAPER, MU = "#06525C", "#F7F9F8", "#C9DCDA"
g.INK = TEAL
g.BLUE = TEAL

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
            f'width: 60px; height: 60px; overflow: visible"><path d="{d}" fill="{PAPER}"></path></svg>')

def ring():
    o = [f'<div role="img" aria-label="에이전트 4단계 폐루프: 상황인지, 자원배분 결정, 자원할당, 판단검증을 매 스텝(15분) 반복" '
         f'style="position: relative; width: {W}px; height: {HH}px">',
         '<h2 style="position: absolute; left: 0px; top: 0px; margin: 0">에이전트 4단계 폐루프</h2>']
    # leaders first (paint order: lines, then shapes, then text)
    for corner, *_ in STAGES:
        nx, ny = node_xy(corner)
        if corner in ("nw", "sw"):
            o.append(g.arrow_svg(ZONE + 24, ny, nx - 30, ny, PAPER, 4, False))
        else:
            o.append(g.arrow_svg(nx + 30, ny, W - ZONE - 24, ny, PAPER, 4, False))
    o.append(f'<div style="position: absolute; left: {CX - D // 2}px; top: 0px; width: {D}px; height: {D}px; box-sizing: border-box; '
             f'border: {RING}px solid {PAPER}; border-radius: 50%"></div>')
    o.append(tri(CX, CY - R, "right"))
    o.append(tri(CX + R, CY, "down"))
    o.append(tri(CX, CY + R, "left"))
    o.append(tri(CX - R, CY, "up"))
    for corner, *_ in STAGES:
        nx, ny = node_xy(corner)
        o.append(f'<div style="position: absolute; left: {nx - 30}px; top: {ny - 30}px; width: 60px; height: 60px; box-sizing: border-box; '
                 f'border-radius: 50%; border: 14px solid {PAPER}; background: {TEAL}"></div>')
    # centre: the result the loop produces
    o.append(f'<div style="position: absolute; left: {CX - 340}px; top: {CY - 232}px; width: 680px; text-align: center">'
             f'<p class="mu" style="margin: 0; font-size: 36px; line-height: 1.3; font-weight: 700">매 스텝(15분) 반복</p>'
             f'<p style="margin: 8px 0 0; font-size: 300px; line-height: 0.9; font-weight: 700; letter-spacing: -0.06em">51%</p>'
             f'<p style="margin: 14px 0 0; font-size: 48px; line-height: 1.25; font-weight: 700">SLA 위반 감소</p>'
             f'<p class="mu" style="margin: 2px 0 0; font-size: 40px; line-height: 1.3">(평균 7.8 → 3.8회)</p></div>')
    for corner, name, agent, desc, foot, num, unit, ntext in STAGES:
        nx, ny = node_xy(corner)
        left = 0 if corner in ("nw", "sw") else W - ZONE
        block = [f'<div style="position: absolute; left: {left}px; top: {ny - 35}px; width: {ZONE}px; display: flex; flex-direction: column; gap: 8px">',
                 f'<p style="margin: 0; font-size: 64px; line-height: 1.1; font-weight: 700">{name}<span class="mu" style="font-size: 32px; font-weight: 400; letter-spacing: 0">&nbsp;&nbsp;{agent}</span></p>',
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

s = open(tpl_path, encoding="utf-8").read()
s = s.replace("@@DIAGRAM@@", g.diagram(1700, band="#E6EEED", comp="#FFFFFF", sup=TEAL))
s = s.replace("@@RING@@", ring())
s = s.replace("@@CHART@@", g.chart(960, G="#3F6F75", grid="#D5E0DF", axis="#8A9A99", base_c="#8A8F8E",
                                   hollow=PAPER, rim=PAPER, prop_c=TEAL))
open(out_path, "w", encoding="utf-8").write(s)
print("written", len(s))
