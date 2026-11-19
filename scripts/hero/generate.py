# Generates the profile hero (day/night) and the social preview cards of the showcase repos.
# The scene is Caracas under El Ávila, drawn from the SRTM ridge data the Portfolio uses.
# Run: python scripts/hero/generate.py   (PNG previews also need Chrome, see render_png)
import base64
import random
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
ASSETS = ROOT / "assets"

DAY = dict(text="#14231c", amber="#b86e00", crest="#4f8a74", mid="#2f6b4f", city="#1f4a37",
           cable="#14231c", sky=("#3f8fcf", "#bfe2f5"))
NIGHT = dict(text="#eef4f0", amber="#ffcf6e", crest="#16263f", mid="#0f1b30", city="#0a1222",
             cable="#a9bcb2", sky=("#050a1a", "#1b2c5a"))

FONT_B64 = base64.b64encode((HERE / "space-grotesk-latin-700.woff2").read_bytes()).decode()
FONT_CSS = ("@font-face{font-family:'SG';font-weight:700;"
            f"src:url(data:font/woff2;base64,{FONT_B64}) format('woff2');}}")

# Ávila ridges (elevation angles every 0.5° of azimuth) and landmarks, from the Portfolio repo.
_src = (HERE / "avila-data.ts").read_text(encoding="utf-8")
_ridges = [[float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", chunk)]
           for chunk in re.findall(r"\[([^\[\]]+)\]", _src[_src.index("RIDGE_ANGLES"):_src.index("LANDMARK_ANGLES")])]
_, MID, CREST = [r for r in _ridges if len(r) == 161]
AZ0, AZ1 = -8.0, 72.0
LAND = {k: (float(az), float(el)) for k, az, el in
        re.findall(r"(\w+): \[([-\d.]+), ([-\d.]+)\]", _src[_src.index("LANDMARK_ANGLES"):])}


def area_path(angles, w, base, k, bottom):
    pts = [(i / (len(angles) - 1) * w, base - max(a, -1) * k) for i, a in enumerate(angles)]
    return (f"M0,{bottom} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts) + f" L{w},{bottom} Z")


def scene(night, w, h, text, animated=True, label="Diego Rangel, Full-Stack Lead Developer"):
    p = NIGHT if night else DAY
    rnd = random.Random(7)
    base = h - 8
    parts = [f"<defs><linearGradient id='sky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='{p['sky'][0]}'/>"
             f"<stop offset='1' stop-color='{p['sky'][1]}'/></linearGradient></defs>"
             f"<rect width='{w}' height='{h}' fill='url(#sky)'/>"]
    style = ""
    if night:
        parts.append("".join(
            f"<circle class='tw t{i % 3}' cx='{rnd.uniform(0, w):.0f}' cy='{rnd.uniform(8, base - 182):.0f}' "
            f"r='{rnd.choice([0.8, 1.1, 1.5])}' fill='#fff'/>" for i in range(int(70 * h / 360))))
        parts.append(f"<circle cx='{w - 130}' cy='70' r='22' fill='#f4f1de'/>"
                     f"<circle cx='{w - 120}' cy='63' r='20' fill='{p['sky'][0]}' opacity='.9'/>")
        style += (".tw{animation:tw 3s ease-in-out infinite}.t1{animation-delay:1s}.t2{animation-delay:2s}"
                  "@keyframes tw{50%{opacity:.25}}")
    else:
        parts.append(f"<circle cx='{w - 130}' cy='78' r='30' fill='#ffe7a3'/>")
        parts.append("".join(
            f"<g class='cl' style='animation-duration:{d}s;animation-delay:-{o}s'>"
            f"<ellipse cx='0' cy='{y}' rx='{rx}' ry='{rx * .28:.0f}' fill='#fff' opacity='.75'/>"
            f"<ellipse cx='{rx * .45:.0f}' cy='{y - rx * .15:.0f}' rx='{rx * .55:.0f}' ry='{rx * .26:.0f}' fill='#fff' opacity='.75'/></g>"
            for y, rx, d, o in [(60, 70, 90, 10), (110, 50, 120, 70), (40, 40, 140, 30)]))
        style += (".cl{animation:drift linear infinite}"
                  f"@keyframes drift{{from{{transform:translateX(-200px)}}to{{transform:translateX({w + 200}px)}}}}")
    parts.append(f"<path d='{area_path(CREST, w, base, 24, h)}' fill='{p['crest']}'/>")
    parts.append(f"<path d='{area_path(MID, w, base - 22, 16, h)}' fill='{p['mid']}'/>")

    # Cable car between its lower and upper stations, the cabin going up and down.
    def station(name):
        az, el = LAND[name]
        return (az - AZ0) / (AZ1 - AZ0) * w, base - el * 24
    (lx, ly), (ux, uy) = station("lowerStation"), station("upperStation")
    parts.append(f"<path d='M{lx:.0f},{ly:.0f} L{ux:.0f},{uy:.0f}' stroke='{p['cable']}' stroke-width='1' opacity='.6'/>"
                 f"<rect class='cab' x='-5' y='-4' width='10' height='8' rx='2' fill='{p['amber']}' "
                 f"transform='translate({lx:.0f} {ly:.0f})'/>")
    # CSS rather than SMIL, so the reduced-motion rule below also stops the cabin.
    style += (".cab{animation:cab 18s linear infinite}"
              f"@keyframes cab{{0%,100%{{transform:translate({lx:.0f}px,{ly:.0f}px)}}50%{{transform:translate({ux:.0f}px,{uy:.0f}px)}}}}")

    x, buildings, lights = 0, [], []
    while x < w:
        bw, bh = rnd.randint(14, 34), rnd.randint(18, 70)
        if 0.3 * w < x < 0.6 * w:
            bh += rnd.randint(10, 40)
        buildings.append(f"<rect x='{x}' y='{h - bh}' width='{bw}' height='{bh}'/>")
        if night:
            for wy in range(h - bh + 6, h - 4, 9):
                for wx in range(x + 3, x + bw - 3, 7):
                    if rnd.random() < .35:
                        lights.append(f"<rect class='w{rnd.randint(0, 2)}' x='{wx}' y='{wy}' width='3' height='3'/>")
        x += bw + rnd.randint(0, 4)
    parts.append(f"<g fill='{p['city']}'>{''.join(buildings)}</g>")
    if night:
        parts.append(f"<g fill='#ffcf6e'>{''.join(lights)}</g>")
        style += (".w0{animation:wl 7s steps(1) infinite}.w1{animation:wl 11s steps(1) infinite 3s}"
                  "@keyframes wl{60%{opacity:.15}}")
    parts.append(text(p))
    if not animated:
        style = ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}"><style>{FONT_CSS}{style}'
            "@media (prefers-reduced-motion: reduce){*{animation:none!important}}</style>"
            f"{''.join(parts)}</svg>")


