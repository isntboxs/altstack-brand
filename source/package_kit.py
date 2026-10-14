#!/usr/bin/env python3
"""Refresh checksums and build a distributable ZIP from tracked kit files."""
from pathlib import Path
import hashlib
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent.parent
tracked = subprocess.check_output(
    ['git', 'ls-files', '-z'], cwd=ROOT
).decode().split('\0')
files = sorted(ROOT / p for p in tracked if p and p != 'SHA256SUMS.txt')
checksums = ''.join(
    f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}\n'
    for p in files
)
(ROOT / 'SHA256SUMS.txt').write_text(checksums)
folder = ROOT / 'dist'
folder.mkdir(exist_ok=True)
output = folder / 'altstack-logo-kit.zip'
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for p in files + [ROOT / 'SHA256SUMS.txt']:
        archive.write(p, 'altstack-logo-kit/' + p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(output) as archive:
    assert archive.testzip() is None
print(f'Packaged {len(files) + 1} files: {output}')
