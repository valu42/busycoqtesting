"""Generate the BB(6) research queue from the register, claim board and cited leads."""

import argparse
import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import NamedTuple

from tracker import ROOT, load_register


STATES = "ABCDEF"
LIMIT = 65_536
MOVES = (None, *product(range(2), (-1, 1), range(6)))
OUTCOMES = ("HALTS", "NONHALTS", "HALT_PR", "NONHALT_PR", "SIMULATED_HALT")
PAGE = ROOT / "RANKINGS.md"


class Source(NamedTuple):
    label: str
    url: str

    def link(self):
        return f"[{self.label}]({self.url})"


def read_sources(rows):
    sources = defaultdict(dict)
    kinds = {"replay", "checkpoint", "map", "structure", "halt_case", "analogy"}
    with (ROOT / "ranking_sources.csv").open(encoding="utf-8", newline="") as stream:
        for item in csv.DictReader(stream):
            line, kind = int(item["line"]), item["kind"]
            if (line not in rows or rows[line]["machine_id"] != item["machine_id"]
                    or kind not in kinds or kind in sources[line] or not item["label"] or not item["source"]):
                raise ValueError(f"invalid or duplicate ranking source for line {line}, {kind}")
            sources[line][kind] = Source(item["label"], item["source"])
    return sources


def read_claims():
    claims = defaultdict(list)
    board = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    section = board.split("## Claim board\n", 1)[1].split("\n## ", 1)[0]
    for row in section.splitlines():
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", row.strip().strip("|"))]
        if len(cells) >= 5 and cells[0].isdecimal():
            state = cells[2].strip("`")
            if state in {"CLAIMED", "BLOCKED"}:
                claims[int(cells[0])].append((f"{cells[1]} ({state.lower()})", cells[4]))
    return claims


def parse_table(machine):
    def parse(cell):
        if cell == "---":
            return None
        write, direction, state = cell
        return int(write), {"L": -1, "R": 1}[direction], STATES.index(state)

    return tuple(parse(cell) for pair in machine.split("_") for cell in (pair[:3], pair[3:]))


def instruction(move):
    if move is None:
        return "---"
    write, direction, state = move
    return f"{write}{'R' if direction == 1 else 'L'}{STATES[state]}"


def rooted_table(table, root):
    """Read both slots in discovery order, naming states from root and orienting the tape."""
    order, names, cells = [root], {root: 0}, []
    orientation = None
    for state in order:
        for move in table[2 * state : 2 * state + 2]:
            if move is None:
                cells.append(None)
                continue
            write, direction, target = move
            if target not in names:
                names[target] = len(order)
                order.append(target)
            if orientation is None:
                orientation = direction
            cells.append((write, direction == orientation, names[target]))
    # A partial traversal cannot witness a match of two complete six-state tables.
    return (tuple(cells) if len(order) == 6 else None), orientation


class Match(NamedTuple):
    peer: int
    entry: int
    mirrored: bool
    slot: int | None
    replacement: tuple | None


def related_tables(tables, references, open_lines):
    all_roots, cited_roots = defaultdict(list), defaultdict(list)
    for peer, table in tables.items():
        for entry in range(6):
            key, orientation = rooted_table(table, entry)
            if key is not None:
                record = (peer, entry, orientation)
                all_roots[key].append(record)
                if peer in references:
                    cited_roots[key].append(record)

    families, analogues = {}, {}
    for line in open_lines:
        table = tables[line]
        key, orientation = rooted_table(table, 0)
        family = [Match(peer, entry, other != orientation, None, None)
                  for peer, entry, other in all_roots.get(key, ()) if peer != line]
        # Keep one mapped blank entry per peer if a table has an automorphism.
        families[line] = {}
        for m in sorted(family):
            if m.peer in open_lines:
                families[line].setdefault(m.peer, m)
        matches = [m for m in family if m.peer in references]
        # Change a slot in the candidate's own alphabet, then compare all twelve
        # slots. This also finds matches whose differing edge changes discovery order.
        for slot, old in enumerate(table):
            for change in MOVES:
                if change == old:
                    continue
                key, orientation = rooted_table(table[:slot] + (change,) + table[slot + 1:], 0)
                for peer, entry, other in cited_roots.get(key, ()):
                    if peer != line:
                        matches.append(Match(peer, entry, other != orientation, slot, change))
        analogues[line] = matches
    return families, analogues