def hero_text(p):
    return (f"<text x='60' y='100' font-family='SG,sans-serif' font-weight='700' font-size='84' fill='{p['text']}'>Diego Rangel</text>"
            f"<text x='63' y='146' font-family='SG,sans-serif' font-weight='700' font-size='36' fill='{p['text']}' opacity='.9'>"
            "Full-Stack Lead Developer</text>")


def card_text(name, lines):
    def text(p):
        out = [f"<text x='72' y='150' font-family='SG,sans-serif' font-weight='700' font-size='96' fill='{p['text']}'>{name}</text>"]
        out += [f"<text x='76' y='{222 + i * 46}' font-family='SG,sans-serif' font-weight='700' font-size='34' "
                f"fill='{p['text']}' opacity='.88'>{line}</text>" for i, line in enumerate(lines)]
        return "".join(out)
    return text


# Social preview cards: repo name and its GitHub description, wrapped by hand.
CARDS = {
    "Portfolio": ["Bilingual portfolio of a Full-Stack Lead Developer:",
                  "React 19, TypeScript and an animated SVG/WebGL",
                  "scene of Caracas."],
    "live-chat": ["Real-time chat monorepo: React, Express, Socket.IO,",
                  "Prisma/PostgreSQL and Redis, with rotating",
                  "refresh tokens and Playwright E2E."],
    "wedding-invitation": ["Mobile-first wedding invitation with token-based",
                           "RSVP and a host dashboard, built with Astro."],
}


def render_png(svg_path, png_path, w, h):
    """Rasterizes an SVG with headless Chrome (the cards are uploaded as PNG)."""
    chrome = next((c for c in (shutil.which("chrome"), shutil.which("google-chrome"),
                               r"C:\Program Files\Google\Chrome\Application\chrome.exe") if c and Path(c).exists()), None)
    if not chrome:
        print(f"skip {png_path.name}: Chrome not found, kept {svg_path.name}")
        return False
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={profile}",
                        f"--window-size={w},{h}", f"--screenshot={png_path}", svg_path.resolve().as_uri()],
                       check=True, capture_output=True)
    return True


def main():
    (ASSETS / "social").mkdir(parents=True, exist_ok=True)
    for name, night in (("hero-day.svg", False), ("hero-night.svg", True)):
        (ASSETS / name).write_text(scene(night, 1280, 360, hero_text), encoding="utf-8")
    for repo, lines in CARDS.items():
        svg_path = ASSETS / "social" / f"{repo}.svg"
        svg_path.write_text(scene(True, 1280, 640, card_text(repo, lines), animated=False,
                                  label=f"{repo} by Diego Rangel"), encoding="utf-8")
        if render_png(svg_path, svg_path.with_suffix(".png"), 1280, 640):
            svg_path.unlink()
    for f in sorted(ASSETS.rglob("*.*")):
        print(f"{f.relative_to(ROOT)}: {f.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
