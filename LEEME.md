# Grupo C Piletas — landing page

Online: https://grupocpiletas.pages.dev (Cloudflare Pages, proyecto `grupocpiletas`)
Dominio a conectar: grupocpiletas.com.ar

## Carpetas

- `sitio/` → **lo que se publica**. Versión final: `index.html`, `styles.css`
  (Tailwind ya compilado), `robots.txt` y `sitemap.xml`.
- `desarrollo/index.html` → la misma página con Tailwind cargado en vivo.
  Sirve para probar cambios de diseño (clases nuevas) abriéndola en el navegador.
- `herramientas/deploy.py` → publica `sitio/` en Cloudflare Pages por API.

## Cómo actualizar

Todos los cambios se hacen en `desarrollo/index.html`. Después:

1. `python herramientas/build.py` → genera `sitio/index.html`.
2. Solo si agregaste clases de Tailwind nuevas: regenerar `sitio/styles.css` con
   `python herramientas/servidor_css.py` (las instrucciones están en el archivo).

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