@dataclass
class Probe:
    first_read: list
    halt: int | None
    records: int
    edge: str
    last_step: int
    variety: int
    period: int
    support: int


def probe(table, limit=LIMIT):
    tape = bytearray(2 * limit + 9)
    head = lo = hi = limit + 4
    state = mid = last_step = 0
    reads, events = [None] * 12, []
    halt = None
    for step in range(limit + 1):
        slot = 2 * state + tape[head]
        if reads[slot] is None:
            reads[slot] = step
        move = table[slot]
        if move is None:
            halt = step
            break
        if step == limit:
            break
        write, delta, state = move
        tape[head] = write
        head += delta
        if lo <= head <= hi:
            continue
        if head > hi:
            hi = head
            side, inside = "R", tape[head - 4 : head][::-1]
        else:
            lo = head
            side, inside = "L", tape[head + 1 : head + 5]
        events.append((side, state, bytes(inside)))
        last_step = step + 1
        if last_step <= limit // 2:
            mid += 1

    period = support = 0
    if mid >= 12 and len(events) - mid >= 12:
        for p in range(1, 5):
            start = len(events) - p
            while start and events[start - 1] == events[start - 1 + p]:
                start -= 1
            if mid - start >= 12:
                period, support = p, len(events) - start
                break
    edge = "—"
    if events:
        side, state, bits = events[-1]
        edge = f"{side}/{STATES[state]}/" + "".join(map(str, bits))
    return Probe(reads, halt, len(events), edge, last_step, len(set(events[-24:])), period, support)


TIERS = [
    ("Replay a decision", "Check the cited theorem or replay the finite halt from blank, including its assumptions."),
    ("Adapt a decision argument", "A theorem or proposed proof supplies either a complete table match or a single changed instruction with the same blank entry. Check the entry or the altered branch before reusing the argument."),
    ("Decide a representative", "Follow the representative's blank orbit. A decision can also settle its linked lines once the equivalence is verified."),
    ("Resume a checkpoint", "The cited work identifies the machine and a resumable calculation. Seek an invariant or a reachable halting case in the recorded model."),
    ("Analyze a return map", "Start at the specified seed. Prove that its iterates reach a halting branch or stay in a closed set of continuing states."),
    ("Use a structural reduction", "Use the cited stack, odometer or tape invariant to write the return rules for the reachable start and check their halting exits."),
    ("Transfer a related model", "Translate the peer's model to the listed entry. Check each changed instruction on the new blank orbit."),
    ("Test a repeating tape edge", "Derive a return rule for the repeated edge signature and test it against the full interior tape at the next extension."),
    ("Compare blank starts", "Use one transition table for the listed open lines. Compare the complete configurations reached from their distinct initial states."),
    ("Collect the next edge records", "Replay through the last extension shown. Compare the interior tape at the next occurrence of that side, state and four-bit word."),
]


def cited_reference(row, sources):
    if "replay" in sources:
        return 0, sources["replay"].link()
    status = row["status"]
    if status in OUTCOMES:
        level = 0 if status in {"HALTS", "NONHALTS"} else 2 if status == "SIMULATED_HALT" else 1
        return level, f"[{status} source]({row['source']})"
    for kind in ("checkpoint", "map", "structure"):
        if kind in sources:
            return 3, sources[kind].link()
    return None


