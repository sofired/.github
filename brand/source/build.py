#!/usr/bin/env python3
"""Generate the Sofired brand SVGs and PNGs in brand/ from the geometry below.

Run from anywhere: python3 brand/source/build.py
Needs only the Python 3 standard library. The wordmark letters "ofired" are
stored here as outlines (Zilla Slab Bold, SIL Open Font License), so the font
is not needed to rebuild. extract_wordmark.py printed them; see its docstring.
"""
import math
import os
import struct
import zlib

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# Palette: what a fire leaves behind. Ember is the one warm note.
CHAR, ASH, EMBER, EMBER_LIGHT = '#231A15', '#EEEBE6', '#C9561A', '#F28A45'

STROKE = 7  # mark weight on the 64-unit grid

# The S Bar, read top to bottom as a ranch brand: an S over a bar. The bar
# always sits clear of the S, never through it, so it cannot read as a dollar
# sign. Both strokes have round caps and joins. The mark is centred on the grid:
# 15.5..48.5 wide for the S, 14.5..49.5 for the bar, 5.5..58.5 tall.
S_PATH = 'M43 15C40 11 36 9 31 9C24 9 19 13 19 18.5C19 31 45 22 45 35.5C45 41 40 45 32 45C26 45 21 42 19 38'
BAR_PATH = 'M18 55H46'


def stroke(colour, d, width=STROKE):
    """Return one stroked path with round caps and joins."""
    return (f'<path d="{d}" stroke="{colour}" stroke-width="{width}" '
            'stroke-linecap="round" stroke-linejoin="round" fill="none"/>')


def mark(fg, accent, width=STROKE, bar_y=55):
    """Return the S Bar on a 64x64 grid: the S in fg, the bar in accent.

    bar_y moves the bar down when the strokes are heavier, to keep the gap.
    """
    return stroke(fg, S_PATH, width) + stroke(accent, f'M18 {bar_y:g}H46', width)


# Avatar: the mark at 76% on a full-bleed Char square. GitHub rounds the
# corners itself, so the file is square.
AVATAR_SCALE = 0.76
AVATAR_OFFSET = 32 * (1 - AVATAR_SCALE)


def avatar(ground=CHAR, fg=ASH, accent=EMBER_LIGHT):
    """Return the avatar tile markup on a 64x64 grid."""
    return (f'<rect width="64" height="64" fill="{ground}"/>'
            f'<g transform="translate({AVATAR_OFFSET:.2f} {AVATAR_OFFSET:.2f}) scale({AVATAR_SCALE})">'
            f'{mark(fg, accent)}</g>')


# The 16 px file: the mark placed pixel by pixel, because at 16 px the master's
# curves blur. '#' is ink, 'b' is the bar. Two-pixel strokes, one empty row
# between the S and the bar.
FAVICON_16 = [
    '................',
    '................',
    '.....######.....',
    '....########....',
    '....##....##....',
    '....##..........',
    '....#######.....',
    '.....#######....',
    '..........##....',
    '....##....##....',
    '....########....',
    '.....######.....',
    '................',
    '....bbbbbbbb....',
    '....bbbbbbbb....',
    '................',
]


def favicon(fg, accent):
    """Return the 16 px pixel-art mark as crisp 1x1 rects."""
    cells = ''.join(
        f'<rect x="{x}" y="{y}" width="1" height="1" fill="{fg if ch == "#" else accent}"/>'
        for y, row in enumerate(FAVICON_16) for x, ch in enumerate(row) if ch != '.')
    return f'<g shape-rendering="crispEdges">{cells}</g>'


def png_chunk(kind, data):
    """Return one PNG chunk: length, type, data and the CRC over type and data."""
    body = kind + data
    return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body) & 0xFFFFFFFF)


