# Widgets dinámicos para el README de perfil: qué es fiable (nov 2026) y cómo alojarlo

Ticket: [#5](https://github.com/Starloss/Starloss/issues/5) · Mapa: [#3](https://github.com/Starloss/Starloss/issues/3) · Fecha de la investigación: 2026-11-12

Contexto: casi todo el trabajo de Starloss está en repos privados (3 repos públicos). El perfil apunta a recruiters y quiere 1–2 elementos dinámicos sobrios, no un dashboard.

Fuentes: READMEs, issues, PRs y releases de cada proyecto (vía `gh api`), GitHub Docs, y una comprobación HTTP en vivo de cada instancia pública hecha el 2026-11-12. Lo que es opinión o recomendación está marcado como tal.

## TL;DR

- **Lo más fiable hoy es "SVG generado por una GitHub Action y commiteado en el repo".** Ya no depende de que alguien pague Vercel por ti. Lo recomiendan explícitamente github-readme-stats/GitHub Stats Extended, streak-stats y snk.
- **La instancia pública original `github-readme-stats.vercel.app` está muerta**: responde `503 DEPLOYMENT_PAUSED` (comprobado el 2026-11-12), y el repo `anuraghazra/github-readme-stats` se declaró **sin mantenimiento** (junio de 2026). Su sucesor es **GitHub Stats Extended** (`stats-organization`).
- **La instancia pública de github-readme-activity-graph también está caída** (`402 DEPLOYMENT_DISABLED`). **lowlighter/metrics** no recibe commits en `master` desde diciembre de 2023.
- **Contribuciones privadas:** todo lo que lee el *contribution calendar* (snake, streak) las cuenta como números anónimos si activas "Private contributions" en tu perfil, sin token extra. Las tarjetas de stats y top-langs necesitan un **PAT classic (`repo`, `read:user`)** guardado como secret, o bien darle acceso OAuth "Private Access" a la instancia pública de GitHub Stats Extended.
- **Recomendación para Starloss (opinión):** (1) la tarjeta **top-langs** de GitHub Stats Extended, generada con su Action y un PAT, porque es la única forma de que se vea el stack real de los repos privados; y, de forma opcional, (2) el **snake** de Platane/snk, que no necesita ningún secret. Evitar streak, que expone los huecos, y metrics.

## 1. Estado de cada proyecto (al 2026-11-12)

| Widget / proyecto | Mantenimiento | Instancia pública | Formas de alojarlo |
|---|---|---|---|
| **github-readme-stats** (`anuraghazra`) | **Sin mantenimiento.** Aviso CAUTION en el README desde el PR [#4895](https://github.com/anuraghazra/github-readme-stats/pull/4895) (mergeado el 2026-06-30) | `github-readme-stats.vercel.app` → **503 `DEPLOYMENT_PAUSED`** | Ninguna recomendada. Usar el sucesor |
| **GitHub Stats Extended** (`stats-organization/github-stats-extended`), sucesor (stats, top-langs, pin, gist, wakatime) | **Activo**: v2.3.0 (2026-11-04), commits el 2026-11-08 | `github-stats-extended.vercel.app` → 200 OK | Instancia pública · Action ([`stats-organization/github-readme-stats-action@v2`](https://github.com/stats-organization/github-readme-stats-action), v2.1.0 del 2026-09-23) · self-host en Vercel (preset Container) o Docker |
| **github-readme-streak-stats** (`DenverCoder1`) | **Activo**: v1.8.2 (2026-11-05) | `streak-stats.demolab.com` → 200 OK (con quejas puntuales de caídas, p. ej. [#865](https://github.com/DenverCoder1/github-readme-streak-stats/issues/865)) | Instancia pública · Action `DenverCoder1/github-readme-streak-stats@v1` · self-host (PHP en Vercel/Heroku/Docker) |
| **github-readme-activity-graph** (`Ashutosh00710`) | Poco activo (último commit 2026-05-17). Sin respuesta del mantenedor a las caídas | `github-readme-activity-graph.vercel.app` → **402 `DEPLOYMENT_DISABLED`**. Hay issues abiertas desde agosto de 2026 ([#259](https://github.com/Ashutosh00710/github-readme-activity-graph/issues/259), [#261](https://github.com/Ashutosh00710/github-readme-activity-graph/issues/261), [#273](https://github.com/Ashutosh00710/github-readme-activity-graph/issues/273)) | Solo self-host (Vercel/Replit con `TOKEN`). No tiene Action oficial |
| **snk** (`Platane/snk`, snake) | **Activo** y estable: v3.5.0 (2026-04-25), 3 issues abiertas | No existe ni hace falta | Solo Action (`Platane/snk@v3` o `Platane/snk/svg-only@v3`). El SVG va a una rama `output` o se commitea |
| **metrics** (`lowlighter/metrics`) | **De facto abandonado**: última release v3.34 (2023-09), último commit en `master` en 2023-12. Solo entran ramas de dependabot. Hay plugins rotos abiertos ([#1694](https://github.com/lowlighter/metrics/issues/1694) languages, [#1706](https://github.com/lowlighter/metrics/issues/1706)), y un usuario señala que el proyecto está "currently inactive" ([#1672](https://github.com/lowlighter/metrics/issues/1672)) | `metrics.lecoq.io` responde 200, pero sin mantenimiento | Action (pesada, muchos plugins) |

### Qué pasó con la instancia pública de github-readme-stats

- El README antiguo ya advertía que la instancia pública era *best-effort* y "can be unreliable due to rate limits and traffic spikes" ([#1471](https://github.com/anuraghazra/github-readme-stats/issues/1471)). También recomendaba hacer self-host o usar la Action ([README, "Important Notices" y "Deploy on your own"](https://github.com/anuraghazra/github-readme-stats#readme)).
- En enero de 2026 el despliegue pasó a devolver `503 DEPLOYMENT_PAUSED` ([#4737](https://github.com/anuraghazra/github-readme-stats/issues/4737)). Según el mantenedor @rickstaa, uno de los motivos de la pausa fue que Vercel dejó de patrocinar el proyecto y que sus precios son altos ([comentario en #4737](https://github.com/anuraghazra/github-readme-stats/issues/4737), que remite a [#3851](https://github.com/anuraghazra/github-readme-stats/issues/3851)). El mismo hilo explica que el mantenimiento se trasladó a la organización `stats-organization`.
- El 2026-01-18 se documentó la GitHub Action como método recomendado ([PR #4716](https://github.com/anuraghazra/github-readme-stats/pull/4716), [#4748](https://github.com/anuraghazra/github-readme-stats/issues/4748)). El 2026-06-30 el README se marcó como "no longer maintained" y redirige a GitHub Stats Extended o a la Action ([PR #4895](https://github.com/anuraghazra/github-readme-stats/pull/4895)).
- Comprobación en vivo (2026-11-12): `GET https://github-readme-stats.vercel.app/api?username=Starloss` → `503`, cuerpo `DEPLOYMENT_PAUSED`.
- Sobre la instancia pública del sucesor, la documentación dice: "We cache generated cards for a few hours or days to avoid potential rate-limiting in the GitHub API or on Vercel", y que precalcula y cachea las tarjetas de forma proactiva ([docs/deploy](https://github-stats-extended.vercel.app/frontend/docs/deploy/), [docs/fork](https://github-stats-extended.vercel.app/frontend/docs/fork/)). No publica ningún compromiso de disponibilidad. Funciona, pero sigue siendo un Vercel que paga un tercero, igual que el que se cayó.

## 2. Modelos de alojamiento

| Modelo | Fiabilidad | Frescura | Coste de mantenimiento |
|---|---|---|---|
| **Instancia pública** (URL en `<img>`) | La más baja. Dos de las cuatro instancias populares están caídas hoy (github-readme-stats y activity-graph) | Caché de horas a días | Cero hasta que se cae. Entonces la imagen aparece rota en tu perfil |
| **Self-host en Vercel** (fork + PAT en variables de entorno) | Media-alta, y depende de tu cuenta de Vercel (límites del plan gratuito, timeouts, redeploys) | La mejor (caché configurable; en GSE el `CACHE_SECONDS` por defecto es de 10 h) | Un proyecto de Vercel, un PAT que rotar y redeploys al cambiar variables de entorno ([docs/deploy](https://github-stats-extended.vercel.app/frontend/docs/deploy/)) |
| **GitHub Action → SVG commiteado** | **La más alta**: el README sirve un archivo del propio repo. Si la Action falla, se queda el último SVG bueno | Diaria (cron) | Un workflow con `contents: write`. Si se quieren datos privados, un PAT como secret. Ver la nota sobre el cron de 60 días |

**Nota sobre el cron (GitHub Docs):** "In a public repository, scheduled workflows are automatically disabled when no repository activity has occurred in 60 days" ([Disabling and enabling a workflow](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/disabling-and-enabling-a-workflow)). Los workflows de ejemplo hacen `git commit ... || exit 0`, así que si el SVG no cambia no hay commit y el repo puede quedarse "inactivo". En la práctica las tarjetas cambian casi a diario y esto no debería pasar. Aun así, conviene revisarlo si el perfil se queda quieto.

**Recomendación (opinión):** usar la Action para todo. La instancia pública no es una opción para un perfil dirigido a recruiters, porque una imagen rota da peor impresión que no tener widget.

## 3. Cómo cuenta cada uno las contribuciones privadas

Hay dos familias de datos:

**A) Los que leen el contribution calendar (snake, streak, activity graph).** El calendario muestra contribuciones privadas como recuentos diarios anónimos **solo si el usuario activa "Private contributions"** en la configuración de contribuciones de su perfil. Por defecto solo muestra actividad pública ([GitHub Docs: Manage visibility settings for private contributions](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/manage-visibility-settings-for-private-contributions-and-achievements), [Contributions on your profile](https://docs.github.com/en/account-and-profile/concepts/contributions-on-your-profile)).

- **snk:** consulta `contributionsCollection.contributionCalendar` por GraphQL con el token de la Action ([`packages/github-user-contribution/index.ts`](https://github.com/Platane/snk/blob/main/packages/github-user-contribution/index.ts)). Con el ajuste del perfil activado, el `GITHUB_TOKEN` por defecto basta. **Sin PAT.**
- **streak-stats:** "To include contributions in private repositories, turn on the setting for 'Private contributions' from the dropdown menu above the contribution graph on your profile page" ([README, "How these stats are calculated"](https://github.com/DenverCoder1/github-readme-streak-stats#readme)). Para la Action, el README también sugiere un PAT; una sección dice "no scopes required" y otra pide el scope `repo`, así que es inconsistente.
- **activity-graph:** para ver repos privados en un self-host pide un PAT con `repo` ([README](https://github.com/Ashutosh00710/github-readme-activity-graph#readme)).

**B) Los que agregan datos por repositorio (tarjetas stats y top-langs de GitHub Stats Extended / github-readme-stats).** Por defecto solo cuentan repos públicos: "By default, the stats card only shows statistics like stars, commits, and pull requests from public repositories" ([docs/cards/stats](https://github-stats-extended.vercel.app/frontend/docs/cards/stats/)). Lo mismo vale para top-langs. Hay tres formas de incluir los privados:

1. **Action + PAT classic** con scopes `repo` y `read:user`, guardado como secret ([README de la Action, input `token`](https://github.com/stats-organization/github-readme-stats-action#inputs)). Con el `GITHUB_TOKEN` por defecto solo se ven datos públicos. Un PAT fine-grained "limits the scope of commits to public repositories only" ([docs/deploy](https://github-stats-extended.vercel.app/frontend/docs/deploy/)), así que **hace falta el classic**.
2. **Self-host** con `PAT_1` (mismos scopes). Se pueden ocultar nombres de repos privados con `EXCLUDE_REPO` sin exponerlos en la URL ([docs/deploy](https://github-stats-extended.vercel.app/frontend/docs/deploy/)).
3. **Instancia pública de GitHub Stats Extended con "GitHub Private Access"**: haces login OAuth en su wizard y "You no longer have to deploy your own instance for that" ([docs/fork](https://github-stats-extended.vercel.app/frontend/docs/fork/)). El coste es darle a un servicio de terceros acceso a tus datos privados, y depende de su Vercel.

Para Starloss esto importa mucho. Con 3 repos públicos, una tarjeta stats o top-langs sin datos privados enseñaría un perfil casi vacío o engañoso. **Si se usa top-langs, tiene que ser con datos privados.**

## 4. Tema claro/oscuro

GitHub soporta `<picture>` con `prefers-color-scheme` para servir una imagen distinta según el tema del visitante ([GitHub Docs: Quickstart for writing on GitHub](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github)). Los sufijos `#gh-dark-mode-only` / `#gh-light-mode-only` siguen apareciendo en los READMEs de los proyectos, pero `<picture>` es la vía documentada.

| Widget | Soporte |
|---|---|
| GitHub Stats Extended | Temas `light_github` / `dark_github`, que imitan la UI de GitHub, más variantes `_repocard`. Hay que generar dos SVG y usar `<picture>` ([README](https://github.com/stats-organization/github-stats-extended#readme), [docs/fork](https://github-stats-extended.vercel.app/frontend/docs/fork/)). También existe `theme=transparent` (un solo SVG que funciona razonablemente en ambos temas) |
| snk | Paletas `github`, `github-light` y `github-dark`. Una sola ejecución genera ambos archivos (`dist/github-snake.svg` y `dist/github-snake-dark.svg?palette=github-dark`) para usarlos con `<picture>` ([README](https://github.com/Platane/snk#readme)) |
| streak-stats | `theme=dark`, etc. Dos SVG más `<picture>`. Cada variante es un step más de la Action |
| activity-graph | Temas como `react-dark` y `github-compact`. Dos imágenes más `<picture>` |

## 5. Coste de mantenimiento por opción (con Action)

| Opción | Secrets | Workflow | Riesgo |
|---|---|---|---|
| snk (snake) | Ninguno (`GITHUB_TOKEN`) | Cron diario y push a la rama `output` o commit en `main` | Muy bajo. Solo hay que activar "Private contributions" en el perfil |
| GSE top-langs / stats | **PAT classic `repo` + `read:user`** como secret (p. ej. `GH_STATS_PAT`) | Cron diario, `contents: write`, un step por variante de tema | Medio: el PAT tiene scope amplio y caduca (rotación). Si falla, `fail_on_error: true` evita commitear una tarjeta "Something went wrong" ([inputs de la Action](https://github.com/stats-organization/github-readme-stats-action#inputs)) |
| streak | Ninguno si el perfil muestra contribuciones privadas. Opcionalmente un PAT | Cron diario | Bajo |
| activity-graph | Self-host en Vercel más PAT `repo` | — | Medio-alto (sin Action oficial, mantenimiento escaso) |
| metrics | PAT, más tokens extra por plugin | Action pesada | Alto (sin mantenimiento) |

## 6. Recomendación para Starloss (opinión, basada en lo anterior)

Objetivo: 1–2 elementos sobrios, de cara a recruiters, con el trabajo en repos privados.

1. **Top languages (GitHub Stats Extended) generado con `stats-organization/github-readme-stats-action@v2` y un PAT classic.** Es el único widget que comunica *qué stack usas* a partir del código privado. Conviene `layout=compact`, `langs_count` entre 6 y 8, `hide_title` o un título propio, variantes `light_github` y `dark_github` con `<picture>`, y `exclude_repo`/`hide` para quitar ruido (por ejemplo HTML/CSS de plantillas).
2. **(Opcional) Snake de Platane/snk.** No necesita secrets, es la Action más estable del grupo y tiene modo oscuro nativo. Requiere activar "Private contributions" en el perfil para no salir "vacío". Ojo: el perfil de GitHub **ya muestra el calendario de contribuciones** debajo del README, así que el snake lo duplica en clave lúdica. Para un público de recruiters puede sobrar: es una decisión de gusto.
3. **Evitar:**
   - Cualquier URL a `github-readme-stats.vercel.app` (caída).
   - activity-graph (instancia caída y sin Action).
   - metrics (abandonado).
   - Racha (streak), porque pone el foco en días sin contribuir. En perfiles con mucha actividad en el trabajo fuera de GitHub puede jugar en contra.
   - La tarjeta stats con número de estrellas/commits, porque con 3 repos públicos las estrellas serán bajas y el rank puede quedar pobre. Si se usa, hacerlo con PAT y ocultando `stars`/rank.

## Preguntas abiertas

- ¿Está ya activado "Private contributions" en el perfil de Starloss? Es requisito para el snake y la racha.
- ¿Se acepta tener un PAT classic con scope `repo` como secret del repo público del perfil? Los secrets no se exponen a forks ni a PRs externos, pero el scope es amplio. La alternativa es el OAuth "Private Access" de la instancia pública de GSE, que tiene menos mantenimiento pero vuelve a depender de un tercero.
