"""Print the outlines of "ofired" in Zilla Slab Bold, for pasting into build.py.

Design-time only: build.py does not run this. It needs fontTools and
uharfbuzz (pip install fonttools uharfbuzz) and the Zilla Slab Bold TTF
(SIL Open Font License), passed as the only argument. HarfBuzz shapes the
text, so the fi ligature and any kerning match what a browser draws.
"""
import sys

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

TEXT = "ofired"


def main(path):
    data = open(path, "rb").read()
    font = TTFont(path)
    order = font.getGlyphOrder()
    glyphs = font.getGlyphSet()
    buf = hb.Buffer()
    buf.add_str(TEXT)
    buf.guess_segment_properties()
    hb.shape(hb.Font(hb.Face(data)), buf, {})
    x = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        pen = SVGPathPen(glyphs, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip("."))
        # Font units are y-up; flip so the baseline is y = 0 and up is negative.
        glyphs[name].draw(TransformPen(pen, (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset)))
        print(f'    ("{name}", "{pen.getCommands()}"),')
        x += pos.x_advance
    print(f"# advance: {x}")


if __name__ == "__main__":
    main(sys.argv[1])
