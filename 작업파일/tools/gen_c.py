import sys

tpl_path, out_path = (sys.argv[1], sys.argv[2]) if __name__ == "__main__" else (None, None)
INK, BLUE = "#111111", "{{blue}}"
_mid = [0]

def arrow_svg(x1, y1, x2, y2, color, sw, head):
    """One straight segment as the editor's arrow svg; (x1,y1)->(x2,y2) is tail->tip."""
    _mid[0] += 1
    h = 2 * sw if head else 0
    if y1 == y2:
        left, n = min(x1, x2), abs(x2 - x1)
        top, W, H = y1 - 4, n, 8
        d = f"M 0 4 L {n - h} 4" if x2 > x1 else f"M {n} 4 L {h} 4"
    else:
        top, n = min(y1, y2), abs(y2 - y1)
        left, W, H = x1 - 4, 8, n
        d = f"M 4 0 L 4 {n - h}" if y2 > y1 else f"M 4 {n} L 4 {h}"
    defs, me = "", ""
    if head:
        mid = f"dc-arrow-head-filled-{_mid[0]}"
        defs = (f'<defs><marker id="{mid}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible">'
                f'<path d="M0 0 L4 2 L0 4 Z" fill="{color}" stroke="none" style="stroke: none; fill: {color}; fill: context-stroke"></path></marker></defs>')
        me = f' marker-end="url(#{mid})"'
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" preserveAspectRatio="none" style="position: absolute; left: {left}px; top: {top}px; '
            f'width: {W}px; height: {H}px; overflow: visible; fill: none; stroke: {color}; stroke-width: {sw}; stroke-linecap: round; stroke-linejoin: round">'
            f'{defs}<path d="{d}"{me}></path></svg>')

def box(left, top, w, h, label, bg, color=INK, bold=False):
    fw = "; font-weight: 700" if bold else ""
    return (f'<div style="position: absolute; left: {left}px; top: {top}px; width: {w}px; height: {h}px; background: {bg}; color: {color}; '
            f'display: flex; align-items: center; justify-content: center{fw}">{label}</div>')

