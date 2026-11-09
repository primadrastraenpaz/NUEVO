# somosmadrastras.com (nueva web)

Web estática (HTML y CSS, sin WordPress) con la identidad visual de Madrastra en Paz, preparada para Vercel.

## Páginas
- `/` inicio: comunidad, sobre mí, pilares, acompañamiento, libros, podcast, prensa, newsletter
- `/acompanamiento` sesiones individuales, parejas y testimonios
- `/newsletter` formulario de Substack
- `/aviso-legal`, `/politica-privacidad`, `/politica-de-cookies`

`vercel.json` redirige las direcciones antiguas de WordPress (`/pilares/`, `/index.php/politica-privacidad/`, etc.).

## Pendiente antes de publicar
Buscar `pendiente` en los archivos:
- `#pendiente-skool`: enlace de la comunidad en Skool
- `#pendiente-libro-divorcio`: enlace de "¿Qué es el divorcio?"
- `#pendiente-pareja-en-paz`: enlace del acompañamiento en pareja
- Datos legales (titular, NIF, domicilio, correo) en aviso legal y privacidad

## Vercel
Importar el repositorio en Vercel con **Root Directory = `web`**, sin framework ni comando de build.
