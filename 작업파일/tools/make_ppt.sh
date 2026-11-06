S="$(cd "$(dirname "$0")/.." && pwd)"   # 작업파일 폴더 (도구·원본)
# Edge가 한글 경로를 못 열어서, 렌더링 중간 파일은 영문 경로에 둔다. 사용자 이름이 한글이면 A0_WORK 로 지정
R="${A0_WORK:-$(cygpath -m "${TEMP:-/tmp}")/a0-poster-work}"
mkdir -p "$R/render" "$R/ppt"
E="${EDGE:-/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe}"   # 다른 위치면 EDGE 환경변수로 지정
python -I -c "
import sys; p=sys.argv[1]; s=open(p+'/render/poster.html',encoding='utf-8').read(); js=open(sys.argv[2]+'/tools/extract.js',encoding='utf-8').read()
open(p+'/render/extract.html','w',encoding='utf-8').write(s.replace('</body>','<script>'+js+'</script></body>'))" "$R" "$S"
"$E" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=20000 --window-size=3179,4494 --user-data-dir="$R/edge-profile" --dump-dom "file:///$R/render/extract.html" 2>/dev/null > "$R/ppt/dom.html"
python -I -c "
import sys,re,json,html
s=open(sys.argv[1]+'/ppt/dom.html',encoding='utf-8').read(); m=re.search(r'<pre id=\"extract-out\">EXTRACT(.*?)ENDX</pre>',s,re.S); d=json.loads(html.unescape(m.group(1)))
json.dump(d,open(sys.argv[1]+'/ppt/layout.json','w',encoding='utf-8'),ensure_ascii=False)
print({k:(len(v) if isinstance(v,list) else v) for k,v in d.items()})" "$R" "$S"
rm -f "$R"/ppt/img_*.png
python -I "$S/tools/build_pptx.py" "$R/ppt" "$R/ppt/${3:-poster_A0}.pptx" "${1:-0}" "${2:-A}"
