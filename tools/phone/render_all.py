import json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phone
SITE = phone.SITE
days = json.load(open(os.path.join(SITE, "content/days.json")))
out = os.path.join(SITE, "content/phone"); os.makedirs(out, exist_ok=True)
start = sys.argv[1] if len(sys.argv) > 1 else "0000"
n = 0
for d, e in sorted(days.items()):
    if d < start or not e.get("img"): continue
    phone.render("blur", e, os.path.join(SITE, "content/img", e["img"]), os.path.join(out, d + ".jpg"), text_style="widget")
    n += 1
print("rendered", n)
