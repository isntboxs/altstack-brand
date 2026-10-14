#!/usr/bin/env python3
"""Export the kit using the installed logo-design tooling and librsvg."""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import xml.etree.ElementTree as ET

KIT=Path(__file__).resolve().parents[1]
SVG_NS='http://www.w3.org/2000/svg'

def run(*args):
    result=subprocess.run([str(a) for a in args],capture_output=True,text=True)
    if result.returncode: raise RuntimeError(result.stderr or result.stdout)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--skill-dir',type=Path,required=True);args=parser.parse_args()
    script=args.skill_dir / 'scripts'
    for directory in ['digital/svg','digital/png','web','licenses','presentation']:
        (KIT / directory).mkdir(parents=True,exist_ok=True)
    for stem in ['altstack-symbol','altstack-logo-horizontal','altstack-logo-stacked','altstack-wordmark']:
        run('python3',script/'export_variants.py',KIT/'masters'/f'{stem}.svg','--out-dir',KIT/'digital/svg','--name',stem,'--only','black','white')
    run('python3',script/'export_variants.py',KIT/'masters/altstack-symbol.svg','--out-dir',KIT/'digital/svg','--name','altstack-symbol',
        '--only','square','app-icon','--icon-bg','#000000','--icon-fg','#ffffff','--icon-scale','0.56','--optical-offset','0')
    shutil.copyfile(KIT/'masters/altstack-symbol-small.svg',KIT/'digital/svg/altstack-symbol-small-black.svg')
    white=(KIT/'masters/altstack-symbol-small.svg').read_text().replace('#000000','#ffffff')
    (KIT/'digital/svg/altstack-symbol-small-white.svg').write_text(white)
    shutil.copyfile(KIT/'masters/altstack-symbol-white-optical.svg',KIT/'digital/svg/altstack-symbol-white-optical.svg')
    # Normalize accessible titles, including wrappers emitted by the export helper.
    for path in (KIT/'digital/svg').glob('*.svg'):
        root=ET.parse(path).getroot()
        for parent in root.iter():
            for child in list(parent):
                if child.tag.endswith('title'): parent.remove(child)
        title=ET.Element(f'{{{SVG_NS}}}title',{'id':'title'});title.text=path.stem.replace('altstack','Altstack').replace('-',' ')
        root.insert(0,title);root.set('role','img');root.set('aria-labelledby','title')
        ET.register_namespace('',SVG_NS);path.write_text(ET.tostring(root,encoding='unicode')+'\n')
    for color in ['black','white']:
        for size in [16,32,64,128,256,512,1024,2048]:
            run('python3',script/'render_png.py',KIT/'digital/svg'/f'altstack-symbol-{color}.svg','--size',size,
                '-o',KIT/'digital/png'/f'altstack-symbol-{color}-{size}.png')
        for stem in ['altstack-logo-horizontal','altstack-logo-stacked','altstack-wordmark']:
            root=ET.parse(KIT/'digital/svg'/f'{stem}-{color}.svg').getroot()
            _,_,width,height=map(float,root.get('viewBox').split())
            for pixels in [256,512,1024,2048]:
                run('python3',script/'render_png.py',KIT/'digital/svg'/f'{stem}-{color}.svg',
                    '--width',pixels,'--height',round(pixels*height/width),'-o',KIT/'digital/png'/f'{stem}-{color}-{pixels}.png')
    for size in [512,1024]:
        run('python3',script/'render_png.py',KIT/'digital/svg/altstack-symbol-app-icon.svg','--size',size,
            '-o',KIT/'digital/png'/f'altstack-app-icon-{size}.png')
    run('python3',script/'export_variants.py',KIT/'masters/altstack-symbol.svg','--out-dir',KIT/'web',
        '--name','altstack','--only','--web-icons','--icon-bg','#000000','--icon-fg','#ffffff',
        '--icon-scale','0.56','--optical-offset','0','--favicon-source',KIT/'masters/altstack-symbol-small.svg')
    # Favicon drawing stays on the canonical integer grid, without a second fit transform.
    for size in [16,32,48]:
        run('python3',script/'render_png.py',KIT/'masters/altstack-symbol-small.svg','--size',size,
            '-o',KIT/'web'/f'favicon-{size}.png')
    run('python3',script/'render_png.py',KIT/'masters/altstack-symbol-small.svg','--ico',KIT/'web/favicon.ico','--ico-sizes','16','32','48')
    shutil.copyfile(KIT/'masters/altstack-symbol-small.svg',KIT/'web/altstack-favicon.svg')
    favicon=ET.parse(KIT/'masters/altstack-symbol-small.svg').getroot()
    style=ET.Element(f'{{{SVG_NS}}}style')
    style.text='@media (prefers-color-scheme: dark) { :root { fill: #ffffff; } }'
    favicon.insert(1,style)
    ET.register_namespace('',SVG_NS)
    (KIT/'web/favicon.svg').write_text(ET.tostring(favicon,encoding='unicode')+'\n')
    manifest=json.loads((KIT/'web/site.webmanifest').read_text());manifest.update({'name':'Altstack','short_name':'Altstack','start_url':'.'})
    for icon in manifest['icons']: icon['src']=icon['src'].lstrip('/')
    (KIT/'web/site.webmanifest').write_text(json.dumps(manifest,indent=2)+'\n')
    (KIT/'web/head-snippet.html').write_text('''<!-- Copy web/ assets to your public root before using these paths. -->
<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#000000">
''')
    print(f'Exported {len(list((KIT/"digital/svg").glob("*.svg")))} SVGs, '
          f'{len(list((KIT/"digital/png").glob("*.png")))} PNG exports, and the complete web-icon set.')
