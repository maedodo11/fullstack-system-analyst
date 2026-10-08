#!/usr/bin/env python3
"""Render verified SVG/PNG pairs from PlantUML without partial file replacement."""
from pathlib import Path
import io
import os
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image
from diagram_catalog import GROUPS

ROOT = Path(__file__).resolve().parents[1]

def main():
    if not shutil.which('java') or not shutil.which('dot'):
        raise SystemExit('Java 17+ and Graphviz (dot) are required')
    environment = dict(os.environ, GRAPHVIZ_DOT=shutil.which('dot'))
    # Pipe captures output in memory before Python writes it: incomplete Java exports
    # cannot overwrite the images being read on GitHub.
    with tempfile.TemporaryDirectory(prefix='.render-stage.', dir=ROOT) as directory:
        staging = Path(directory)
        count = 0
        for source_dir, output_dir in GROUPS:
            for source in sorted((ROOT/source_dir).glob('*.puml')):
                content = source.read_bytes()
                match = re.search(rb'^@startuml[ \t]+([^\s]+)', content, re.M)
                if not match:
                    raise ValueError(f'Missing explicit output name: {source}')
                name = match[1].decode('utf-8')
                if Path(name).name != name:
                    raise ValueError(f'Output name must be a filename: {name}')
                result = subprocess.run(
                    ['java','-Djava.awt.headless=true','-jar',str(ROOT/'plantuml.jar'),
                     '-pipe','-tsvg','-failfast','-nometadata','-charset','UTF-8'],
                    input=content, capture_output=True, env=environment, check=True)
                vector = ET.fromstring(result.stdout)
                if vector.tag != '{http://www.w3.org/2000/svg}svg':
                    raise ValueError(f'Not SVG: {source}')
                target = staging/output_dir/(name+'.svg')
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(result.stdout)
                png = cairosvg.svg2png(bytestring=result.stdout, background_color="#FFFFFF")
                with Image.open(io.BytesIO(png)) as image:
                    image.verify()
                target.with_suffix('.png').write_bytes(png)
                count += 1
        # No final images are changed until every render and raster check succeeds.
        for source in staging.rglob('*'):
            if source.is_file():
                target = ROOT/source.relative_to(staging)
                target.parent.mkdir(parents=True, exist_ok=True)
                os.replace(source, target)
    print(f'Rendered {count} verified SVG/PNG pairs')

if __name__ == '__main__':
    main()
