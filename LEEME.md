# Grupo C Piletas — landing page

Online: https://grupocpiletas.pages.dev (Cloudflare Pages, proyecto `grupocpiletas`)
Dominio a conectar: grupocpiletas.com.ar

## Carpetas

- `sitio/` → **lo que se publica**. Versión final: `index.html`, las páginas
  internas (`como-trabajamos.html`, `preguntas-frecuentes.html`), `styles.css`
  (Tailwind ya compilado), `robots.txt` y `sitemap.xml`. Cloudflare las sirve
  sin `.html`: `/como-trabajamos`, `/preguntas-frecuentes`.
- `desarrollo/index.html` → la misma página con Tailwind cargado en vivo.
  Sirve para probar cambios de diseño (clases nuevas) abriéndola en el navegador.
- `desarrollo/contenido/<página>.html` → el contenido propio de cada página
  interna. El `<head>`, el header, el footer y los scripts salen de la home.
- `herramientas/paginas.py` → arma `desarrollo/<página>.html` (home + contenido).
- `herramientas/deploy.py` → publica `sitio/` en Cloudflare Pages por API.

## Cómo actualizar

Todos los cambios se hacen en `desarrollo/index.html`. Después:

1. `python herramientas/paginas.py` → vuelve a armar las páginas internas
   (necesario si cambiaste el header, el footer o el contenido de una).
2. `python herramientas/build.py` → genera `sitio/` (la home y las internas).
3. Solo si agregaste clases de Tailwind nuevas: regenerar `sitio/styles.css` con
   `python herramientas/servidor_css.py` (las instrucciones están en el archivo).
   Ojo: el CSS se compila con las clases de la página que abras; si usás una
   clase nueva solo en una página interna, abrí esa. Lo más simple es usar
   clases que ya existen.
4. Si sumás una página, agregala al menú de `paginas.py` y a `sitio/sitemap.xml`.

## Cómo publicar

Opción A (panel): Cloudflare → Workers & Pages → grupocpiletas → Create deployment
→ arrastrar la carpeta `sitio`.

Opción B (script): con un token de Cloudflare con permiso *Cloudflare Pages: Edit*:

```bash
CLOUDFLARE_API_TOKEN=xxxx python herramientas/deploy.py sitio
```

**Nunca guardes el token en un archivo del repositorio.**

## Datos a mano

- WhatsApp: constante `WA_NUMBER` al final del HTML (5491130446269).
- Llamadas: links `tel:+5491130446269` (atributo `data-call`).
- Medición de consultas: script `ads-ia-garfar.vercel.app/m.js` antes de `</body>`.
- Fotos de stock a reemplazar por fotos propias: buscar `REEMPLAZAR FOTO`.
- Marca: navy #0F2A3D · teal #2AA7A0 · crema #F7F5EF · Fraunces + Manrope.
