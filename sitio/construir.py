#!/usr/bin/env python3
"""Genera la web estática en ../web a partir de sitio/paginas/*.html.

Cada página empieza con un bloque de metadatos:

<!--
ruta: /charlas/
titulo: Charlas y formación
descripcion: ...
menu: /charlas/
-->

La ruta conserva la barra final de las direcciones de WordPress para no
cambiar ninguna URL indexada. Uso: python3 sitio/construir.py
"""
import html
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent
WEB = RAIZ.parent / "web"
DOMINIO = "https://www.somosmadrastras.com"
SUFIJO = "Pri dos Santos"

MENU = [
    ("/sobre-mi/", "Sobre mí"),
    ("/madrastra-en-paz/", "Madrastra en Paz"),
    ("/charlas/", "Charlas"),
    ("/astras/", "ASTRAS"),
    ("/divulgacion/", "Divulgación"),
    ("/prensa/", "Prensa"),
]

CABECERA = """<header class="cabecera">
  <div class="contenedor">
    <a class="marca" href="/">Pri <span>dos Santos</span></a>
    <button class="menu-boton" type="button" aria-expanded="false" aria-controls="menu">Menú</button>
    <nav class="menu" id="menu" aria-label="Principal">
{enlaces}
      <a class="boton" href="/contacto/">Contacto</a>
    </nav>
  </div>
</header>"""

PIE = """<footer class="pie">
  <div class="contenedor">
    <div>
      <a class="marca" href="/">Pri <span>dos Santos</span></a>
      <p>Comunico, divulgo y acompaño a madrastras y familias ensambladas. Fundadora de Madrastra en Paz y presidenta de ASTRAS.</p>
    </div>
    <div>
      <h3>Trabajo</h3>
      <ul>
        <li><a href="/madrastra-en-paz/">Madrastra en Paz</a></li>
        <li><a href="/charlas/">Charlas</a></li>
        <li><a href="/astras/">ASTRAS</a></li>
      </ul>
    </div>
    <div>
      <h3>Divulgación</h3>
      <ul>
        <li><a href="/divulgacion/">Podcast y libros</a></li>
        <li><a href="/newsletter/">Newsletter</a></li>
        <li><a href="/prensa/">Prensa</a></li>
        <li><a href="/contacto/">Contacto</a></li>
      </ul>
    </div>
    <div>
      <h3>Redes</h3>
      <ul>
        <li><a href="https://www.instagram.com/pri.madrastraenpaz/" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="https://www.youtube.com/@pri.madrastraenpaz" target="_blank" rel="noopener">YouTube</a></li>
        <li><a href="https://open.spotify.com/show/601LgQSnyQIpU74ceh1kwN" target="_blank" rel="noopener">Spotify</a></li>
      </ul>
    </div>
    <div class="pie-final">
      <span>© <span data-anio>2026</span> Pri dos Santos</span>
      <span><a href="/aviso-legal/">Aviso legal</a> · <a href="/politica-privacidad/">Privacidad</a> · <a href="/politica-de-cookies/">Cookies</a></span>
    </div>
  </div>
</footer>"""

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo_completo}</title>
<meta name="description" content="{descripcion}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="Pri dos Santos">
<meta property="og:title" content="{titulo_completo}">
<meta property="og:description" content="{descripcion}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{dominio}/assets/img/pri-portada.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FEF9F3">
<link rel="icon" href="/favicon.png">
<link rel="preload" href="/assets/fonts/playfair-display-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/jost-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/estilos.css">
{extra_head}</head>
<body>

{cabecera}

<main>
{cuerpo}
</main>

{pie}

<script src="/assets/js/menu.js" defer></script>
</body>
</html>
"""

PERSONA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://www.somosmadrastras.com/#pri",
      "name": "Pri dos Santos",
      "alternateName": "Priscila dos Santos",
      "url": "https://www.somosmadrastras.com/",
      "image": "https://www.somosmadrastras.com/assets/img/pri-portada.webp",
      "jobTitle": "Comunicadora y divulgadora sobre madrastras y familias ensambladas",
      "description": "Fundadora de la comunidad Madrastra en Paz, presidenta de ASTRAS y conferenciante sobre madrastras y familias ensambladas.",
      "memberOf": { "@type": "Organization", "name": "ASTRAS", "url": "https://asociacionastras.org/" },
      "knowsAbout": ["Madrastras", "Familias ensambladas", "Comunicación no violenta", "Inteligencia emocional", "Crianza respetuosa"],
      "sameAs": [
        "https://www.instagram.com/pri.madrastraenpaz/",
        "https://www.youtube.com/@pri.madrastraenpaz",
        "https://open.spotify.com/show/601LgQSnyQIpU74ceh1kwN"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.somosmadrastras.com/#web",
      "name": "Pri dos Santos",
      "url": "https://www.somosmadrastras.com/",
      "inLanguage": "es-ES",
      "publisher": { "@id": "https://www.somosmadrastras.com/#pri" }
    }
  ]
}
</script>
"""


def leer_pagina(ruta_archivo):
    texto = ruta_archivo.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->\s*", texto, re.S)
    meta = {}
    for linea in m.group(1).strip().splitlines():
        clave, _, valor = linea.partition(":")
        meta[clave.strip()] = valor.strip()
    return meta, texto[m.end():]


def construir():
    rutas = []
    for archivo in sorted((RAIZ / "paginas").glob("*.html")):
        meta, cuerpo = leer_pagina(archivo)
        ruta = meta["ruta"]
        actual = meta.get("menu", ruta)
        enlaces = "\n".join(
            f'      <a href="{href}"' + (' aria-current="page"' if href == actual else "") + f">{texto}</a>"
            for href, texto in MENU
        )
        titulo = meta["titulo"]
        titulo_completo = titulo if meta.get("titulo_exacto") == "si" else f"{titulo} · {SUFIJO}"
        salida = PLANTILLA.format(
            titulo_completo=html.escape(titulo_completo, quote=True),
            descripcion=html.escape(meta["descripcion"], quote=True),
            url=DOMINIO + ruta,
            dominio=DOMINIO,
            extra_head=PERSONA if ruta == "/" else "",
            cabecera=CABECERA.format(enlaces=enlaces),
            cuerpo=cuerpo.rstrip(),
            pie=PIE,
        )
        destino = WEB / ruta.strip("/") / "index.html" if ruta != "/" else WEB / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(salida, encoding="utf-8")
        if meta.get("indexar", "si") == "si":
            rutas.append(ruta)
        print("ok", ruta)

    mapa = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    mapa += [f"  <url><loc>{DOMINIO}{r}</loc></url>" for r in rutas]
    mapa.append("</urlset>")
    (WEB / "sitemap.xml").write_text("\n".join(mapa) + "\n", encoding="utf-8")


if __name__ == "__main__":
    construir()
