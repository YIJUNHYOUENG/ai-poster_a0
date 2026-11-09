# usage: run_ar.sh [section gap px] [aragon|kens] — 템플릿판 내용 HTML을 만들고 영역별 넘침을 잰다
S="$(cd "$(dirname "$0")/.." && pwd)"   # 작업파일 폴더 (도구·원본)
# Edge가 한글 경로를 못 열어서, 렌더링 중간 파일은 영문 경로에 둔다. 사용자 이름이 한글이면 A0_WORK 로 지정
R="${A0_WORK:-$(cygpath -m "${TEMP:-/tmp}")/a0-poster-work}"
mkdir -p "$R/render" "$R/ppt"
E="${EDGE:-/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe}"   # 다른 위치면 EDGE 환경변수로 지정
python -I "$S/tools/gen_ar.py" "$R/render/poster.html" "${1:-60}" "${2:-aragon}" >/dev/null
python -I -c "
import sys; p=sys.argv[1]; s=open(p+'/render/poster.html',encoding='utf-8').read(); js=open(sys.argv[2]+'/tools/measure_areas.js',encoding='utf-8').read()
open(p+'/render/areas.html','w',encoding='utf-8').write(s.replace('</body>','<script>'+js+'</script></body>'))" "$R" "$S"
"$E" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=20000 --window-size=3179,4494 --user-data-dir="$R/edge-profile" --dump-dom "file:///$R/render/areas.html" 2>/dev/null > "$R/render/areas_dom.html"
python -I -c "
import sys,re,json,html
sys.stdout.reconfigure(encoding='utf-8')
s=open(sys.argv[1],encoding='utf-8').read(); m=re.search(r'<pre id=\"area-out\">AREAS(.*?)ENDA</pre>',s,re.S); d=json.loads(html.unescape(m.group(1)))
for a in d['areas']: print(a)
print('fonts', d['fonts'])" "$R/render/areas_dom.html"
"$E" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=15000 --window-size=3179,4494 --user-data-dir="$R/edge-profile" --screenshot="$R/render/poster.png" "file:///$R/render/poster.html" >/dev/null 2>&1
python -I -c "
from PIL import Image; import sys
p=sys.argv[1]+'/render/'; im=Image.open(p+'poster.png').convert('RGB'); im.resize((1060,1498)).save(p+'full.png'); print('shot', p+'full.png')" "$R"