def indexed_png(width, height, rows, palette, transparent_first=False):
    """Return an 8-bit indexed PNG from rows of palette indices.

    No metadata chunks, and the deflate stream is stored (level 0): stored
    blocks do not depend on the zlib build, so the bytes are the same on every
    machine.
    """
    raw = b''.join(bytes([0]) + bytes(row) for row in rows)  # filter 0 on every row
    plte = b''.join(bytes.fromhex(c.lstrip('#')) for c in palette)
    chunks = [png_chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 3, 0, 0, 0)),
              png_chunk(b'PLTE', plte)]
    if transparent_first:
        chunks.append(png_chunk(b'tRNS', bytes([0])))  # index 0 transparent; the rest opaque
    chunks += [png_chunk(b'IDAT', zlib.compress(raw, 0)), png_chunk(b'IEND', b'')]
    return b'\x89PNG\r\n\x1a\n' + b''.join(chunks)


def favicon_png(fg, accent, scale):
    """Return the 16 px pixel mark as a PNG, each pixel scale x scale."""
    index = {'.': 0, '#': 1, 'b': 2}
    rows = []
    for row in FAVICON_16:
        line = [index[ch] for ch in row for _ in range(scale)]
        rows += [line] * scale
    size = 16 * scale
    return indexed_png(size, size, rows, ('#000000', fg, accent), transparent_first=True)


# Rasterising the avatar. The mark is only round-capped strokes, so each
# pixel's coverage follows from its distance to the stroke's centre line:
# full inside, none outside, a one-pixel ramp at the edge. Curves are
# flattened into short segments first.

def parse_path(d):
    """Return the polyline points of a path using only M, C and H commands."""
    tokens = d.replace('M', ' M ').replace('C', ' C ').replace('H', ' H ').split()
    points, i, cmd = [], 0, None
    while i < len(tokens):
        if tokens[i] in 'MCH':
            cmd = tokens[i]
            i += 1
        if cmd == 'M':
            points.append((float(tokens[i]), float(tokens[i + 1])))
            i += 2
        elif cmd == 'H':
            points.append((float(tokens[i]), points[-1][1]))
            i += 1
        else:
            p0 = points[-1]
            p1, p2, p3 = [(float(tokens[i + k]), float(tokens[i + k + 1])) for k in (0, 2, 4)]
            for step in range(1, 33):
                t = step / 32
                u = 1 - t
                points.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                               u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
            i += 6
    return points


def coverage(size, points, width, transform):
    """Return a size x size grid of stroke coverage, 0.0 to 1.0."""
    scale, offset = transform
    px = [((x * scale + offset) * size / 64, (y * scale + offset) * size / 64) for x, y in points]
    radius = width * scale * size / 64 / 2
    dist = [[math.inf] * size for _ in range(size)]
    for (ax, ay), (bx, by) in zip(px, px[1:]):
        dx, dy = bx - ax, by - ay
        length2 = dx * dx + dy * dy or 1e-9
        x0, x1 = max(0, int(min(ax, bx) - radius - 1)), min(size, int(max(ax, bx) + radius + 2))
        y0, y1 = max(0, int(min(ay, by) - radius - 1)), min(size, int(max(ay, by) + radius + 2))
        for y in range(y0, y1):
            cy = y + 0.5
            row = dist[y]
            for x in range(x0, x1):
                cx = x + 0.5
                t = max(0.0, min(1.0, ((cx - ax) * dx + (cy - ay) * dy) / length2))
                d = math.hypot(cx - ax - t * dx, cy - ay - t * dy)
                if d < row[x]:
                    row[x] = d
    return [[max(0.0, min(1.0, radius + 0.5 - d)) for d in row] for row in dist]


def blend(a, b, t):
    """Return colour a mixed toward colour b by t, as #RRGGBB."""
    ca, cb = bytes.fromhex(a.lstrip('#')), bytes.fromhex(b.lstrip('#'))
    return '#' + ''.join(f'{round(x + (y - x) * t):02X}' for x, y in zip(ca, cb))


