import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_c as g

tpl_path, out_path = sys.argv[1], sys.argv[2]
ACC = "{{accent}}"
INK = "#222222"
FS = 29.33          # 22 pt: text inside figures, tables and boxes

def est(label, bold=False):
    """Box width for a latin label at 22 pt (Noto Sans KR runs ~0.56 em a character, bold ~0.6)."""
    return round(len(label) * (0.6 if bold else 0.56) * FS + 22)

def box(left, top, w, h, label, solid=False, bold=False):
    border = f"2px dashed {ACC}"
    bg = ACC if solid else "#EEF3F8"
    color = "#FFFFFF" if solid else INK
    fw = "; font-weight: 700" if bold else ""
    return (f'<div style="position: absolute; left: {left}px; top: {top}px; width: {w}px; height: {h}px; box-sizing: border-box; border: {border}; '
            f'border-radius: 10px; background: {bg}; color: {color}; display: flex; align-items: center; justify-content: center; white-space: nowrap{fw}">{label}</div>')

def band(top, h, W, label=None, centered=False):
    inner = ""
    if label:
        inner = label
    align = "justify-content: center" if centered else "justify-content: flex-start; padding-left: 18px"
    return (f'<div style="position: absolute; left: 0px; top: {top}px; width: {W}px; height: {h}px; box-sizing: border-box; border: 3px solid {ACC}; '
            f'border-radius: 14px; background: #FFFFFF; display: flex; align-items: center; {align}; font-weight: 700; color: {ACC}">{inner}</div>')

