#!/usr/bin/env python3
"""Build the one-page usage guide as a portable, vector SVG."""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET

KIT = Path(__file__).resolve().parent.parent
NS = '{http://www.w3.org/2000/svg}'
parts = []

def text(x, y, content, size=16, weight=400, fill='#333333'):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(content)}</text>')

def lines(x, y, content, size=16, gap=24):
    for i, line in enumerate(content):
        text(x, y+i*gap, line, size)

def logo(name, x, y, width, height, fill='#000000'):
    root = ET.parse(KIT / 'masters' / f'{name}.svg').getroot()
    paths = ''.join(f'<path d="{p.get("d")}"/>' for p in root.iter(NS+'path'))
    parts.append(f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="{root.get("viewBox")}" fill="{fill}">{paths}</svg>')

def rule(y):
    parts.append(f'<path d="M48 {y}H792" stroke="#dddddd"/>')

def heading(x, y, content):
    text(x, y, content, 13, 600, '#555555')

parts.append('<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 840 1188"><title>Altstack one-page identity guide</title><rect width="840" height="1188" fill="white"/><g font-family="Inter, sans-serif">')
heading(48, 52, 'ALTSTACK / IDENTITY GUIDE')
text(48, 92, 'Offset Blocks', 32, 600, '#000000')
logo('altstack-logo-horizontal', 48, 124, 442, 100)
parts.append('<rect x="540" y="100" width="252" height="144" fill="black"/>')
logo('altstack-symbol', 618, 124, 96, 96, '#ffffff')
text(48, 264, 'Two balanced bodies. One stepped diagonal channel. Always lowercase.', 16)
rule(292)

heading(48, 326, '01 / CLEAR SPACE')
parts.append('<rect x="48" y="352" width="216" height="216" fill="none" stroke="#aaaaaa" stroke-dasharray="5 5"/><path d="M72 370H96M72 364V376M96 364V376" stroke="black"/>')
logo('altstack-symbol', 60, 364, 192, 192)
text(104, 371, 'x', 14, 500)
lines(270, 390, ['x = one notch width.', '32 units on the', '256-unit canvas.', 'Keep at least x from', 'the visible silhouette', 'to other elements.'])
heading(492, 326, '02 / MINIMUM SIZES')
logo('altstack-symbol-small', 494, 362, 16, 16)
logo('altstack-symbol-small', 540, 350, 32, 32)
logo('altstack-symbol-small', 608, 334, 64, 64)
text(494, 420, 'Screen / print', 16, 500, '#000000')
lines(494, 450, ['Symbol: 16 px / 6 mm', 'Horizontal: 96 px / 25 mm wide', 'Stacked: 96 px / 20 mm wide', 'Wordmark: 64 px / 18 mm wide'])
text(48, 586, 'Use the supplied lockups intact; their internal spacing is already resolved.', 16)
rule(612)

heading(48, 646, '03 / MONOCHROME PALETTE')
parts.append('<rect x="48" y="668" width="40" height="40" fill="black"/><rect x="48" y="734" width="40" height="40" fill="white" stroke="#bbbbbb"/>')
text(104, 684, 'Black / #000000', 17, 500, '#000000')
text(104, 708, 'RGB 0, 0, 0 · CMYK 0, 0, 0, 100', 14)
text(104, 750, 'White / #FFFFFF', 17, 500, '#000000')
text(104, 774, 'RGB 255, 255, 255 · CMYK 0, 0, 0, 0', 14)
text(48, 806, 'Black on light; white on dark. Contrast: 21:1.', 15)
heading(456, 646, '04 / TYPE AND OPTICAL MASTERS')
lines(456, 680, ['Inter Medium 500; lowercase altstack.', 'The exported wordmark is outlined.', 'It needs no installed font.', '', '16 / 32 px: regular small master.', '64 px and above: optional optical white', 'reduces each body by 1.5% in scale.'], 15, 23)
rule(842)

heading(48, 876, '05 / CHOOSE THE FILE')
lines(48, 910, ['SVG: interfaces, documents, scalable artwork.', 'PNG: fixed-size images; transparent black / white.', 'K100 PDF: outlined, one-ink print artwork.', 'Web set: favicon, touch icon, maskable icon,', 'manifest and a head-snippet integration example.'], 15, 24)
heading(456, 876, '06 / KEEP THE GEOMETRY')
lines(456, 910, ['Do not stretch, rotate or rearrange the bodies.', 'Do not close or narrow the negative channel.', 'Do not add strokes, shadows or gradients.', 'Avoid busy or low-contrast backgrounds.', 'White print artwork uses paper, knockout or', 'white ink agreed with the production printer.'], 15, 24)
rule(1076)
text(48, 1108, 'Masters, exports, source scripts and mockups: see README.md in this kit.', 14)
text(48, 1134, 'Inter: SIL Open Font License 1.1 · Symbol: original vector construction for Altstack.', 13)
parts.append('</g></svg>')
(KIT / 'usage-guide.svg').write_text('\n'.join(parts)+'\n')
print('Built the A4 one-page usage guide SVG.')
