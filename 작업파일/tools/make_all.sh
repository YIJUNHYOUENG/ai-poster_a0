# usage: make_all.sh <artboard stem> <theme> <out stem>
S="$(cd "$(dirname "$0")/.." && pwd)"   # 작업파일 폴더 (도구·원본)
# Edge가 한글 경로를 못 열어서, 렌더링 중간 파일은 영문 경로에 둔다. 사용자 이름이 한글이면 A0_WORK 로 지정
R="${A0_WORK:-$(cygpath -m "${TEMP:-/tmp}")/a0-poster-work}"
mkdir -p "$R/render" "$R/ppt"
E="${EDGE:-/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe}"   # 다른 위치면 EDGE 환경변수로 지정
python -I "$S/tools/to_static.py" "$S/a0-poster/project/$1.dc.html" "$R/render/poster.html" 1 >/dev/null
"$E" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --virtual-time-budget=15000 --window-size=3179,4494 --user-data-dir="$R/edge-profile" --screenshot="$R/ppt/poster@2x.png" "file:///$R/render/poster.html" >/dev/null 2>&1
bash "$S/tools/make_ppt.sh" 0 "$2" "$3" | tail -1
python -I -c "
import sys; p=sys.argv[1]; s=open(p+'/render/poster.html',encoding='utf-8').read()
s=s.replace('<style>','<style>@page{size:841mm 1189mm;margin:0}html,body{-webkit-print-color-adjust:exact;print-color-adjust:exact}',1)
open(p+'/render/print.html','w',encoding='utf-8').write(s)" "$R" "$S"
"$E" --headless=new --disable-gpu --virtual-time-budget=20000 --no-pdf-header-footer --user-data-dir="$R/edge-profile" --print-to-pdf="$R/ppt/$3.pdf" "file:///$R/render/print.html" >/dev/null 2>&1
python -I -c "
import fitz,sys
d=fitz.open(sys.argv[1]); pg=d[0]; print('pdf pages',len(d), [round(v,1) for v in pg.rect], 'fonts', sorted(set(f[3] for f in pg.get_fonts() if f[3]))[:6])
pg.get_pixmap(dpi=30).save(sys.argv[2])" "$R/ppt/$3.pdf" "$R/ppt/$3_pdf.png" 2>/dev/null
cp "$R/ppt/poster@2x.png" "$R/ppt/$3@2x.png"
mkdir -p "$S/출력" && cp "$R/ppt/$3.pptx" "$R/ppt/$3.pdf" "$S/출력/" && echo "출력: $S/출력/$3.pptx, .pdf"
