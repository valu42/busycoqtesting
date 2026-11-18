"""Emit an untrusted numerical witness for the formal left-front checker.

Usage: python line36_rocq_left_potential.py BB2X5_DIR > Line36LeftPotential.v
An optional second argument reads a previously emitted state/value text table.
Only the generated integers enter the proof. The Rocq verifier reconstructs
the transitions independently from the word rules.
"""
from itertools import product
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


# Reuse the published state and edge enumerator, including its edge weights.
# Its source has a main function too, so compile that routine under another
# name. A malformed numerical witness simply fails the separate Rocq checker.
WITNESS_CPP = r'''#define main original_certificate_main
#include "line36_left.cpp"
#undef main
int main() {
    for (int t = 0; t < phases; ++t) {
        std::cin >> prefix[t] >> header_size[t];
        for (auto& alternatives : piece[t])
            std::cin >> alternatives[0] >> alternatives[1];
    }
    enumerate_states();
    vector<vector<Edge>> graph;
    for (const auto& s : states) graph.push_back(outgoing(s));
    vector<int> potential(states.size());
    for (int pass = 0; pass < 17; ++pass) {
        auto next = potential;
        for (size_t i = 0; i < states.size(); ++i)
            for (const auto& e : graph[i])
                next[e.destination] = std::min(next[e.destination], potential[i] + weight(e));
        potential.swap(next);
    }
    for (size_t i = 0; i < states.size(); ++i) {
        const auto& s = states[i];
        std::cout << s.phase << s.kind << s.last_choice << s.partial
                  << "|" << s.halo << " " << potential[i] << "\n";
    }
}
'''


def generate_values(bbdir, rows):
    table = []
    for prefix, pieces, header in rows:
        table.extend([prefix, str(header)])
        for kind in range(6):
            table.extend([pieces[kind, 0], pieces[kind, 1]])
    with TemporaryDirectory() as directory:
        source = Path(directory) / 'witness.cpp'
        binary = Path(directory) / 'witness'
        source.write_text(WITNESS_CPP)
        subprocess.run(['c++', '-std=c++17', '-O2', '-Wno-return-type', '-I', bbdir,
                        str(source), '-o', str(binary)], check=True)
        return subprocess.run([str(binary)], input='\n'.join(table)+'\n',
                              capture_output=True, text=True, check=True).stdout


def main():
    bbdir = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(bbdir))
    from line36_left import phases

    phase_rows = phases()
    records = (Path(sys.argv[2]).read_text() if len(sys.argv) > 2
               else generate_values(bbdir, phase_rows))
    vals = {key: int(value) for key, value in
            (line.split() for line in records.splitlines())}
    print('(** Explicit integer witness. The step checker recomputes every transition. *)')
    print('From Coq Require Import ZArith List.\nFrom BusyCoq Require Import Line36Left.')
    print('Import ListNotations L36Left.\nModule L36LeftPotential.\nLocal Open Scope nat_scope.')
    row_ids = {}
    group_ids = {}
    keys = []
    for t, (_, pieces, _) in enumerate(phase_rows):
        for k, prev, choice in product(range(6), range(2), range(2)):
            p = pieces[k, choice]
            group = []
            for n in range(len(p)):
                row = []
                for halo in range(8):
                    h = ''.join('2' if (halo >> i) & 1 else '1' for i in range(3))
                    row.append(vals[f'{t}{k}{prev}{p[:n]}|{h}'])
                values = tuple(row)
                number = row_ids.setdefault(values, len(row_ids))
                group.append(number)
            groups = tuple(group)
            number = group_ids.setdefault(groups, len(group_ids))
            keys.append(number)

    for v, i in row_ids.items():
        print(f'Definition r{i} (h : nat) : Z := match h with')
        for h, cost in enumerate(v):
            print(f'| {h} => ({cost})%Z', end=' ')
        print('| _ => 0%Z end.')
    for v, i in group_ids.items():
        print(f'Definition g{i} (n : nat) : nat -> Z := match n with')
        for n, rid in enumerate(v):
            print(f'| {n} => r{rid}', end=' ')
        print('| _ => fun _ => 0%Z end.')
    print('Definition raw (s : state) : Z := let index :=')
    print('  (((phase s*6 + kind s)*2 + (if last_choice s then 1 else 0))*2')
    print('    + (if partial_choice s then 1 else 0))%nat in')
    print(' (match index with')
    for idx, gid in enumerate(keys):
        print(f' | {idx} => g{gid}')
    print(' | _ => fun _ _ => 0%Z end) (partial_len s) (halo s).')
    print('Definition value := clipped raw.\nEnd L36LeftPotential.')


if __name__ == '__main__':
    main()
