#!/usr/bin/env python3
"""Rebuild the approved vector masters and one-ink print PDFs (stdlib only)."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
KIT = HERE.parent
SVG_NS = 'http://www.w3.org/2000/svg'
XLINK = '{http://www.w3.org/1999/xlink}href'
NUM = r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?'

def fmt(value):
    return f'{value:.2f}'.rstrip('0').rstrip('.')

def translate_path(data, dx=0, dy=0, scale=1):
    commands = re.findall(r'([MLCZ])([^MLCZ]*)', data)
    result = []
    for index, (command, values) in enumerate(commands):
        # Cairo emits a final empty move after a closed contour; remove it.
        if command == 'M' and index == len(commands) - 1:
            continue
        numbers = [float(n) for n in re.findall(NUM, values)]
        if command == 'Z':
            result.append('Z')
            continue
        transformed = [fmt(v * scale + (dx if i % 2 == 0 else dy)) for i, v in enumerate(numbers)]
        result.append(command + ' '.join(transformed))
    return ' '.join(result)

def outline_word():
    tree = ET.parse(HERE / 'inter-medium-outlines.svg').getroot()
    glyphs = {el.get('id'): el.find(f'{{{SVG_NS}}}path').get('d')
              for el in tree.iter() if el.get('id') and el.find(f'{{{SVG_NS}}}path') is not None}
    return [translate_path(glyphs[use.get(XLINK)[1:]], float(use.get('x')), float(use.get('y')))
            for use in tree.iter(f'{{{SVG_NS}}}use')]

def bbox(paths):
    axes = [[], []]
    def extrema(p0,p1,p2,p3):
        a=-p0+3*p1-3*p2+p3;b=3*p0-6*p1+3*p2;c=-3*p0+3*p1
        times=[0,1]
        if abs(a)<1e-9:
            if abs(b)>1e-9: times.append(-c/(2*b))
        else:
            disc=4*b*b-12*a*c
            if disc>=0: times.extend([(-2*b+math.sqrt(disc))/(6*a),(-2*b-math.sqrt(disc))/(6*a)])
        return [((a*t+b)*t+c)*t+p0 for t in times if 0<=t<=1]
    for data in paths:
        point=(0,0)
        for command,values in re.findall(r'([MLCZ])([^MLCZ]*)',data):
            numbers=[float(n) for n in re.findall(NUM,values)]
            if command in ('M','L'):
                point=tuple(numbers);axes[0].append(point[0]);axes[1].append(point[1])
            elif command=='C':
                for axis in (0,1): axes[axis].extend(extrema(point[axis],numbers[axis],numbers[axis+2],numbers[axis+4]))
                point=tuple(numbers[-2:])
    return min(axes[0]),min(axes[1]),max(axes[0]),max(axes[1])

def svg(paths, width, height, title, fill='#000000'):
    content = ''.join(f'  <path d="{data}"/>\n' for data in paths)
    return (f'<svg xmlns="{SVG_NS}" viewBox="0 0 {fmt(width)} {fmt(height)}" '
            f'width="{fmt(width)}" height="{fmt(height)}" fill="{fill}" role="img" aria-labelledby="title">\n'
            f'  <title id="title">{title}</title>\n{content}</svg>\n')

def symbol_paths():
    source = KIT / 'masters/altstack-symbol.svg'
    root = ET.parse(source).getroot()
    return [p.get('d') for p in root.iter(f'{{{SVG_NS}}}path')]

def expanded_symbol(data):
    # The approved symbol has only M/H/V/L/Z commands; expand to absolute pairs.
    x = y = 0
    parts = []
    for command, values in re.findall(r'([MHVLZ])([^MHVLZ]*)', data):
        numbers = [float(n) for n in re.findall(NUM, values)]
        if command in ('M', 'L'):
            x, y = numbers
        elif command == 'H': x = numbers[0]
        elif command == 'V': y = numbers[0]
        if command == 'Z': parts.append('Z')
        else: parts.append(('M' if command == 'M' else 'L') + f'{fmt(x)} {fmt(y)}')
    return ' '.join(parts)

def shrink_body(data, amount=0.985):
    pts = [(float(x), float(y)) for x, y in re.findall(r'[ML]('+NUM+') ('+NUM+')', data)]
    area = cx = cy = 0
    for a, b in zip(pts, pts[1:] + pts[:1]):
        cross = a[0]*b[1] - b[0]*a[1]
        area += cross; cx += (a[0]+b[0])*cross; cy += (a[1]+b[1])*cross
    cx /= 3*area; cy /= 3*area
    # Keep the final closing command; translator only drops a trailing empty M.
    return translate_path(data, cx*(1-amount), cy*(1-amount), amount)

def build():
    masters = KIT / 'masters'; masters.mkdir(parents=True, exist_ok=True)
    symbols = [expanded_symbol(p) for p in symbol_paths()]
    word = outline_word()
    bx0, by0, bx1, by1 = bbox(word)
    middle = (by0+by1)/2
    baseline_shift = 128-middle
    horizontal_word = [translate_path(p, 332.8, baseline_shift) for p in word]
    horizontal_width = math.ceil(332.8 + bx1 + 32)
    normalized_word = [translate_path(p, 32-bx0, baseline_shift) for p in word]
    word_width = math.ceil(bx1-bx0+64)
    stack_scale = 320/(bx1-bx0)
    stacked_word = [translate_path(p, 32-bx0*stack_scale, 206-middle*stack_scale, stack_scale) for p in word]
    stacked_symbol = [translate_path(p, 124, 8, 136/256) for p in symbols]
    files = {
      'altstack-symbol.svg': (symbols, 256, 256, 'Altstack symbol'),
      'altstack-symbol-small.svg': (symbols, 256, 256, 'Altstack symbol - small sizes'),
      'altstack-symbol-white-optical.svg': ([shrink_body(p) for p in symbols], 256, 256, 'Altstack symbol - optical reversed'),
      'altstack-logo-horizontal.svg': (symbols+horizontal_word, horizontal_width, 256, 'Altstack horizontal logo'),
      'altstack-logo-stacked.svg': (stacked_symbol+stacked_word, 384, 256, 'Altstack stacked logo'),
      'altstack-wordmark.svg': (normalized_word, word_width, 256, 'Altstack wordmark'),
    }
    for name, (paths, width, height, title) in files.items():
        (masters / name).write_text(svg(paths,width,height,title,'#ffffff' if 'optical' in name else '#000000'))
    (KIT / 'source' / 'construction.json').write_text(json.dumps({
      'symbol_viewbox':[0,0,256,256], 'symbol_grid':16, 'minimum_gap':32,
      'wordmark_font':'Inter', 'wordmark_weight':500, 'wordmark_em':204.8,
      'horizontal_wordmark_origin_x':332.8, 'horizontal_viewbox':[0,0,horizontal_width,256],
      'stacked_viewbox':[0,0,384,256], 'optical_reverse_body_scale':0.985,
      'font_source':'@fontsource-variable/inter/files/inter-latin-wght-normal.woff2',
      'approved_geometry_sha256':hashlib.sha256(' '.join(symbols).encode()).hexdigest(),
    },indent=2)+'\n')
    print(f'Built {len(files)} vector masters; horizontal {horizontal_width}x256; wordmark {word_width}x256.')

def pdf_commands(data):
    x = y = 0
    result = []
    for command, values in re.findall(r'([MLCHVZ])([^MLCHVZ]*)', data):
        numbers = [float(n) for n in re.findall(NUM, values)]
        if command in ('M', 'L'):
            x,y = numbers
            result.append(f'{fmt(x)} {fmt(y)} '+('m' if command=='M' else 'l'))
        elif command == 'H':
            x=numbers[0];result.append(f'{fmt(x)} {fmt(y)} l')
        elif command == 'V':
            y=numbers[0];result.append(f'{fmt(x)} {fmt(y)} l')
        elif command == 'C':
            result.append(' '.join(fmt(n) for n in numbers)+' c');x,y=numbers[-2:]
        elif command == 'Z': result.append('h')
    return '\n'.join(result)+'\nf\n'

def print_pdf(source, output):
    root = ET.parse(source).getroot()
    _,_,width,height=[float(n) for n in root.get('viewBox').split()]
    # Explicit process-black CMYK, all artwork outlined, no font resources.
    stream = f'q\n0.75 0 0 -0.75 0 {fmt(height*.75)} cm\n0 0 0 1 k\n'
    stream += ''.join(pdf_commands(p.get('d')) for p in root.iter(f'{{{SVG_NS}}}path'))+'Q\n'
    objects = [
      b'<< /Type /Catalog /Pages 2 0 R >>',
      b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
      f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {fmt(width*.75)} {fmt(height*.75)}] /Resources << >> /Contents 4 0 R >>'.encode(),
      f'<< /Length {len(stream.encode())} >>\nstream\n{stream}endstream'.encode(),
    ]
    data=bytearray(b'%PDF-1.7\n%\xe2\xe3\xcf\xd3\n');offsets=[0]
    for index,obj in enumerate(objects,1):
        offsets.append(len(data));data.extend(f'{index} 0 obj\n'.encode()+obj+b'\nendobj\n')
    xref=len(data);data.extend(f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode())
    for offset in offsets[1:]: data.extend(f'{offset:010d} 00000 n \n'.encode())
    data.extend(f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
    output.write_bytes(data)

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--print',action='store_true');args=parser.parse_args()
    if args.print:
        folder=KIT / 'print';folder.mkdir(exist_ok=True)
        for name in ['altstack-symbol','altstack-logo-horizontal','altstack-logo-stacked','altstack-wordmark']:
            print_pdf(KIT / 'masters' / f'{name}.svg',folder / f'{name}-K100.pdf')
        print('Built four outlined K100 print masters.')
    else: build()
