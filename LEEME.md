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

- **Cambios de texto, fotos o links:** editá `sitio/index.html` y hacé el mismo
  cambio en `desarrollo/index.html` para que queden iguales.
- **Cambios de diseño con clases de Tailwind nuevas:** hacelos en `desarrollo/`
  y después hay que regenerar `sitio/styles.css`.

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
- Medición de consultas: script `ads-ia-garfar.vercel.app/m.js` antes de `</body>`.
- Fotos de stock a reemplazar por fotos propias: buscar `REEMPLAZAR FOTO`.
- Marca: navy #0F2A3D · teal #2AA7A0 · crema #F7F5EF · Fraunces + Manrope.
