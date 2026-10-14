# Altstack logo kit

The official brand assets for [Altstack](https://github.com/isntboxs/altstack),
maintained separately from the application. Only the approved identity is
included. The application keeps its own deployed logo and icon files; it
does not fetch assets from this repository at runtime.

[Download the logo kit](https://github.com/isntboxs/altstack-brand/releases/latest)
as a ZIP, or clone this repository to work with its sources.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="digital/svg/altstack-logo-horizontal-white.svg">
  <img src="digital/svg/altstack-logo-horizontal-black.svg" alt="Altstack logo" width="420">
</picture>

Approved identity: **Offset Blocks**. Two equal polygonal bodies form a
stepped diagonal channel with opposing registration notches. The symbol is
an independent abstract identifier. It has no letterform construction.

Start with [the one-page usage guide](usage-guide.pdf) and
[the presentation board](presentation/board.html). The board includes README,
app-icon, website, terminal, sticker and social placements.

## Choose a file

- `digital/svg/`: ready-to-use black and white horizontal, stacked, symbol
  and wordmark artwork. All typography is outlined. Backgrounds are
  transparent except the square avatar and black app-icon tile.
- `digital/png/`: transparent black and white symbol exports at
  16, 32, 64, 128, 256, 512, 1024 and 2048 px; lockups and wordmarks at
  256, 512, 1024 and 2048 px **wide**. App-icon tiles are 512 and 1024 px.
- `masters/`: clean editable vector geometry, including the canonical
  small-size master and the optional optical white symbol.
- `print/`: symbol, horizontal, stacked and wordmark PDF masters, with
  explicit **CMYK 0/0/0/100** fill, outlined paths and transparent backgrounds.
  These are scalable artwork, not imposed or bleed-ready page layouts.
- `web/`: theme-aware SVG favicon; 16/32/48 px PNGs and multi-resolution ICO;
  180 px Apple touch icon; 192/512 px app icons; 512 px maskable icon;
  manifest and head-snippet example. Paths in the example assume this whole
  folder is copied to the website root; adapt paths to the host application.
- `presentation/`: self-contained HTML board, five PNG slides and its JSON
  source. The mockups are identity-placement examples, not UI specifications.
- `source/`: outlined Inter source, construction metadata and reproducible
  build scripts. `licenses/Inter-OFL.txt` contains the original font license.
- `verification/`: SVG audit results and visual QA sheets.

## Usage

Use pure black on a light surface and pure white on a dark surface. Preserve
the aspect ratio and supplied lockup spacing. Keep at least one notch width
(32 units on the 256-unit symbol canvas) clear from the visible silhouette
to other elements. Apply that clearance outside a complete lockup as well.

Minimum digital sizes: symbol **16 px**, horizontal **96 px wide**,
stacked **96 px wide**, wordmark **64 px wide**. Minimum print sizes:
symbol **6 mm**, horizontal **25 mm wide**, stacked **20 mm wide** and
wordmark **18 mm wide**. Prefer a 20 px or larger symbol in navigation.

The small master deliberately retains the approved geometry: the 16-unit
grid aligns to whole pixels at 16 and 32 px and leaves the two-pixel terminal
gaps open at 16 px. Use regular white at these sizes. For white symbols at
64 px or larger, the optional `altstack-symbol-white-optical.svg` scales
each body by 0.985 about its own area centroid, reducing apparent white
weight while retaining the construction. It is a symbol-only alternative;
the regular reversed lockups are the default.

Do not rotate, distort, outline or rearrange the shapes; alter their channel;
add gradients or shadows; or place them on a busy, low-contrast background.
Do not replace the outlined lowercase wordmark with a different font.
The application's live Inter wordmark and existing layout remain intact.

## Palette and typography

- Black: HEX `#000000`, RGB `0, 0, 0`, CMYK `0, 0, 0, 100`.
- White: HEX `#FFFFFF`, RGB `255, 255, 255`, CMYK `0, 0, 0, 0`.

Black/white contrast is 21:1. No accent or spot color is specified. A white
print mark normally uses the substrate or a knockout; white ink requires
an explicit printer setup. The print PDFs use process black, avoiding
four-color rich black on small artwork.

The wordmark is **Inter Medium 500**, taken from the project's actual
`@fontsource-variable/inter` font and converted to paths through Pango/Cairo.
The export keeps the font's original shapes, including its diagonal `k`.
Finished logo files require no fonts. Inter is licensed under SIL OFL 1.1;
its license is included. The kit does not redistribute a font binary.

## Rebuild

From this kit folder, with Python 3:

```sh
python3 source/build_masters.py
python3 source/build_masters.py --print
python3 source/build_guide.py
python3 source/build_exports.py --skill-dir /path/to/logo-design/skill
python3 source/build_presentation.py --skill-dir /path/to/logo-design/skill
python3 source/package_kit.py
```

The scripts use Python's standard library. Digital exports also use the
logo-design skill scripts and a native SVG renderer (`rsvg-convert` here).
`build_masters.py` always reads `masters/altstack-symbol.svg` in this repository.
The outlined font source makes rebuilding independent of installed fonts.
The theme-aware favicon is generated from the local small master, and
the Inter license is included in `licenses/`; no Altstack checkout or
`node_modules` is required.
`rsvg-convert -f pdf usage-guide.svg -o usage-guide.pdf` builds the guide PDF;
use Inter installed or a private fontconfig profile for matching guide text.
The documentation SVG contains text; the logo artwork does not.

`package_kit.py` refreshes `SHA256SUMS.txt` and writes the full ZIP to
`dist/altstack-logo-kit.zip`. It packages tracked files, so add new kit files
to Git before running it. The generated `dist/` directory is ignored;
release archives can be uploaded to GitHub Releases.

The brand source of truth is `masters/altstack-symbol.svg` here. When the
approved geometry changes, update the application's bundled
`apps/web/public/brand/altstack-symbol.svg`, `BrandMark`, favicon and raster
icons together. Rebuilding this kit does not modify application assets.

## Handover

The symbol's two seven-vertex bodies use horizontal, vertical and 45-degree
edges on a 256-unit canvas. Its 224-unit footprint is centered, with equal
body areas and 180-degree rotational balance. The horizontal lockup uses
the existing navbar's relative wordmark size and gap. Stacked and wordmark
masters add convenient layouts without changing the font.

Audit and render evidence is in `verification/`. The symbol masters have
no text, strokes, masks, filters, gradients or raster content. The Inter
wordmark's original diagonal angles are intentionally retained; heuristic
near-angle warnings are documented rather than changing the font.

The application's light, dark and mobile placements were verified during
implementation. This kit supplies production artwork, not a trademark
clearance; a professional trademark and reverse-image search remains the
appropriate check before commercial registration.