def diagram(W, band="#F2F2F2", comp="#FFFFFF", sup=None):
    cx = W // 2
    out = [f'<div role="img" aria-label="그림 1: Intent/Service, Agent, MCP, Network Infra의 4계층 구조" style="position: relative; width: {W}px; height: 498px; font-size: 32px; line-height: 1.25">']
    bandf = lambda top, h, label="": (f'<div style="position: absolute; left: 0px; top: {top}px; width: {W}px; height: {h}px; box-sizing: border-box; padding-left: 32px; '
                                      f'background: {band}; display: flex; align-items: center; font-weight: 700">{label}</div>')
    out += [bandf(0, 56, "Intent / Service Layer"), bandf(86, 216), bandf(332, 80), bandf(442, 56, "Network Infra Layer")]
    for top in (302, 412):   # bidirectional only Agent-MCP and MCP-Network Infra
        out.append(arrow_svg(cx - 20, top, cx - 20, top + 29, INK, 3, True))
        out.append(arrow_svg(cx + 20, top + 30, cx + 20, top + 1, INK, 3, True))
    out.append(arrow_svg(cx + 170, 132, cx + 240, 132, INK, 3, False))
    out.append(arrow_svg(cx, 160, cx, 184, INK, 3, False))
    bw, gap = 260, 52
    start = (W - (5 * bw + 4 * gap)) // 2
    lefts = [start + i * (bw + gap) for i in range(5)]
    centers = [l + bw // 2 for l in lefts]
    out.append(arrow_svg(centers[0], 184, centers[-1], 184, INK, 3, False))
    for c in centers:
        out.append(arrow_svg(c, 184, c, 213, INK, 3, True))
    for l in lefts[:-1]:
        out.append(arrow_svg(l + bw, 242, l + bw + gap - 1, 242, INK, 3, True))
    out.append(arrow_svg(centers[4], 270, centers[4], 286, INK, 3, False))
    out.append(arrow_svg(centers[1], 286, centers[4], 286, INK, 3, False))
    out.append(arrow_svg(centers[1], 286, centers[1], 271, INK, 3, True))
    out.append(box(cx - 170, 104, 340, 56, "Supervisor Agent", sup or BLUE, "#FFFFFF", True))
    out.append(box(cx + 240, 104, 120, 56, "RAG", comp))
    for l, name in zip(lefts, ["Monitoring", "Diagnosis", "Planning", "Execution", "Verification"]):
        out.append(box(l, 214, bw, 56, name, comp))
    mw, mg = 260, 50
    for l, name in zip([cx - 25 - 2 * mw - mg, cx - 25 - mw, cx + 25, cx + 25 + mw + mg], ["Telemetry", "Topology", "Orchestrator", "Configuration"]):
        out.append(box(l, 346, mw, 52, name, comp))
    out.append('<div style="position: absolute; left: 32px; top: 100px; font-weight: 700">Agent Layer</div>')
    out.append('<div style="position: absolute; left: 32px; top: 352px; font-weight: 700">MCP Layer</div>')
    out.append('</div>')
    return "\n".join(out)

def stage_arrow(width):
    _mid[0] += 1
    mid = f"dc-arrow-head-filled-{_mid[0]}"
    return (f'<div style="width: {width}px; flex: none; display: flex; align-items: center; justify-content: center"><svg width="52" height="10" viewBox="0 0 52 10" aria-hidden="true" '
            f'style="overflow: visible; fill: none; stroke: {INK}; stroke-width: 5; stroke-linecap: round"><defs><marker id="{mid}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible">'
            f'<path d="M0 0 L4 2 L0 4 Z" fill="{INK}" stroke="none" style="stroke: none; fill: {INK}; fill: context-stroke"></path></marker></defs><path d="M 0 5 L 42 5" marker-end="url(#{mid})"></path></svg></div>')

def loop(W, c_first, c_last, color=None, lbg="#FFFFFF"):
    color = color or BLUE
    out = [f'<div style="position: relative; width: {W}px; height: 60px; margin-top: 18px">']
    out.append(arrow_svg(c_last, 0, c_last, 32, color, 6, False))
    out.append(arrow_svg(c_first, 32, c_last, 32, color, 6, False))
    out.append(arrow_svg(c_first, 32, c_first, 1, color, 6, True))
    mid = (c_first + c_last) // 2
    out.append(f'<div style="position: absolute; left: {mid - 200}px; top: 8px; width: 400px; height: 48px; background: {lbg}; color: {color}; display: flex; align-items: center; '
               f'justify-content: center; font-size: 36px; line-height: 1; font-weight: 700">매 스텝(15분) 반복</div>')
    out.append('</div>')
    return "\n".join(out)

def chart(CW, G="#555555", grid="#E0E0E0", axis="#8C8C8C", base_c="#8C8C8C", hollow="#FFFFFF", rim="#FFFFFF", prop_c=None):
    prop_c = prop_c or BLUE
    H, TOP, BOT, LO, HI = 400, 20, 310, 0.5, 2.3
    X0, X1 = 110, CW - 28
    base = [0.897, 1.000, 1.132, 1.503, 1.184, 2.208, 1.259, 1.106, 1.539, 1.614]
    prop = [0.741, 0.793, 0.946, 1.060, 1.014, 1.039, 1.028, 0.929, 0.936, 0.864]
    buys = {3: "v1", 4: "v1", 5: "v1", 8: "v3", 9: "v5"}
    x = lambda i: round(X0 + i * (X1 - X0) / 9, 1)
    y = lambda v: round(BOT - (v - LO) * (BOT - TOP) / (HI - LO), 1)
    o = [f'<svg width="{CW}" height="{H}" viewBox="0 0 {CW} {H}" role="img" aria-label="그림 2: 시드 3의 스텝별 최대 슬라이스 부하율. 기존 PoC는 위반 8회, 제안 구조는 위반 4회" '
         f'style="display: block; font-family: \'Pretendard\', \'Noto Sans KR\', sans-serif">']
    for v in (2.0, 1.5):
        o.append(f'<line x1="{X0}" y1="{y(v)}" x2="{X1}" y2="{y(v)}" stroke="{grid}" stroke-width="2"></line>')
    o.append(f'<line x1="{X0}" y1="{BOT}" x2="{X1}" y2="{BOT}" stroke="{axis}" stroke-width="2"></line>')
    for v in (2.0, 1.5, 1.0, 0.5):
        o.append(f'<text x="{X0 - 20}" y="{round(y(v) + 11, 1)}" font-size="32" fill="{G}" text-anchor="end">{v:.1f}</text>')
    for i in range(10):
        o.append(f'<text x="{x(i)}" y="{BOT + 42}" font-size="32" fill="{G}" text-anchor="middle">{i}</text>')
    o.append(f'<text x="{(X0 + X1) // 2}" y="{BOT + 84}" font-size="32" fill="{G}" text-anchor="middle">스텝 (15분 간격)</text>')
    o.append(f'<line x1="{X0}" y1="{y(1.0)}" x2="{X1}" y2="{y(1.0)}" stroke="#E07B00" stroke-width="4"></line>')
    o.append('<polyline points="' + " ".join(f"{x(i)},{y(v)}" for i, v in enumerate(base)) + f'" fill="none" stroke="{base_c}" stroke-width="4" stroke-dasharray="14 10" stroke-linejoin="round"></polyline>')
    for i, v in enumerate(base):
        o.append(f'<rect x="{round(x(i) - 10, 1)}" y="{round(y(v) - 10, 1)}" width="20" height="20" fill="{hollow}" stroke="{base_c}" stroke-width="4"></rect>')
    o.append('<polyline points="' + " ".join(f"{x(i)},{y(v)}" for i, v in enumerate(prop)) + f'" fill="none" stroke="{prop_c}" stroke-width="5" stroke-linejoin="round"></polyline>')
    for i, v in enumerate(prop):
        o.append(f'<circle cx="{x(i)}" cy="{y(v)}" r="11" fill="{prop_c}" stroke="{rim}" stroke-width="3"></circle>')
    for i, name in buys.items():
        cx, cy = x(i), round(y(prop[i]) + 34, 1)
        d = f"M{cx} {round(cy - 13, 1)} L{round(cx + 13, 1)} {round(cy + 9, 1)} L{round(cx - 13, 1)} {round(cy + 9, 1)} Z"
        o.append(f'<path d="{d}" fill="{hollow}" stroke="{prop_c}" stroke-width="3"></path>' if i == 9 else f'<path d="{d}" fill="{prop_c}"></path>')
        if i >= 8:
            o.append(f'<text x="{round(cx - 22, 1)}" y="{round(cy + 11, 1)}" font-size="32" font-weight="700" fill="{prop_c}" text-anchor="end">{name}</text>')
        else:
            o.append(f'<text x="{round(cx + 18, 1)}" y="{round(cy + 11, 1)}" font-size="32" font-weight="700" fill="{prop_c}" text-anchor="start">{name}</text>')
    o.append('</svg>')
    return "\n".join(o)

if __name__ == "__main__":
  s = open(tpl_path, encoding="utf-8").read()
  s = s.replace("@@DIAGRAM@@", diagram(1700))
  while "@@ARROW@@" in s:
      s = s.replace("@@ARROW@@", stage_arrow(77), 1)
  s = s.replace("@@LOOP@@", loop(2951, 340, 2611))
  s = s.replace("@@CHART@@", chart(960))
  open(out_path, "w", encoding="utf-8").write(s)
  print("written", len(s))
