# Brand

The visual identity of Sofired (Southern Fired Software, LLC): the mark, its
16 px version, the wordmark, the avatar, colour, type, and how Sofired sits
above its products. [`decisions.md`](decisions.md) records how the mark was
chosen.

| | |
| --- | --- |
| Name | Sofired, capital S. The legal name, Southern Fired Software, LLC, is for legal and package-vendor contexts. |
| Mark | The S Bar. |
| Wordmark | The S Bar standing in for the S, followed by "ofired" in Zilla Slab Bold. |
| Colour | Char `#231A15`, Ash `#EEEBE6`, Ember `#C9561A` (`#F28A45` on dark). |
| Type | Zilla Slab (display), IBM Plex Sans (body), IBM Plex Mono (code). |
| GitHub | Org `sofired`, display name "Sofired". |

## Files

| File | Use |
| ---- | --- |
| `sofired-mark.svg` | The mark on light grounds, 20 px and up. |
| `sofired-mark-dark.svg` | The mark on dark grounds, 20 px and up. |
| `sofired-mark-mono.svg`, `sofired-mark-mono-dark.svg` | The mark in one ink, Char or Ash, for one-colour uses. |
| `sofired-favicon-16.svg`, `sofired-favicon-16-dark.svg` | The mark at 16 px. Pixel-built; use it only at 16 px. |
| `sofired-favicon-16.png`, `sofired-favicon-32.png` | The 16 px mark as PNG at 16 × 16 and 32 × 32 (the same grid at 2x), light grounds. |
| `sofired-favicon-16-dark.png`, `sofired-favicon-32-dark.png` | The same, for dark grounds. |
| `sofired-avatar.svg` | The avatar: the dark mark on a full-bleed Char square. |
| `sofired-avatar-512.png` | The avatar as a 512 × 512 PNG, for the GitHub organization and other profile pictures. |
| `sofired-touch-icon-180.png` | The avatar at 180 × 180, the website's `apple-touch-icon`. |
| `sofired-logo.svg`, `sofired-logo-dark.svg` | The wordmark on light and dark grounds. |
| `sofired-logo-mono.svg`, `sofired-logo-mono-dark.svg` | The wordmark in one ink. |
| `tokens.css` | Colour and type as CSS custom properties, for the website. |
| `source/build.py` | Regenerates every SVG and PNG above. Python 3 standard library only. |
| `source/extract_wordmark.py` | Prints the wordmark outlines from the font. Design-time only. |

The SVGs and PNGs are generated. Change the geometry or colours in
`source/build.py`, then run `python3 brand/source/build.py`; don't hand-edit
them. The PNGs are indexed, carry no metadata and use a stored deflate stream,
so they are the same bytes on every machine. `build.py` draws the avatar PNGs
itself: the mark is only round-capped strokes, so each pixel's coverage comes
from its distance to the stroke. The wordmark letters are stored in the
script as outlines, so the font is not needed to rebuild.

## The mark

The S Bar is read the way a ranch brand is read, top to bottom: an S over a
bar. A brand is a mark burned in to say who made something, which is what
Sofired is to its products.

Construction, on a 64-unit grid:

- Both strokes are 7 units wide, with round caps and joins.
- The S spans 15.5 to 48.5 across and 5.5 to 48.5 down; the bar runs from 18
  to 46 at y = 55. The mark is centred on the grid.
- The bar is Ember, as if still hot from the iron; the S is ink.
- The bar sits below the S with a clear gap. It never touches the S and never
  crosses it, so the mark can't be read as a dollar sign.
- Clear space is the bar's height on every side.

Don't:

- Close the gap or run the bar through the S.
- Colour the S Ember. The ember is the bar.
- Rotate, mirror or outline the mark.
- Scale the master below 20 px. Use the 16 px file at 16 px.

### Small sizes

`sofired-favicon-16.svg` draws the mark pixel by pixel: a two-pixel S, one
empty row, and a two-pixel bar. Use it at 16 px, and the master from 20 px up.

## The wordmark

The wordmark is "Tucked": the S Bar takes the place of the S, and "ofired"
follows in Zilla Slab Bold with the fi ligature, converted to outlines. The
drawn S is sized to Zilla Slab's own S (it overshoots the baseline and cap
height by the same amounts) and drawn at 6.6 units instead of 7 to match the
letters' stems. Its bar drops into the descender space under the S only.

