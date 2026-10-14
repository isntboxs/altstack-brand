#!/usr/bin/env python3
"""Build the self-contained board and individual HTML slide sources."""
from pathlib import Path
import argparse
import re
import subprocess

KIT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--skill-dir', type=Path, required=True)
args = parser.parse_args()
board = KIT / 'presentation' / 'board.html'
subprocess.run(['python3', str(args.skill_dir / 'scripts/presentation_board.py'),
                str(KIT / 'presentation/spec.json'), '-o', str(board)], check=True)
html = board.read_text()
# Context fixtures use neutral tones so the presentation supports the approved
# monochrome identity. These changes do not alter any logo artwork.
neutral = '''
.readme .badges i{background:#777!important}
.screen,.sticker{background:#aaa!important}
.term span{color:#bbb!important}
'''
html = html.replace('</style>', neutral+'</style>', 1)
board.write_text(html)
css = re.search(r'<style>(.*?)</style>', html, re.S).group(1)
css += '\nbody{background:#fff}.slide{margin:0;box-shadow:none;overflow:visible}'
slides = re.findall(r'<section class="slide">.*?</section>', html, re.S)
for i, slide in enumerate(slides, 1):
    (board.parent / f'slide-{i:02}.html').write_text(
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Altstack / {i}</title><style>{css}</style></head><body>{slide}</body></html>\n')
print(f'Built {len(slides)} individual slide sources.')
