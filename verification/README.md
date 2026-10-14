# Verification

The approved geometry is retained in the symbol, small master and regular
black/white exports. The SVG audit is saved in `svg-audit.json`; export
consistency checks are recorded in `checks.json`.

The canonical and small symbols score 100/100 on the structural heuristic.
Horizontal, stacked and wordmark masters score 91/100 because two native
Inter `k` diagonals trigger near-angle warnings. Those font shapes are
intentional and preserved. No finished logo SVG contains live text, raster
artwork, strokes, masks, gradients or filters.

`size-and-reverse.png` shows regular black, regular white and optical white;
native 16/32 px PNGs; 16 px pixels enlarged without smoothing; and lockups
at their minimum widths. It was inspected after export. The two-pixel
channel remains open at 16 px. Black and white alpha masks match at all
eight exported symbol sizes.

The favicon PNGs match the canonical symbol at 16/32 px. The ICO contains
16/32/48 px frames matching their PNGs, including every color and alpha
channel. The maskable artwork fits the central 80% safe-zone circle.

All four print-master PDFs were rendered with Poppler and visually
inspected; `print-review.png` records the comparison. `pdffonts` reports
no fonts, and Ghostscript ink coverage reports zero cyan, magenta and
yellow on every page. The artwork uses explicit 100K vector fills.
The A4 guide was rendered and inspected as a single page.

All five presentation slides were inspected through T3's HTML preview;
screenshots are in `presentation/`. No console errors were reported.
The responsive overview was checked at 728 px in light mode and 360 px
in dark mode. The six placements are identity mockups rather than claims
that an Altstack CLI or native app currently exists.

The application's implemented navbar, sidebar and favicon geometry is
unchanged by this kit. Application checks were rerun: all 185 web tests
across 18 suites passed. `vp check` covers formatting, lint and types.
