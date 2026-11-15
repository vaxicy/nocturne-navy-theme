#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nocturne Navy Theme — flat vector logo candidates (SVG, headless Chromium).

Style follows the most recent direction: **flat** — solid fills only, no gradients,
no highlights, no outlines. Two or three shapes per mark, each large enough to
still read at 32px.

The palette is a single navy→indigo→lilac ramp plus cream, so the marks use cream
and lilac for their shapes and let navy stay in the background: that way an icon
reads on a cream page and on a navy toolbar alike.

Playwright screenshots each SVG cell with omit_background=True (true
transparency); PIL only composes the contact sheets, the inline strip and the
official logo/logo.png exported from SELECTED.

Colours come from manifest.json. Change SELECTED and re-run; never hand-copy PNGs.
"""
import json
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

SIZE = 128
CELL = 512
PREVIEW = 256
SELECTED = "05"
CAND_DIR = Path("logo/candidates")
LOGO_OUT = Path("logo/logo.png")

with open("manifest.json", "r", encoding="utf-8") as f:
    _m = json.load(f)
_C, _P = _m["theme"]["colors"], _m["theme"]["properties"]


def hx(vals):
    return "#%02X%02X%02X" % tuple(vals)


NAVY = hx(_C["frame"])                             # #00105B
CREAM = hx(_C["ntp_background"])                   # #FCF9EC
INK = hx(_C["ntp_text"])                           # #00105B
INDIGO = hx(_C["button_background_secondary"])     # #6061B6
LILAC = hx(_C["button_background"])                # #C9B5E0
LINK = hx(_C["ntp_link"])                          # #3F4090


def svg_open(body, defs=""):
    # 0.94 about the centre keeps every mark inside the safe box
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s<g transform="translate(128 128) scale(0.94) '
            'translate(-128 -128)">%s</g></svg>' % (CELL, CELL, defs, body))


def star(cx, cy, r_out, r_in, fill, opacity=1.0):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(-90 + i * 36)
        pts.append("%.1f %.1f" % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return ('<path d="M%s Z" fill="%s" fill-opacity="%.2f"/>'
            % (" L".join(pts), fill, opacity))


def circle(cx, cy, r, fill):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, fill)


def crescent(mask_id, cx, cy, r, offset, fill):
    """Crescent built from a mask (works on a transparent canvas)."""
    defs = ('<mask id="%s"><circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff"/>'
            '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#000"/></mask>'
            % (mask_id, cx, cy, r, cx + offset, cy - offset * 0.55, r * 0.86))
    body = ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" mask="url(#%s)"/>'
            % (cx, cy, r, fill, mask_id))
    return defs, body


# ------------------------------------------------------------------ candidates
d1, b1 = crescent("m1", 122, 118, 84, 40, CREAM)
SVG_01 = svg_open("""
<defs>%s</defs>
%s
%s
%s
%s
%s
""" % (d1, circle(120, 122, 92, NAVY), b1,
       star(196, 62, 15, 6.5, LILAC),
       star(210, 148, 10, 4.2, LILAC, .9),
       star(178, 208, 8, 3.4, LILAC, .75)))

SVG_02 = svg_open("""
%s
%s
%s
%s
<path d="M70 176 L118 128 L166 158 L196 104" fill="none" stroke="%s"
      stroke-width="4" stroke-opacity=".55" stroke-linecap="round"/>
