#!/usr/bin/env python3
"""Render the reviewed outlook rows; --check also validates baseline identity."""
import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABELS = {'Proven halting', 'Probable halting', 'Possible halting', 'Unknown',
          'Probable nonhalting', 'Proven nonhalting'}


def generate():
    baseline = json.loads((HERE / 'baseline.json').read_text())
    for file, field in [('SIMULATION_TABLE.md', 'simulation_table_sha256'),
                        ('BB2x5_Rocq_holdouts_37.txt', 'holdouts_sha256')]:
        assert hashlib.sha256((ROOT / file).read_bytes()).hexdigest() == baseline[field], file
    rows = json.loads((HERE / 'rows.json').read_text())
    originals = [(int(n), m) for n, m in re.findall(
        r'^\| (\d+) \| `([^`]+)`', (ROOT / 'SIMULATION_TABLE.md').read_text(), re.M)]
    assert len(rows) == len(originals) == 37
    assert [(r['line'], r['machine']) for r in rows] == originals
    out = (HERE / 'table-intro.txt').read_text().rstrip() + '\n'
    for row in rows:
        assert row['outlook'] in LABELS
        fields = [str(row['line']), f"`{row['machine']}`", row['structure'],
                  row['outlook'], row['floor'], row['estimate'], row['evidence'],
                  f"[Analysis](halting-outlook/{row['report']})"]
        assert all('|' not in field and '\n' not in field for field in fields)
        out += '| ' + ' | '.join(fields) + ' |\n'
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    target = ROOT / 'HALTING_OUTLOOK.md'
    content = generate()
    if args.check:
        assert target.read_text() == content, 'Outlook table needs regeneration'
        for row in json.loads((HERE / 'rows.json').read_text()):
            path, _, anchor = row['report'].partition('#')
            report = HERE / path
            assert report.is_file(), report
            if anchor:
                text = report.read_text()
                explicit = f'id="{anchor}"' in text or f"id='{anchor}'" in text
                headings = re.findall(r'^#+ (.+)', text, re.M)
                slugs = [re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in headings]
                assert explicit or anchor in slugs, (path, anchor)
        print('37 original rows and full strings; baseline hashes, labels, reports and table: OK')
    else:
        target.write_text(content)


if __name__ == '__main__':
    main()
