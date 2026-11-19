"""Check the 57 segments of the BB(6) line 448 proof with Coq 8.18.0."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

SOURCE = Path(__file__).resolve().parent
PREFIX = """From BusyCoq Require Import Individual62 Line448Engine.
From Coq Require Import List NArith ZArith PrimInt63.
From Coq Require Uint63.
Require Import ChunkTools.
Import ListNotations Line448Engine.H155900.
"""
FIRST = [0, 10000, 131072, 180224, 212992, 245760]
MIDDLE = [*range(245760, 393216, 4096), *range(393216, 423937, 2048)]
POINTS = FIRST[:-1] + MIDDLE
TOKEN = re.compile(r"0x[0-9a-f]+|[A-Za-z_][A-Za-z0-9_]*|[][();,]")


def numeral(token):
    value = int(token, 16)
    if value < 1 << 17:
        return token + "%N"
    limbs = []
    while value:
        limbs.append(hex(value % (1 << 60)) + "%uint63")
        value >>= 60
    return "(from_limbs [" + ";".join(reversed(limbs)) + "])"


def state_source(raw):
    definitions = []
    stream = iter(TOKEN.findall(raw))

    def coq_list():
        words = []
        current = []
        for token in stream:
            if token in ("]", ";"):
                if current:
                    words.append(" ".join(current))
                    current = []
                if token == "]":
                    break
            else:
                current.append(render(token))
        if len(words) <= 48:
            return "[" + ";".join(words) + "]"
        kind = "Runs" if "SW_" in words[0] else "Digits" if words[0].startswith("(") else "list Sym"
        names = []
        for offset in range(0, len(words), 32):
            name = "cells" + str(len(definitions))
            values = ";".join(words[offset:offset+32])
            definitions.append(f"Definition {name} : {kind} := [{values}].")
            names.append(name)
        return "(List.concat [" + ";".join(names) + "])"

    def render(token):
        if token == "[":
            return coq_list()
        if token.startswith("0x"):
            return numeral(token)
        return token

    state = " ".join(render(token) for token in stream)
    return PREFIX + "\n".join(definitions) + "\nDefinition checkpoint : FastState := " + state + ".\n"


def first_segment(n, m):
    span = m - n
    powers = ";".join(f"{i}%nat" for i in range(span.bit_length()) if (1 << i) & span)
    ps = "[" + powers + "]"
    return PREFIX + f"""Require S{n} S{m}.
Lemma checked : pieces {ps} S{n}.checkpoint = Some S{m}.checkpoint.
Proof. vm_check_eq. Qed.
Lemma segment : halts src_tm (fs_denote S{m}.checkpoint) -> halts src_tm (fs_denote S{n}.checkpoint).
Proof. intro h. apply (backwards {ps} S{n}.checkpoint). rewrite checked. exact h. Qed.
"""


def middle_segment(n, m):
    span = m - n
    assert span and span & (span - 1) == 0
    k = span.bit_length() - 1
    return PREFIX + f"""
Require S{n} S{m}.
Lemma verified : run_pow {k} S{n}.checkpoint = Some S{m}.checkpoint.
Proof. vm_check_eq. Qed.
Lemma segment : halts src_tm (fs_denote S{m}.checkpoint) -> halts src_tm (fs_denote S{n}.checkpoint).
Proof.
  intro ht. pose proof (run_pow_spec {k} S{n}.checkpoint) as H.
  rewrite verified in H. exact (evstep_halts _ _ H ht).
Qed.
"""


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("witness_dir", type=Path, help="directory built by replay_line448.sh in witness mode")
    parser.add_argument("--jobs", type=int, default=2, help="simultaneous Coq checks (default 2)")
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    witness = args.witness_dir.resolve()
    lib = witness / "BusyCoq"
    version = subprocess.check_output(["coqc", "--version"])
    signature = hashlib.sha256(version)
    for path in [SOURCE/"replay.py", SOURCE/"dump.ml", SOURCE/"ChunkTools.v",
                 SOURCE/"Part17.v", SOURCE/"Joined448.v", witness/"Line448Sweeps.v",
                 lib/"Line448Engine.vo", witness/"engine448.cmx"]:
        signature.update(path.read_bytes())
    output = witness / ("line448-checkpoints-" + signature.hexdigest()[:16])
    output.mkdir(exist_ok=True)
    print(f"Checking in {output}", flush=True)
    for name in ["ChunkTools.v", "Part17.v", "Joined448.v", "dump.ml"]:
        shutil.copyfile(SOURCE/name, output/name)
    shutil.copyfile(witness/"Line448Sweeps.v", output/"Line448Sweeps.v")
    missing = [n for n in POINTS if not (output/f"S{n}.v").is_file()]
    if missing:
        subprocess.run(["ocamlfind","ocamlopt","-O3","-thread","-rectypes","-package",
                        "zarith,coq-core.kernel","-linkpkg","-I",str(witness),
                        str(witness/"engine448.cmx"),"dump.ml","-o","dump448"],cwd=output,check=True)
        subprocess.run([str(output/"dump448"), *map(str, missing)], cwd=output, check=True)
        for n in missing:
            raw = output/f"state-{n}.txt"
            path = output/f"S{n}.v"
            temporary = path.with_suffix(".tmp")
            temporary.write_text(state_source(raw.read_text()), encoding="utf-8")
            temporary.replace(path)
            raw.unlink()
    first_names = []
    for i, (n,m) in enumerate(zip(FIRST, FIRST[1:])):
        name = f"Part{i}"
        (output/f"{name}.v").write_text(first_segment(n,m))
        first_names.append(name)
    for n,m in zip(MIDDLE, MIDDLE[1:]):
        (output/f"J{n}.v").write_text(middle_segment(n,m))
    env = dict(os.environ)
    env.setdefault("OCAMLRUNPARAM", "o=35,O=250,s=512k")

    def build(name):
        if (output/f"{name}.vo").is_file():
            return
        log = output/f"{name}.log"
        with log.open("w") as out:
            result = subprocess.run(["coqc","-q","-Q",str(lib),"BusyCoq",name+".v"],
                                    cwd=output,env=env,stdout=out,stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"{name} failed. See {log}\n{log.read_text()[-1000:]}")
        print(f"Checked {name}",flush=True)

    build("ChunkTools")
    build("Line448Sweeps")
    with ThreadPoolExecutor(args.jobs) as pool:
        list(pool.map(build, (f"S{n}" for n in POINTS)))
        list(pool.map(build, first_names + [f"J{n}" for n in MIDDLE[:-1]] + ["Part17"]))
    build("Joined448")
    print((output/"Joined448.log").read_text(),end="")


if __name__ == "__main__":
    run()
