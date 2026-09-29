# Genera sitio/index.html a partir de desarrollo/index.html
# (saca Tailwind en vivo y enlaza el CSS compilado sitio/styles.css).
# Uso: python herramientas/build.py
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / "desarrollo/index.html").read_text(encoding="utf-8")
s, n = re.subn(r'\s*<script src="https://cdn\.jsdelivr\.net/npm/@tailwindcss/browser@4"></script>\s*<style type="text/tailwindcss">.*?</style>',
               '\n  <link rel="stylesheet" href="/styles.css">', s, flags=re.S)
assert n == 1, "No encontré el bloque de Tailwind en desarrollo/index.html"
s = s.replace("""    5) PRODUCCIÓN: el CDN de Tailwind es para prototipo. Para Google Ads
       (velocidad = Quality Score), compilá el CSS con Tailwind CLI.
""", """    5) ESTILOS: styles.css es el Tailwind ya compilado. Si agregás clases
       nuevas, editá la versión de desarrollo y volvé a generar el CSS.
""")
(root / "sitio/index.html").write_text(s, encoding="utf-8", newline="\r\n")
print("sitio/index.html generado")
