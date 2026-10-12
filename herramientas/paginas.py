# Arma las páginas internas (desarrollo/<slug>.html) con el mismo <head>,
# header, footer, botones flotantes y scripts que desarrollo/index.html,
# y el contenido propio de cada una en desarrollo/contenido/<slug>.html.
# Así, si cambia el header o el footer de la home, se vuelven a generar igual.
# Uso: python herramientas/paginas.py   (después: python herramientas/build.py)
import re, pathlib, html

root = pathlib.Path(__file__).resolve().parent.parent
dev = root / "desarrollo"
base = (dev / "index.html").read_text(encoding="utf-8")

PAGINAS = {
    "como-trabajamos": {
        "titulo": "Cómo trabajamos | Grupo C Piletas",
        "descripcion": "Cómo construimos tu pileta de hormigón armado: consulta, visita técnica sin cargo, presupuesto cerrado con cronograma por escrito, obra con avances semanales y entrega con garantía firmada.",
    },
    "piletas-a-medida": {
        "titulo": "Piletas de hormigón a medida | Grupo C Piletas",
        "descripcion": "Piletas de hormigón armado a medida: de nado, con desnivel, con solárium, deck o borde atérmico. Proyecto y cálculo estructural para tu terreno, visita técnica sin cargo y garantía escrita.",
    },
    "piletas-en-countries": {
        "titulo": "Piletas en countries y barrios cerrados | Grupo C Piletas",
        "descripcion": "Piletas de hormigón armado en countries y barrios cerrados de zona norte y oeste: reglamento del barrio, accesos, suelos con napa alta y desniveles. Visita técnica sin cargo.",
    },
    "preguntas-frecuentes": {
        "titulo": "Preguntas frecuentes | Grupo C Piletas",
        "descripcion": "Respuestas sobre piletas de hormigón armado: financiación y pagos por avance de obra, plazos, garantía escrita, zonas de trabajo y visita técnica sin cargo.",
    },
}

def una(patron, texto, desc):
    m = re.search(patron, texto, flags=re.S)
    assert m, f"No encontré {desc} en desarrollo/index.html"
    return m

head = una(r"^.*?</head>\n", base, "el <head>").group(0)
sprite_y_header = una(r"\n  <!-- Ícono WhatsApp reutilizable -->.*?</header>\n", base, "el header").group(0)
pie = una(r"\n  <!-- ===================== 9\. FOOTER ===================== -->.*$", base, "el footer").group(0)

# En las páginas internas, los links del menú vuelven a la home o van a su página.
sprite_y_header = (
    sprite_y_header.replace('href="#top" class="flex items-center gap-2.5"', 'href="/" class="flex items-center gap-2.5"')
    .replace('href="#diferenciales"', 'href="/#diferenciales"')
    .replace('href="#proceso"', 'href="/como-trabajamos"')
    .replace('href="#obras"', 'href="/#obras"')
    .replace('href="#faq"', 'href="/preguntas-frecuentes"')
)
assert sprite_y_header.count('href="/') == 5, "Cambiaron los links del menú: revisá paginas.py"

for slug, meta in PAGINAS.items():
    url = f"https://grupocpiletas.com.ar/{slug}"
    h = head
    h = re.sub(r"<title>.*?</title>", f"<title>{html.escape(meta['titulo'])}</title>", h)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(meta["descripcion"]), h)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, h)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, h)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(meta["titulo"]), h)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(meta["descripcion"]), h)
    # La foto del hero de la home no se usa en estas páginas: no se precarga.
    h = re.sub(r'\s*<!-- REEMPLAZAR FOTO: imagen del hero, precargada para mejorar LCP -->\s*<link rel="preload" as="image"[^>]*>', "", h)
    contenido = (dev / "contenido" / f"{slug}.html").read_text(encoding="utf-8")
    datos_extra = ""
    m = re.search(r"<!-- HEAD -->(.*?)<!-- /HEAD -->", contenido, flags=re.S)
    if m:
        datos_extra = m.group(1).strip() + "\n"
        contenido = contenido.replace(m.group(0), "").lstrip()
        h = h.replace("</head>\n", f"  {datos_extra}</head>\n")
    pagina = (
        h
        + "\n<body class=\"bg-ink text-stone font-sans leading-relaxed\">\n"
        + sprite_y_header
        + f"\n  <main>\n{contenido.rstrip()}\n  </main>\n"
        + pie
    )
    (dev / f"{slug}.html").write_text(pagina, encoding="utf-8", newline="\n")
    print(f"desarrollo/{slug}.html generado")
