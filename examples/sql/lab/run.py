#!/usr/bin/env python3
"""Deterministic SQLite exercises; --check never executes writes."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parent

def database():
    db = sqlite3.connect(':memory:')
    db.executescript((ROOT/'schema.sql').read_text())
    db.executescript((ROOT/'seed.sql').read_text())
    return db

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--init', type=Path)
    group.add_argument('--check', choices=['exercises','solutions'])
    args = parser.parse_args()
    if sqlite3.sqlite_version_info < (3,25,0):
        parser.error('SQLite 3.25+ is required')
    if args.init:
        # Exclusive creation avoids overwriting the learner's database.
        with args.init.open('xb'):
            pass
        with database() as source, sqlite3.connect(args.init) as target:
            source.backup(target)
        print(f'Created {args.init}')
        return
    expected = json.loads((ROOT/'expected.json').read_text())
    failures = 0
    for name, rows in expected.items():
        with database() as db:
            db.execute('PRAGMA query_only=ON')
            budget = [0]
            def stop_expensive_query():
                budget[0] += 1
                return budget[0] > 10000
            db.set_progress_handler(stop_expensive_query, 1000)
            try:
                actual = [list(row) for row in db.execute((ROOT/args.check/(name+'.sql')).read_text())]
                if actual != rows:
                    raise ValueError(f'expected {rows}, got {actual}')
                print(f'PASS {name}')
            except (sqlite3.Error, ValueError) as exc:
                failures += 1
                print(f'FAIL {name}: {exc}')
    if failures:
        sys.exit(1)

if __name__ == '__main__':
    main()
