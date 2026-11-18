#!/usr/bin/env python3
"""Reproduce exact_blocks pilots, full-state benchmarks, and deep checkpoints.

Benchmark timing compares this Python accelerator with prior_sweeps.TapeMachine
at an IDENTICAL complete configuration and raw step count. It is not a comparison
with the fastest available TM simulator. All searches remain bounded experiments.
"""
import argparse
import json
from pathlib import Path
import platform
import time

from exact_blocks import Engine, ResourceLimit, Run, integer_text, save_checkpoint
from prior_sweeps import TapeMachine

DATA = Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt')


def numbers(text):
    return [int(x) for x in text.split(',')]


def simulate(encoding, level, work, macros):
    start = time.perf_counter()
    engine = Engine(encoding, max_work=work, max_nodes=work + 100,
                    max_cache=work + 100)
    run = Run.blank(engine, level)
    reason = 'macro budget'
    try:
        for _ in range(macros):
            run.advance(engine)
            if run.status != 'running':
                reason = run.status
                break
    except ResourceLimit as error:
        reason = str(error)
    elapsed = time.perf_counter() - start
    record = {'machine': encoding, 'level': level, 'steps': integer_text(run.steps),
              'macros': run.macros, 'work': engine.work, 'misses': engine.misses,
              'hits': engine.hits, 'nodes': len(engine.blocks.nodes),
              'cache': len(engine.cache), 'seconds': elapsed,
              'reason': reason, 'status': 'unknown' if run.status == 'running' else run.status,
              'head': integer_text(run.head), 'state': chr(65 + run.state)}
    return engine, run, record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['pilot', 'benchmark', 'deep'])
    parser.add_argument('--lines', type=numbers)
    parser.add_argument('--levels', type=numbers)
    parser.add_argument('--work', type=int)
    parser.add_argument('--macros', type=int)
    parser.add_argument('--output', type=Path, required=True,
                        help='result JSON; deep checkpoints saved beside it')
    args = parser.parse_args()
    if args.mode == 'pilot':
        lines = args.lines or [x for x in range(1, 38) if x not in (2, 10, 17, 26)]
        levels = args.levels or [6, 10, 14]
        work, macros = args.work or 100000, args.macros or 50000
    else:
        lines, levels = args.lines or [29, 30, 31], args.levels or [10]
        work = args.work or (1000000 if args.mode == 'deep' else 200000)
        macros = args.macros or (1000000 if args.mode == 'deep' else 5000)
    machines = DATA.read_text().splitlines()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for line in lines:
        if not 1 <= line <= len(machines):
            parser.error(f'invalid line {line}')
        for level in levels:
            engine, run, record = simulate(machines[line-1], level, work, macros)
            record['line'] = line
            if args.mode == 'benchmark':
                literal = TapeMachine(machines[line-1])
                start = time.perf_counter()
                for _ in range(run.steps):
                    if not literal.step():
                        raise AssertionError('literal halted before accelerated endpoint')
                record['literal_seconds'] = time.perf_counter() - start
                assert (literal.head, literal.state, literal.tape) == (run.head, chr(65+run.state), run.sparse_tape(engine))
                record['full_state_equal'] = True
                record['speedup_over_python_literal'] = record['literal_seconds'] / record['seconds']
            if args.mode == 'deep':
                document = run.checkpoint(engine)
                checkpoint = args.output.with_name(f'line-{line}-level-{level}.json')
                save_checkpoint(run, engine, checkpoint)
                fresh = Engine(run.encoding, max_nodes=work + 100)
                resumed = Run.restore(fresh, json.loads(checkpoint.read_text()))
                assert resumed.checkpoint(fresh) == document
                record['checkpoint'] = checkpoint.name
                record['checkpoint_sha256'] = document['sha256']
                record['checkpoint_roundtrip_equal'] = True
                engine.max_work += 1000000
                fresh.max_work += 1000000
                for _ in range(100):
                    run.advance(engine)
                    resumed.advance(fresh)
                assert run.checkpoint(engine) == resumed.checkpoint(fresh)
                record['resume_100_macros_equal'] = True
            records.append(record)
            print(json.dumps(record, sort_keys=True), flush=True)
    report = {'python': platform.python_version(), 'platform': platform.platform(),
              'mode': args.mode, 'work_budget': work, 'macro_budget': macros,
              'note': 'Timing is environment-specific. No new blank-tape classification is claimed.',
              'records': records}
    args.output.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
