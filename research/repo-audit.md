# Auditoría de repos candidatos a repo vitrina

Ticket: [#6](https://github.com/Starloss/Starloss/issues/6) · Mapa: [#3](https://github.com/Starloss/Starloss/issues/3) · Fecha: 2026-11-12

**Pregunta.** Para cada repo de Starloss (privados: game-dev-empire, live-chat, EmporiaEtImperia, solidity-no-loss-lottery, solidity-swapper, solidity-nft-marketplace, solidity-nft-drop, Solidity_Voting_System, boda-dicor, wocoon-plantilla, CONSORVEN, job-search; públicos: Portfolio, wedding-invitation): ¿puede ser **repo vitrina** en un perfil orientado a reclutadores de un Full-Stack Lead Developer?

## Método y fuentes

Las fuentes primarias son los propios repos. No se cambió la visibilidad, los ajustes ni el contenido de ninguno.

- Metadatos: `gh repo list Starloss` (visibilidad, fork/template, último push, licencia, lenguaje, tamaño) y `gh repo view ai-job-search-dev/ai-job-search` para el upstream de job-search.
- Historial completo: se clonó cada repo sin checkout en un directorio temporal y se volcó `git log --all -p` (todas las ramas). Sobre las líneas añadidas se buscaron bloques de clave privada, claves AWS/Google/Stripe/GitHub/Slack/OpenAI/SendGrid, URLs de Infura/Alchemy con clave, hex de 64 caracteres (posibles claves privadas de Ethereum), JWT, cadenas de conexión con contraseña, mnemónicos y asignaciones genéricas (`apiKey|secret|password|token = ...`). También se buscaron archivos con nombre sensible añadidos alguna vez (`.env`, `.pem`, `.key`, `google-services.json`, `.csv`, `.pdf`, `.sql`…) y datos personales (emails, teléfonos, cuentas de pago, direcciones). gitleaks y trufflehog no están instalados, así que el escaneo es con expresiones regulares propias. Se descartaron a mano los falsos positivos (checksums de `Cargo.lock`, hashes de caché, `keyHash` de Chainlink, direcciones de contratos públicos, placeholders de `.env.example`).
- HEAD: `git ls-tree -r HEAD` y lectura de README, LICENSE, `package.json` y la estructura de carpetas.
- No se ejecutó ningún script, instalación ni build del código descargado.

Este documento es público: los secretos y datos personales se describen solo por tipo, ruta y commit, nunca por su valor.

## Veredictos

| Repo | Visib. | Último push | Veredicto | Motivo principal |
|---|---|---|---|---|
| Portfolio | pública | 2026-11-07 | **apto** | El mejor del lote: README en inglés de calidad, CI, 52 archivos de test, ADRs, Lighthouse CI, cobertura. Sin secretos. |
| game-dev-empire | privada | 2026-10-27 | **apto** | Proyecto propio, activo, sin secretos. React + Zustand + Tauri 2, simulación determinista, 34 archivos de test, docs de arquitectura y decisiones. Le faltan licencia y CI. |
| live-chat | privada | 2026-04-29 | **apto tras limpieza** | Sin secretos reales. Monorepo full-stack con auth por refresh token rotatorio, Socket.IO, Prisma/Postgres, Redis, E2E con Playwright y CI. Hay que quitar archivos sueltos y pasar el README a inglés. |
| wedding-invitation | pública | 2026-03-04 | **apto tras limpieza** | Versión demo saneada de boda-dicor (stubs, nombres ficticios, sin cuentas reales). README de una línea, carpeta `.astro/` generada en el repo y audio y fotos sin acreditar. |
| solidity-nft-marketplace | privada | 2022-03-09 | **apto tras limpieza** (valor bajo) | El más completo de los Solidity: contrato upgradeable con roles y comisiones, ~67 KB de tests. README copiado con título equivocado; usa Rinkeby, ya cerrada. |
| solidity-nft-drop | privada | 2022-02-24 | **apto tras limpieza** (valor bajo) | ERC20/721/1155 con tests. README con descripción de otro repo ("Vote System") y enlaces muertos a Rinkeby y OpenSea testnets. |
| Solidity_Voting_System | privada | 2022-02-12 | **apto tras limpieza** (valor bajo) | Contrato upgradeable (V1→V2) con tests. Ejercicio académico pequeño. |
| solidity-no-loss-lottery | privada | 2022-04-08 | **no apto** | Interesante (Chainlink VRF v2 + Compound) pero sin terminar: el último commit es "Trying to solve problems with eth send". README con título de otro repo. |
| solidity-swapper | privada | 2022-03-17 | **no apto** | Roto: el último commit dice "Test with paraswapper-sdk doesn't work". README con título de otro repo. |
| EmporiaEtImperia | privada | 2025-06-28 | **no apto** | Tras el commit "Fresh restart" el HEAD solo tiene la configuración de Unreal (8 archivos, sin README). El trabajo anterior son assets binarios `.uasset` que GitHub no muestra. Inactivo. |
| boda-dicor | privada | 2026-04-18 | **no apto** | Datos personales reales en el historial (ver detalle). wedding-invitation ya es su versión publicable. |
| CONSORVEN | privada | 2021-05-14 | **no apto** | Proyecto de cliente con **credenciales SMTP en claro** (todavía en HEAD), emails del cliente y assets de marca del cliente. Sin README. |
| wocoon-plantilla | privada | 2021-11-17 | **no apto** | Plantilla comercial comprada (Enappd "Ionic 5 Full App PRO"). Su licencia **prohíbe distribuir el código**. Además, claves de terceros en el historial. |
| job-search | privada | 2026-11-10 | **no apto** | Derivado de [ai-job-search-dev/ai-job-search](https://github.com/ai-job-search-dev/ai-job-search) (MIT, © Mads Lorentzen): solo 11 de 446 commits son del usuario. Contiene CV, cartas, respuestas a formularios y el tracker de postulaciones. |

**En resumen.** Repos vitrina viables: **Portfolio** y **game-dev-empire** tal cual (con pulido), y **live-chat** tras una limpieza menor. **wedding-invitation** sirve como pieza secundaria si se le da un README. Los Solidity de 2022 son ejercicios académicos que no apoyan la narrativa de Full-Stack Lead; como mucho uno (nft-marketplace) como muestra de Web3. El resto no debe hacerse público.

## Detalle por repo

### Portfolio (pública)

- **Secretos:** ninguno en el historial. `.mcp.json` solo registra el servidor local de CodeGraph, sin tokens.
- **Datos personales:** el email de contacto del autor está en `src/app/config/site.ts` y `src/content/data/profile.ts`. Es intencional, porque ya se publica en el sitio. Un `public/cv.pdf` se añadió en `c50a285` y se borró en `d9f0c17`; es el CV público y sigue en el historial. El riesgo es bajo.
- **README:** muy bueno, en inglés: stack, decisiones técnicas con enlaces a ADRs, quality gates y scripts. Badges de CI y Codecov.
- **Licencia:** ninguna, lo que es razonable para un sitio personal (todos los derechos reservados).
- **Actividad:** 209 commits, último el 2026-11-07. 16 son autofixes de coderabbitai[bot].
- **Demuestra:** React 19 + TS + Vite, escena SVG/WebGL con `ogl` en un Web Worker con OffscreenCanvas, i18n, generación de CV PDF y OG en build, validación de contenido, Lighthouse CI, 52 archivos de test unitarios y E2E, ESLint estricto.
- **Pulido:** la homepage del repo apunta a una URL de Vercel (`portfolio-omega-one-50.vercel.app`) en vez de diegorangel.dev, y no tiene topics.

### game-dev-empire (privada)

- **Secretos:** ninguno. Los únicos aciertos son checksums de `src-tauri/Cargo.lock` y un comentario de CSS.
- **Datos personales:** ninguno.
- **README:** bueno, en inglés: cómo jugar, build del instalador de Windows, arquitectura en una frase por carpeta y límites conocidos de la alpha.
- **Licencia:** ninguna. **CI:** ninguno.
- **Actividad:** 149 commits entre 2026-07-29 y 2026-10-27; 141 del usuario y 7 autofixes de coderabbitai[bot].
- **Demuestra:** núcleo de simulación puro y determinista separado de la UI (`src/core` frente a `src/ui`), reglas de arquitectura con dependency-cruiser, Zustand, Tauri 2 con empaquetado NSIS/MSI, i18n en/es, 34 archivos de test (Vitest) y documentación extensa (`docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/GDD.md`, planes).
- **Limpieza menor:** quitar `scratch-golden.js` de la raíz; añadir licencia y un workflow de CI.

### live-chat (privada)

- **Secretos:** ninguno real. `apps/api/.env.example` (`ad1b61b`) y `.github/workflows/ci.yml` (`ad1b61b`) solo tienen la cadena de conexión de un Postgres local de desarrollo y un JWT secret de CI evidentemente ficticio. En `apps/web/e2e/critical-flow.spec.ts` (`c6b1b5e`) hay un token de QA de mentira.
- **Datos personales:** ninguno.
- **README:** completo pero en español. La numeración de pasos está desordenada (5, 7, 8, 6) y la sección "Siguiente paso sugerido" está obsoleta.
- **Licencia:** ninguna. **CI:** GitHub Actions (typecheck, migraciones, tests de API).
- **Actividad:** 8 commits entre 2026-03-13 y 2026-04-29, grandes y por tareas.
- **Demuestra:** monorepo pnpm (React 19 + Vite, Express + Socket.IO, tipos compartidos), Prisma/Postgres con migraciones, access token corto y refresh token rotatorio hasheado en cookie HttpOnly, idempotencia de mensajes, read receipts, presencia, Redis opcional, rate limiting, `/health` y `/readyz`, 13 archivos de test y E2E con Playwright.
- **Limpieza antes de publicar:** borrar `task002-test-output.txt` (~100 KB) y `tmp_chat_diff.txt` de la raíz, pasar el README a inglés y añadir licencia.

### wedding-invitation (pública)

- **Secretos:** ninguno. `src/pages/anfitrion.astro` (`93243b0`) tiene un fallback de contraseña de admin por defecto (`ADMIN_PASSWORD || "<default>"`). En una demo sin backend no expone nada, pero un revisor lo verá como mala práctica.
- **Datos personales:** ninguno detectado. El commit `c3d0514` marca explícitamente los datos como DEMO: novios ficticios, cuenta de regalo enmascarada y dirección genérica.
- **README:** solo el título. **Licencia:** ninguna.
- **Actividad:** 5 commits (2026-03-02 a 2026-03-03).
- **Demuestra:** Astro + TS, invitación mobile-first con RSVP por token, panel de anfitrión, subida de fotos y peticiones de canciones (todo como stubs en esta versión).
- **Limpieza antes de fijarlo:** escribir un README en inglés que explique que es la demo de un proyecto real; quitar `.astro/` (generado) del repo; quitar o parametrizar el fallback de contraseña; documentar el origen y los derechos de `public/audio/boda-civil.mp3` (~5 MB) y de `public/fotos/*.jpg`.

### Solidity (5 repos, privados, 2022)

Comunes a los cinco:

- **Secretos:** ninguno. Infura, Alchemy, Etherscan y la clave privada se leen de `process.env` en `hardhat.config.js`, y no se commiteó ningún `.env` en ningún commit. Los hex de 64 caracteres son el `keyHash` público de Chainlink y hashes de roles de OpenZeppelin en los tests.
- **README:** plantilla copiada entre repos con errores: lottery, swapper y marketplace se titulan "solidity-nft-drop", el propio nft-drop se describe como "Vote System", hay errores de ortografía en inglés y todos dicen "academic purposes only". Todos usan Rinkeby, una testnet ya cerrada.
- **Actividad:** de febrero a abril de 2022, hace más de 4 años. Hardhat + OpenZeppelin, Solidity 0.8.11.

| Repo | Commits | Licencia | Contenido | Estado |
|---|---|---|---|---|
| solidity-nft-marketplace | 37 | — | Marketplace upgradeable con AccessControl y comisión de admin, ERC1155, V2, ~67 KB de tests, `.solcover.js` | Terminado |
| solidity-nft-drop | 13 | — | ERC20/ERC721/ERC1155; el README enlaza contratos en Rinkeby y una colección en OpenSea testnets, enlaces ya muertos | Terminado |
| Solidity_Voting_System | 11 | — | Votación upgradeable V1→V2 con scripts de upgrade y tests | Terminado |
| solidity-no-loss-lottery | 11 | GPL-3.0 | Lotería sin pérdida con Chainlink VRF v2 (upgradeable) + Compound cETH, mocks y tests; "Used solidity-swapper as template" | Sin terminar |
| solidity-swapper | 8 | — | Swapper con Uniswap V2 y un intento con Paraswap | Roto según el último commit |

Si se quiere mostrar algo de Web3, nft-marketplace es el único candidato razonable: habría que reescribir el README en inglés, quitar Rinkeby y añadir licencia. Aun así resta foco a la narrativa de Full-Stack Lead.

### EmporiaEtImperia (privada)

- **Secretos:** `Config/DefaultEngine.ini` (`fced071`) tiene un `SecurityToken` de Unreal. Lo genera el editor por proyecto y no es una credencial de servicio, así que el riesgo es bajo.
- **Contenido:** el commit `fed8bf4` ("Fresh restart") dejó el HEAD con 8 archivos: configuración de Unreal, `.uproject` y LICENSE. Los commits anteriores son Blueprints y mapas `.uasset`/`.umap`, binarios que GitHub no puede mostrar.
- **README:** no tiene. **Licencia:** BSD-3-Clause.
- **Actividad:** 12 commits en junio de 2025.
- **Veredicto:** no apto. No hay nada legible que mostrar.

### boda-dicor (privada)

- **Datos personales y financieros en el historial (motivo del no apto):**
  - un email de Zelle de un tercero en `src/components/GiftInfo.astro`, commit `8749d4d`;
  - el email personal del autor como cuenta de Binance en el mismo archivo, commit `19f556b`, y un ID de Binance en `8749d4d`;
  - los nombres reales de los novios en `src/pages/index.astro` (varios commits, p. ej. `9199bb3`, `13b484f`) y la ubicación del evento en `5cf9c42`;
  - fotos reales de los novios en `public/fotos/carrusel-*.jpg`, con alt text que las identifica.
- **Secretos:** ninguna clave real. `.env.example` y `functions/.env.example` (`abcc019`) son placeholders. `src/pages/anfitrion.astro` (`e92def3`) tiene un fallback de contraseña de admin por defecto en código.
- **Otros:** 5 commits de copilot-swe-agent[bot]; `.astro/` generado está en el repo; no hay tests.
- **Veredicto:** no apto. La limpieza exigiría reescribir el historial, y wedding-invitation ya cumple ese papel.

### CONSORVEN (privada)

- **Credenciales en claro (motivo del no apto):** `functions/index.js`, commit `d64bf68` y **todavía en HEAD**, tiene una URL SMTP de Gmail con usuario y contraseña de una cuenta del cliente. Hay que rotar esa contraseña aunque el repo siga privado.
- **Otros datos del cliente:** una lista de emails de destinatarios del cliente en el mismo archivo (`d64bf68`); la configuración web de Firebase del proyecto del cliente en `src/environments/environment.ts` y `environment.prod.ts` (`8c19ff5`); la caché de Firebase Hosting `.firebase/hosting.*.cache`; GIFs y vídeos con la marca del servicio (decenas de MB de assets).
- **README:** no tiene. **Licencia:** ninguna.
- **Actividad:** 38 commits entre noviembre de 2020 y mayo de 2021.
- **Demuestra:** Ionic/Angular + Capacitor + Firebase (auth, Firestore, Functions), con accesibilidad (macrotipo, contraste) y videollamada. Es trabajo de cliente, que según el mapa se cuenta en el portfolio y no aquí.
- **Veredicto:** no apto.

### wocoon-plantilla (privada)

- **Origen:** es la plantilla comercial "Ionic 5 Full App – PRO Package 2.1.0" de Enappd (`package.json`: `"author": "Enappd Team"`). El `LICENCE.md` es un acuerdo de licencia de desarrollador que **prohíbe distribuir o revelar el código fuente** a terceros. Publicarlo incumpliría esa licencia.
- **Claves en el historial (commit `68e2921`, el commit inicial):** API keys de Google y Firebase en `GoogleService-Info.plist`, `google-services.json` y `src/environments/environment*.ts`; una clave publicable de Stripe en modo test en dos páginas del módulo `stripe-module`; un consumer secret de WooCommerce en `src/app/feature_modules/woocommerce/services/woo-commerce.service.ts`; IDs de OAuth de Google/Facebook y de AdMob en `package.json`. La mayoría parecen ser las credenciales de demo del vendedor.
- **Actividad:** 2 commits en noviembre de 2021. No hay trabajo propio visible.
- **Veredicto:** no apto.

### job-search (privada)

- **Origen:** el historial incluye entero el upstream [ai-job-search-dev/ai-job-search](https://github.com/ai-job-search-dev/ai-job-search) (MIT, © 2026 Mads Lorentzen, ~71k estrellas), fusionado en `6e0bdfb` ("Merge ai-job-search upstream framework"). Tiene unos 100 autores distintos y solo 11 de 446 commits son del usuario. No figura como fork en GitHub, así que publicarlo se leería como trabajo propio cuando no lo es.
- **Datos personales:** el CV propio en PDF (`documents/cv/`, `e1f3a19`), CV y carta adaptados a una postulación concreta (`cv/`, `cover_letters/`, `e1f3a19`), respuestas de formulario y resultado de esa postulación (`documents/applications/…`, `b2bf47d` / `7a6bac9`), `job_search_tracker.csv` y `job_scraper/seen_jobs.json` (`f4e0514`).
- **Secretos:** ninguno. Los aciertos fueron SHA-256 de fixtures de test y una URL de LinkedIn.
- **Veredicto:** no apto. Además, el mapa lo usa como fuente de verdad privada del perfil de candidato.

## Recomendaciones para el mapa

1. **Repos vitrina candidatos:** Portfolio y game-dev-empire, más live-chat tras la limpieza. wedding-invitation como secundario si se le escribe un README.
2. **No hacer públicos:** boda-dicor, CONSORVEN, wocoon-plantilla, job-search, EmporiaEtImperia, solidity-swapper y solidity-no-loss-lottery.
3. **Solidity:** decidir si se quiere una señal de Web3 en el perfil. Si se quiere, solo nft-marketplace y con README rehecho; si no, todos siguen privados.
4. **Acción de seguridad fuera del perfil:** rotar la contraseña de la cuenta SMTP que aparece en CONSORVEN (`functions/index.js`, `d64bf68`).
5. **Ticket de pulido** ("Pulido de cada repo vitrina" en el mapa): licencia, topics, homepage (Portfolio → diegorangel.dev), README en inglés (live-chat, wedding-invitation) y CI (game-dev-empire).
