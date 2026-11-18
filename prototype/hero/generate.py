# PROTOTYPE (throwaway): three hero variants for the profile README.
# Answers "Cómo se ve el hero" (Starloss/Starloss#9). Not production code.
# Run: python prototype/hero/generate.py  -> writes out/*.svg, then open index.html.
import base64
import math
import random
import re
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

W, H = 1280, 360

DAY = dict(page="#5ea8dc", primary="#2f6b4f", amber="#b86e00", text="#14231c",
           muted="#4b5d55", surface="#fafcf8")
NIGHT = dict(page="#050a1a", primary="#6fcf97", amber="#ffcf6e", text="#eef4f0",
             muted="#a9bcb2", surface="#08121b")

FONT_B64 = base64.b64encode((HERE / "space-grotesk-latin-700.woff2").read_bytes()).decode()
FONT_CSS = (
    "@font-face{font-family:'SG';font-weight:700;"
    f"src:url(data:font/woff2;base64,{FONT_B64}) format('woff2');}}"
)
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

# --- Ávila data (generated in the Portfolio repo from NASA SRTM) -------------
src = (HERE / "avila-data.ts").read_text(encoding="utf-8")
body = src[src.index("RIDGE_ANGLES"):src.index("LANDMARK_ANGLES")]
RIDGES = []
for chunk in re.findall(r"\[([^\[\]]+)\]", body):
    nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", chunk)]
    if len(nums) == 161:
        RIDGES.append(nums)
near, mid, crest = RIDGES
AZ0, AZ1 = -8.0, 72.0
LAND = {k: (float(az), float(el)) for k, az, el in
        re.findall(r"(\w+): \[([-\d.]+), ([-\d.]+)\]", src[src.index("LANDMARK_ANGLES"):])}


def ridge_points(angles, base, k, x0=0, width=W):
    pts = []
    for i, a in enumerate(angles):
        x = x0 + i / (len(angles) - 1) * width
        pts.append((x, base - max(a, -1) * k))
    return pts


def area_path(pts, bottom):
    d = f"M{pts[0][0]:.1f},{bottom} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts)
    return d + f" L{pts[-1][0]:.1f},{bottom} Z"


def line_path(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def az_to_x(az, x0=0, width=W):
    return x0 + (az - AZ0) / (AZ1 - AZ0) * width


def svg(inner, style="", w=W, h=H, label="Diego Rangel, Full-Stack Lead Developer"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}"><style>{FONT_CSS}{style}'
            "@media (prefers-reduced-motion: reduce){*{animation:none!important}}</style>"
            f"{inner}</svg>")


