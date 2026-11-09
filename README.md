# A0 포스터 — 에이젠틱 AI를 이용한 자율망에서 동적 자원할당 자동화를 위한 구조 및 설계

KICS 추계 2026 포스터 세션용 A0 세로 포스터(841 × 1189 mm). 채택안은 **B안(폐루프 중심) + C안 디자인**이다.

- Design 캔버스(웹, 비공개): https://claude.ai/artifact/FRuVTXMx42dGjnZ2pBf5Zf — A·B·C·D안 보드
- 포스터 설계 문서(Claude Docs): 처음 받은 링크 https://claude.ai/artifact/HvZsPVH4h9effSBwby2EYw
- 둘 다 같은 claude.ai 계정으로 로그인하면 집에서도 열린다.

## 폴더 구성

```
A0포스터/
├─ README.md                    이 문서 (집에서 이어서 하는 방법)
├─ CLAUDE.md                    Claude Code가 읽는 작업 규칙
├─ 작업에_사용한_기술.md         사용한 AI·도구 정리
├─ A0포스터_A안_설계문서사양.pdf / .pptx
├─ A0포스터_B안_폐루프중심.pdf / .pptx      B안 원본 (청록 버전)
├─ A0포스터_C안_결론문장.pdf / .pptx
├─ A0포스터_D안_대조표.pdf / .pptx
├─ B안추가수정/                 채택 후 B안 수정본 (지금: C안 디자인, 사사 삭제)
├─ Aragon템플릿/                교수님 요청 구조: PosterPresentations A0 Aragon 템플릿 두 단에 B안 내용
│                               (PPTX는 템플릿 파일 그대로 + 내용 도형, PDF는 PowerPoint로 저장)
├─ Kensington템플릿/            같은 내용을 Kensington 템플릿(파란 띠 + 둥근 흰 패널, 김정훈 선배 포스터와 같은 틀)에
├─ Gemini디자인/                같은 구조(제목 띠 + 두 단)에 GitHub anishathalye/gemini 포스터 테마의 색·블록 규칙 적용
├─ 가독성디자인/                제목 띠 아래 '한눈에 보기'(문제 → 제안 → 결과 51%) 띠 + 번호 붙은 섹션 1–7, 남색 한 가지
├─ Pretendard 글꼴 (A안 PPT용)/  A·D안 PPTX를 열 PC에 설치할 글꼴
└─ 작업파일/
   ├─ a0-poster/project/        캔버스 원본 — Main(A) · Alt(B) · PosterC(C) · PosterD(D) .dc.html, canvas.json
   ├─ a0-poster/Alt_teal_backup.dc.html   B안 청록 원본
   ├─ fonts-dl/                 Pretendard woff2·otf (렌더링·PDF에 씀)
   └─ tools/                    생성·측정·내보내기 스크립트
```

## 집 PC 준비 (Windows 기준, 한 번만)

1. 저장소 받기
   ```bash
   git clone https://github.com/YIJUNHYOUENG/ai-poster_a0.git A0포스터
   ```
2. 프로그램
   - Git for Windows (Git Bash) — 스크립트가 bash로 되어 있다
   - Python 3.10 이상
   - Microsoft Edge — 렌더링·측정·PDF에 쓴다. 기본 위치(`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`)가 아니면 `EDGE` 환경변수로 지정
   - PowerPoint — PPTX를 열어 확인할 때만 필요
3. Python 패키지
   ```bash
   pip install python-pptx pillow pymupdf lxml
   ```
   회사 PC에서 쓴 버전: python-pptx 1.0.2, Pillow 12.3.0, PyMuPDF 1.28.2, lxml 6.1.3
4. 글꼴: A·D안 PPTX를 PowerPoint에서 볼 거면 `Pretendard 글꼴 (A안 PPT용)` 안 OTF 세 개를 설치한다. B·C안은 Noto Sans KR을 쓴다(없으면 설치).
5. Windows 사용자 이름에 한글이 있으면 Edge가 임시 폴더를 못 연다. 그때는 영문 경로를 지정한다.
   ```bash
   export A0_WORK=C:/a0-poster-work
   ```

## 자주 하는 작업

모든 명령은 `작업파일/tools` 폴더에서 Git Bash로 실행한다.

