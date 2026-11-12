# Qué permite GitHub renderizar en un README de perfil (nov 2026)

Ticket: [#4](https://github.com/Starloss/Starloss/issues/4) · Mapa: [#3](https://github.com/Starloss/Starloss/issues/3) · Fecha de la investigación: 2026-11-12

Objetivo: saber qué se puede usar para un **hero** visual a medida (SVG propio, tema día/noche) en el README de perfil, y qué limita GitHub.

## Niveles de confianza

- **[Doc]**: documentación oficial de GitHub (`docs.github.com`, fuente en `github/docs`), changelog o blog de GitHub.
- **[Fuente]**: código fuente público (Camo, `html-pipeline`) o especificación (GFM spec, W3C, MDN).
- **[Probado]**: verificado hoy contra sistemas de producción de GitHub: la API `POST /markdown` (`mode: gfm`), que usa el mismo pipeline de renderizado que github.com, y cabeceras HTTP reales de `camo.githubusercontent.com` y `raw.githubusercontent.com`. Es first-party, pero el comportamiento no está documentado y puede cambiar.
- **[Comunidad]**: solo lo observa la comunidad (discusiones, blogs, PRs ajenos). Hay que verificarlo antes de depender de ello.

## Respuesta corta

1. **El hero tiene que ser un archivo SVG (o PNG/GIF/WebP) referenciado con `<img>`**. El `<svg>` inline en el Markdown se elimina por completo. [Probado]
2. **Un SVG cargado como imagen puede animarse** (CSS `@keyframes` y SMIL), pero **no ejecuta scripts, no es interactivo y no carga recursos externos**. Las fuentes y las imágenes tienen que ir incrustadas como `data:` URI. [Fuente]
3. **Día/noche: usar `<picture>` + `<source media="(prefers-color-scheme: dark)">`**, que es el método documentado. Los fragmentos `#gh-dark-mode-only` / `#gh-light-mode-only` siguen funcionando en la web, pero ya no aparecen en la documentación actual. [Doc] [Probado]
4. **La app móvil de GitHub no soporta imágenes por tema** (ni `<picture>` ni, según la comunidad, los fragmentos). Último dato de un empleado de GitHub: agosto de 2023, sin fecha de solución. Hace falta un `<img>` de respaldo que se lea bien en ambos temas. [Comunidad, con respuesta de staff]
5. **Camo** hace de proxy para las imágenes **externas** (no para las relativas del repo). Respeta el `Cache-Control` del origen, valida el `Content-Type` contra una lista de tipos de imagen y no modifica los bytes. Un SVG local (ruta relativa) se sirve desde `raw.githubusercontent.com` con `max-age=300`. [Doc] [Fuente] [Probado]
6. **Sanitizer**: sobreviven `align`, `width`, `height`, `<details open>`/`<summary>`, `<picture>`/`<source>`, `<table>`, `<kbd>`, `<sup>`/`<sub>`, `<br clear>`. Se eliminan `style`, `class`, `target`, `<center>`, `<font>`, `<svg>`, `<video>` externo, `<iframe>`, `<style>`, `data:` en `<img src>` y los formularios. [Probado] [Fuente]

## 1. SVG: `<img>` frente a inline

| Capacidad | Estado | Fuente |
|---|---|---|
| `<svg>` inline en el README | **Eliminado entero**: la API devuelve `<p dir="auto"></p>`. | [Probado] |
| SVG como archivo vía `<img src>` o `![]()` | Funciona: local (relativo) o externo (vía Camo). | [Doc] `attaching-files`: SVG es un tipo soportado; [Probado] |
| Scripts dentro del SVG | **No** se ejecutan. | [Fuente] W3C SVG Integration: con `img` se usa el *secure animated mode* (sin script). MDN: "JavaScript is disabled." |
| Recursos externos (CSS, imágenes, fuentes por URL) | **No** se cargan. | [Fuente] MDN: "External resources (e.g., images, stylesheets) cannot be loaded, though they can be used if inlined through `data:` URLs." W3C: "not allowed to resolve external references" |
| Fuentes web | Solo como `@font-face` con `src: url(data:font/woff2;base64,...)` incrustado. Google Fonts por `<link>`/`@import` no carga. | [Fuente] (MDN, regla de `data:`); [Comunidad]: es lo que hacen generadores como readme-typing-svg |
| Animación declarativa (SMIL `<animate>`, CSS `@keyframes`/`transition` en un `<style>` interno del SVG) | **Sí** corre. | [Fuente] W3C SVG Integration: el *secure animated mode* permite "declarative animation". [Comunidad]: ampliamente usado en READMEs |
| Interactividad (`:hover`, clics, enlaces internos del SVG) | **No.** El `<img>` entero puede ir envuelto en un `<a>` del Markdown. | [Fuente] W3C: interactivity "No" para `img` |
| `<foreignObject>` (HTML+CSS dentro del SVG) | Renderiza en navegadores de escritorio dentro de `<img>`, con las mismas restricciones: sin red ni script. El soporte en Safari/iOS y en la app móvil no está confirmado. | [Comunidad]. Hay que probarlo antes de depender de ello. |
| `@media (prefers-color-scheme)` **dentro** del SVG | Funciona en navegadores, pero refleja el tema del sistema/navegador, no necesariamente el ajuste de tema de GitHub. Hay reportes de comportamiento inconsistente en la app móvil. | [Comunidad]. Es preferible tener dos archivos y usar `<picture>`. |
| ¿Camo "congela" o reescribe animaciones? | **No.** Camo reenvía la respuesta tal cual (stream). Las afirmaciones de lo contrario en blogs son falsas según el código. | [Fuente] `atmos/camo/server.coffee` |

Cabeceras observadas hoy en el SVG servido:
- Relativo (repo): `raw.githubusercontent.com` responde con `Content-Type: image/svg+xml`, `Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; sandbox` y `Cache-Control: max-age=300`. En el README, la ruta relativa `github.com/<o>/<r>/raw/...` redirige (302) ahí. [Probado]
- Externo (Camo): `Content-Security-Policy: default-src 'none'; img-src data:; style-src 'unsafe-inline'`. Esa CSP solo afecta si alguien abre el SVG directamente. Dentro de `<img>` ya mandan las reglas del modo imagen. [Probado] [Fuente]

## 2. Tema claro/oscuro

| Método | Estado | Fuente |
|---|---|---|
| `<picture>` + `<source media="(prefers-color-scheme: dark\|light)" srcset=…>` + `<img>` de respaldo | **Método documentado actual.** La quickstart oficial lo usa justo para un banner de README de perfil. El `<img>` es el respaldo "if the visitor is using a browser that does not support the `prefers-color-scheme` feature". | [Doc] [quickstart-for-writing-on-github](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github); [Doc] basic syntax: "The `<picture>` HTML element is supported."; [Doc] [changelog GA 2022](https://github.blog/changelog/2022-05-19-specify-theme-context-for-images-in-markdown-ga/) |
| Cómo lo renderiza GitHub | Envuelve el bloque en un elemento propio `<themed-picture data-catalyst-inline="true">` y pasa cada `srcset` por Camo. Parece que el JS de GitHub ajusta la selección al tema elegido en GitHub, pero no está documentado. Hay reportes comunitarios contradictorios: unos dicen que sigue el tema de GitHub y otros que sigue el del SO. | [Probado] (salida de la API); [Comunidad] (comportamiento) |
| `![](img.png#gh-dark-mode-only)` / `#gh-light-mode-only` | Anunciado en el [changelog de 2021-11-24](https://github.blog/changelog/2021-11-24-specify-theme-context-for-images-in-markdown/). **Ya no aparece en la documentación actual** (`basic-writing-and-formatting-syntax` solo menciona `<picture>`). GitHub aún lo usa en sus propios repos, p. ej. el README de `primer/octicons`. La API conserva el fragmento en `data-canonical-src`, y el ocultado lo hace el CSS de github.com. | [Doc] (changelog); [Probado]; sigue funcionando según [Comunidad] |
| App móvil de GitHub | **No soporta imágenes por tema.** Respuesta de staff (aconsuegra) en [community#41758](https://github.com/orgs/community/discussions/41758): 15-12-2022 "the Mobile apps still don't support `<picture>` for dark/light mode images", y 14-08-2023 "still an issue on the Mobile apps, and we don't have an ETA for a fix". En la misma discusión, un usuario preguntó por novedades en sep-2025 y no hubo respuesta. Con los fragmentos `#gh-*-mode-only`, la app puede mostrar ambas imágenes o dejar un hueco. | [Comunidad con respuesta de staff]. No hay ninguna entrada de changelog que anuncie la solución. |

Implicación de diseño: el `<img>` de respaldo dentro de `<picture>` es el que verán la app móvil y los clientes sin soporte. Conviene que sea una variante legible tanto sobre fondo claro como oscuro, o que tenga fondo propio no transparente.

## 3. Proxy de imágenes Camo

| Aspecto | Detalle | Fuente |
|---|---|---|
| Qué pasa por Camo | Las imágenes con URL externa `http(s)` se reescriben a `camo.githubusercontent.com/<hmac>/<url-en-hex>`. **Las rutas relativas del repo no pasan por Camo**: se quedan relativas y se sirven desde `raw.githubusercontent.com`. Los vídeos no pasan por Camo, y GitHub "does not support externally hosted videos". | [Doc] [about-anonymized-urls](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-anonymized-urls); [Probado] |
| Content-Type | Tiene que ser un tipo de imagen de la [lista de Camo](https://github.com/atmos/camo/blob/master/mime-types.json) (incluye `image/svg+xml`, `image/png`, `image/gif`, `image/webp`, `image/jpeg`). Si no, la imagen no se muestra (Camo responde 404 "Non-Image content-type returned"). El origen debe enviar el tipo correcto: p. ej., un SVG servido como `text/plain` falla. | [Doc] (enlaza la lista); [Fuente] `server.coffee` |
| Caché | Camo reenvía el `Cache-Control` del origen. Si el origen no lo envía, el código de referencia aplica `public, max-age=31536000` (1 año). Producción va detrás de Varnish/CDN (`Via: 1.1 varnish`, `X-Cache`). Para que un widget dinámico se refresque, el origen debe enviar `Cache-Control: no-cache` (o un `max-age` corto). Último recurso: `curl -X PURGE <url-camo>`. | [Doc] (no-cache y PURGE); [Fuente] (`cache-control … \|\| 'public, max-age=31536000'`); [Probado]: shields.io devolvió `max-age=432000` y w3.org `max-age=2592000`, ambos reenviados tal cual |
| Tamaño máximo | El código de referencia rechaza `Content-Length` > **5 MiB** (`CAMO_LENGTH_LIMIT` = 5242880). GitHub no documenta el límite de producción, así que conviene asumir 5 MB como techo práctico. Otros límites de referencia: 4 redirecciones y 10 s de timeout de socket. | [Fuente]; producción no verificada |
| Subidas a GitHub (`user-attachments`) | Máximo 10 MB para imágenes y GIFs. SVG soportado. | [Doc] `attaching-files` |
| Orígenes privados o con autenticación | No se pueden mostrar. | [Doc] |
| Privacidad | Camo oculta al origen los datos del navegador del visitante. | [Doc] |

## 4. Sanitizer: qué HTML sobrevive

El sanitizer de producción de GitHub no es público. Las fuentes disponibles son: (a) [github/markup](https://github.com/github/markup), que dice que el HTML "is sanitized, aggressively removing things that could harm you and your kin—such as `script` tags, inline-styles, and `class` or `id` attributes"; (b) la allowlist de `html-pipeline` v2 ([`SanitizationFilter`](https://github.com/gjtorikian/html-pipeline/blob/v2.14.3/lib/html/pipeline/sanitization_filter.rb)), extraída de GitHub pero **más estricta que producción**, porque no incluye `picture`/`source`; (c) la extensión *tagfilter* de la [GFM spec](https://github.github.com/gfm/#disallowed-raw-html-extension-), que escapa `<title> <textarea> <style> <xmp> <iframe> <noembed> <noframes> <script> <plaintext>` reemplazando `<` por `&lt;`. La tabla siguiente es el resultado de producción vía la API, con un archivo de prueba renderizado hoy:

| Entrada | Resultado en producción [Probado] |
|---|---|
| `<p align="center">`, `<div align="right">`, `<h1 align="center">` | Se conserva `align` (y GitHub añade `dir="auto"`). **`align="center"` es la única forma de centrar.** |
| `<img width="800" height="200">` | Se conservan `width` y `height`. GitHub añade su propio `style="max-width: 100%; height: auto; …aspect-ratio…"`, así que la imagen es responsive y escala al ancho del contenedor. `width="100%"` también se conserva. |
| `<img>` en general | GitHub lo envuelve en `<a target="_blank" href="<misma imagen>">`: hacer clic abre la imagen. Si se envuelve en un `<a href>` propio, el destino es ese enlace. |
| atributo `style` del usuario | **Eliminado** (también en `div`). |
| atributo `class` | **Eliminado** (GitHub pone sus propias clases). |
| atributo `id` | Se conserva con el prefijo `user-content-` (`id="user-content-y"`). |
| `<center>`, `<font>`, `<marquee>` | Etiqueta eliminada; el texto queda. |
| `<svg>` inline (con `<animate>`) | Eliminado entero. |
| `<style>…</style>`, `<iframe>` | Escapados como texto (tagfilter). |
| `<details open><summary>…</summary>…</details>` | Se conserva, incluido `open`. [Doc] [collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections) |
| `<picture>` + `<source media srcset>` | Se conserva (envuelto en `<themed-picture>`, con `srcset` vía Camo). |
| `<video src="https://externo…">` | **Eliminado entero.** Solo funcionan los vídeos subidos a GitHub. [Doc] |
| `<a target="_blank" rel="noopener">` | `target` eliminado. `rel` se fuerza a `nofollow` en enlaces externos. **No se puede forzar a que un enlace abra en pestaña nueva.** |
| `<img src="data:…">` | Se elimina el `src`: imagen rota. Los `data:` solo valen **dentro** de un SVG. |
| `<object>`, `<embed>`, `<form>`, `<input>` | Eliminados. |
| `<table align width>`, `<td valign width>` | Se conservan (envueltos en `<markdown-accessiblity-table>`). Útil para maquetar columnas. |
| `<kbd> <sup> <sub> <ins> <mark>`, `<br clear="all">`, `<hr>` | Se conservan. |

La allowlist de atributos de `html-pipeline` (referencia [Fuente]) incluye entre otros `align`, `alt`, `width`, `height`, `valign`, `hspace`, `vspace`, `border`, `title`, `media`, `open`, `aria-*`, `role`, `lang`, `dir`, `clear`, `color`. En `<img>` solo admite los protocolos `http`, `https` y relativo.

## 5. Móvil

| Contexto | Comportamiento | Fuente |
|---|---|---|
| Web móvil (github.com en un navegador móvil) | Mismo HTML que en escritorio. `max-width: 100%; height: auto` hace que el hero escale al ancho. Un SVG con texto pequeño quedará ilegible en un ancho de unos 360 px. `<picture>` admite además `media="(max-width: …)"` para servir otra variante a móvil, pero solo en el navegador. | [Probado] (estilos inyectados); el escalado depende del navegador |
| App GitHub Mobile (iOS/Android) | Renderiza el README, pero **sin soporte de imágenes por tema** (ver §2). La ejecución de animaciones SVG, `foreignObject` y fuentes incrustadas en la app **no está documentada**. | [Comunidad con respuesta de staff]; **sin datos primarios. Hay que probarlo en un dispositivo real.** |

## 6. Restricciones del propio README de perfil

- Se muestra si existe un repo **público** con el mismo nombre que el usuario y con un `README.md` no vacío en la raíz. [Doc] [managing-your-profile-readme](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- Las imágenes relativas (`assets/hero.svg`) funcionan y se recomiendan para imágenes del propio repo. [Doc] basic syntax ("use relative links instead of absolute links")

## Recomendaciones para el hero (derivadas)

1. Dos SVG estáticos o animados (`hero-light.svg`, `hero-dark.svg`) en el repo, referenciados con ruta relativa. Así no pasan por Camo, la caché es de 5 min y se actualizan con cada commit.
2. Un `<picture>` con `<source>` dark/light y un `<img>` de respaldo que funcione en ambos temas (pensando en la app móvil), con `alt` descriptivo y `width="100%"`.
3. Todo autocontenido dentro del SVG: estilos en `<style>` interno, fuentes con un subset incrustado en base64 (para no pesar), sin `<script>` ni URLs externas. La animación, con CSS `@keyframes` o SMIL y moderada (`prefers-reduced-motion` dentro del SVG es posible, [Comunidad]).
4. Nada de `style`/`class` en el HTML del README: maquetar solo con `align`, `width`, `height` y `<table>`.
5. Widgets dinámicos externos: verificar que el origen envía `Content-Type` de imagen y un `Cache-Control` corto o `no-cache`, y que pesan bastante menos de 5 MB.
6. Antes de dar el hero por bueno, probarlo en la app GitHub Mobile (iOS y Android) y en Safari/iOS, sobre todo si se usa `foreignObject`.

## Fuentes

- GitHub Docs (fuente en `github/docs`, rama `main`, leída el 2026-11-12):
  - [Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax): imágenes, rutas relativas y "The `<picture>` HTML element is supported."
  - [Quickstart for writing on GitHub](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github): `<picture>` + `prefers-color-scheme` para un banner de perfil
  - [About anonymized URLs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-anonymized-urls): Camo, Content-Type, Cache-Control y PURGE
  - [Attaching files](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files): límites de subida y tipos soportados (SVG)
  - [Organizing information with collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)
  - [Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- GitHub changelog y blog:
  - [2021-11-24 Specify theme context for images in Markdown](https://github.blog/changelog/2021-11-24-specify-theme-context-for-images-in-markdown/) (`#gh-dark-mode-only`)
  - [2022 Specify theme context for images in Markdown (GA)](https://github.blog/changelog/2022-05-19-specify-theme-context-for-images-in-markdown-ga/) (`<picture>`)
  - [GitHub Blog, abr-2025: How to make your images in Markdown on GitHub adjust for dark mode and light mode](https://github.blog/developer-skills/github/how-to-make-your-images-in-markdown-on-github-adjust-for-dark-mode-and-light-mode/)
- Código y especificaciones:
  - [github/markup README](https://github.com/github/markup): paso de sanitización
  - [html-pipeline v2.14.3 SanitizationFilter](https://github.com/gjtorikian/html-pipeline/blob/v2.14.3/lib/html/pipeline/sanitization_filter.rb): allowlist de referencia
  - [GFM spec: Disallowed Raw HTML (tagfilter)](https://github.github.com/gfm/#disallowed-raw-html-extension-)
  - [atmos/camo server.coffee](https://github.com/atmos/camo/blob/master/server.coffee) y [mime-types.json](https://github.com/atmos/camo/blob/master/mime-types.json): límite de 5 MiB, caché por defecto y CSP
  - [W3C SVG Integration](https://www.w3.org/TR/svg-integration/): *secure animated mode* para `img`
  - [MDN: SVG as an image](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image)
- Producción (pruebas propias del 2026-11-12): `POST https://api.github.com/markdown` (`mode: gfm`) con un archivo de prueba, más `curl -I` sobre `camo.githubusercontent.com` y `raw.githubusercontent.com`.
- Comunidad: [community discussion #41758](https://github.com/orgs/community/discussions/41758) (respuestas de staff sobre la app móvil, 2022–2023).
