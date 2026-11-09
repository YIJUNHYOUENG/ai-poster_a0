"""Aragon 템플릿판 — 내용 영역만 그리는 HTML.

PosterPresentations.com A0 Aragon 템플릿(84.1 × 118.9 cm)의 두 단에 맞춰 섹션을 쌓는다.
제목 띠·물결·아래 띠는 템플릿 것을 그대로 쓰므로 여기서는 그리지 않고,
섹션 제목 막대(h2.bar)는 build_aragon.py가 템플릿의 제목 자리 표시자로 바꿔 넣는다.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_c as g

out_path = sys.argv[1]
VARIANT = sys.argv[3] if len(sys.argv) > 3 else "aragon"
CM = 3179 / 84.1                   # px per cm
INK, MUTED, GREY, ORANGE = "#222222", "#555555", "#8C8C8C", "#E07B00"
FS = 29.33                         # 22 pt: text inside figures, tables and boxes
if VARIANT == "kens":
    # Kensington: 파란 제목 띠, 두 단은 둥근 흰 패널, 섹션 제목은 막대 없이 가운데 정렬 글자
    NAVY, LIGHT, RULE, HEAD = "#2F5597", "#DEE6F4", "#C9D3E6", "#203864"
    COL_W = round(40.0 * CM)
    LEFT_X, RIGHT_X = round(1.4 * CM), round(42.8 * CM)
    TOP, BOTTOM = round(17.8 * CM), round(114.2 * CM)
    PAD = 46                       # 패널 둥근 테두리 안쪽 여백
    H2_CSS = f"margin:0;height:68px;color:{HEAD};font-size:48px;line-height:68px;font-weight:700;text-align:center"
elif VARIANT == "gemini":
    # Gemini (github.com/anishathalye/gemini) 기본 색 테마: 파랑 #40739E 제목 띠와 짙은 파랑 #273C75 띠 아래 선,
    # 가운데 정렬 파랑 블록 제목 + 얇은 검정 구분선, 흰 본문, 강조 블록 #E8F4FF, 예시 블록 #F5F6FA
    NAVY, LIGHT, RULE, HEAD = "#40739E", "#E8F4FF", "#D9DEE8", "#40739E"
    DARK, EXAMPLE = "#273C75", "#F5F6FA"
    LEFT_X, COL_GAP = 110, 100
    COL_W = (3179 - 2 * LEFT_X - COL_GAP) // 2
    RIGHT_X = LEFT_X + COL_W + COL_GAP
    HEADLINE, HEAD_RULE = 520, 16
    TOP, BOTTOM = HEADLINE + HEAD_RULE + 70, 4404
    PAD = 4
    H2_CSS = f"margin:0;padding:0 0 14px;border-bottom:3px solid #000000;color:{HEAD};font-size:60px;line-height:1.2;font-weight:700;text-align:center"
else:
    # Aragon: 남색 제목 띠와 물결, 섹션 제목은 남색 막대
    NAVY, LIGHT, RULE, HEAD = "#1F3864", "#E9EEF6", "#D0D7E5", "#1F3864"
    COL_W = round(39.7 * CM)       # template column width
    LEFT_X, RIGHT_X = round(1.7 * CM), round(42.6 * CM)
    TOP, BOTTOM = round(15.6 * CM), round(114.6 * CM)
    PAD = 24                       # template body inset (0.62 cm)
    H2_CSS = f"margin:0;height:76px;background:{NAVY};color:#FFFFFF;font-size:48px;line-height:76px;font-weight:700;text-align:center"
IN_W = COL_W - 2 * PAD

g.INK = NAVY
g.BLUE = NAVY

def alert(html):
    """Gemini의 alertblock(연한 파랑 바탕). 템플릿판에서는 그대로 둔다."""
    if VARIANT != "gemini":
        return html
    return f'<div style="background: {LIGHT}; padding: 34px 40px">{html}</div>'

def example(html):
    """Gemini의 exampleblock(연한 회색 바탕). 템플릿판에서는 그대로 둔다."""
    if VARIANT != "gemini":
        return html
    return f'<div style="background: {EXAMPLE}; padding: 28px 36px">{html}</div>'

def headline():
    if VARIANT != "gemini":
        return ""
    logo = lambda t: (f'<div style="width: 300px; height: 220px; margin: 0 auto; background: #F5F6FA; display: flex; align-items: center; justify-content: center; '
                      f'text-align: center; font-size: 28px; line-height: 1.3; color: {NAVY}">{t}</div>')
    return (f'<header style="position: absolute; left: 0px; top: 0px; width: 3179px; height: {HEADLINE}px; background: {NAVY}; color: #F5F6FA; '
            f'display: grid; grid-template-columns: 420px minmax(0, 1fr) 420px; align-items: center">'
            f'{logo("한국공학대학교<br>로고")}'
            f'<div style="text-align: center">'
            f'<p style="margin: 0; font-size: 100px; line-height: 1.15; font-weight: 700; letter-spacing: -0.02em">에이젠틱 AI를 이용한 자율망에서<br>동적 자원할당 자동화를 위한 구조 및 설계</p>'
            f'<p style="margin: 14px 0 0; font-size: 40px; line-height: 1.3">Architecture and Design for Automated Dynamic Resource Allocation in Autonomous Network using Agentic AI</p>'
            f'<p style="margin: 16px 0 0; font-size: 50px; line-height: 1.3; font-weight: 700">이준형, 김재경, 최윤경, 김양중*<span style="font-size: 32px; font-weight: 400"> (* 교신저자)</span></p>'
            f'<p style="margin: 6px 0 0; font-size: 36px; line-height: 1.3">한국공학대학교 컴퓨터전자공학과 · {{ljh040325, 2023531014, dhksejs235, *zeroplus}}@tukorea.ac.kr</p>'
            f'</div>{logo("IITP<br>로고")}</header>'
            f'<div style="position: absolute; left: 0px; top: {HEADLINE}px; width: 3179px; height: {HEAD_RULE}px; background: {DARK}"></div>')

def est(label, bold=False):
    return round(len(label) * (0.62 if bold else 0.58) * FS + 24)

# ---------- 그림 1 ----------
def diagram(W=IN_W, H=707):
    def band(top, h, label=None):
        return (f'<div style="position: absolute; left: 0px; top: {top}px; width: {W}px; height: {h}px; box-sizing: border-box; border: 3px solid {NAVY}; '
                f'background: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700; color: {NAVY}">{label or ""}</div>')
    def box(left, top, w, h, label, solid=False, bold=False):
        bg, color = (NAVY, "#FFFFFF") if solid else (LIGHT, INK)
        fw = "; font-weight: 700" if bold else ""
        return (f'<div style="position: absolute; left: {left}px; top: {top}px; width: {w}px; height: {h}px; background: {bg}; color: {color}; '
                f'display: flex; align-items: center; justify-content: center; white-space: nowrap{fw}">{label}</div>')
    o = [f'<div role="img" aria-label="그림 1: Intent/Service, Agent, MCP, Network Infra의 4계층 구조" style="position: relative; width: {W}px; height: {H}px; font-size: {FS}px; line-height: 1.2">']
    I0, I1, A0, A1, M0, M1, N0, N1 = 0, 66, 116, 362, 442, 572, 641, 707
    o += [band(I0, I1 - I0, "Intent / Service Layer"), band(A0, A1 - A0), band(M0, M1 - M0), band(N0, N1 - N0, "Network Infra Layer")]
    cx, pad = W // 2, 20
    names = ["Monitoring", "Diagnosis", "Planning", "Execution", "Verification"]
    ws = [est(n) for n in names]
    gap = (W - 2 * pad - sum(ws)) / 4
    lefts, x = [], pad
    for w in ws:
        lefts.append(round(x)); x += w + gap
    cents = [l + w // 2 for l, w in zip(lefts, ws)]
    by0, bh = A0 + 128, 56
    sup_w, rag_w = est("Supervisor Agent", True), 110
    sup_l, sy = cx - sup_w // 2, A0 + 22
    o.append(g.arrow_svg(sup_l + sup_w, sy + 28, sup_l + sup_w + 60, sy + 28, NAVY, 3, False))
    o.append(g.arrow_svg(cx, sy + 56, cx, sy + 82, NAVY, 3, False))
    o.append(g.arrow_svg(cents[0], sy + 82, cents[-1], sy + 82, NAVY, 3, False))
    for c in cents:
        o.append(g.arrow_svg(c, sy + 82, c, by0 - 1, NAVY, 3, True))
    for i in range(4):
        o.append(g.arrow_svg(lefts[i] + ws[i], by0 + bh // 2, lefts[i + 1] - 1, by0 + bh // 2, NAVY, 3, True))
    lane = by0 + bh + 22
    o.append(g.arrow_svg(cents[4], by0 + bh, cents[4], lane, NAVY, 3, False))
    o.append(g.arrow_svg(cents[1], lane, cents[4], lane, NAVY, 3, False))
    o.append(g.arrow_svg(cents[1], lane, cents[1], by0 + bh + 1, NAVY, 3, True))
    mn = ["Telemetry", "Topology", "Orchestrator", "Configuration"]
    mw = [est(n) for n in mn]
    mgap = (W - 2 * pad - sum(mw)) / 3
    ml, x = [], pad
    for w in mw:
        ml.append(round(x)); x += w + mgap
    ax = round((ml[1] + mw[1] + ml[2]) / 2)
    for top, bot in ((A1, M0), (M1, N0)):            # bidirectional only Agent-MCP and MCP-Network Infra
        o.append(g.arrow_svg(ax - 16, top, ax - 16, bot - 1, NAVY, 3, True))
        o.append(g.arrow_svg(ax + 16, bot, ax + 16, top + 1, NAVY, 3, True))
    o.append(box(sup_l, sy, sup_w, 56, "Supervisor Agent", solid=True, bold=True))
    o.append(box(sup_l + sup_w + 60, sy, rag_w, 56, "RAG"))
    for l, w, n in zip(lefts, ws, names):
        o.append(box(l, by0, w, bh, n))
    for l, w, n in zip(ml, mw, mn):
        o.append(box(l, M0 + 58, w, 54, n))
    o.append(f'<div style="position: absolute; left: 18px; top: {A0 + 12}px; font-weight: 700; color: {NAVY}">Agent Layer</div>')
    o.append(f'<div style="position: absolute; left: 18px; top: {M0 + 10}px; font-weight: 700; color: {NAVY}">MCP Layer</div>')
    o.append('</div>')
    return "\n".join(o)

# ---------- 에이전트 4단계 폐루프: 2 × 2, 시계 방향 ----------
STAGES = {
    "tl": ("상황인지", "Monitoring · Diagnosis", "Telemetry MCP로 슬라이스별 수요 <i>x</i>를 모으고 상황 <i>s</i>(평시·응급·대형 행사·IoT 급증)를 추론", "식 1, 같은 상황 유지 확률 0.98"),
    "tr": ("자원배분 결정", "Planning", "이용률 임계값 <i>θ</i>와 용량 <i>C</i>로 목표 배분을 산출해 Orchestrator MCP로 적용하고 수요 압력 <i>P</i>를 계산", "식 2, <i>P</i>가 1을 넘으면 배분만으로는 SLA 불가"),
    "br": ("자원할당", "Execution", "<i>P</i>가 임계값 이상이면 압력을 가장 크게 낮추는 슬라이스의 용량을 마켓플레이스에서 조달", "응급 0.8 · 그 밖 1.0, 벤더는 PoC 점수식으로 선택"),
    "bl": ("판단검증", "Verification", "상황 신뢰도가 0.9 미만일 때만 망관리자에게 질의하고 결과를 Diagnosis로 되돌리며, SLA 충족 여부를 벤더 평판에 반영", "신뢰도 = 사후확률 최댓값"),
}
GAP_X, GAP_Y = 110, 96
BOX_W = (IN_W - GAP_X) // 2

def arrow(direction, length):
    g._mid[0] += 1
    mid = f"dc-arrow-head-filled-{g._mid[0]}"
    horiz = direction in ("right", "left")
    W, H = (length, 12) if horiz else (12, length)
    d = {"right": f"M 0 6 L {length - 10} 6", "left": f"M {length} 6 L 10 6",
         "down": f"M 6 0 L 6 {length - 10}", "up": f"M 6 {length} L 6 10"}[direction]
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true" style="display: block; overflow: visible; fill: none; stroke: {NAVY}; stroke-width: 5; stroke-linecap: round">'
            f'<defs><marker id="{mid}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible">'
            f'<path d="M0 0 L4 2 L0 4 Z" fill="{NAVY}" stroke="none" style="stroke: none; fill: {NAVY}; fill: context-stroke"></path></marker></defs>'
            f'<path d="{d}" marker-end="url(#{mid})"></path></svg>')

def stage_box(key):
    name, agent, desc, foot = STAGES[key]
    return (f'<div style="box-sizing: border-box; background: {LIGHT}; padding: 26px 30px; display: flex; flex-direction: column; gap: 8px">'
            f'<p style="margin: 0; font-size: 46px; line-height: 1.2; font-weight: 700; color: {NAVY}">{name} '
            f'<span style="font-size: {FS}px; font-weight: 400; color: {MUTED}">{agent}</span></p>'
            f'<p class="sm" style="margin: 4px 0 0">{desc}</p>'
            f'<p class="sm" style="margin: auto 0 0; padding-top: 8px; font-weight: 700">{foot}</p></div>')

def loop():
    cell = 'display: flex; align-items: center; justify-content: center'
    return (f'<div style="display: grid; grid-template-columns: {BOX_W}px {GAP_X}px {BOX_W}px; grid-template-rows: auto {GAP_Y}px auto">'
            f'{stage_box("tl")}<div style="{cell}">{arrow("right", 80)}</div>{stage_box("tr")}'
            f'<div style="grid-column: 1 / 4; position: relative; {cell}">'
            f'<div style="position: absolute; left: {BOX_W // 2 - 6}px; top: 10px">{arrow("up", GAP_Y - 20)}</div>'
            f'<p style="margin: 0; font-size: 36px; line-height: 1.2; font-weight: 700; color: {NAVY}">매 스텝(15분) 반복</p>'
            f'<div style="position: absolute; left: {BOX_W + GAP_X + BOX_W // 2 - 6}px; top: 10px">{arrow("down", GAP_Y - 20)}</div></div>'
            f'{stage_box("bl")}<div style="{cell}">{arrow("left", 80)}</div>{stage_box("br")}'
            '</div>')

M = lambda s: f'<sub style="font-size: 0.6em">{s}</sub>'
SUM = lambda s: (f'<span style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; line-height: 1">'
                 f'<span style="font-size: 1.3em">∑</span><span style="font-size: 0.5em">{s}</span></span>')
EQ1 = (f'<i>b</i>{M("<i>t</i>")}(<i>s</i>) ∝ <i>p</i>(<i>x</i>{M("<i>t</i>")} | <i>s</i>) {SUM("<i>s</i>′")} '
       f'<i>A</i>{M("<i>s</i>′<i>s</i>")} <i>b</i>{M("<i>t</i>−1")}(<i>s</i>′)')
EQ2 = (f'<i>P</i>{M("<i>t</i>")} = {SUM("<i>i</i>")} <span style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; line-height: 1.15; font-size: 0.85em">'
       f'<span style="padding: 0 8px 4px"><i>x</i>{M("<i>i</i>,<i>t</i>")}</span><span style="border-top: 3px solid {INK}; padding: 4px 8px 0"><i>θ</i>{M("<i>i</i>")} <i>C</i>{M("<i>i</i>,<i>t</i>")}</span></span>')
SV = (f'<i>S<sub style="font-size: 0.6em">v</sub></i> = 100[<i>w</i>{M("Q")} (∑{M("<i>j</i>")} <i>ω<sub style="font-size: 0.6em">j</sub> q<sub style="font-size: 0.6em">v,j</sub></i> / '
      f'∑{M("<i>j</i>")} <i>ω<sub style="font-size: 0.6em">j</sub></i>) + <i>w</i>{M("P")} <i>p<sub style="font-size: 0.6em">v</sub></i> + <i>w</i>{M("R")} <i>r<sub style="font-size: 0.6em">v</sub></i>/5]')
DC = f'Δ<i>C<sub style="font-size: 0.6em">k</sub></i> = 0.25 · <i>B</i>{M("<i>v</i>*")} / <i>B</i>{M("ref")}'

def formula(label, tag, eq, size):
    return (f'<div><p class="cap" style="margin: 0; font-weight: 700; color: {MUTED}">{label}</p>'
            f'<div style="margin-top: 8px; display: flex; align-items: center; gap: 36px"><div class="math" style="font-size: {size}px; line-height: 1.25">{eq}</div>'
            f'<p style="margin: 0; font-size: 32px; font-weight: 700; color: {NAVY}; white-space: nowrap">{tag}</p></div></div>')

# ---------- 그림 2 ----------
def chart(CW=IN_W, H=820):
    TOP_, BOT, LO, HI = 20, H - 90, 0.5, 2.3
    X0, X1 = 110, CW - 28
    base = [0.897, 1.000, 1.132, 1.503, 1.184, 2.208, 1.259, 1.106, 1.539, 1.614]
    prop = [0.741, 0.793, 0.946, 1.060, 1.014, 1.039, 1.028, 0.929, 0.936, 0.864]
    buys = {3: "v1", 4: "v1", 5: "v1", 8: "v3", 9: "v5"}
    x = lambda i: round(X0 + i * (X1 - X0) / 9, 1)
    y = lambda v: round(BOT - (v - LO) * (BOT - TOP_) / (HI - LO), 1)
    o = [f'<svg width="{CW}" height="{H}" viewBox="0 0 {CW} {H}" role="img" aria-label="그림 2: 시드 3의 스텝별 최대 슬라이스 부하율. 기존 PoC는 위반 8회, 제안 구조는 위반 4회" '
         f'style="display: block; font-family: \'Malgun Gothic\', sans-serif">']
    for v in (2.0, 1.5):
        o.append(f'<line x1="{X0}" y1="{y(v)}" x2="{X1}" y2="{y(v)}" stroke="#E0E4EC" stroke-width="2"></line>')
    o.append(f'<line x1="{X0}" y1="{BOT}" x2="{X1}" y2="{BOT}" stroke="{GREY}" stroke-width="2"></line>')
    for v in (2.0, 1.5, 1.0, 0.5):
        o.append(f'<text x="{X0 - 20}" y="{round(y(v) + 11, 1)}" font-size="32" fill="{MUTED}" text-anchor="end">{v:.1f}</text>')
    for i in range(10):
        o.append(f'<text x="{x(i)}" y="{BOT + 42}" font-size="32" fill="{MUTED}" text-anchor="middle">{i}</text>')
    o.append(f'<text x="{(X0 + X1) // 2}" y="{BOT + 84}" font-size="32" fill="{MUTED}" text-anchor="middle">스텝 (15분 간격)</text>')
    o.append(f'<line x1="{X0}" y1="{y(1.0)}" x2="{X1}" y2="{y(1.0)}" stroke="{ORANGE}" stroke-width="4"></line>')
    o.append('<polyline points="' + " ".join(f"{x(i)},{y(v)}" for i, v in enumerate(base)) + f'" fill="none" stroke="{GREY}" stroke-width="4" stroke-dasharray="14 10" stroke-linejoin="round"></polyline>')
    for i, v in enumerate(base):
        o.append(f'<rect x="{round(x(i) - 10, 1)}" y="{round(y(v) - 10, 1)}" width="20" height="20" fill="#FFFFFF" stroke="{GREY}" stroke-width="4"></rect>')
    o.append('<polyline points="' + " ".join(f"{x(i)},{y(v)}" for i, v in enumerate(prop)) + f'" fill="none" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"></polyline>')
    for i, v in enumerate(prop):
        o.append(f'<circle cx="{x(i)}" cy="{y(v)}" r="11" fill="{NAVY}" stroke="#FFFFFF" stroke-width="3"></circle>')
    for i, name in buys.items():
        cx, cy = x(i), round(y(prop[i]) + 36, 1)
        dd = f"M{cx} {round(cy - 13, 1)} L{round(cx + 13, 1)} {round(cy + 9, 1)} L{round(cx - 13, 1)} {round(cy + 9, 1)} Z"
        o.append(f'<path d="{dd}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"></path>' if i == 9 else f'<path d="{dd}" fill="{NAVY}"></path>')
        anchor, tx = ("end", cx - 22) if i >= 8 else ("start", cx + 18)
        o.append(f'<text x="{round(tx, 1)}" y="{round(cy + 11, 1)}" font-size="32" font-weight="700" fill="{NAVY}" text-anchor="{anchor}">{name}</text>')
    o.append('</svg>')
    return "\n".join(o)

def legend():
    item = lambda svg, label: f'<span style="display: inline-flex; align-items: center; gap: 12px">{svg}{label}</span>'
    return ('<div class="sm" style="display: flex; flex-wrap: wrap; column-gap: 36px; row-gap: 6px">'
            + item(f'<svg width="64" height="24" viewBox="0 0 64 24" aria-hidden="true"><line x1="2" y1="12" x2="62" y2="12" stroke="{GREY}" stroke-width="4" stroke-dasharray="10 7"></line><rect x="22" y="2" width="20" height="20" fill="#FFFFFF" stroke="{GREY}" stroke-width="4"></rect></svg>', "기존 PoC (위반 8회)")
            + item(f'<svg width="64" height="24" viewBox="0 0 64 24" aria-hidden="true"><line x1="2" y1="12" x2="62" y2="12" stroke="{NAVY}" stroke-width="5"></line><circle cx="32" cy="12" r="10" fill="{NAVY}" stroke="#FFFFFF" stroke-width="3"></circle></svg>', "제안 구조 (위반 4회)")
            + item(f'<svg width="32" height="26" viewBox="0 0 32 26" aria-hidden="true"><path d="M16 2 L29 24 L3 24 Z" fill="{NAVY}"></path></svg>', "용량 조달 (v: 벤더)")
            + item(f'<svg width="64" height="24" viewBox="0 0 64 24" aria-hidden="true"><line x1="2" y1="12" x2="62" y2="12" stroke="{ORANGE}" stroke-width="4"></line></svg>', "SLA 위반 경계 (부하율 1.0)")
            + '</div>')

def stat(num, label, size):
    return (f'<div><p class="num" style="margin: 0; font-size: {size}px; line-height: 1; font-weight: 700; letter-spacing: -0.03em; color: {NAVY}; white-space: nowrap">{num}</p>'
            f'<p class="tx" style="margin: 10px 0 0">{label}</p></div>')

def section(title, body, area):
    return (f'<section data-area="{area}" style="display: flex; flex-direction: column">'
            f'<h2 class="bar">{title}</h2><div class="body">{body}</div></section>')

S1 = section("연구 배경과 문제", f'''<ul class="pb">
<li>AI 기반 망관리가 확산되지만, 에이전트에 자원관리를 전적으로 맡기기엔 신뢰와 위험부담 문제가 남아 있다.</li>
<li>ITU-T FG-AINN(2024년 7월 SG13 설립)은 PoC로 5G 네트워크 슬라이싱의 AI 기반 관리를 시연했다.</li>
<li>PoC 구조의 두 한계: 망관리자가 상황을 직접 지정해야 하고, 마켓플레이스가 오케스트레이터와 분리돼 용량 확보를 사람이 한다.</li>
</ul>
<table class="pt" style="margin-top: 28px; table-layout: fixed">
<thead><tr><th style="width: 190px; background: {LIGHT}; color: {NAVY}">구분</th><th style="width: 520px; background: {GREY}; color: #FFFFFF">기존 PoC 구조</th><th style="background: {NAVY}; color: #FFFFFF">제안 구조</th></tr></thead>
<tbody>
<tr><td style="font-weight: 700">상황인지</td><td class="mu">망관리자가 직접 지정</td><td style="font-weight: 700; color: {NAVY}">HMM 전진 필터로 자동 추론</td></tr>
<tr><td style="font-weight: 700">자원배분</td><td class="mu">상황별 고정 배분표</td><td style="font-weight: 700; color: {NAVY}">수요·잡음·임계값으로 산출</td></tr>
<tr><td style="font-weight: 700">용량 확보</td><td class="mu">마켓플레이스 분리, 사람이 조달</td><td style="font-weight: 700; color: {NAVY}">수요 압력 기준 자동 조달</td></tr>
<tr><td style="font-weight: 700">사람 개입</td><td class="mu">상시 감시</td><td style="font-weight: 700; color: {NAVY}">신뢰도 0.9 미만일 때만 질의</td></tr>
<tr><td style="font-weight: 700">결정 기록</td><td class="mu">상태 이력만 저장</td><td style="font-weight: 700; color: {NAVY}">결정 근거와 호출 순서까지 기록</td></tr>
</tbody></table>''', "연구 배경과 문제")

S2 = section("제안 구조 (그림 1)", f'''{diagram()}
<p class="tx" style="margin: 26px 0 0; font-weight: 700; color: {NAVY}">배분 결정은 Agent Layer가 내리고, Orchestrator MCP는 결정된 배분을 적용한다.</p>
<div class="sm" style="margin-top: 18px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 44px; row-gap: 14px">
<p style="margin: 0"><b>Intent / Service Layer</b> — 망관리자 의도와 SLA를 정책으로 변환해 에이전트 계층에 목표로 전달</p>
<p style="margin: 0"><b>Agent Layer</b> — 마스터 에이전트(Supervisor Agent)가 하위 전문 에이전트를 조율하고, 공유 지식베이스(과거 장애·조치 이력, RAG)를 참조</p>
<p style="margin: 0"><b>MCP Layer</b> — 텔레메트리·토폴로지·설정·오케스트레이터 기능을 독립 MCP 서버로 분리</p>
<p style="margin: 0"><b>Network Infra Layer</b> — 테스트베드의 RAN·코어·전송 네트워크</p>
</div>''', "제안 구조")

FORM_COLS, FORM_SIZE = ("minmax(0, 1.35fr) minmax(0, 1fr)", 46) if VARIANT == "gemini" else ("minmax(0, 1fr) minmax(0, 1fr)", 50)
FORMULAS = f'''<div style="display: grid; grid-template-columns: {FORM_COLS}; column-gap: 40px">
{formula("식 1 — 상황 사후확률 (HMM 전진 필터)", "(식1)", EQ1, FORM_SIZE)}
{formula("식 2 — 수요 압력", "(식2)", EQ2, FORM_SIZE)}
</div>
<p class="sm mu" style="margin: 18px 0 0"><i>b</i> = 상황 <i>s</i>의 사후확률, <i>A</i> = 상황 전이확률, <i>x</i> = 슬라이스별 수요, <i>θ<sub>i</sub></i> = 슬라이스 <i>i</i>의 이용률 임계값(eMBB 0.9 · URLLC 1.2 · mMTC 0.8), <i>C<sub>i,t</sub></i> = 슬라이스 <i>i</i>의 용량(기본 1.6, 조달로 최대 2.6).</p>
<div style="margin-top: 16px; display: flex; flex-wrap: wrap; align-items: center; column-gap: 48px; row-gap: 6px">
<span class="cap" style="width: 100%; font-weight: 700; color: {MUTED}">PoC 벤더 점수식과 조달 용량</span>
<span class="math" style="font-size: 36px">{SV}</span>
<span class="math" style="font-size: 36px">{DC}</span>
<span class="sm mu">URLLC <i>B</i><sub>ref</sub> = 500 Mbps</span>
</div>'''

S3 = section("에이전트 4단계 폐루프", f'''{loop()}
<div style="margin-top: 30px">{example(FORMULAS)}</div>
<p class="tx" style="margin: 22px 0 0; font-weight: 700">하위 에이전트끼리는 직접 호출하지 않고 Supervisor Agent를 거치므로 판단 근거가 모두 기록에 남는다.</p>''', "에이전트 4단계 폐루프")

S4 = section("실험 설정", f'''<table class="pt">
<tbody>
<tr><td style="width: 190px; font-weight: 700">시나리오</td><td>응급 상황이 처음부터 이어지는 10스텝 (1스텝 = 15분)</td></tr>
<tr><td style="font-weight: 700">반복</td><td>시드 0~4로 5회, 같은 시드에는 두 방식에 같은 트래픽</td></tr>
<tr><td style="font-weight: 700">비교군</td><td class="mu">기존 PoC 재현 — 망관리자가 정답 상황을 즉시 지정, 고정 배분표, 조달 없음</td></tr>
<tr><td style="font-weight: 700">제안</td><td style="font-weight: 700; color: {NAVY}">에이전트 기반 오케스트레이터 — LLM(Claude), 5개 MCP 서버 · 21개 도구</td></tr>
<tr><td style="font-weight: 700">공통 설정</td><td>PoC의 슬라이스 구성(eMBB·URLLC·mMTC), SLA 임계값, 트래픽 생성식, 배분 평활</td></tr>
<tr><td style="font-weight: 700">용량</td><td>슬라이스당 기본 1.6, 조달 시 최대 2.6</td></tr>
</tbody></table>''', "실험 설정")

SEED = [("0", "9", "3", "5", "4,550", "0"), ("1", "7", "3", "2", "2,500", "0"), ("2", "9", "5", "6", "5,225", "0"),
        ("3", "8", "4", "5", "4,975", "2"), ("4", "6", "4", "4", "3,750", "1")]
seed_rows = "".join(f'<tr><td>{a}</td><td class="mu">{b}</td><td style="font-weight: 700; color: {NAVY}">{c}</td><td>{d}</td><td>{e}</td><td>{f}</td></tr>' for a, b, c, d, e, f in SEED)
seed_rows += ''.join([f'<tr>'] + [f'<td style="font-weight: 700; border-top: 4px solid {NAVY}{"; color: " + NAVY if i == 2 else ""}">{v}</td>' for i, v in enumerate(("평균", "7.8", "3.8", "4.4", "4,200", "0.6"))] + ['</tr>'])

STATS = f'''<div style="display: flex; align-items: center; gap: 48px">
<p class="num" style="margin: 0; font-size: 230px; line-height: 0.95; font-weight: 700; letter-spacing: -0.04em; color: {NAVY}; white-space: nowrap">51%</p>
<p style="margin: 0; font-size: 56px; line-height: 1.25; font-weight: 700">SLA 위반 감소<br><span style="font-size: 44px; font-weight: 400; color: {MUTED}">(평균 7.8 → 3.8회)</span></p>
</div>
<div style="margin-top: 36px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: 44px; align-items: start">
{stat("22 / 22", "용량이 모자란 스텝을 모두 자동 조달", 120)}
{stat("3 / 50", "망관리자 질의가 필요했던 스텝", 120)}
{stat("47 / 47", "자율 판단한 스텝의 상황인지 정확", 120)}
</div>'''

S5 = section("실험 결과", f'''{alert(STATS)}
<figure style="margin: 40px 0 0; display: flex; flex-direction: column; gap: 10px">
{legend()}
<p class="sm mu" style="margin: 8px 0 0">최대 슬라이스 부하율 (이용률 ÷ 임계값)</p>
{chart()}
<figcaption class="cap">그림 2. 응급 상황에서 기존 PoC 대비 스텝별 최대 슬라이스 부하율 (시드 3, 5회 중 평균에 가장 가까운 시드)</figcaption>
</figure>
<div style="margin-top: 34px; display: grid; grid-template-columns: 820px minmax(0, 1fr); column-gap: 44px; align-items: start">
<table class="pt pn">
<thead><tr><th>시드</th><th>기존 PoC<br>위반(회)</th><th>제안<br>위반(회)</th><th>조달<br>(회)</th><th>조달 비용<br>(USD)</th><th>망관리자<br>질의(회)</th></tr></thead>
<tbody>{seed_rows}</tbody></table>
<ul class="pb">
<li>모든 시드에서 위반이 줄었고, 평균 7.8회에서 3.8회로 51% 감소했다.</li>
<li>기존 PoC는 수요 압력 0.8 이상인 34스텝에서 용량을 늘릴 수단이 없었고, 제안 구조는 22스텝 모두에서 벤더를 조달했다.</li>
<li>망관리자 질의는 50스텝 중 3스텝뿐이었다.</li>
</ul>
</div>''', "실험 결과")

S6 = section("결론과 기여", f'''<div style="display: grid; grid-template-columns: minmax(0, 1fr) 95px; column-gap: 40px; align-items: start">
<ul class="pb">
<li><b style="color: {NAVY}">폐루프 자동화</b> — FG-AINN PoC에 에이전트 계층을 더해 상황인지부터 용량 조달까지 사람 없이 돌게 했다.</li>
<li><b style="color: {NAVY}">수요 압력 지표</b> — “배분 조정으로 충분한가, 용량 확보가 필요한가”를 식 2 하나로 판정한다.</li>
<li><b style="color: {NAVY}">선택적 개입</b> — 상시 감시 대신, 상황 신뢰도가 낮을 때만 망관리자에게 묻는다.</li>
<li><b style="color: {NAVY}">한계와 향후</b> — 검증이 응급 시나리오에 한정되어, 혼합 상황 실험과 FG-AINN 표준 기고 연계로 넓힌다.</li>
</ul>
<div style="width: 95px; height: 95px; background: {LIGHT}; display: flex; align-items: center; justify-content: center; text-align: center; font-size: 24px; line-height: 1.15; color: {MUTED}">QR<br>미정</div>
</div>''', "결론과 기여")

S7 = section("참고문헌", '''<div style="display: grid; grid-template-columns: 48px minmax(0, 1fr); row-gap: 8px; font-size: 24px; line-height: 1.35">
<span>[1]</span><span>ITU-T Rec. Y.3061 (12/2023), Autonomous networks – Architecture framework.</span>
<span>[2]</span><span>ITU-T FG-AINN, Technical Report: Proof-of-Concept activities, 2026.</span>
<span>[3]</span><span>ITU-T FG-AINN, LS on FG-AINN 2026 work plan (FG-AINN-O-016), Dec. 2025.</span>
<span>[4]</span><span>Anthropic, Model Context Protocol Specification, modelcontextprotocol.io, 2024.</span>
</div>''', "참고문헌")

GAP = int(sys.argv[2]) if len(sys.argv) > 2 else 60
html = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><title>A0 포스터 — Aragon 템플릿 내용</title>
<link href="https://fonts.googleapis.com/css2?family=STIX+Two+Text:ital,wght@0,400;1,400&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0}}
.ar{{position:relative;width:3179px;height:4494px;background:#FFFFFF;font-family:'Malgun Gothic',sans-serif;color:{INK};word-break:keep-all;letter-spacing:-0.01em}}
.ar .col{{position:absolute;top:{TOP}px;width:{COL_W}px;height:{BOTTOM - TOP}px;display:flex;flex-direction:column;justify-content:space-between;gap:{GAP}px}}
.ar h2.bar{{{H2_CSS}}}
.ar .body{{padding:28px {PAD}px 0}}
.ar .tx{{font-size:36px;line-height:1.35;text-wrap:pretty}}
.ar .sm{{font-size:32px;line-height:1.35;text-wrap:pretty}}
.ar .cap{{font-size:26.67px;line-height:1.35;color:{MUTED}}}
.ar .mu{{color:{MUTED}}}
.ar ul.pb{{margin:0;padding-left:44px;font-size:36px;line-height:1.35;text-wrap:pretty}}
.ar ul.pb li{{margin:0 0 12px;padding-left:4px}}
.ar ul.pb li:last-child{{margin-bottom:0}}
.ar table.pt{{border-collapse:collapse;width:100%;font-size:32px;line-height:1.3;font-variant-numeric:tabular-nums}}
.ar table.pt th,.ar table.pt td{{padding:10px 14px;text-align:left;vertical-align:top;border-bottom:2px solid {RULE}}}
.ar table.pt th{{font-weight:700}}
.ar table.pt tr:last-child td{{border-bottom:none}}
.ar table.pn th{{background:{NAVY};color:#FFFFFF;text-align:right;padding:8px 10px}}
.ar table.pn td{{text-align:right;padding:8px 10px}}
.ar table.pn td:first-child,.ar table.pn th:first-child{{text-align:left}}
.ar .math{{font-family:'STIX Two Text','Cambria Math',serif;letter-spacing:0;white-space:nowrap}}
.ar .num{{font-variant-numeric:tabular-nums}}
</style></head><body>
<div class="ar">
{headline()}
<div class="col" data-area="왼쪽 단" style="left: {LEFT_X}px">{S1}{S2}{S3}</div>
<div class="col" data-area="오른쪽 단" style="left: {RIGHT_X}px">{S4}{S5}{S6}{S7}</div>
</div>
</body></html>'''
open(out_path, "w", encoding="utf-8").write(html)
print("written", len(html))
