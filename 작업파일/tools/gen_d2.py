"""D안 2판 — 문제 · 단계 · 증거 대조표가 포스터의 중심.

기존 PoC 구조의 한계(①의 비교표 행)와 그것을 푸는 폐루프 단계(③), 그 단계를 증명하는 수치(⑤)를
한 줄에 놓는다. 수요 압력으로 이어지는 자원배분 결정 → 자원할당 두 줄에는 형광펜을 칠한다.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_c as g
import gen_d as d1

out_path = sys.argv[1]
INK, GREY, MUTED, PAPER, RULE = "#161616", "#948E80", "#6B655A", "#ECE8E0", "#D5CFC3"
HL = "#FFEB8A"                 # highlighter
FS = 29.33
W = 2953
C1, C2, C3, GAP = 480, 1690, 655, 64
GRID = f"grid-template-columns: {C1}px {C2}px {C3}px; column-gap: {GAP}px"
BRACKET_GUTTER = 120

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

def before(cat, text):
    return (f'<div style="padding: 36px 0 36px 30px">'
            f'<p class="sm" style="margin: 0; font-weight: 700; color: {MUTED}">{cat}</p>'
            f'<p style="margin: 8px 0 0; font-size: 40px; line-height: 1.25; font-weight: 500; color: {MUTED}">{text}</p></div>')

def stage(name, agent, gist, desc, foot, side=""):
    body = (f'<p style="margin: 0; font-size: 58.67px; line-height: 1.15; font-weight: 700">{name} '
            f'<span style="margin-left: 8px; font-size: {FS}px; font-weight: 500; color: {MUTED}">{agent}</span></p>'
            f'<p style="margin: 8px 0 0; font-size: 40px; line-height: 1.25; font-weight: 700">{gist}</p>'
            f'<p class="tx" style="margin: 12px 0 0">{desc}</p>'
            f'<p class="sm" style="margin: 10px 0 0; font-weight: 700">{foot}</p>')
    if side:
        body = (f'<div style="display: grid; grid-template-columns: minmax(0, 1fr) 630px; column-gap: 36px; align-items: center">'
                f'<div style="min-width: 0">{body}</div><div>{side}</div></div>')
    return f'<div style="padding: 36px 30px 36px {BRACKET_GUTTER}px; min-width: 0">{body}</div>'

def evidence(num, label):
    return (f'<div style="padding: 36px 30px; display: flex; flex-direction: column; justify-content: center">'
            f'<p class="num" style="margin: 0; font-size: 150px; line-height: 1; font-weight: 700; letter-spacing: -0.04em; white-space: nowrap">{num}</p>'
            f'<p class="tx" style="margin: 12px 0 0; font-weight: 500">{label}</p></div>')

def formula(label, eq, size):
    return (f'<p class="cap" style="margin: 0; font-weight: 700; color: {INK}">{label}</p>'
            f'<div class="math" style="margin-top: 8px; font-size: {size}px; line-height: 1.25">{eq}</div>')

def row(cells, top_rule=True, bg=None):
    bt = f"border-top: 2px solid {RULE}; " if top_rule else ""
    b = f"background: {bg}; " if bg else ""
    return f'<div style="{bt}{b}display: grid; {GRID}">' + "".join(cells) + '</div>'

S1 = stage("상황인지", "Monitoring · Diagnosis", "HMM 전진 필터로 자동 추론",
           "Telemetry MCP로 슬라이스별 수요 <i>x</i>를 모으고 상황 <i>s</i>(평시·응급·대형 행사·IoT 급증)를 추론",
           "식 1, 같은 상황 유지 확률 0.98", formula("식 1 — 상황 사후확률 (HMM 전진 필터)", EQ1, 44))
S2 = stage("자원배분 결정", "Planning", "수요·잡음·임계값으로 산출",
           "이용률 임계값 <i>θ</i>와 용량 <i>C</i>로 목표 배분을 산출해 Orchestrator MCP로 적용하고 수요 압력 <i>P</i>를 계산",
           "식 2, <i>P</i>가 1을 넘으면 배분만으로는 SLA 불가", formula("식 2 — 수요 압력", EQ2, 60))
S3 = stage("자원할당", "Execution", "수요 압력 기준 자동 조달",
           "<i>P</i>가 임계값 이상이면 압력을 가장 크게 낮추는 슬라이스의 용량을 마켓플레이스에서 조달",
           "응급 0.8 · 그 밖 1.0, 벤더는 PoC 점수식으로 선택",
           '<sc-if value="{{extra}}" hint-placeholder-val="{{ true }}">'
           f'<p class="cap" style="margin: 0; font-weight: 700; color: {INK}">PoC 벤더 점수식과 조달 용량</p>'
           f'<div class="math" style="margin-top: 8px; font-size: 30px; line-height: 1.35">{SV}</div>'
           f'<div style="margin-top: 6px; display: flex; align-items: baseline; gap: 30px"><span class="math" style="font-size: 34px">{DC}</span>'
           f'<span class="sm" style="color: {MUTED}">URLLC <i>B</i><sub>ref</sub> = 500 Mbps</span></div>'
           '</sc-if>')
S4 = stage("판단검증", "Verification", "신뢰도 0.9 미만일 때만 질의",
           "상황 신뢰도가 0.9 미만일 때만 망관리자에게 질의하고 결과를 Diagnosis로 되돌리며, SLA 충족 여부를 벤더 평판에 반영",
           "신뢰도 = 사후확률 최댓값")

def ev_or_blank(num, label):
    return ('<sc-if value="{{extra}}" hint-placeholder-val="{{ true }}">' + evidence(num, label) + '</sc-if>'
            '<sc-if value="{{noExtra}}" hint-placeholder-val="{{ false }}"><div></div></sc-if>')

def hero():
    o = [f'<section data-area="중심 대조표" data-mm="0" style="flex: none; background: #FFFFFF">',
         # column heads
         f'<div style="display: grid; {GRID}; font-size: 32px; line-height: 1.2; font-weight: 700; color: #FFFFFF">'
         f'<div style="background: {GREY}; padding: 18px 30px">기존 PoC 구조</div>'
         f'<div style="background: {INK}; padding: 18px 30px 18px {BRACKET_GUTTER}px">제안 구조 — 에이전트 4단계 폐루프</div>'
         f'<div style="background: {INK}; padding: 18px 30px">결과</div></div>',
         '<div style="position: relative">']
    o.append(row([before("상황인지", "망관리자가 직접 지정"), S1, ev_or_blank("47 / 47", "자율 판단한 스텝의 상황인지 정확")], top_rule=False))
    # rows 2-3 share one highlighter band and one evidence cell
    o.append(f'<div style="background: {HL}; display: grid; {GRID}">'
             f'<div style="grid-column: 1; grid-row: 1">{before("자원배분", "상황별 고정 배분표")}</div>'
             f'<div style="grid-column: 2; grid-row: 1; min-width: 0">{S2}</div>'
             f'<div style="grid-column: 3; grid-row: 1 / 3; display: flex">{ev_or_blank("22 / 22", "용량이 모자란 스텝을 모두 자동 조달")}</div>'
             f'<div style="grid-column: 1; grid-row: 2; border-top: 2px solid #E4CF6A">{before("용량 확보", "마켓플레이스 분리, 사람이 조달")}</div>'
             f'<div style="grid-column: 2; grid-row: 2; min-width: 0; border-top: 2px solid #E4CF6A">{S3}</div></div>')
    o.append(row([before("사람 개입", "상시 감시"), S4, ev_or_blank("3 / 50", "망관리자 질의가 필요했던 스텝")], top_rule=False))
    # loop: stage 4 back to stage 1
    bx = C1 + GAP + 34
    o.append(f'<div style="position: absolute; left: {bx}px; top: 70px; bottom: 120px; width: 62px; box-sizing: border-box; border: 6px solid {INK}; border-right: none; border-radius: 30px 0 0 30px"></div>')
    o.append(f'<svg width="26" height="28" viewBox="0 0 26 28" aria-hidden="true" style="position: absolute; left: {bx + 58}px; top: 59px"><path d="M0 0 L26 14 L0 28 Z" fill="{INK}"></path></svg>')
    o.append(f'<div style="position: absolute; left: {bx - 2}px; top: calc(50% - 25px); transform: translate(-50%, -50%) rotate(-90deg); background: {HL}; padding: 0 16px; '
             f'font-size: {FS}px; line-height: 1.2; font-weight: 700; white-space: nowrap">매 스텝(15분) 반복</div>')
    o.append('</div>')
    o.append(row([before("결정 기록", "상태 이력만 저장"),
                  f'<div style="padding: 36px 30px 36px {BRACKET_GUTTER}px"><p style="margin: 0; font-size: 40px; line-height: 1.25; font-weight: 700">결정 근거와 호출 순서까지 기록</p>'
                  f'<p class="tx" style="margin: 12px 0 0">하위 에이전트끼리는 직접 호출하지 않고 Supervisor Agent를 거치므로 판단 근거가 모두 기록에 남는다.</p></div>',
                  '<div></div>'], top_rule=True))
    # outcome band
    o.append(f'<div style="background: {INK}; color: #FFFFFF; display: grid; grid-template-columns: minmax(0, 1fr) {C3}px; column-gap: {GAP}px; align-items: center">'
             f'<div style="padding: 30px 30px"><p style="margin: 0; font-size: 58.67px; line-height: 1.2; font-weight: 700">SLA 위반 감소 (평균 7.8 → 3.8회)</p>'
             f'<p class="tx" style="margin: 10px 0 0; color: #D9D4CA">모든 시드에서 위반이 줄었고, 평균 7.8회에서 3.8회로 51% 감소했다.</p></div>'
             f'<p class="num" style="margin: 0; padding: 10px 30px; font-size: 230px; line-height: 1; font-weight: 700; letter-spacing: -0.05em; color: {HL}">51%</p></div>')
    o.append('</section>')
    return "\n".join(o)

def chart(CW=1100, H=790):
    # gen_c.chart drawn taller: same marks and labels, plot box stretched to H
    TOP, BOT, LO, HI = 20, H - 90, 0.5, 2.3
    X0, X1 = 110, CW - 28
    base, prop = d1.BASE, d1.PROP
    buys = {3: "v1", 4: "v1", 5: "v1", 8: "v3", 9: "v5"}
    x = lambda i: round(X0 + i * (X1 - X0) / 9, 1)
    y = lambda v: round(BOT - (v - LO) * (BOT - TOP) / (HI - LO), 1)
    o = [f'<svg width="{CW}" height="{H}" viewBox="0 0 {CW} {H}" role="img" aria-label="그림 2: 시드 3의 스텝별 최대 슬라이스 부하율. 기존 PoC는 위반 8회, 제안 구조는 위반 4회" '
         f'style="display: block; font-family: Pretendard, \'Noto Sans KR\', sans-serif">']
    for v in (2.0, 1.5):
        o.append(f'<line x1="{X0}" y1="{y(v)}" x2="{X1}" y2="{y(v)}" stroke="#DDD7CB" stroke-width="2"></line>')
    o.append(f'<line x1="{X0}" y1="{BOT}" x2="{X1}" y2="{BOT}" stroke="{GREY}" stroke-width="2"></line>')
    for v in (2.0, 1.5, 1.0, 0.5):
        o.append(f'<text x="{X0 - 20}" y="{round(y(v) + 11, 1)}" font-size="32" fill="{MUTED}" text-anchor="end">{v:.1f}</text>')
    for i in range(10):
        o.append(f'<text x="{x(i)}" y="{BOT + 42}" font-size="32" fill="{MUTED}" text-anchor="middle">{i}</text>')
    o.append(f'<text x="{(X0 + X1) // 2}" y="{BOT + 84}" font-size="32" fill="{MUTED}" text-anchor="middle">스텝 (15분 간격)</text>')
    o.append(f'<line x1="{X0}" y1="{y(1.0)}" x2="{X1}" y2="{y(1.0)}" stroke="{{{{accent}}}}" stroke-width="4"></line>')
    o.append('<polyline points="' + " ".join(f"{x(i)},{y(v)}" for i, v in enumerate(base)) + f'" fill="none" stroke="{GREY}" stroke-width="4" stroke-dasharray="14 10" stroke-linejoin="round"></polyline>')
    for i, v in enumerate(base):
        o.append(f'<rect x="{round(x(i) - 10, 1)}" y="{round(y(v) - 10, 1)}" width="20" height="20" fill="#FFFFFF" stroke="{GREY}" stroke-width="4"></rect>')
    o.append('<polyline points="' + " ".join(f"{x(i)},{y(v)}" for i, v in enumerate(prop)) + f'" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"></polyline>')
    for i, v in enumerate(prop):
        o.append(f'<circle cx="{x(i)}" cy="{y(v)}" r="11" fill="{INK}" stroke="#FFFFFF" stroke-width="3"></circle>')
    for i, name in buys.items():
        cx, cy = x(i), round(y(prop[i]) + 36, 1)
        dd = f"M{cx} {round(cy - 13, 1)} L{round(cx + 13, 1)} {round(cy + 9, 1)} L{round(cx - 13, 1)} {round(cy + 9, 1)} Z"
        o.append(f'<path d="{dd}" fill="#FFFFFF" stroke="{INK}" stroke-width="3"></path>' if i == 9 else f'<path d="{dd}" fill="{INK}"></path>')
        anchor, tx = ("end", cx - 22) if i >= 8 else ("start", cx + 18)
        o.append(f'<text x="{round(tx, 1)}" y="{round(cy + 11, 1)}" font-size="32" font-weight="700" fill="{INK}" text-anchor="{anchor}">{name}</text>')
    o.append('</svg>')
    return "\n".join(o)

def sw(c, label):
    return f'<span><span style="display: inline-block; width: 40px; height: 26px; background: {c}; vertical-align: -3px; margin-right: 10px"></span>{label}</span>'

HEAD = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "d_template.html"), encoding="utf-8").read()
head = HEAD[:HEAD.index('<div style="height: @@BODY_H@@px')]
tail = HEAD[HEAD.index('<p data-area="사사"'):]
head = head.replace(".dl h2{margin:0 0 22px;", ".dl h2{margin:0 0 20px;")

BODY_TOP = 610 + 64
BODY_H = 4494 - BODY_TOP - 44 - 33 - 80
body = f'''<div style="height: {BODY_H}px; flex: none; margin: 64px 113px 0; display: flex; flex-direction: column; gap: 60px">

<section data-area="연구 배경" data-mm="0" style="flex: none; display: grid; grid-template-columns: 560px minmax(0, 1fr); column-gap: 64px; align-items: start">
<h2 style="margin: 0">연구 배경과 문제</h2>
<ul class="pb" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: 70px">
<li style="margin: 0">AI 기반 망관리가 확산되지만, 에이전트에 자원관리를 전적으로 맡기기엔 신뢰와 위험부담 문제가 남아 있다.</li>
<li style="margin: 0">ITU-T FG-AINN(2024년 7월 SG13 설립)은 PoC로 5G 네트워크 슬라이싱의 AI 기반 관리를 시연했다.</li>
<li style="margin: 0">PoC 구조의 두 한계: 망관리자가 상황을 직접 지정해야 하고, 마켓플레이스가 오케스트레이터와 분리돼 용량 확보를 사람이 한다.</li>
</ul>
</section>

{hero()}

<p class="sm" style="margin: -34px 0 0; flex: none; color: {MUTED}"><i>b</i> = 상황 <i>s</i>의 사후확률, <i>A</i> = 상황 전이확률, <i>x</i> = 슬라이스별 수요, <i>θ<sub>i</sub></i> = 슬라이스 <i>i</i>의 이용률 임계값(eMBB 0.9 · URLLC 1.2 · mMTC 0.8), <i>C<sub>i,t</sub></i> = 슬라이스 <i>i</i>의 용량(기본 1.6, 조달로 최대 2.6).</p>

<div style="flex: 1; min-height: 0; display: grid; grid-template-columns: 1000px 1100px minmax(0, 1fr); column-gap: 70px">

<div data-area="제안 구조 · 참고문헌" data-mm="0" style="min-width: 0; display: flex; flex-direction: column; justify-content: space-between; gap: 50px">
<section>
<h2>제안 구조 (그림 1)</h2>
{d1.diagram()}
<p class="tx" style="margin: 24px 0 0; font-weight: 700">배분 결정은 Agent Layer가 내리고, Orchestrator MCP는 결정된 배분을 적용한다.</p>
<div style="margin-top: 16px; display: flex; flex-direction: column; gap: 10px">
<p class="sm" style="margin: 0"><b>Intent / Service Layer</b> — 망관리자 의도와 SLA를 정책으로 변환해 에이전트 계층에 목표로 전달</p>
<p class="sm" style="margin: 0"><b>Agent Layer</b> — 마스터 에이전트(Supervisor Agent)가 하위 전문 에이전트를 조율하고, 공유 지식베이스(과거 장애·조치 이력, RAG)를 참조</p>
<p class="sm" style="margin: 0"><b>MCP Layer</b> — 텔레메트리·토폴로지·설정·오케스트레이터 기능을 독립 MCP 서버로 분리</p>
<p class="sm" style="margin: 0"><b>Network Infra Layer</b> — 테스트베드의 RAN·코어·전송 네트워크</p>
</div>
</section>
<section>
<h2 style="font-size: 42.67px">참고문헌</h2>
<div style="display: grid; grid-template-columns: 40px minmax(0, 1fr); row-gap: 8px; font-size: 24px; line-height: 1.3">
<span>[1]</span><span>ITU-T Rec. Y.3061 (12/2023), Autonomous networks – Architecture framework.</span>
<span>[2]</span><span>ITU-T FG-AINN, Technical Report: Proof-of-Concept activities, 2026.</span>
<span>[3]</span><span>ITU-T FG-AINN, LS on FG-AINN 2026 work plan (FG-AINN-O-016), Dec. 2025.</span>
<span>[4]</span><span>Anthropic, Model Context Protocol Specification, modelcontextprotocol.io, 2024.</span>
</div>
</section>
</div>

<section data-area="실험 설정 · 그림 2" data-mm="0" style="min-width: 0">
<h2>실험 설정</h2>
<table class="pt">
<tbody>
<tr><td style="width: 150px; font-weight: 700">시나리오</td><td>응급 상황이 처음부터 이어지는 10스텝 (1스텝 = 15분)</td></tr>
<tr><td style="font-weight: 700">반복</td><td>시드 0~4로 5회, 같은 시드에는 두 방식에 같은 트래픽</td></tr>
<tr><td style="font-weight: 700">비교군</td><td class="mu">기존 PoC 재현 — 망관리자가 정답 상황을 즉시 지정, 고정 배분표, 조달 없음</td></tr>
<tr><td style="font-weight: 700">제안</td><td style="font-weight: 700">에이전트 기반 오케스트레이터<sc-if value="{{{{extra}}}}" hint-placeholder-val="{{{{ true }}}}"> — LLM(Claude), 5개 MCP 서버 · 21개 도구</sc-if></td></tr>
<tr><td style="font-weight: 700">공통 설정</td><td>PoC의 슬라이스 구성(eMBB·URLLC·mMTC), SLA 임계값, 트래픽 생성식, 배분 평활</td></tr>
<tr><td style="font-weight: 700">용량</td><td>슬라이스당 기본 1.6, 조달 시 최대 2.6</td></tr>
</tbody>
</table>
<div class="sm" style="margin-top: 40px; display: flex; flex-wrap: wrap; column-gap: 30px; row-gap: 6px">{sw(GREY, "기존 PoC (위반 8회)")}{sw(INK, "제안 구조 (위반 4회)")}{sw("var(--sig)", "SLA 위반 경계 (부하율 1.0)")}<span>▲ 용량 조달 (v: 벤더)</span></div>
<p class="sm" style="margin: 14px 0 6px; color: {MUTED}">최대 슬라이스 부하율 (이용률 ÷ 임계값)</p>
{chart()}
<p class="cap" style="margin: 10px 0 0">그림 2. 응급 상황에서 기존 PoC 대비 스텝별 최대 슬라이스 부하율 (시드 3, 5회 중 평균에 가장 가까운 시드)</p>
</section>

<div data-area="결과 · 결론 · 참고문헌" data-mm="0" style="min-width: 0; display: flex; flex-direction: column; justify-content: space-between; gap: 50px">
<sc-if value="{{{{extra}}}}" hint-placeholder-val="{{{{ true }}}}">
<section>
<h2>시드별 결과</h2>
<table class="pt pn" style="background: #FFFFFF">
<thead>
<tr><th>시드</th><th class="mu">기존 PoC<br>위반(회)</th><th>제안<br>위반(회)</th><th>조달<br>(회)</th><th>조달 비용<br>(USD)</th><th>망관리자<br>질의(회)</th></tr>
</thead>
<tbody>
<tr><td>0</td><td class="mu">9</td><td style="font-weight: 700">3</td><td>5</td><td>4,550</td><td>0</td></tr>
<tr><td>1</td><td class="mu">7</td><td style="font-weight: 700">3</td><td>2</td><td>2,500</td><td>0</td></tr>
<tr><td>2</td><td class="mu">9</td><td style="font-weight: 700">5</td><td>6</td><td>5,225</td><td>0</td></tr>
<tr><td>3</td><td class="mu">8</td><td style="font-weight: 700">4</td><td>5</td><td>4,975</td><td>2</td></tr>
<tr><td>4</td><td class="mu">6</td><td style="font-weight: 700">4</td><td>4</td><td>3,750</td><td>1</td></tr>
<tr><td style="font-weight: 700; border-top: 4px solid {INK}">평균</td><td class="mu" style="font-weight: 700; border-top: 4px solid {INK}">7.8</td><td style="font-weight: 700; border-top: 4px solid {INK}">3.8</td><td style="font-weight: 700; border-top: 4px solid {INK}">4.4</td><td style="font-weight: 700; border-top: 4px solid {INK}">4,200</td><td style="font-weight: 700; border-top: 4px solid {INK}">0.6</td></tr>
</tbody>
</table>
<ul class="pb" style="margin-top: 24px">
<li>기존 PoC는 수요 압력 0.8 이상인 34스텝에서 용량을 늘릴 수단이 없었고, 제안 구조는 22스텝 모두에서 벤더를 조달했다.</li>
<li>망관리자 질의는 50스텝 중 3스텝뿐이었다.</li>
</ul>
</section>
</sc-if>
<section>
<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 30px">
<h2>결론과 기여</h2>
<div style="width: 95px; height: 95px; flex: none; background: #FFFFFF; display: flex; align-items: center; justify-content: center; text-align: center; font-size: 24px; line-height: 1.15; color: #555555">QR<br>미정</div>
</div>
<ul class="pb">
<li><b>폐루프 자동화</b> — FG-AINN PoC에 에이전트 계층을 더해 상황인지부터 용량 조달까지 사람 없이 돌게 했다.</li>
<li><b>수요 압력 지표</b> — “배분 조정으로 충분한가, 용량 확보가 필요한가”를 식 2 하나로 판정한다.</li>
<li><b>선택적 개입</b> — 상시 감시 대신, 상황 신뢰도가 낮을 때만 망관리자에게 묻는다.</li>
<li><b>한계와 향후</b> — 검증이 응급 시나리오에 한정되어, 혼합 상황 실험과 FG-AINN 표준 기고 연계로 넓힌다.</li>
</ul>
</section>

</div>

</div>
</div>

'''
s = head + body + tail
s = s.replace("<title>A0 포스터 D안 — 운영 로그형</title>", "<title>A0 포스터 D안 — 문제·단계·증거 대조표</title>")
open(out_path, "w", encoding="utf-8").write(s)
print("written", len(s), "body", BODY_H)
