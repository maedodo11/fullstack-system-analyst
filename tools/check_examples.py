#!/usr/bin/env python3
"""Verify business invariants and SQL boundary result in educational examples."""
from pathlib import Path
import importlib.util
import json
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('payment_model', ROOT/'examples/payment/simulator.py')
model_module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = model_module
spec.loader.exec_module(model_module)
PaymentModel, Conflict = model_module.PaymentModel, model_module.Conflict

def rejects(exception, code, action):
    try:
        action()
    except exception as exc:
        assert str(exc) == code, (str(exc), code)
    else:
        raise AssertionError(f'Expected rejection: {code}')

m = PaymentModel()
p = m.create('buyer-A','key-1','O123','pm_demo')
assert m.create('buyer-A','key-1','O123','pm_demo').payment_id == p.payment_id
assert len(m.payments) == 1
rejects(Conflict,'IDEMPOTENCY_CONFLICT',lambda:m.create('buyer-A','key-1','O123','different'))
rejects(Conflict,'PAYMENT_ACTIVE',lambda:m.create('buyer-A','key-2','O123','pm_demo'))
rejects(PermissionError,'NOT_FOUND',lambda:m.create('buyer-B','key-1','O123','pm_demo'))
p.dispatched = True
rejects(Conflict,'PROVIDER_RESULT_REQUIRED',lambda:m.transition(p.payment_id,'CANCELLED'))
m.transition(p.payment_id,'UNKNOWN')
assert not m.orders['O123']['paid']
rejects(Conflict,'PAYMENT_ACTIVE',lambda:m.create('buyer-A','key-2','O123','pm_demo'))
rejects(Conflict,'INVALID_TRANSITION',lambda:m.transition(p.payment_id,'CANCELLED'))
m.webhook('evt-1',p.payment_id,'SUCCESS')
m.webhook('evt-1',p.payment_id,'SUCCESS')
assert len(m.events) == 1 and m.orders['O123']['paid']
rejects(Conflict,'EVENT_ID_CONFLICT',lambda:m.webhook('evt-1',p.payment_id,'FAILED'))
rejects(Conflict,'INVALID_TRANSITION',lambda:m.webhook('evt-2',p.payment_id,'FAILED'))
assert 'evt-2' not in m.events
rejects(Conflict,'ORDER_PAID',lambda:m.create('buyer-A','key-3','O123','pm_demo'))
assert m.create('buyer-A','key-1','O123','pm_demo').status == 'SUCCESS'
# Definitive failure permits a new attempt; cancellation is allowed only before dispatch.
n = PaymentModel()
first = n.create('buyer-A','a','O123','pm_demo')
n.transition(first.payment_id,'FAILED')
second = n.create('buyer-A','b','O123','pm_demo')
assert first.payment_id != second.payment_id
n.transition(second.payment_id,'CANCELLED')
assert n.create('buyer-A','c','O123','pm_demo').status == 'PENDING'
# Actual execution and exact comparison includes threshold and excluded-status rows.
connection = sqlite3.connect(':memory:')
sql = (ROOT/'examples/sql/having.sql').read_text()
setup, query = sql.split('SELECT city,',1)
connection.executescript(setup)
query = 'SELECT city,'+query
assert connection.execute(query).fetchall() == [('Иркутск',15000),('Казань',12000)]
assert connection.execute(query.replace('> 10000','> 15000')).fetchall() == []
connection.close()
# This checks cross-document agreement and references, not full OpenAPI validation.
api = json.loads((ROOT/'examples/payment/openapi.json').read_text())
assert set(api['components']['schemas']['Payment']['properties']['status']['enum']) == model_module.STATUSES
post = api['paths']['/v1/payments']['post']
assert '202' in post['responses'] and 'Location' in post['responses']['202']['headers']
assert set(post['requestBody']['content']['application/json']['schema']) == {'$ref'}
def refs(value):
    if isinstance(value,dict):
        for key,child in value.items():
            if key == '$ref':
                node = api
                for part in child.removeprefix('#/').split('/'):
                    node = node[part]
            else:
                refs(child)
    elif isinstance(value,list):
        for child in value:
            refs(child)
refs(api)
print('OK: repeat/conflict/ownership, timeout/late webhook, finality, retry after failure, SQL thresholds and contract agreement')