# --- Variant A: Panorama (full-bleed Caracas scene, day/night) ---------------
def variant_a(night):
    p = NIGHT if night else DAY
    rnd = random.Random(7)
    sky = ("<linearGradient id='sky' x1='0' y1='0' x2='0' y2='1'>"
           + ("<stop offset='0' stop-color='#050a1a'/><stop offset='1' stop-color='#1b2c5a'/>" if night
              else "<stop offset='0' stop-color='#3f8fcf'/><stop offset='1' stop-color='#bfe2f5'/>")
           + "</linearGradient>")
    crest_c = "#16263f" if night else "#4f8a74"
    mid_c = "#0f1b30" if night else "#2f6b4f"
    city_c = "#0a1222" if night else "#1f4a37"
    crest_pts = ridge_points(crest, 352, 24)
    mid_pts = ridge_points(mid, 330, 16)
    parts = [f"<defs>{sky}</defs><rect width='{W}' height='{H}' fill='url(#sky)'/>"]
    style = ""
    if night:
        stars = "".join(
            f"<circle class='tw t{i % 3}' cx='{rnd.uniform(0, W):.0f}' cy='{rnd.uniform(8, 170):.0f}' r='{rnd.choice([0.8, 1.1, 1.5])}' fill='#fff'/>"
            for i in range(70))
        parts.append(stars)
        parts.append("<circle cx='1150' cy='70' r='22' fill='#f4f1de'/><circle cx='1160' cy='63' r='20' fill='#050a1a' opacity='.9'/>")
        style += (".tw{animation:tw 3s ease-in-out infinite}.t1{animation-delay:1s}.t2{animation-delay:2s}"
                  "@keyframes tw{50%{opacity:.25}}")
    else:
        parts.append("<circle cx='1150' cy='78' r='30' fill='#ffe7a3'/>")
        clouds = "".join(
            f"<g class='cl' style='animation-duration:{d}s;animation-delay:-{o}s'>"
            f"<ellipse cx='0' cy='{y}' rx='{rx}' ry='{rx * .28:.0f}' fill='#fff' opacity='.75'/>"
            f"<ellipse cx='{rx * .45:.0f}' cy='{y - rx * .15:.0f}' rx='{rx * .55:.0f}' ry='{rx * .26:.0f}' fill='#fff' opacity='.75'/></g>"
            for y, rx, d, o in [(60, 70, 90, 10), (110, 50, 120, 70), (40, 40, 140, 30)])
        parts.append(clouds)
        style += ".cl{animation:drift linear infinite}@keyframes drift{from{transform:translateX(-200px)}to{transform:translateX(1480px)}}"
    parts.append(f"<path d='{area_path(crest_pts, H)}' fill='{crest_c}'/>")
    parts.append(f"<path d='{area_path(mid_pts, H)}' fill='{mid_c}'/>")
    # cable car: a cable from the lower to the upper station, cabin moving along it
    lx, ly = az_to_x(LAND["lowerStation"][0]), 352 - LAND["lowerStation"][1] * 24
    ux, uy = az_to_x(LAND["upperStation"][0]), 352 - LAND["upperStation"][1] * 24
    cable_c = "#a9bcb2" if night else "#14231c"
    parts.append(f"<path id='cable' d='M{lx:.0f},{ly:.0f} L{ux:.0f},{uy:.0f}' stroke='{cable_c}' stroke-width='1' opacity='.6'/>"
                 f"<rect x='-5' y='-4' width='10' height='8' rx='2' fill='{p['amber']}'>"
                 f"<animateMotion dur='18s' repeatCount='indefinite' keyPoints='0;1;0' keyTimes='0;.5;1' calcMode='linear'>"
                 "<mpath href='#cable'/></animateMotion></rect>")
    # city skyline
    x, bld, lights = 0, [], []
    while x < W:
        bw, bh = rnd.randint(14, 34), rnd.randint(18, 70)
        if 380 < x < 760:
            bh += rnd.randint(10, 40)
        bld.append(f"<rect x='{x}' y='{H - bh}' width='{bw}' height='{bh}'/>")
        if night:
            for wy in range(H - bh + 6, H - 4, 9):
                for wx in range(x + 3, x + bw - 3, 7):
                    if rnd.random() < .35:
                        lights.append(f"<rect class='w{rnd.randint(0, 2)}' x='{wx}' y='{wy}' width='3' height='3'/>")
        x += bw + rnd.randint(0, 4)
    parts.append(f"<g fill='{city_c}'>{''.join(bld)}</g>")
    if night:
        parts.append(f"<g fill='#ffcf6e'>{''.join(lights)}</g>")
        style += (".w0{animation:wl 7s steps(1) infinite}.w1{animation:wl 11s steps(1) infinite 3s}"
                  "@keyframes wl{60%{opacity:.15}}")
    parts.append(f"<text x='60' y='100' font-family='SG,sans-serif' font-weight='700' font-size='84' fill='{p['text']}'>Diego Rangel</text>"
                 f"<text x='63' y='146' font-family='SG,sans-serif' font-weight='700' font-size='36' fill='{p['text']}' opacity='.9'>Full-Stack Lead Developer</text>")
    return svg("".join(parts), style)


