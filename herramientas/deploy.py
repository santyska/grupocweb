# Publica la carpeta sitio/ en Cloudflare Pages (proyecto grupocpiletas).
# Uso:  CLOUDFLARE_API_TOKEN=xxxx python herramientas/deploy.py sitio
import json, os, sys, base64, hashlib, mimetypes, urllib.request, uuid
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN") or sys.exit("Falta la variable CLOUDFLARE_API_TOKEN")
SITE = sys.argv[1] if len(sys.argv) > 1 else "sitio"
ACC = "796c0f18a0f1ca3b67dfd20f57da9e04"; PROJ = "grupocpiletas"
API = f"https://api.cloudflare.com/client/v4/accounts/{ACC}/pages/projects"
def req(url, data=None, method=None, tok=TOKEN, ctype="application/json", raw=False):
    body = data if raw else (json.dumps(data).encode() if data is not None else None)
    r = urllib.request.Request(url, data=body, method=method or ("POST" if body else "GET"),
        headers={"Authorization": f"Bearer {tok}", **({"Content-Type": ctype} if body else {})})
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:800]); sys.exit(1)
# 1) proyecto
projs = [p["name"] for p in req(API)["result"]]
if PROJ not in projs:
    print("create:", req(API, {"name": PROJ, "production_branch": "main"})["success"])
# 2) token de subida
jwt = req(f"{API}/{PROJ}/upload-token")["result"]["jwt"]
files = {}
for n in os.listdir(SITE):
    b = open(os.path.join(SITE, n), "rb").read()
    b64 = base64.b64encode(b).decode()
    h = hashlib.sha256((b64 + n.rsplit(".",1)[-1]).encode()).hexdigest()[:32]
    files["/" + n] = (h, b64, mimetypes.guess_type(n)[0] or "application/octet-stream")
PA = "https://api.cloudflare.com/client/v4/pages/assets"
missing = req(f"{PA}/check-missing", {"hashes": [v[0] for v in files.values()]}, tok=jwt)["result"]
if missing:
    payload = [{"key": h, "value": b64, "metadata": {"contentType": ct}, "base64": True} for h, b64, ct in files.values() if h in missing]
    print("upload:", req(f"{PA}/upload", payload, tok=jwt)["success"])
req(f"{PA}/upsert-hashes", {"hashes": [v[0] for v in files.values()]}, tok=jwt)
# 3) deployment
bnd = uuid.uuid4().hex
manifest = json.dumps({k: v[0] for k, v in files.items()})
body = (f"--{bnd}\r\nContent-Disposition: form-data; name=\"manifest\"\r\n\r\n{manifest}\r\n"
        f"--{bnd}\r\nContent-Disposition: form-data; name=\"branch\"\r\n\r\nmain\r\n--{bnd}--\r\n").encode()
d = req(f"{API}/{PROJ}/deployments", body, raw=True, ctype=f"multipart/form-data; boundary={bnd}")["result"]
print("deployment:", d["id"], d["url"], "| stage:", d["latest_stage"]["name"], d["latest_stage"]["status"])
print("subdomain:", req(f"{API}/{PROJ}")["result"]["subdomain"])