- Always set it as one piece: never re-type "Sofired" in a font with the mark
  in front.
- Below 24 px tall, use the mark alone or plain text. The short bar turns into
  a smudge.
- The one-ink versions are for stamps, engraving and single-colour placements.

## Avatar

`sofired-avatar-512.png` is the mark at 76% on a full-bleed Char square, with
an Ash S and an Ember Light bar. GitHub rounds the corners itself, so the file
is square. At 20 px, next to each repository name, the S and the bar stay
apart.

## Colour

| Name | Hex | Use | Contrast |
| ---- | --- | --- | -------- |
| Char | `#231A15` | Ink: the mark, text, the avatar's ground. | 14.36:1 on Ash |
| Ash | `#EEEBE6` | Light grounds; the mark on dark. | 15.74:1 on Hearth |
| Ember | `#C9561A` | The bar, and other graphics on light grounds. Not for text. | 3.66:1 on Ash |
| Ember Deep | `#B5480F` | Ember as text or links on light grounds. | 4.53:1 on Ash; white on it 5.39:1 |
| Ember Light | `#F28A45` | Ember on dark grounds, text included. | 7.57:1 on Hearth; 6.91:1 on Char |
| Hearth | `#17110D` | Dark page grounds. | |
| Smoke | `#6E6158` | Secondary text on light grounds only. | 5.03:1 on Ash; fails on Hearth (3.13:1) |
| Smoke Light | `#B3A597` | Secondary text on dark grounds. | 7.79:1 on Hearth; 7.11:1 on Char |

Char and Ash carry nearly everything; Ember is the one warm note. Text meets
WCAG 2.1 AA (4.5:1) only in the pairings above. Ratios use the WCAG 2.1
relative-luminance formula.

## Type

All three faces are on Google Fonts under the SIL Open Font License.

- **Zilla Slab**, 700: headings and display. It's the slab of feed-store and
  fairground signs, and the face of the wordmark.
- **IBM Plex Sans**, 400 and 600: body text. treerig uses it too, which ties
  the family together.
- **IBM Plex Mono**, 400 and 500: code and commands.

## Sofired and its products

Sofired endorses; the products lead.

- **Products keep their own brands.** treerig keeps its name, mark, colours
  and voice. Its brand lives in `sofired/treerig` under `docs/brand/`.
- **Sofired appears once, at the end.** A product's README or site closes
  with "treerig is made by Sofired", linking to sofired.io, with the mark
  small or no mark at all.
- **Inside a product's surface, Sofired is one ink.** Draw the endorsement in
  the product's ink (Evergreen `#15271E` for treerig), never Ember, so the
  product's own accent keeps its meaning. treerig's red means "your branch"
  and nothing else.
- **Sofired leads where the company is the subject.** That means the GitHub
  organization, the website, proposals and invoices, package-vendor metadata
  (`packages@sofired.io`), and conduct contacts (`conduct@sofired.io`).

## Voice

Plain and warm, with a little Southern charm. The website already sounds
like this ("Services that Sizzle", "a pinch of Southern charm"). Keep the wit
in headings and asides. Never let it into product output, errors or docs:
those follow each product's own voice.

## Setup

Each step says whether it is done.

1. **GitHub avatar** (not done). Upload `sofired-avatar-512.png` under the
   organization's Settings → Profile → Profile picture. GitHub has no API for
   this.
2. **GitHub display name** (not done). Set the name to "Sofired" in the same
   settings page.
3. **Organization profile** (done). `profile/README.md` in this repository is
   the page GitHub shows on github.com/sofired.
4. **Website** (not done). Replace the template logo with
   `sofired-logo.svg` and `sofired-logo-dark.svg`. Link the favicons with the
   32 and 16 px PNGs first and the master SVGs after, each pair carrying
   `media="(prefers-color-scheme: ...)"` the way treerig's checkout index does,
   and link `sofired-touch-icon-180.png` as the `apple-touch-icon`. Import
   `tokens.css` for colour and type. The site's indigo, stock photos and
   template logo go.
5. **Product endorsements** (not done). Add the "made by Sofired" line to
   each product README, in that product's ink.
6. **Domains** (open). The website is southernfiredsoftware.com; package
   metadata and contacts use sofired.io. Pick one as primary and redirect the
   other.
