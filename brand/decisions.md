# Brand decisions

How the Sofired mark and wordmark were chosen, so later changes can build on
what was tried. Recorded in October 2026.

## The brief

- **What Sofired is.** A software development company based in Alabama. It
  built tools for its own development work (treerig, composemux, tracedoc,
  grizzle) and shares them as open source.
- **How it should feel.** Crafted and warm, with some personality.
- **How it relates to products.** It endorses them: each product keeps its own
  brand, and Sofired appears once, small, at the end.
- **Constraints.** The avatar must read at 20 px beside every repository name
  on GitHub. The website's previous logo came with its template and was
  dropped.

## Round 1: five readings of "fired"

1. **S Bar**: a cattle brand, an S over a bar.
2. **Firefly**: a firefly's flight path writing an S, ending in an ember.
3. **Live Coal**: a lump of charcoal with an S glowing through a crack.
4. **Kiln**: an arched kiln door with a flame inside.
5. **Cast Iron**: a skillet seen from above, with a hot centre.

Kiln was generic and carried no S. Live Coal was heavy and read as a gem or a
shield. Cast Iron read as cooking first. **S Bar** and **Firefly** went
forward.

The palette came out of this round as Char, Ash and Ember, meaning what a
fire leaves behind. Cream and terracotta were avoided on purpose, as was any
hue shared with treerig's red.

## Round 2: S Bar and Firefly

- S Bar: the original, a one-ink version, and a Rocking S (a curved rocker
  instead of the bar).
- Firefly: the original, a bold version, and a blinking version with a break
  in the trail.

Firefly's ember disappeared below 20 px until the bold version enlarged it,
and even then the mark read as "S." to fresh eyes. S Bar was the clearest at
16 and 20 px.

## Round 2b: the mark as the S

Seven wordmarks set the mark in place of the typed S, in Zilla Slab and
Bricolage Grotesque: a "ranch sign" with the bar under the whole word, a
"tucked" version with the S Bar as the S, and Firefly versions with the
ember on the S or dotting the i.

What it showed:

- A drawn S that matches the font's weight and height reads as an ordinary
  letter, so the bar is what identifies the brand.
- The ranch-sign bar read as a hyperlink underline below 24 px.

**Chosen: Tucked, in Zilla Slab.** The lockup's S and the avatar are the same
mark, and the short bar can't be mistaken for an underline. Zilla Slab won over
Bricolage for its signage feel. "Sofired", capital S, is the name in the
wordmark and the GitHub display name.

## Production notes

- The wordmark letters are Zilla Slab Bold outlines, shaped with HarfBuzz so
  the fi ligature matches what a browser sets. `source/extract_wordmark.py`
  regenerates them. HarfBuzz applied no kerning between these letters.
- The space between the S and the "o" was tightened from the browser mock-up
  (about 76 font units of white) to about 50, close to Zilla Slab's own S–o.
- The first production wordmark drew the S at 6.6 grid units, about 104 font
  units, and it read visibly lighter than the letters. Measured against Zilla
  Slab Bold (stems 129, its own S 116 to 144), the stroke went to 8.8 grid
  units, about 132. The bar moved down with it so the gap keeps the master's
  3-to-7 proportion to the stroke.
- The avatar PNGs are rasterised by `build.py` from the stroke geometry,
  using the standard library only, so the build needs no image tools.
