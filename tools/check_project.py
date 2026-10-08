#!/usr/bin/env python3
"""Validate project contract, BPMN references/DI and SQL invariants."""
from pathlib import Path
import json
import sqlite3
import subprocess
import sys
import xml.etree.ElementTree as ET
from openapi_spec_validator import validate

ROOT = Path(__file__).resolve().parents[1]
B = '{http://www.omg.org/spec/BPMN/20100524/MODEL}'
D = '{http://www.omg.org/spec/BPMN/20100524/DI}'

validate(json.loads((ROOT/'project/openapi.json').read_text()))
for path in (ROOT/'project/bpmn').glob('*.bpmn'):
    tree = ET.parse(path)
    ids = [e.get('id') for e in tree.iter() if e.get('id')]
    assert len(ids) == len(set(ids)), f'duplicate id in {path}'
    index = {e.get('id'): e for e in tree.iter() if e.get('id')}
    process = tree.find(B+'process')
    nodes = {e.get('id') for e in process if e.tag not in (B+'laneSet',B+'sequenceFlow')}
    for flow in process.findall(B+'sequenceFlow'):
        assert flow.get('sourceRef') in nodes and flow.get('targetRef') in nodes
        source, target = index[flow.get('sourceRef')], index[flow.get('targetRef')]
        assert flow.get('id') in [x.text for x in source.findall(B+'outgoing')]
        assert flow.get('id') in [x.text for x in target.findall(B+'incoming')]
    for node in process.findall(B+'boundaryEvent'):
        assert node.get('attachedToRef') in nodes
        assert node.find('.//'+B+'timeDuration').text == 'PT2H'
    for gateway in process.findall(B+'exclusiveGateway'):
        assert gateway.get('default') in index
    for ref in tree.iter(B+'flowNodeRef'):
        assert ref.text in nodes
    diagram_ids = {x.get('bpmnElement') for x in tree.iter() if x.tag in (D+'BPMNShape',D+'BPMNEdge')}
    assert nodes <= diagram_ids, f'missing diagram shapes: {path}'
    for element in tree.iter():
        for attr in ('sourceRef','targetRef','processRef','messageRef','bpmnElement'):
            if element.get(attr): assert element.get(attr) in index
    assert ET.parse(path.with_suffix('.svg')).getroot().tag.endswith('svg')
    print('BPMN structure PASS',path.name)

subprocess.run([sys.executable,str(ROOT/'examples/sql/lab/run.py'),'--check','solutions'],check=True)
# Database constraints matter independently of query result snapshots.
db=sqlite3.connect(':memory:')
for name in ['schema.sql','seed.sql']:
    db.executescript((ROOT/'examples/sql/lab'/name).read_text())
for sql in [
    "INSERT INTO appointments VALUES(99,107,2,'CONFIRMED','2026-10-01T00:00:00Z')",
    "INSERT INTO appointments VALUES(99,999,2,'CONFIRMED','2026-10-01T00:00:00Z')",
    "INSERT INTO appointments VALUES(99,106,2,'UNKNOWN','2026-10-01T00:00:00Z')",
]:
    try:
        db.execute(sql)
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError('Invalid data unexpectedly accepted: '+sql)
print('PASS project contract, BPMN structure, SQL results and constraints')
