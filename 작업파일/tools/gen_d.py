import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_c as g

tpl_path, out_path = (sys.argv[1], sys.argv[2]) if __name__ == "__main__" else (None, None)
INK, GREY, MUTED, PAPER, ZEBRA = "#161616", "#948E80", "#5E594F", "#ECE8E0", "#F5F3EE"
SIG = "var(--sig)"
FS = 29.33          # 22 pt: text inside figures, tables and boxes
COL_L, COL_C, COL_R = 1000, 1113, 700
BODY_H = 4494 - 610 - 70 - 44 - 33 - 80

def est(label, bold=False):
    return round(len(label) * (0.6 if bold else 0.56) * FS + 22)

# ---------- 그림 1 ----------
def diagram(W=COL_L, H=707):
    def band(top, h, label=None):
        return (f'<div style="position: absolute; left: 0px; top: {top}px; width: {W}px; height: {h}px; box-sizing: border-box; border: 3px solid {INK}; '
                f'background: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700">{label or ""}</div>')
    def box(left, top, w, h, label, solid=False, bold=False):
        bg, color = (INK, "#FFFFFF") if solid else (PAPER, INK)
        fw = "; font-weight: 700" if bold else ""
        return (f'<div style="position: absolute; left: {left}px; top: {top}px; width: {w}px; height: {h}px; background: {bg}; color: {color}; '
                f'display: flex; align-items: center; justify-content: center; white-space: nowrap{fw}">{label}</div>')
    o = [f'<div role="img" aria-label="그림 1: Intent/Service, Agent, MCP, Network Infra의 4계층 구조" style="position: relative; width: {W}px; height: {H}px; font-size: {FS}px; line-height: 1.2">']
    I0, I1, A0, A1, M0, M1, N0, N1 = 0, 66, 116, 362, 442, 572, 641, 707
    o += [band(I0, I1 - I0, "Intent / Service Layer"), band(A0, A1 - A0), band(M0, M1 - M0), band(N0, N1 - N0, "Network Infra Layer")]
    cx, pad = W // 2, 14
    names = ["Monitoring", "Diagnosis", "Planning", "Execution", "Verification"]
    ws = [est(n) - 8 for n in names]
    gap = (W - 2 * pad - sum(ws)) / 4
    lefts, x = [], pad
    for w in ws:
        lefts.append(round(x)); x += w + gap
    cents = [l + w // 2 for l, w in zip(lefts, ws)]
    by0, bh = A0 + 128, 56
    sup_w, rag_w = est("Supervisor Agent", True), 100
    sup_l, sy = cx - sup_w // 2, A0 + 22
    o.append(g.arrow_svg(sup_l + sup_w, sy + 28, sup_l + sup_w + 50, sy + 28, INK, 3, False))
    o.append(g.arrow_svg(cx, sy + 56, cx, sy + 82, INK, 3, False))
    o.append(g.arrow_svg(cents[0], sy + 82, cents[-1], sy + 82, INK, 3, False))
    for c in cents:
        o.append(g.arrow_svg(c, sy + 82, c, by0 - 1, INK, 3, True))
    for i in range(4):
        o.append(g.arrow_svg(lefts[i] + ws[i], by0 + bh // 2, lefts[i + 1] - 1, by0 + bh // 2, INK, 3, True))
    lane = by0 + bh + 22
    o.append(g.arrow_svg(cents[4], by0 + bh, cents[4], lane, INK, 3, False))
    o.append(g.arrow_svg(cents[1], lane, cents[4], lane, INK, 3, False))
    o.append(g.arrow_svg(cents[1], lane, cents[1], by0 + bh + 1, INK, 3, True))
    mn = ["Telemetry", "Topology", "Orchestrator", "Configuration"]
    mw = [est(n) for n in mn]
    mgap = (W - 2 * pad - sum(mw)) / 3
    ml, x = [], pad
    for w in mw:
        ml.append(round(x)); x += w + mgap
    ax = round((ml[1] + mw[1] + ml[2]) / 2)
    for top, bot in ((A1, M0), (M1, N0)):            # bidirectional only Agent-MCP and MCP-Network Infra
        o.append(g.arrow_svg(ax - 16, top, ax - 16, bot - 1, INK, 3, True))
        o.append(g.arrow_svg(ax + 16, bot, ax + 16, top + 1, INK, 3, True))
    o.append(box(sup_l, sy, sup_w, 56, "Supervisor Agent", solid=True, bold=True))
    o.append(box(sup_l + sup_w + 50, sy, rag_w, 56, "RAG"))
    for l, w, n in zip(lefts, ws, names):
        o.append(box(l, by0, w, bh, n))
    for l, w, n in zip(ml, mw, mn):
        o.append(box(l, M0 + 58, w, 54, n))
    o.append(f'<div style="position: absolute; left: 18px; top: {A0 + 12}px; font-weight: 700">Agent Layer</div>')
    o.append(f'<div style="position: absolute; left: 18px; top: {M0 + 10}px; font-weight: 700">MCP Layer</div>')
    o.append('</div>')
    return "\n".join(o)

# ---------- ③ 네 단계: 위에서 아래로, 왼쪽 괄호가 4단계에서 1단계로 되돌아감 ----------
STAGES = [
    ("상황인지", "Monitoring · Diagnosis", "Telemetry MCP로 슬라이스별 수요 <i>x</i>를 모으고 상황 <i>s</i>(평시·응급·대형 행사·IoT 급증)를 추론", "식 1, 같은 상황 유지 확률 0.98"),
    ("자원배분 결정", "Planning", "이용률 임계값 <i>θ</i>와 용량 <i>C</i>로 목표 배분을 산출해 Orchestrator MCP로 적용하고 수요 압력 <i>P</i>를 계산", "식 2, <i>P</i>가 1을 넘으면 배분만으로는 SLA 불가"),
    ("자원할당", "Execution", "<i>P</i>가 임계값 이상이면 압력을 가장 크게 낮추는 슬라이스의 용량을 마켓플레이스에서 조달", "응급 0.8 · 그 밖 1.0, 벤더는 PoC 점수식으로 선택"),
    ("판단검증", "Verification", "상황 신뢰도가 0.9 미만일 때만 망관리자에게 질의하고 결과를 Diagnosis로 되돌리며, SLA 충족 여부를 벤더 평판에 반영", "신뢰도 = 사후확률 최댓값"),
]

def down_arrow():
    g._mid[0] += 1
    mid = f"dc-arrow-head-filled-{g._mid[0]}"
    return (f'<div style="height: 76px; flex: none; position: relative"><svg width="10" height="62" viewBox="0 0 10 62" aria-hidden="true" '
            f'style="position: absolute; left: 22px; top: 7px; overflow: visible; fill: none; stroke: {INK}; stroke-width: 5; stroke-linecap: round"><defs><marker id="{mid}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible">'
            f'<path d="M0 0 L4 2 L0 4 Z" fill="{INK}" stroke="none" style="stroke: none; fill: {INK}; fill: context-stroke"></path></marker></defs><path d="M 5 0 L 5 52" marker-end="url(#{mid})"></path></svg></div>')

def stages():
    o = ['<div style="position: relative; padding-left: 110px">',
         # return path: from stage 4 back up into stage 1
         f'<div style="position: absolute; left: 0px; top: 27px; bottom: 27px; width: 76px; box-sizing: border-box; border: 6px solid {INK}; border-right: none; border-radius: 30px 0 0 30px"></div>',
         f'<svg width="26" height="28" viewBox="0 0 26 28" aria-hidden="true" style="position: absolute; left: 72px; top: 16px"><path d="M0 0 L26 14 L0 28 Z" fill="{INK}"></path></svg>',
         f'<div style="position: absolute; left: -2px; top: 50%; transform: translate(-50%, -50%) rotate(-90deg); background: {PAPER}; padding: 0 16px; font-size: {FS}px; line-height: 1.2; font-weight: 700; white-space: nowrap">매 스텝(15분) 반복</div>',
         '<div style="display: flex; flex-direction: column">']
    for i, (name, agent, desc, foot) in enumerate(STAGES):
        if i:
            o.append(down_arrow())
        o.append(f'<div><p style="margin: 0; font-size: 46px; line-height: 1.2; font-weight: 700">{name} <span style="margin-left: 10px; font-size: {FS}px; font-weight: 500; color: {MUTED}">{agent}</span></p>'
                 f'<p class="tx" style="margin: 8px 0 0">{desc}</p>'
                 f'<p class="sm" style="margin: 8px 0 0; font-weight: 700">{foot}</p></div>')
    o.append('</div></div>')
    return "\n".join(o)

# ---------- 그림 2: 스텝별 운영 기록 ----------
BASE = [0.897, 1.000, 1.132, 1.503, 1.184, 2.208, 1.259, 1.106, 1.539, 1.614]
PROP = [0.741, 0.793, 0.946, 1.060, 1.014, 1.039, 1.028, 0.929, 0.936, 0.864]
BUY = {3: ("v1", "0.25"), 4: ("v1", "0.25"), 5: ("v1", "0.25"), 8: ("v3", "0.25"), 9: ("v5", "0")}
STEP_W, PROC_W, GAP = 120, 236, 24
BAR_AREA = (COL_C - 80) - STEP_W - PROC_W - 2 * GAP
K = 222              # px per 1.0 of load ratio
BAR_H = 68
ROW_PAD = 30

def bar(v, fill, row_bg):
    under, over = min(v, 1.0) * K, max(v - 1.0, 0) * K
    lab_c = SIG if v > 1.0 else (INK if fill == INK else MUTED)
    segs = f'<div style="width: {under:.1f}px; height: {BAR_H}px; flex: none; background: {fill}"></div>'
    if over > 0:
        segs += f'<div style="width: {over:.1f}px; height: {BAR_H}px; flex: none; background: {SIG}"></div>'
    return (f'<div style="position: relative; height: {BAR_H}px; display: flex; align-items: center">{segs}'
            f'<span class="num" style="margin-left: 8px; padding: 6px 8px; background: {row_bg}; font-size: 34px; line-height: 1; font-weight: 700; color: {lab_c}">{v:.3f}</span></div>')

def swatch(c):
    return f'<span style="display: inline-block; width: 44px; height: 30px; background: {c}; vertical-align: -5px; margin-right: 12px"></span>'

def log():
    grid = f"grid-template-columns: {STEP_W}px {BAR_AREA}px {PROC_W}px; column-gap: {GAP}px"
    x1 = STEP_W + GAP + K           # x of load ratio 1.0 inside a row
    o = [f'<div style="margin-top: 44px; border-top: 8px solid {INK}; padding-top: 36px">',
         f'<p style="margin: 0; font-size: 46px; line-height: 1.2; font-weight: 700">그림 2 · 응급 시나리오 스텝별 기록 (시드 3)</p>',
         f'<div class="sm" style="margin-top: 20px; display: flex; flex-wrap: wrap; column-gap: 36px; row-gap: 8px">'
         f'<span>{swatch(GREY)}기존 PoC</span><span>{swatch(INK)}제안 구조</span><span>{swatch(SIG)}부하율 1.0 초과 = SLA 위반</span></div>',
         f'<div class="sm mu" style="margin-top: 30px; display: grid; {grid}; font-weight: 700"><span>스텝</span><span>최대 슬라이스 부하율 (이용률 ÷ 임계값)</span><span>용량 조달</span></div>',
         '<div style="margin-top: 12px">']
    # load ratio 1.0: one strip per row, painted before the bars so bars and labels sit on top of it
    line = f'<div style="position: absolute; left: {K - 2}px; top: 0px; bottom: 0px; width: 4px; background: {SIG}"></div>'
    for i in range(10):
        bg = ZEBRA if i % 2 == 0 else "#FFFFFF"
        proc = ""
        if i in BUY:
            v, cap = BUY[i]
            proc = (f'<p style="margin: 0; font-size: 32px; line-height: 1.2; font-weight: 700">{v} 조달</p>'
                    f'<p class="sm mu" style="margin: 4px 0 0">반영 용량 {cap}</p>')
        o.append(f'<div style="display: grid; {grid}; align-items: stretch; background: {bg}">'
                 f'<p class="num" style="margin: 0; font-size: 104px; line-height: 1; font-weight: 700; display: flex; align-items: center; justify-content: center">{i}</p>'
                 f'<div style="position: relative; padding: {ROW_PAD}px 0; display: flex; flex-direction: column; gap: 14px">{line}{bar(BASE[i], GREY, bg)}{bar(PROP[i], INK, bg)}</div>'
                 f'<div style="display: flex; flex-direction: column; justify-content: center">{proc}</div></div>')
    o.append('</div>')
    o.append(f'<div style="display: grid; {grid}; align-items: baseline; padding-top: 20px; border-top: 4px solid {INK}; font-size: 32px; line-height: 1.3; font-weight: 700">'
             f'<span style="text-align: center">위반</span><span>기존 PoC 8회 → 제안 구조 4회</span><span>조달 5회</span></div>')
    o.append('<p class="cap" style="margin: 24px 0 0">그림 2. 응급 상황에서 기존 PoC 대비 스텝별 최대 슬라이스 부하율 (시드 3, 5회 중 평균에 가장 가까운 시드)</p>')
    o.append('</div>')
    return "\n".join(o)

FORMULAS = '''<div style="display: flex; flex-direction: column; gap: 22px">
<div style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); column-gap: 40px">
<div>
<p class="cap" style="margin: 0; font-weight: 700; color: #161616">식 1 — 상황 사후확률 (HMM 전진 필터)</p>
<div class="math" style="margin-top: 8px; font-size: 44px; line-height: 1.25"><i>b</i><sub style="font-size: 0.6em"><i>t</i></sub>(<i>s</i>) ∝ <i>p</i>(<i>x</i><sub style="font-size: 0.6em"><i>t</i></sub> | <i>s</i>) <span style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; line-height: 1"><span style="font-size: 1.3em">∑</span><span style="font-size: 0.5em"><i>s</i>′</span></span> <i>A</i><sub style="font-size: 0.6em"><i>s</i>′<i>s</i></sub> <i>b</i><sub style="font-size: 0.6em"><i>t</i>−1</sub>(<i>s</i>′)</div>
</div>
<div>
<p class="cap" style="margin: 0; font-weight: 700; color: #161616">식 2 — 수요 압력</p>
<div class="math" style="margin-top: 8px; font-size: 44px; line-height: 1.25"><i>P</i><sub style="font-size: 0.6em"><i>t</i></sub> = <span style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; line-height: 1"><span style="font-size: 1.3em">∑</span><span style="font-size: 0.5em"><i>i</i></span></span> <span style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; line-height: 1.15; font-size: 0.85em"><span style="padding: 0 8px 4px"><i>x</i><sub style="font-size: 0.6em"><i>i</i>,<i>t</i></sub></span><span style="border-top: 3px solid #161616; padding: 4px 8px 0"><i>θ</i><sub style="font-size: 0.6em"><i>i</i></sub> <i>C</i><sub style="font-size: 0.6em"><i>i</i>,<i>t</i></sub></span></span></div>
</div>
</div>
<p class="sm" style="margin: 0"><i>b</i> = 상황 <i>s</i>의 사후확률, <i>A</i> = 상황 전이확률, <i>x</i> = 슬라이스별 수요, <i>θ<sub>i</sub></i> = 슬라이스 <i>i</i>의 이용률 임계값(eMBB 0.9 · URLLC 1.2 · mMTC 0.8), <i>C<sub>i,t</sub></i> = 슬라이스 <i>i</i>의 용량(기본 1.6, 조달로 최대 2.6).</p>
<sc-if value="{{extra}}" hint-placeholder-val="{{ true }}">
<div style="display: flex; flex-wrap: wrap; align-items: center; column-gap: 48px; row-gap: 6px; font-size: 29.33px; line-height: 1.3">
<span class="mu" style="font-weight: 700; width: 100%">PoC 벤더 점수식과 조달 용량</span>
<span class="math" style="font-size: 34px"><i>S<sub style="font-size: 0.6em">v</sub></i> = 100[<i>w</i><sub style="font-size: 0.6em">Q</sub> (∑<sub style="font-size: 0.6em"><i>j</i></sub> <i>ω<sub style="font-size: 0.6em">j</sub> q<sub style="font-size: 0.6em">v,j</sub></i> / ∑<sub style="font-size: 0.6em"><i>j</i></sub> <i>ω<sub style="font-size: 0.6em">j</sub></i>) + <i>w</i><sub style="font-size: 0.6em">P</sub> <i>p<sub style="font-size: 0.6em">v</sub></i> + <i>w</i><sub style="font-size: 0.6em">R</sub> <i>r<sub style="font-size: 0.6em">v</sub></i>/5]</span>
<span class="math" style="font-size: 34px">Δ<i>C<sub style="font-size: 0.6em">k</sub></i> = 0.25 · <i>B</i><sub style="font-size: 0.6em"><i>v</i>*</sub> / <i>B</i><sub style="font-size: 0.6em">ref</sub></span>
<span class="sm mu">URLLC <i>B</i><sub>ref</sub> = 500 Mbps</span>
</div>
</sc-if>
</div>'''

if __name__ == "__main__":
    s = open(tpl_path, encoding="utf-8").read()
    for k, v in {"@@BODY_H@@": str(BODY_H), "@@COL_L@@": str(COL_L), "@@COL_C@@": str(COL_C), "@@COL_R@@": str(COL_R),
                 "@@DIAGRAM@@": diagram(), "@@STAGES@@": stages(), "@@LOG@@": log(), "@@FORMULAS@@": FORMULAS}.items():
        s = s.replace(k, v)
    open(out_path, "w", encoding="utf-8").write(s)
    print("written", len(s), "bar area", BAR_AREA, "body", BODY_H)
