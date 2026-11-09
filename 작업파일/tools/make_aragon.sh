# usage: make_aragon.sh <out stem>
# Aragon 템플릿판: 내용 HTML → 2배 스크린샷·도형 추출 → 템플릿 PPTX에 채우기 → PowerPoint로 PDF·PNG
S="$(cd "$(dirname "$0")/.." && pwd)"   # 작업파일 폴더 (도구·원본)
# Edge가 한글 경로를 못 열어서, 렌더링 중간 파일은 영문 경로에 둔다. 사용자 이름이 한글이면 A0_WORK 로 지정
R="${A0_WORK:-$(cygpath -m "${TEMP:-/tmp}")/a0-poster-work}"
mkdir -p "$R/render" "$R/ppt"
E="${EDGE:-/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe}"   # 다른 위치면 EDGE 환경변수로 지정
OUT="${1:-aragon}"
python -I "$S/tools/gen_ar.py" "$R/render/poster.html" >/dev/null
"$E" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --virtual-time-budget=15000 --window-size=3179,4494 --user-data-dir="$R/edge-profile" --screenshot="$R/ppt/poster@2x.png" "file:///$R/render/poster.html" >/dev/null 2>&1
python -I -c "
import sys; p=sys.argv[1]; s=open(p+'/render/poster.html',encoding='utf-8').read(); js=open(sys.argv[2]+'/tools/extract.js',encoding='utf-8').read()
open(p+'/render/extract.html','w',encoding='utf-8').write(s.replace('</body>','<script>'+js+'</script></body>'))" "$R" "$S"
"$E" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=20000 --window-size=3179,4494 --user-data-dir="$R/edge-profile" --dump-dom "file:///$R/render/extract.html" 2>/dev/null > "$R/ppt/dom.html"
python -I -c "
import sys,re,json,html
s=open(sys.argv[1]+'/ppt/dom.html',encoding='utf-8').read(); m=re.search(r'<pre id=\"extract-out\">EXTRACT(.*?)ENDX</pre>',s,re.S); d=json.loads(html.unescape(m.group(1)))
json.dump(d,open(sys.argv[1]+'/ppt/layout.json','w',encoding='utf-8'),ensure_ascii=False)
print({k:(len(v) if isinstance(v,list) else v) for k,v in d.items()})" "$R"
rm -f "$R"/ppt/img_*.png
cp "$S/template/Aragon.pptx" "$R/ppt/template.pptx"
python -I "$S/tools/build_aragon.py" "$R/ppt" "$R/ppt/aragon.pptx" 0 AR "$R/ppt/template.pptx" || exit 1
WIN_R="$(cygpath -w "$R/ppt")"
powershell.exe -NoProfile -Command "\$pp = New-Object -ComObject PowerPoint.Application; \$pr = \$pp.Presentations.Open('$WIN_R\\aragon.pptx', -1, 0, 0); \$pr.SaveAs('$WIN_R\\aragon.pdf', 32); \$pr.Slides(1).Export('$WIN_R\\aragon_render.png', 'PNG', 3179, 4494); \$pr.Close(); \$pp.Quit()"
mkdir -p "$S/출력" && cp "$R/ppt/aragon.pptx" "$S/출력/$OUT.pptx" && cp "$R/ppt/aragon.pdf" "$S/출력/$OUT.pdf" && echo "출력: $S/출력/$OUT.pptx, .pdf (미리보기 $R/ppt/aragon_render.png)"