%s
%s
""" % (circle(70, 176, 13, CREAM), circle(118, 128, 10, LILAC),
       circle(166, 158, 9, CREAM), circle(196, 104, 14, LILAC),
       INDIGO,
       star(128, 208, 12, 5.0, LILAC, .8),
       circle(84, 92, 7, CREAM)))

SVG_03 = svg_open("""
%s
<defs>%s</defs>
%s
%s
""" % (circle(128, 128, 96, NAVY),
       crescent("m3", 118, 122, 62, 30, CREAM)[0],
       crescent("m3", 118, 122, 62, 30, CREAM)[1],
       circle(176, 78, 13, LILAC)))

SVG_04 = svg_open("""
%s
%s
%s
%s
%s
""" % (circle(128, 128, 96, NAVY),
       '<rect x="96" y="72" width="11" height="104" rx="4" fill="%s"/>' % CREAM,
       '<ellipse cx="84" cy="182" rx="30" ry="22" fill="%s"/>' % CREAM,
       '<path d="M107 74 q46 -10 44 34 q-2 26 -30 22 q-12 -2 -14 -14" fill="%s"/>' % LILAC,
       circle(150, 196, 15, LILAC)))

SVG_05 = svg_open("""
%s
%s
%s
%s
%s
""" % (circle(128, 112, 84, NAVY),
       '<path d="M44 168 q28 -22 56 0 q28 22 56 0 q28 -22 56 0 V212 H44 Z" fill="%s"/>' % INDIGO,
       '<path d="M44 196 q28 -18 56 0 q28 18 56 0 q28 -18 56 0 V212 H44 Z" fill="%s"/>' % LILAC,
       crescent("m5", 120, 98, 46, 22, CREAM)[1],
       crescent("m5", 120, 98, 46, 22, CREAM)[0]))

SVG_06 = svg_open("""
<defs>%s</defs>
%s
%s
%s
%s
""" % (crescent("m6", 128, 92, 50, 23, CREAM)[0],
       '<path d="M52 214 V132 a76 76 0 0 1 152 0 V214" fill="none" stroke="%s" '
       'stroke-width="22" stroke-linecap="round"/>' % NAVY,
       '<path d="M74 214 V134 a54 54 0 0 1 108 0 V214 Z" fill="%s"/>' % NAVY,
       crescent("m6", 128, 92, 50, 23, CREAM)[1],
       circle(128, 196, 18, LILAC)))

CANDIDATES = [
    ("01", "moon-stars", "Cream crescent with three lilac stars", SVG_01),
    ("02", "constellation", "Five dots joined into a constellation", SVG_02),
    ("03", "moon-disc", "Navy disc holding a cream crescent", SVG_03),
    ("04", "night-note", "A note shape for the nocturne name", SVG_04),
    ("05", "moon-waves", "Crescent over two lilac waves", SVG_05),
    ("06", "arch-moon", "Lilac arch with a crescent inside", SVG_06),
]


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render_cells():
    cells = "".join('<div id="cell%s" style="width:%dpx;height:%dpx">%s</div>' % (num, CELL, CELL, svg)
                    for num, _n, _d, svg in CANDIDATES)
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
            'html,body{margin:0;padding:0;background:transparent}'
            '#grid{display:flex;flex-wrap:wrap;width:%dpx}div[id^=cell]{display:block}'
            '</style></head><body><div id="grid">%s</div></body></html>' % (CELL * 3, cells))
    out = {}
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception:
            # bundled headless shell may be missing after a Playwright update
            b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": CELL * 3, "height": CELL * 2})
        pg.set_content(html)
        for num, name, _d, _svg in CANDIDATES:
            path = CAND_DIR / ("%s-%s.png" % (num, name))
            pg.locator("#cell" + num).screenshot(path=str(path), omit_background=True)
            img = Image.open(path).convert("RGBA").resize((PREVIEW, PREVIEW), Image.LANCZOS)
            img.save(path)
            bbox = img.split()[3].getbbox()
            assert bbox, "candidate %s rendered empty" % name
            assert bbox[0] > 6 and bbox[1] > 6 and bbox[2] < PREVIEW - 6 and bbox[3] < PREVIEW - 6, \
                "candidate %s touches the canvas edge: %s" % (name, bbox)
            out[num] = img
            print("candidate %s %s -> alpha bbox %s" % (num, name, bbox))
        b.close()
    return out


def contact_sheet(rendered, bg, txt, sub, path, title):
    cols, rows = 3, 2
    cw, ch = 384, 374
    gap, margin = 28, 40
    W = margin * 2 + cols * cw + (cols - 1) * gap
    H = margin * 2 + 34 + rows * ch + (rows - 1) * gap
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    f_title, f_name, f_desc, f_file = font(24, True), font(21, True), font(15), font(14)
    d.text((margin, margin), title, font=f_title, fill=txt)
    y0 = margin + 34
    for i, (num, name, desc, _svg) in enumerate(CANDIDATES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = y0 + r * (ch + gap)
        big = rendered[num].resize((220, 220), Image.LANCZOS)
        sheet.paste(big, (x + (cw - 220) // 2, y + 14), big)
        d.text((x + 18, y + 250), "%s · %s" % (num, name), font=f_name, fill=txt)
        d.text((x + 18, y + 280), desc, font=f_desc, fill=sub)
        thumb = rendered[num].resize((32, 32), Image.LANCZOS)
        sheet.paste(thumb, (x + 18, y + 330), thumb)
        d.text((x + 60, y + 339), "%s.png  256x256" % name, font=f_file, fill=sub)
        assert y + 300 <= y + 322, "text block collides with the thumbnail row"
    sheet.save(path)
    print("saved:", path, sheet.size)


def inline_strip(rendered, path):
    n, cell, gap, margin = len(CANDIDATES), 108, 22, 30
    W = margin * 2 + n * cell + (n - 1) * gap
    H = margin * 2 + cell + 30
    strip = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(strip)
    f = font(15, True)
    for i, (num, _n, _d, _s) in enumerate(CANDIDATES):
        x = margin + i * (cell + gap)
        img = rendered[num].resize((cell, cell), Image.LANCZOS)
        strip.paste(img, (x, margin), img)
        d.text((x + cell // 2 - 8, margin + cell + 8), num, font=f, fill=NAVY)
    strip.save(path)
    print("saved:", path, strip.size)


def main():
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rendered = render_cells()
    contact_sheet(rendered, (252, 249, 236), (0, 16, 91), (120, 120, 150),
                  CAND_DIR / "contact-light.png", "Nocturne Navy — flat candidates (light)")
    contact_sheet(rendered, (0, 16, 91), (252, 249, 236), (170, 170, 210),
                  CAND_DIR / "contact-dark.png", "Nocturne Navy — flat candidates (dark)")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")
    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    icon = rendered[sel[0]].resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, icon.size)


if __name__ == "__main__":
    main()