def describe_match(match, table, trace, link):
    entry = f"A → {STATES[match.entry]}" + (" mirrored" if match.mirrored else "")
    text = f"Compare line {match.peer} ({link}), `{entry}`"
    if match.slot is None:
        return text + ", all 12 instructions match."
    slot = match.slot
    visit = trace.first_read[slot]
    when = f"first read at step {visit:,}" if visit is not None else f"unseen through step {LIMIT:,}"
    return (f"{text}. At `{STATES[slot // 2]}{slot % 2}` ({when}), the candidate uses "
            f"`{instruction(table[slot])}` and the aligned peer uses `{instruction(match.replacement)}`.")


def assess(line, table, trace, own, children, matches, references, siblings):
    def match_key(m):
        return (m.slot is not None, m.entry != 0, references[m.peer][0], m.peer)

    leads = " · ".join(own[k].link() for k in
                       ("replay", "checkpoint", "map", "structure", "halt_case", "analogy") if k in own)
    if trace.halt is not None:
        return 0, (0,), f"Replay the undefined instruction after {trace.halt:,} steps."
    if "replay" in own:
        return 0, (1,), leads
    transfer = [m for m in matches if references[m.peer][0] < 2 and (m.slot is None or m.entry == 0)]
    if transfer:
        best = min(transfer, key=match_key)
        return 1, match_key(best)[:3], describe_match(best, table, trace, references[best.peer][1])
    if children:
        aliases = ", ".join(f"[{r['line']} ({r['status']})]({r['source']})" for r in children)
        return 2, (-len(children),), f"Linked to {aliases}. {leads}".rstrip()
    if "checkpoint" in own:
        return 3, ("analogy" not in own,), leads
    if "map" in own:
        return 4, ("halt_case" not in own,), leads
    if "structure" in own:
        return 5, (), leads
    if matches:
        best = min(matches, key=match_key)
        return 6, match_key(best)[:3], describe_match(best, table, trace, references[best.peer][1])
    if "analogy" in own:
        return 6, (2,), leads
    if trace.period:
        return 7, (trace.period, -trace.support), f"Period {trace.period} across the last {trace.support} edge records."
    if siblings:
        size = min(trace.records, 24)
        return 8, (-len(siblings), 24 - size, trace.variety), f"Compare the mapped starts at the next `{trace.edge}` extension."
    size = min(trace.records, 24)
    return 9, (24 - size, trace.variety), f"{trace.variety} different signatures in the last {size} records."


def line_link(line):
    return f"[{line}](BB6_holdouts_608.txt#L{line})"


def review_order(numbers, rows, sources):
    # One checkout can serve several lines in the same pending proof.
    batches = defaultdict(list)
    for n in numbers:
        batches[rows[n]["source"]].append(n)

    def key(n):
        status = rows[n]["status"]
        if "replay" in sources[n]:
            tier = 0
        elif status in {"HALT_PR", "NONHALT_PR"}:
            tier = 1
        elif status == "SIMULATED_HALT":
            tier = 2
        else:
            tier = 3
        batch = batches[rows[n]["source"]]
        return tier, -len(batch), min(batch), n

    return sorted(numbers, key=key)


