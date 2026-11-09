# Web personal de Pri dos Santos (dominio somosmadrastras.com)

Web estática (HTML y CSS, sin WordPress) preparada para Vercel. Fase 1: se mantiene el dominio somosmadrastras.com y todas las URL que Google ya tiene indexadas.

## Cómo se edita
Los textos de cada página están en `sitio/paginas/*.html`. Después de cambiar algo:

    python3 sitio/construir.py

El generador escribe las páginas en `web/` con la cabecera, el pie, los metadatos SEO y el `sitemap.xml`. El menú y el pie se cambian en `sitio/construir.py`.

## SEO
- Se conservan las direcciones de WordPress, con barra final: `/`, `/newsletter/`, `/politica-privacidad/`, `/politica-de-cookies/`.
- `/acompanamiento/` redirige de forma permanente a `/madrastra-en-paz/`.
- `vercel.json` redirige de forma permanente `/pilares/` (a `/sobre-mi/#enfoque`), `/index.php/politica-privacidad/` y otras direcciones antiguas.
- En Vercel, el dominio principal debe ser `www.somosmadrastras.com`, con `somosmadrastras.com` redirigiendo a él, igual que ahora.

## Pendiente antes de publicar
Buscar `pendiente` en `sitio/paginas/`:
- Datos legales (titular, NIF, domicilio) en aviso legal y privacidad

## Vercel
Importar el repositorio con Root Directory = `web`, sin framework ni comando de build.