# --- Variant B: Terminal card (one SVG, works on any theme) ------------------
def variant_b():
    p = NIGHT
    lines = [
        [("const ", "#c792ea"), ("diego", p["text"]), (" = {", p["muted"])],
        [("  role", p["primary"]), (": ", p["muted"]), ('"Full-Stack Lead Developer"', p["amber"]), (",", p["muted"])],
        [("  leads", p["primary"]), (": ", p["muted"]), ('"10+ engineers, hands-on"', p["amber"]), (",", p["muted"])],
        [("  ships", p["primary"]), (": ", p["muted"]), ('["React", "TypeScript", "Node.js"]', p["amber"]), (",", p["muted"])],
        [("  basedIn", p["primary"]), (": ", p["muted"]), ('"Caracas, Venezuela · Remote"', p["amber"]), (",", p["muted"])],
        [("};", p["muted"])],
    ]
    cw = 13.2  # approx monospace advance at 22px
    rows, clips = [], []
    for i, segs in enumerate(lines):
        y = 126 + i * 34
        n = sum(len(t) for t, _ in segs)
        tspans = "".join(f"<tspan fill='{c}'>{t.replace('<', '&lt;')}</tspan>" for t, c in segs)
        clips.append(f"<clipPath id='c{i}'><rect class='ty' x='88' y='{y - 26}' height='34' width='{n * cw + 8:.0f}' "
                     f"style='animation-delay:{0.4 + i * 0.7:.1f}s;animation-timing-function:steps({n})'/></clipPath>")
        rows.append(f"<text x='92' y='{y}' font-family=\"{MONO}\" font-size='22' xml:space='preserve' clip-path='url(#c{i})'>{tspans}</text>")
    pts = ridge_points(crest, 352, 9, 640, 600)
    ridge = f"<path d='{line_path(pts)}' fill='none' stroke='{p['primary']}' stroke-width='1.5' opacity='.35'/>"
    style = (".ty{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:type .6s forwards}"
             "@keyframes type{to{transform:scaleX(1)}}"
             ".cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}")
    inner = (f"<defs>{''.join(clips)}</defs>"
             f"<rect x='24' y='12' width='{W - 48}' height='{H - 24}' rx='18' fill='{p['surface']}' stroke='{p['primary']}' stroke-opacity='.35'/>"
             f"<circle cx='60' cy='46' r='7' fill='#ff5f57'/><circle cx='84' cy='46' r='7' fill='#febc2e'/><circle cx='108' cy='46' r='7' fill='#28c840'/>"
             f"<text x='{W / 2}' y='52' text-anchor='middle' font-family=\"{MONO}\" font-size='16' fill='{p['muted']}'>diego-rangel.ts</text>"
             f"<line x1='24' y1='76' x2='{W - 24}' y2='76' stroke='{p['primary']}' stroke-opacity='.2'/>"
             f"{ridge}{''.join(rows)}"
             f"<rect class='cur' x='130' y='{126 + 5 * 34 - 22}' width='12' height='26' fill='{p['primary']}'/>"
             f"<text x='{W - 72}' y='{H - 44}' text-anchor='end' font-family='SG,sans-serif' font-weight='700' font-size='40' fill='{p['text']}'>Diego Rangel</text>")
    return svg(inner, style)


# --- Variant C: Contour (typographic, self-drawing Ávila line, day/night) ----
def variant_c(night):
    p = NIGHT if night else DAY
    bg = p["page"] if night else p["surface"]
    pts = ridge_points(crest, 362, 16)
    d = line_path(pts)
    lx, ly = az_to_x(LAND["lowerStation"][0]), 362 - LAND["lowerStation"][1] * 16
    ux, uy = az_to_x(LAND["upperStation"][0]), 362 - LAND["upperStation"][1] * 16
    style = (".ridge{stroke-dasharray:3000;stroke-dashoffset:3000;animation:draw 3.5s ease-out forwards}"
             "@keyframes draw{to{stroke-dashoffset:0}}"
             ".fade{opacity:0;animation:fade 1s 3.2s forwards}@keyframes fade{to{opacity:1}}")
    inner = (f"<rect width='{W}' height='{H}' rx='16' fill='{bg}'/>"
             f"<text x='{W / 2}' y='138' text-anchor='middle' font-family='SG,sans-serif' font-weight='700' font-size='88' fill='{p['text']}'>Diego Rangel</text>"
             f"<text x='{W / 2}' y='184' text-anchor='middle' font-family='SG,sans-serif' font-weight='700' font-size='22' letter-spacing='6' fill='{p['primary']}'>FULL-STACK LEAD DEVELOPER</text>"
             f"<path class='ridge' d='{d}' fill='none' stroke='{p['primary']}' stroke-width='2.5' stroke-linejoin='round'/>"
             f"<g class='fade'><path id='cab' d='M{lx:.0f},{ly:.0f} L{ux:.0f},{uy:.0f}' stroke='{p['muted']}' stroke-width='1' stroke-dasharray='4 4'/>"
             f"<circle r='5' fill='{p['amber']}'><animateMotion dur='16s' repeatCount='indefinite' keyPoints='0;1;0' keyTimes='0;.5;1' calcMode='linear'><mpath href='#cab'/></animateMotion></circle>"
             f"<text x='{W - 40}' y='{H - 22}' text-anchor='end' font-family='SG,sans-serif' font-weight='700' font-size='14' letter-spacing='2' fill='{p['muted']}'>EL ÁVILA · CARACAS</text></g>")
    return svg(inner, style)


files = {
    "a-light.svg": variant_a(False), "a-dark.svg": variant_a(True),
    "b.svg": variant_b(),
    "c-light.svg": variant_c(False), "c-dark.svg": variant_c(True),
}
for name, content in files.items():
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"{name}: {len(content) / 1024:.0f} KB")