def avatar_png(size, ground=CHAR, fg=ASH, accent=EMBER_LIGHT):
    """Return the avatar as a size x size PNG.

    The S and the bar never overlap, so each pixel is ground blended toward
    one of them. Coverage is quantised to 32 steps, which keeps the image
    indexed: 65 colours at most.
    """
    levels = 32
    transform = (AVATAR_SCALE, AVATAR_OFFSET)
    layers = [(fg, coverage(size, parse_path(S_PATH), STROKE, transform)),
              (accent, coverage(size, parse_path(BAR_PATH), STROKE, transform))]
    palette = [ground] + [blend(ground, colour, step / levels)
                          for colour, _ in layers for step in range(1, levels + 1)]
    rows = []
    for y in range(size):
        row = []
        for x in range(size):
            index = 0
            for n, (_, cov) in enumerate(layers):
                step = round(cov[y][x] * levels)
                if step:
                    index = 1 + n * levels + step - 1
            row.append(index)
        rows.append(row)
    return indexed_png(size, size, rows, palette)


# Wordmark: the S Bar stands in for the S ("Tucked"), followed by "ofired" in
# Zilla Slab Bold, outlines in font units (1000/em), baseline at y = 0, the fi
# ligature as a browser sets it. Ink bounds: x 20..2600, y -698..10.
OFIRED = (
    'M503 -225Q503 -118 433 -54Q363 10 255 10Q151 10 85.5 -50.5Q20 -111 20 -220Q20 -319 80 -390Q140 -461 262 -461Q384 -461 443.5 -390.5Q503 -320 503 -225ZM370 -229Q370 -298 338 -330Q306 -362 260 -362Q210 -362 181.5 -326.5Q153 -291 153 -227Q153 -169 179.5 -129Q206 -89 259 -89Q309 -89 339.5 -126.5Q370 -164 370 -229Z'
    'M913 -98V-353H740V-98H815V0H551V-98H611V-353H556V-451H611V-520Q611 -590 667 -644Q723 -698 832 -698Q870 -698 917 -689Q964 -680 1008 -657L1028 -535L928 -524L909 -588Q902 -590 881.5 -595.5Q861 -601 832 -601Q773 -601 756.5 -576Q740 -551 740 -522V-451H1042V-98H1102V0H853V-98Z'
    'M1434 -457Q1453 -457 1476.5 -451.5Q1500 -446 1523 -432L1543 -274L1445 -263L1428 -340Q1408 -352 1393 -352Q1371 -352 1354.5 -335Q1338 -318 1338 -285V-97H1418V0H1149V-97H1209V-353H1144V-451H1328V-365Q1339 -404 1363.5 -430.5Q1388 -457 1434 -457Z'
    'M2024 -142Q2019 -82 1965 -36Q1911 10 1814 10Q1713 10 1647.5 -47Q1582 -104 1582 -217Q1582 -321 1641.5 -390.5Q1701 -460 1808 -460Q1902 -460 1960.5 -406Q2019 -352 2020 -264Q2020 -231 2013 -199H1717Q1728 -92 1823 -92Q1875 -92 1893.5 -117Q1912 -142 1916 -162ZM1887 -274Q1891 -308 1872.5 -338Q1854 -368 1808 -368Q1768 -368 1746 -342Q1724 -316 1718 -274Z'
    'M2600 0H2411V-84Q2392 -45 2355 -17.5Q2318 10 2257 10Q2168 10 2117 -51Q2066 -112 2066 -217Q2066 -318 2116 -389Q2166 -460 2267 -460Q2322 -460 2357 -438Q2392 -416 2411 -382V-590H2321V-688H2540V-97H2600ZM2411 -228V-239Q2411 -295 2381.5 -326.5Q2352 -358 2308 -358Q2265 -358 2232.5 -326Q2200 -294 2200 -225Q2200 -160 2230 -126Q2260 -92 2301 -92Q2352 -92 2381.5 -135Q2411 -178 2411 -228Z'
)

