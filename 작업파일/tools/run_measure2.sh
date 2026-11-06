S="$(cd "$(dirname "$0")/.." && pwd)"   # 작업파일 폴더 (도구·원본)
# Edge가 한글 경로를 못 열어서, 렌더링 중간 파일은 영문 경로에 둔다. 사용자 이름이 한글이면 A0_WORK 로 지정
R="${A0_WORK:-$(cygpath -m "${TEMP:-/tmp}")/a0-poster-work}"
mkdir -p "$R/render" "$R/ppt"
python -I "$S/tools/to_static.py" "$S/a0-poster/project/${2:-Main}.dc.html" "$R/render/poster.html" "${1:-1}" >/dev/null
python -I -c "
import sys; p=sys.argv[1]; s=open(p+'/render/poster.html',encoding='utf-8').read(); js=open(sys.argv[2]+'/tools/measure.js',encoding='utf-8').read()
open(p+'/render/measure.html','w',encoding='utf-8').write(s.replace('</body>','<script>'+js+'</script></body>'))" "$R" "$S"
E="${EDGE:-/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe}"   # 다른 위치면 EDGE 환경변수로 지정
"$E" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=15000 --window-size=3179,4494 --user-data-dir="$R/edge-profile" --dump-dom "file:///$R/render/measure.html" 2>/dev/null | grep -o 'MEASURE.*END'
"$E" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=15000 --window-size=3179,4494 --user-data-dir="$R/edge-profile" --screenshot="$R/render/poster.png" "file:///$R/render/poster.html" >/dev/null 2>&1
python -I -c "
from PIL import Image
import sys; p=sys.argv[1]+'/render/'
im=Image.open(p+'poster.png').convert('RGB'); im.resize((1060,1498)).save(p+'full.png')
for k,b in {'r1':(0,0,3179,1100),'r2':(0,1050,3179,2150),'r3':(0,2100,3179,3150),'r4':(0,3100,3179,4494)}.items():
  c=im.crop(b); c.resize((1600,int(c.height*1600/c.width))).save(p+k+'.png')" "$R" "$S"
