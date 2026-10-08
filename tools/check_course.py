#!/usr/bin/env python3
"""Check local Markdown targets, diagram mapping and PNG integrity."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
from diagram_catalog import GROUPS

errors = []
for doc in ROOT.rglob('*.md'):
    if '.git' in doc.parts:
        continue
    text = re.sub(r'```.*?```', '', doc.read_text(), flags=re.S)
    for raw in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text):
        target = raw.split('#')[0]
        if not target or re.match(r'^[a-zA-Z][\w+.-]*:', target):
            continue
        if not (doc.parent / target).exists():
            errors.append(f'{doc.relative_to(ROOT)}: missing {raw}')
    if len(re.findall(r'^```', doc.read_text(), flags=re.M)) % 2:
        errors.append(f'{doc.relative_to(ROOT)}: unclosed fenced block')
count = 0
for source, dest in GROUPS:
    expected = set()
    for diagram in (ROOT/source).glob('*.puml'):
        text = diagram.read_text()
        match = re.search(r'^@startuml[ \t]+(\S+)', text, re.M)
        if not match or text.count('@startuml') != 1 or text.count('@enduml') != 1:
            errors.append(f'{diagram.relative_to(ROOT)}: invalid diagram envelope')
            continue
        output = match[1]+'.png'
        if output in expected:
            errors.append(f'{source}: duplicate output {output}')
        expected.add(output)
        image = ROOT/dest/output
        if not image.exists():
            errors.append(f'{image.relative_to(ROOT)}: missing rendered image')
            continue
        try:
            with Image.open(image) as im:
                im.verify()
            with Image.open(image) as im:
                if im.width < 50 or im.height < 50:
                    errors.append(f'{image.relative_to(ROOT)}: suspicious dimensions')
        except Exception as exc:
            errors.append(f'{image.relative_to(ROOT)}: {exc}')
        vector = image.with_suffix('.svg')
        if not vector.exists():
            errors.append(f'{vector.relative_to(ROOT)}: missing vector')
        else:
            try:
                ET.parse(vector)
            except ET.ParseError as exc:
                errors.append(f'{vector.relative_to(ROOT)}: {exc}')
        count += 1
    actual = {p.name for p in (ROOT/dest).glob('*.png')}
    if expected != actual:
        errors.append(f'{dest}: stale images {sorted(actual-expected)}')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'OK: local links, fenced blocks, {count} diagram/image pairs and PNG integrity')