def diagram(W=1036, H=707):
    o = [f'<div role="img" aria-label="그림 1: Intent/Service, Agent, MCP, Network Infra의 4계층 구조" style="position: relative; width: {W}px; height: {H}px; font-size: {FS}px; line-height: 1.2">']
    I0, I1 = 0, 66                 # Intent / Service
    A0, A1 = 116, 362              # Agent
    M0, M1 = 442, 572              # MCP
    N0, N1 = 641, 707              # Network Infra
    o += [band(I0, I1 - I0, W, "Intent / Service Layer", True), band(A0, A1 - A0, W), band(M0, M1 - M0, W), band(N0, N1 - N0, W, "Network Infra Layer", True)]
    cx = W // 2
    # agent row: five boxes sized to their labels, spread across the band
    names = ["Monitoring", "Diagnosis", "Planning", "Execution", "Verification"]
    ws = [est(n) for n in names]
    pad = 18
    gap = (W - 2 * pad - sum(ws)) / 4
    lefts, x = [], pad
    for w in ws:
        lefts.append(round(x)); x += w + gap
    cents = [l + w // 2 for l, w in zip(lefts, ws)]
    by0, bh = A0 + 128, 56
    sup_w, rag_w = est("Supervisor Agent", True), 100
    sup_l = cx - sup_w // 2
    sy = A0 + 22
    # lines first
    o.append(g.arrow_svg(sup_l + sup_w, sy + 28, sup_l + sup_w + 50, sy + 28, ACC, 3, False))
    o.append(g.arrow_svg(cx, sy + 56, cx, sy + 82, ACC, 3, False))
    o.append(g.arrow_svg(cents[0], sy + 82, cents[-1], sy + 82, ACC, 3, False))
    for c in cents:
        o.append(g.arrow_svg(c, sy + 82, c, by0 - 1, ACC, 3, True))
    for i in range(4):
        o.append(g.arrow_svg(lefts[i] + ws[i], by0 + bh // 2, lefts[i + 1] - 1, by0 + bh // 2, ACC, 3, True))
    lane = by0 + bh + 22
    o.append(g.arrow_svg(cents[4], by0 + bh, cents[4], lane, ACC, 3, False))
    o.append(g.arrow_svg(cents[1], lane, cents[4], lane, ACC, 3, False))
    o.append(g.arrow_svg(cents[1], lane, cents[1], by0 + bh + 1, ACC, 3, True))
    # mcp row: two pairs either side of the gap the layer arrows pass through
    mn = ["Telemetry", "Topology", "Orchestrator", "Configuration"]
    mw = [est(n) for n in mn]
    mgap = (W - 2 * pad - sum(mw)) / 3
    ml, x = [], pad
    for w in mw:
        ml.append(round(x)); x += w + mgap
    ax = round((ml[1] + mw[1] + ml[2]) / 2)           # middle of the gap between Topology and Orchestrator
    for top, bot in ((A1, M0), (M1, N0)):            # bidirectional only Agent-MCP and MCP-Network Infra
        o.append(g.arrow_svg(ax - 16, top, ax - 16, bot - 1, ACC, 3, True))
        o.append(g.arrow_svg(ax + 16, bot, ax + 16, top + 1, ACC, 3, True))
    # boxes
    o.append(box(sup_l, sy, sup_w, 56, "Supervisor Agent", solid=True, bold=True))
    o.append(box(sup_l + sup_w + 50, sy, rag_w, 56, "RAG"))
    for l, w, n in zip(lefts, ws, names):
        o.append(box(l, by0, w, bh, n))
    my = M0 + 58
    for l, w, n in zip(ml, mw, mn):
        o.append(box(l, my, w, 54, n))
    o.append(f'<div style="position: absolute; left: 18px; top: {A0 + 12}px; font-weight: 700; color: {ACC}">Agent Layer</div>')
    o.append(f'<div style="position: absolute; left: 18px; top: {M0 + 10}px; font-weight: 700; color: {ACC}">MCP Layer</div>')
    o.append('</div>')
    return "\n".join(o)

STAGES = [
    ("1", "상황인지", "Monitoring · Diagnosis", "Telemetry MCP로 슬라이스별 수요 <i>x</i>를 모으고 상황 <i>s</i>(평시·응급·대형 행사·IoT 급증)를 추론", "식 1, 같은 상황 유지 확률 0.98"),
    ("2", "자원배분 결정", "Planning", "이용률 임계값 <i>θ</i>와 용량 <i>C</i>로 목표 배분을 산출해 Orchestrator MCP로 적용하고 수요 압력 <i>P</i>를 계산", "식 2, <i>P</i>가 1을 넘으면 배분만으로는 SLA 불가"),
    ("3", "자원할당", "Execution", "<i>P</i>가 임계값 이상이면 압력을 가장 크게 낮추는 슬라이스의 용량을 마켓플레이스에서 조달", "응급 0.8 · 그 밖 1.0, 벤더는 PoC 점수식으로 선택"),
    ("4", "판단검증", "Verification", "상황 신뢰도가 0.9 미만일 때만 망관리자에게 질의하고 결과를 Diagnosis로 되돌리며, SLA 충족 여부를 벤더 평판에 반영", "신뢰도 = 사후확률 최댓값"),
]
BOX_W, ARR_W = 667, 65

def stages():
    out = []
    for i, (n, name, agent, desc, foot) in enumerate(STAGES):
        if i:
            g._mid[0] += 1
            mid = f"dc-arrow-head-filled-{g._mid[0]}"
            out.append(f'<div style="width: {ARR_W}px; flex: none; display: flex; align-items: center; justify-content: center"><svg width="46" height="10" viewBox="0 0 46 10" aria-hidden="true" '
                       f'style="overflow: visible; fill: none; stroke: {ACC}; stroke-width: 5; stroke-linecap: round"><defs><marker id="{mid}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible">'
                       f'<path d="M0 0 L4 2 L0 4 Z" fill="{ACC}" stroke="none" style="stroke: none; fill: {ACC}; fill: context-stroke"></path></marker></defs><path d="M 0 5 L 36 5" marker-end="url(#{mid})"></path></svg></div>')
        out.append(f'<div style="width: {BOX_W}px; flex: none; box-sizing: border-box; background: #FFFFFF; border: 3px solid {ACC}; border-radius: 14px; padding: 20px 24px; display: flex; flex-direction: column; gap: 6px">'
                   f'<div style="display: flex; align-items: center; gap: 14px"><span style="width: 50px; height: 50px; flex: none; border-radius: 25px; background: {ACC}; color: #FFFFFF; font-size: 29.33px; font-weight: 700; display: flex; align-items: center; justify-content: center">{n}</span>'
                   f'<span style="font-size: 42.67px; line-height: 1.15; font-weight: 700; color: {ACC}">{name}</span></div>'
                   f'<p class="sm mu" style="margin: 0">{agent}</p>'
                   f'<p class="sm" style="margin: 2px 0 0">{desc}</p>'
                   f'<p class="sm" style="margin: auto 0 0; padding-top: 10px; border-top: 2px solid #D3DBE4; font-weight: 700; color: {ACC}">{foot}</p></div>')
    return "\n".join(out)

def loop(W=2863):
    c1, c4 = BOX_W // 2, 3 * (BOX_W + ARR_W) + BOX_W // 2
    o = [f'<div style="position: relative; width: {W}px; height: 54px; flex: none">']
    o.append(g.arrow_svg(c4, 0, c4, 30, ACC, 4, False))
    o.append(g.arrow_svg(c1, 30, c4, 30, ACC, 4, False))
    o.append(g.arrow_svg(c1, 30, c1, 1, ACC, 4, True))
    mid = (c1 + c4) // 2
    o.append(f'<div style="position: absolute; left: {mid - 170}px; top: 10px; width: 340px; height: 40px; background: #F3F6F9; display: flex; align-items: center; justify-content: center; '
             f'font-size: 29.33px; line-height: 1; font-weight: 700; color: {ACC}">매 스텝(15분) 반복</div>')
    o.append('</div>')
    return "\n".join(o)

def chart(CW=1111, H=680):
    TOP, BOT, LO, HI = 160, 560, 0.5, 2.3
    X0, X1 = 100, CW - 30
    base = [0.897, 1.000, 1.132, 1.503, 1.184, 2.208, 1.259, 1.106, 1.539, 1.614]
    prop = [0.741, 0.793, 0.946, 1.060, 1.014, 1.039, 1.028, 0.929, 0.936, 0.864]
    buys = {3: "v1", 4: "v1", 5: "v1", 8: "v3", 9: "v5"}
    x = lambda i: round(X0 + i * (X1 - X0) / 9, 1)
    y = lambda v: round(BOT - (v - LO) * (BOT - TOP) / (HI - LO), 1)
    G, F = "#444444", FS
    o = [f'<svg width="{CW}" height="{H}" viewBox="0 0 {CW} {H}" role="img" aria-label="그림 2: 시드 3의 스텝별 최대 슬라이스 부하율. 기존 PoC는 위반 8회, 제안 구조는 위반 4회" '
         f'style="display: block; font-family: \'Pretendard\', \'Noto Sans KR\', sans-serif; background: #FFFFFF; border-radius: 12px">']
    # legend (two rows) and y-axis title
    o.append(f'<line x1="24" y1="34" x2="84" y2="34" stroke="#8C8C8C" stroke-width="4" stroke-dasharray="10 7"></line><rect x="44" y="24" width="20" height="20" fill="#FFFFFF" stroke="#8C8C8C" stroke-width="4"></rect>')
    o.append(f'<text x="96" y="44" font-size="{F}" fill="{INK}">기존 PoC (위반 8회)</text>')
    o.append(f'<line x1="420" y1="34" x2="480" y2="34" stroke="{ACC}" stroke-width="5"></line><circle cx="450" cy="34" r="10" fill="{ACC}" stroke="#FFFFFF" stroke-width="3"></circle>')
    o.append(f'<text x="492" y="44" font-size="{F}" fill="{INK}">제안 구조 (위반 4회)</text>')
    o.append(f'<path d="M54 64 L67 86 L41 86 Z" fill="{ACC}"></path><text x="96" y="88" font-size="{F}" fill="{INK}">용량 조달 (v: 벤더)</text>')
    o.append(f'<line x1="420" y1="78" x2="480" y2="78" stroke="#E07B00" stroke-width="4"></line><text x="492" y="88" font-size="{F}" fill="{INK}">SLA 위반 경계 (부하율 1.0)</text>')
    o.append(f'<text x="24" y="138" font-size="{F}" fill="{G}">최대 슬라이스 부하율 (이용률 ÷ 임계값)</text>')
    for v in (2.0, 1.5):
        o.append(f'<line x1="{X0}" y1="{y(v)}" x2="{X1}" y2="{y(v)}" stroke="#E1E6EC" stroke-width="2"></line>')
    o.append(f'<line x1="{X0}" y1="{BOT}" x2="{X1}" y2="{BOT}" stroke="#8C8C8C" stroke-width="2"></line>')
    for v in (2.0, 1.5, 1.0, 0.5):
        o.append(f'<text x="{X0 - 16}" y="{round(y(v) + 10, 1)}" font-size="{F}" fill="{G}" text-anchor="end">{v:.1f}</text>')
    for i in range(10):
        o.append(f'<text x="{x(i)}" y="{BOT + 40}" font-size="{F}" fill="{G}" text-anchor="middle">{i}</text>')
    o.append(f'<text x="{(X0 + X1) // 2}" y="{BOT + 82}" font-size="{F}" fill="{G}" text-anchor="middle">스텝 (15분 간격)</text>')
    o.append(f'<line x1="{X0}" y1="{y(1.0)}" x2="{X1}" y2="{y(1.0)}" stroke="#E07B00" stroke-width="4"></line>')
    o.append('<polyline points="' + " ".join(f"{x(i)},{y(v)}" for i, v in enumerate(base)) + '" fill="none" stroke="#8C8C8C" stroke-width="4" stroke-dasharray="14 10" stroke-linejoin="round"></polyline>')
    for i, v in enumerate(base):
        o.append(f'<rect x="{round(x(i) - 10, 1)}" y="{round(y(v) - 10, 1)}" width="20" height="20" fill="#FFFFFF" stroke="#8C8C8C" stroke-width="4"></rect>')
    o.append('<polyline points="' + " ".join(f"{x(i)},{y(v)}" for i, v in enumerate(prop)) + f'" fill="none" stroke="{ACC}" stroke-width="5" stroke-linejoin="round"></polyline>')
    for i, v in enumerate(prop):
        o.append(f'<circle cx="{x(i)}" cy="{y(v)}" r="11" fill="{ACC}" stroke="#FFFFFF" stroke-width="3"></circle>')
    for i, name in buys.items():
        cx, cy = x(i), round(y(prop[i]) + 34, 1)
        d = f"M{cx} {round(cy - 13, 1)} L{round(cx + 13, 1)} {round(cy + 9, 1)} L{round(cx - 13, 1)} {round(cy + 9, 1)} Z"
        o.append(f'<path d="{d}" fill="#FFFFFF" stroke="{ACC}" stroke-width="3"></path>' if i == 9 else f'<path d="{d}" fill="{ACC}"></path>')
        if i >= 8:
            o.append(f'<text x="{round(cx - 22, 1)}" y="{round(cy + 10, 1)}" font-size="{F}" font-weight="700" fill="{ACC}" text-anchor="end">{name}</text>')
        else:
            o.append(f'<text x="{round(cx + 18, 1)}" y="{round(cy + 10, 1)}" font-size="{F}" font-weight="700" fill="{ACC}" text-anchor="start">{name}</text>')
    o.append('</svg>')
    return "\n".join(o)

s = open(tpl_path, encoding="utf-8").read()
s = s.replace("@@DIAGRAM@@", diagram())
s = s.replace("@@STAGES@@", stages())
s = s.replace("@@LOOP@@", loop())
s = s.replace("@@CHART@@", chart())
open(out_path, "w", encoding="utf-8").write(s)
print("written", len(s))