def render():
    rows = {int(row["line"]): row for row in load_register()}
    open_lines = {line for line, row in rows.items() if row["status"] == "OPEN"}
    claims, sources = read_claims(), read_sources(rows)
    tables = {line: parse_table(row["machine"]) for line, row in rows.items()}
    references = {n: ref for n, row in rows.items() if (ref := cited_reference(row, sources[n]))}
    families, matches = related_tables(tables, references, open_lines)
    children = defaultdict(list)
    for row in rows.values():
        if row["same_as_line"]:
            children[int(row["same_as_line"])].append(row)

    keys, reasons, samples = {}, {}, {}
    for n in open_lines:
        t = probe(tables[n])
        tier, order, reasons[n] = assess(n, tables[n], t, sources[n], children[n], matches[n], references, families[n])
        keys[n] = tier, order, -len(families[n]), n
        samples[n] = f"{t.records} · `{t.edge}` at {t.last_step:,}" if t.records else "0"
    ranking = sorted(open_lines, key=keys.get)
    fresh = [n for n in ranking if n not in claims]
    claimed = [n for n in ranking if n in claims]
    settled = [n for n, row in rows.items() if row["status"] in {"HALTS", "NONHALTS", "EQUIVALENT"}]
    review = review_order([n for n in rows if n not in open_lines and n not in settled], rows, sources)
    page = [
        "# BB(6) machine approach rankings", "",
        f"**{len(fresh)} fresh starts** · {len(claimed)} open lines with existing campaigns · "
        f"{len(review)} verification targets" + (f" · {len(settled)} settled entries" if settled else "") + f". All {len(rows)} permanent lines are included.", "",
        "The fresh queue orders campaigns by how precisely the next proof step is known and how many machines "
        "could use the work. The verification queue orders existing results by the evidence available to check.", "",
        "[Existing campaigns](#existing-campaigns) · [Verification queue](#verification-queue) · "
        "[Ranking method and reproduction](#ranking-method-and-reproduction) · [Claim board](ROADMAP.md#claim-board)", "",
        "| Fresh ranks | Approach | First line |", "|---:|---|---:|",
    ]
    offset = 0
    for tier, (title, _) in enumerate(TIERS):
        group = [n for n in fresh if keys[n][0] == tier]
        if group:
            span = str(offset + 1) if len(group) == 1 else f"{offset + 1}–{offset + len(group)}"
            page.append(f"| {span} | [{title}](#{title.lower().replace(' ', '-')}) | {group[0]} |")
            offset += len(group)

    rank = 0
    for tier, (title, intro) in enumerate(TIERS):
        group = [n for n in fresh if keys[n][0] == tier]
        if not group:
            continue
        page.extend(["", f"## {title}", "", intro, "",
                     "| Rank | Line | Machine ID | First check | Edge records · last signature and step | Other open starts |",
                     "|---:|---:|---:|---|---|---|"])
        for n in group:
            rank += 1
            peers = ", ".join(f"{m.peer} ({STATES[m.entry]}{' mirrored' if m.mirrored else ''})"
                              for m in families[n].values()) or "—"
            page.append(f"| {rank} | {line_link(n)} | {rows[n]['machine_id']} | {reasons[n]} | {samples[n]} | {peers} |")
    page.extend(["", "## Existing campaigns", "",
                 "Coordinate on the [claim board](ROADMAP.md#claim-board). The position shown is where each "
                 "line would enter the fresh queue if that campaign alone were released.", "",
                 "| Position if released | Line | Machine ID | Campaign | Current proof question |", "|---:|---:|---:|---|---|"])
    for n in claimed:
        position = 1 + sum(keys[m] < keys[n] for m in fresh)
        work = " · ".join(c[0] for c in claims[n])
        questions = " · ".join(c[1] for c in claims[n])
        if "replay" in sources[n]:
            questions += " " + sources[n]["replay"].link()
        page.append(f"| {position} | {line_link(n)} | {rows[n]['machine_id']} | {work} | {questions} |")
    page.extend(["", "## Verification queue", "",
                 "First cross-check rows with a second theorem source, then review proposed decisions, reported simulation halts and proposed equivalences. "
                 "Within each group, prefer sources covering more pending rows so one checkout can serve several machines. "
                 "Ties go to the earliest line in the source batch, then the permanent line.", "",
                 "| Review rank | Line | Machine ID | Register status | Evidence to check |", "|---:|---:|---:|---|---|"])
    for position, n in enumerate(review, 1):
        row = rows[n]
        follow = [f"[Register source]({row['source']})"]
        if row["same_as_line"]:
            follow.append("representative " + line_link(row["same_as_line"]))
        if row["simulation_log"]:
            follow.append(f"[simulation log]({row['simulation_log']})")
        if "replay" in sources[n]:
            follow.append(sources[n]["replay"].link())
        page.append(f"| {position} | {line_link(n)} | {row['machine_id']} | `{row['status']}` | {' · '.join(follow)} |")
    if settled:
        page.extend(["", "## Verified decisions and equivalences", "",
                     "| Line | Machine ID | Status | Evidence |", "|---:|---:|---|---|"])
        for n in settled:
            row = rows[n]
            evidence = f"[Verification]({row['source']})"
            if row["same_as_line"]:
                evidence += " · representative " + line_link(row["same_as_line"])
            page.append(f"| {line_link(n)} | {row['machine_id']} | `{row['status']}` | {evidence} |")
    page.extend(["", "## Ranking method and reproduction", "",
                 "1. Only `OPEN` rows can enter the fresh queue. A `CLAIMED` or `BLOCKED` board row moves the line to existing campaigns. Check renewal dates and branches before claiming.",
                 "2. Use the first applicable approach in page order. Exact outcome replays take precedence over all transfers. "
                 "The source catalogue matches machine identities across list editions. It links to individual theorem statements, return maps and checkpoints. "
                 "Published models and machine-specific halt conditions still require an argument from the actual blank start.",
                 "3. Compare both read slots under state renaming and global left/right reflection, keeping symbol 0 blank. "
                 "For a one-instruction match, substitute each possible instruction (including halt) into one candidate slot and compare all twelve again. "
                 "`A → E` means candidate state A corresponds to E in the peer. A changed entry state can change the blank orbit. "
                 "In the last column, `N (B mirrored)` means this line's blank A corresponds to line N's B on a reflected tape.",
                 f"4. Run each open line from blank A for up to {LIMIT:,} elementary steps. A record is the first arrival outside the visited interval. "
                 "`R/B/1011` means a new rightmost cell in state B with interior bits 1011 read inward, nearest first. "
                 "The edge tier requires a period of 1–4 on a continuous suffix with at least 12 records in each half of the run. "
                 "Only a local tape window repeats. A nonhalting proof must also cover the interior and establish infinite progress.",
                 "5. Within a transfer tier prefer fewer changed slots, the same entry and then verified or theorem-backed outcomes, proposed outcomes, simulation reports and models, in that order. "
                 "Prefer representatives with more linked lines, checkpoints with a second proof comparison, and return maps with an explicit halting residue class. "
                 "For edge repetitions prefer the smaller period, then the longer suffix. For shared tables prefer more other open starts. "
                 "In the last two tiers prefer a full 24-record sample, then fewer distinct signatures. "
                 "Remaining ties go to more other open starts on the same table, then the lower permanent line.", "",
                 "The [Lean BB(6) catalogue](https://github.com/google-deepmind/cryptids/tree/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6) "
                 "supplies exact-machine theorem and model links. The [623-entry research diary](https://github.com/valu42/busycoqtesting/tree/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623) "
                 "supplies earlier checkpoints. Their transition strings were matched to the 608-entry register, including the documented reflections for four cubic machines. "
                 "All line numbers on this page use the 608-entry list.", "",
                 "From `research/bb6/`, run `python3 rank.py --write` to refresh this page or `python3 rank.py --check` to detect drift. "
                 "The generator uses Python 3.10+ and the standard library. Edit the [source catalogue](ranking_sources.csv) to add a published lead. "
                 "Use `python3 tracker.py --line N` for the register entry.", ""])
    return "\n".join(page)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write RANKINGS.md")
    mode.add_argument("--check", action="store_true", help="check that RANKINGS.md is current")
    args = parser.parse_args()
    page = render()
    if args.check:
        if not PAGE.exists() or PAGE.read_text(encoding="utf-8") != page:
            parser.exit(1, "RANKINGS.md is stale. Run python3 rank.py --write.\n")
    elif args.write:
        PAGE.write_text(page, encoding="utf-8")
    else:
        print(page, end="")


if __name__ == "__main__":
    main()
