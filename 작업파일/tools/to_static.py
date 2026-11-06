import re, sys

src, dst, extra = sys.argv[1], sys.argv[2], sys.argv[3] == "1"
s = open(src, encoding="utf-8").read()

s = s.replace('<script src="./support.js"></script>', '')
_m = re.search(r'"accent":\{"editor":"color","default":"(#[0-9A-Fa-f]{6})"', s)
s = re.sub(r'<script type="text/x-dc".*?</script>', '', s, flags=re.S)
s = s.replace("{{accent}}", _m.group(1) if _m else "#1F4E79").replace("{{mint}}", "#A1FFCB").replace("{{blue}}", "#1A4BE0")

import base64, os
_FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts-dl")
for _bid, _name in (("7aecd9586478b9bff32aa626ffe9498e", "Regular"), ("9c75082732dd3cea95235c1f82198c55", "Medium"), ("484160b31ce5e7696c870fa303f1d8e0", "Bold")):
    if "/_blob/" + _bid in s:
        _data = base64.b64encode(open(os.path.join(_FD, "Pretendard-%s.woff2" % _name), "rb").read()).decode()
        s = s.replace("/_blob/" + _bid, "data:font/woff2;base64," + _data)

def sc_if(m):
    cond = m.group(1).strip()
    keep = extra if cond == "extra" else not extra
    return m.group(2) if keep else ""

s = re.sub(r'<sc-if value="\{\{(\w+)\}\}"[^>]*>(.*?)</sc-if>', sc_if, s, flags=re.S)
for tag in ("x-dc", "helmet"):
    s = s.replace("<%s>" % tag, "").replace("</%s>" % tag, "")
open(dst, "w", encoding="utf-8").write(s)
print("ok", len(s))