B안(채택안) 다시 만들기 — `b3_template.html`(구조) + `gen_b4.py`(C안 디자인, 사사 삭제 포함)
```bash
python -I gen_b4.py b3_template.html ../a0-poster/project/Alt.dc.html 1050
```

넘침 확인 — 첫 인자 1은 보강 내용 표시, 0은 숨김. `"clipped":[]`이면 잘린 곳 없음
```bash
bash run_measure2.sh 1 Alt
```

PPTX·PDF 만들기 — 결과는 `작업파일/출력/`에 생긴다
```bash
bash make_all.sh Alt C A0포스터_B안_폐루프중심
```
다 되면 `출력/`의 두 파일을 `B안추가수정/`으로 옮긴다.

Aragon 템플릿판 — `gen_ar.py`(내용 HTML) → `build_aragon.py`(+`aragon_setup.py`)가 `작업파일/template/Aragon.pptx`를 열어 채움 → PowerPoint로 PDF. PowerPoint가 설치된 Windows에서만 된다.
```bash
bash run_ar.sh                       # 왼쪽 단·오른쪽 단·섹션별 넘침
bash make_aragon.sh A0포스터_Aragon   # 결과는 작업파일/출력/ → Aragon템플릿/으로 옮긴다
```
Kensington판은 같은 스크립트에 `kens`를 붙인다 (`작업파일/template/Kensington.pptx` 사용).
```bash
bash run_ar.sh 60 kens
bash make_aragon.sh A0포스터_Kensington kens   # → Kensington템플릿/
bash run_ar.sh 60 gemini
bash make_aragon.sh A0포스터_Gemini gemini     # → Gemini디자인/ (템플릿 없이 build_pptx.py로 그림)
```
Gemini판 규칙(anishathalye/gemini 기본 색 테마): 제목 띠 #40739E, 띠 아래 선 #273C75, 블록 제목은 가운데 정렬 파랑 + 얇은 검정 구분선, 핵심 수치는 강조 블록(#E8F4FF), 수식은 예시 블록(#F5F6FA).
가독성판(`clear`): 위에서 한 번에 문제·제안·결과가 읽히도록 '한눈에 보기' 띠를 두고, 섹션에 번호 배지(왼쪽 단 1–3, 오른쪽 단 4–7)를 붙였다.
핵심 수치(51%, 22/22, 3/50, 47/47)는 띠로 옮겨 실험 결과 섹션에서는 뺐고, 그림이 많은 왼쪽 단을 넓게 했다(1560px, `gen_ar.py` 다섯째 인자).
```bash
bash run_ar.sh 60 clear
bash make_aragon.sh A0포스터_가독성 clear       # → 가독성디자인/
```
본문은 맑은 고딕(모든 Windows에 있음)이라 PPTX를 어느 PC에서 열어도 줄바꿈이 같다.

다른 안: A안 `gen_a3.py a3_template.html` → `Main`, 테마 `A3` / C안 `gen_c.py c_template.html` → `PosterC`, 테마 `C` / D안 `gen_d2.py` → `PosterD`, 테마 `D`
(A·D안은 `run_areas.sh`로 영역별 남은 mm를 잰다)

## 캔버스에 올리기

캔버스 원본은 `작업파일/a0-poster/project/`이다. Claude Code에서 이 폴더를 열고 Claude에게 "캔버스 B안 갱신해 줘"라고 하면 된다.
캔버스는 웹에서도 고칠 수 있으니, 고치기 전에 Claude에게 캔버스를 먼저 읽어 로컬과 같은지 확인하게 한다.

## 지금 상태 (2026-11-06)

- B안 채택, C안 디자인 적용, 사사 삭제(지도교수 의견: 사사는 안 넣어도 됨, 지면이 남으면 참고문헌, 아니면 내용으로 채움) — 캔버스·`B안추가수정` 모두 반영
- 2026-11-09 교수님 요청으로 PosterPresentations A0 템플릿 구조(제목 띠 + 두 단) 적용, Aragon 템플릿 선택 → `Aragon템플릿/`, 같은 날 Kensington판 → `Kensington템플릿/`, GitHub Gemini 테마판 → `Gemini디자인/`, 가독성판 → `가독성디자인/`
- 로고 2개와 QR은 아직 자리만 있음 (Aragon판에는 로고 자리 없음)