# The drawn S is sized to Zilla Slab's own S (-10..660 font units, so it
# overshoots the baseline and the 650 cap height by the same amounts). Its
# stroke, 8.8 grid units, comes to about 132 font units: Zilla Slab Bold's
# stems measure 129, its own S 116 to 144. The bar drops into the descender
# space.
WORDMARK_STROKE = 8.8
S_SCALE = 670 / (36 + WORDMARK_STROKE)          # font units per grid unit
S_LEFT = 18 - WORDMARK_STROKE / 2               # bar's left edge on the grid
S_BOTTOM = 45 + WORDMARK_STROKE / 2             # S's lowest point on the grid
S_RIGHT = 45 + WORDMARK_STROKE / 2              # S's rightmost point on the grid
# The gap between the S and the bar keeps the master's proportion to the
# stroke: 3 units of gap to a 7-unit stroke.
WORDMARK_BAR_Y = round(45 + WORDMARK_STROKE * (1 + 3 / STROKE), 2)
# Where "ofired" starts: 30 units after the S, so with the o's 20-unit side
# bearing the white between them is 50, close to Zilla Slab's own S and o.
OFIRED_X = round((S_RIGHT - S_LEFT) * S_SCALE) + 30


def lockup(fg, accent):
    """Return the wordmark: the S Bar as the S, then "ofired"."""
    tx, ty = -S_LEFT * S_SCALE, 10 - S_BOTTOM * S_SCALE
    bar_bottom = 10 + (WORDMARK_BAR_Y + WORDMARK_STROKE / 2 - S_BOTTOM) * S_SCALE
    pad = 20
    width = OFIRED_X + 2600 + 2 * pad
    top = -698 - pad
    height = math.ceil(bar_bottom + pad - top)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {top} {width} {height}">'
            f'<g transform="translate({tx:.1f} {ty:.1f}) scale({S_SCALE:.4f})">'
            f'{mark(fg, accent, WORDMARK_STROKE, WORDMARK_BAR_Y)}</g>'
            f'<path fill="{fg}" transform="translate({OFIRED_X} 0)" d="{OFIRED}"/></svg>')


def svg(inner, size=64):
    """Wrap markup in a square SVG document."""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{inner}</svg>'


def main():
    """Write every brand SVG and PNG into brand/."""
    files = {
        'sofired-mark.svg': svg(mark(CHAR, EMBER)),
        'sofired-mark-dark.svg': svg(mark(ASH, EMBER_LIGHT)),
        'sofired-mark-mono.svg': svg(mark(CHAR, CHAR)),
        'sofired-mark-mono-dark.svg': svg(mark(ASH, ASH)),
        'sofired-avatar.svg': svg(avatar()),
        'sofired-favicon-16.svg': svg(favicon(CHAR, EMBER), 16),
        'sofired-favicon-16-dark.svg': svg(favicon(ASH, EMBER_LIGHT), 16),
        'sofired-logo.svg': lockup(CHAR, EMBER),
        'sofired-logo-dark.svg': lockup(ASH, EMBER_LIGHT),
        'sofired-logo-mono.svg': lockup(CHAR, CHAR),
        'sofired-logo-mono-dark.svg': lockup(ASH, ASH),
    }
    for name, content in files.items():
        with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(content + '\n')
        print(name)
    pngs = {
        'sofired-favicon-16.png': favicon_png(CHAR, EMBER, 1),
        'sofired-favicon-16-dark.png': favicon_png(ASH, EMBER_LIGHT, 1),
        'sofired-favicon-32.png': favicon_png(CHAR, EMBER, 2),
        'sofired-favicon-32-dark.png': favicon_png(ASH, EMBER_LIGHT, 2),
        'sofired-avatar-512.png': avatar_png(512),
        'sofired-touch-icon-180.png': avatar_png(180),
    }
    for name, content in pngs.items():
        with open(os.path.join(OUT, name), 'wb') as f:
            f.write(content)
        print(name)


if __name__ == '__main__':
    main()
