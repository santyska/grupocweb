# Servidor local para regenerar sitio/styles.css.
# 1) python herramientas/servidor_css.py   2) abrir http://localhost:5180/desarrollo/
# 3) en la consola del navegador:
#    await fetch("/_css", {method: "PUT", body: [...document.styleSheets].map(s => s.ownerNode.textContent).find(t => t.includes("tailwindcss v4"))})
# Acepta PUT /_css y guarda el cuerpo en sitio/styles.css.
import http.server, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(root), **k)
    def do_PUT(self):
        if self.path != "/_css": return self.send_error(403)
        data = self.rfile.read(int(self.headers["Content-Length"]))
        (root / "sitio/styles.css").write_bytes(data)
        self.send_response(204); self.end_headers()
    def end_headers(self):
        self.send_header("Cache-Control", "no-store"); super().end_headers()
print("http://localhost:5180/desarrollo/")
http.server.ThreadingHTTPServer(("127.0.0.1", 5180), H).serve_forever()
