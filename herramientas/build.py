# Genera sitio/<página>.html a partir de cada desarrollo/<página>.html
# (la home y las páginas internas que arma herramientas/paginas.py):
# saca Tailwind en vivo y enlaza el CSS compilado sitio/styles.css.
# Uso: python herramientas/paginas.py && python herramientas/build.py
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
VIEJO = """    5) PRODUCCIÓN: el CDN de Tailwind es para prototipo. Para Google Ads
       (velocidad = Quality Score), compilá el CSS con Tailwind CLI.
"""
NUEVO = """    5) ESTILOS: styles.css es el Tailwind ya compilado. Si agregás clases
       nuevas, editá la versión de desarrollo y volvé a generar el CSS.
"""
for origen in sorted((root / "desarrollo").glob("*.html")):
    s = origen.read_text(encoding="utf-8")
    s, n = re.subn(r'\s*<script src="https://cdn\.jsdelivr\.net/npm/@tailwindcss/browser@4"></script>\s*<style type="text/tailwindcss">.*?</style>',
                   '\n  <link rel="stylesheet" href="/styles.css">', s, flags=re.S)
    assert n == 1, f"No encontré el bloque de Tailwind en desarrollo/{origen.name}"
    s = s.replace(VIEJO, NUEVO)
    (root / "sitio" / origen.name).write_text(s, encoding="utf-8", newline="\r\n")
    print(f"sitio/{origen.name} generado")
