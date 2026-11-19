"""Local rule verification and the arithmetic of repeated calls on digit words."""

WALL = "101111111"
H_LEFT = "010101010"
H_RIGHT = "101111"
HUB_LEFT = "10010101010"[::-1]
TAKE = {1, 6, 7, 9, 19}
GIVE = {0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20}
SEND = {11, 15, 17, 21}

def phase_cycle(phase):
    if phase < 6:
        start, end = 0, 6
    elif phase < 18:
        start, end = 6, 18
    else:
        start, end = 18, 22
    return tuple(range(phase, end)) + tuple(range(start, phase))

def face(config, direction):
    _, original, left, right = config
    if original == direction:
        return left, right
    if direction == "R" and left:
        return left[1:], left[0] + right
    if direction == "L" and right:
        return right[0] + left, right[1:]
    return None

def literal(table, config):
    state, direction, left, right = config
    scanned, other = (left, right) if direction == "L" else (right, left)
    if not scanned:
        raise ValueError("Local proof attempted to read an unspecified cell")
    bit = int(scanned[0])
    transition = table[ord(state) - 65][3 * bit:3 * bit + 3]
    if transition == "---":
        raise ValueError("Local proof encountered the undefined transition")
    value, move, dest = transition
    scanned = scanned[1:]
    if direction == move:
        other = value + other
    else:
        scanned = value + scanned
    left, right = (scanned, other) if direction == "L" else (other, scanned)
    weight = 1 + 2 * (state == "A" and bit == 0)
    return (dest, move, left, right), weight

def local_clocks(table, config, dest, direction, left, right, steps):
    weighted = 0
    for _ in range(steps):
        config, tick = literal(table, config)
        weighted += tick
    assert config[0] == dest and face(config, direction) == (left, right)
    return steps, weighted

def one_call(table, before, after, forwards):
    # At D with input H_LEFT on the left, a call on the suffix returns at
    # A with H_RIGHT on the right. Splice that specified contract at most
    # once. No other read outside the displayed word is permitted.
    config = "D", "R", H_LEFT, before
    used = weighted = 0
    for steps in range(1000):
        state = config[0]
        if state == "A" and face(config, "L") == ("", H_RIGHT + after):
            assert used == forwards
            return steps, weighted
        sides = face(config, "R")
        if state == "D" and sides and not sides[1] and sides[0].startswith(H_LEFT) and used < forwards:
            config = "A", "L", sides[0][len(H_LEFT):], H_RIGHT
            used += 1
        config, tick = literal(table, config)
        weighted += tick
    raise ValueError("Digit did not implement its call contract")

def reset_clocks(table):
    # The outer return has an infinite zero tail on the left. The guard
    # in literal() confirms that twelve explicit zeros suffice.
    config = "A", "L", "01" + "0" * 12, H_RIGHT
    weighted = 0
    for steps in range(80):
        sides = face(config, "R")
        if config[0] == "D" and sides and not sides[1] and sides[0].rstrip("0") == HUB_LEFT.rstrip("0"):
            return steps, weighted
        config, tick = literal(table, config)
        weighted += tick
    raise ValueError("Outer call did not return to the hub")

class RuleBook:
    def __init__(self, table, words, macros, scans):
        self.cycles = [phase_cycle(p) for p in range(22)]
        self.macro_clocks, self.scan_clocks = {}, {}
        for index, (q, d, left, right, dest, last_d, lo, ro, steps) in macros.items():
            a = "".join(w * n for w, n in lo)
            b = "".join(w * n for w, n in ro)
            self.macro_clocks[index] = local_clocks(table, (q, d, left, right), dest, last_d, a, b, steps)
        for index, (q, d, inp, out, context, steps) in scans.items():
            if d == "L":
                left, right, lo, ro = inp, context, "", context + out
            else:
                left, right, lo, ro = context, inp, context + out, ""
            self.scan_clocks[index] = local_clocks(table, (q, d, left, right), q, d, lo, ro, steps)
        self.wall_clock = one_call(table, WALL, WALL, 1)
        self.reset_clock = reset_clocks(table)
        digit_clock = []
        for p, cycle in enumerate(self.cycles):
            before = words[p] + WALL * (p in TAKE)
            after = WALL * (p in GIVE) + words[cycle[1]]
            digit_clock.append(one_call(table, before, after, int(p in SEND)))
        self.take_at = [[i for i, p in enumerate(c) if p in TAKE] for c in self.cycles]
        self.send_at = [[i for i, p in enumerate(c) if p in SEND] for c in self.cycles]
        self.prefixes = []
        for cycle in self.cycles:
            used = given = sent = ref = weighted = prior_gives = sent_takes = 0
            rows = [(0, 0, 0, 0, 0, 0, 0)]
            for p in cycle:
                prior_gives += given
                used += p in TAKE
                given += p in GIVE
                if p in SEND:
                    sent_takes += used
                    sent += 1
                ref += digit_clock[p][0]
                weighted += digit_clock[p][1]
                rows.append((used, given, sent, ref, weighted, prior_gives, sent_takes))
            self.prefixes.append(rows)

    def limit(self, digits, closed):
        # The (allowance+1)th matching event is the first prohibited one.
        limit = 0 if closed else None
        for phase, gap in reversed(digits):
            period = len(self.cycles[phase])
            def before_next(allowance, positions):
                cycles, offset = divmod(allowance, len(positions))
                return cycles * period + positions[offset]
            cap = before_next(gap, self.take_at[phase])
            if limit is not None and self.send_at[phase]:
                cap = min(cap, before_next(limit, self.send_at[phase]))
            limit = cap
        return 0 if limit is None else limit

    def update(self, calls, digits):
        out = []
        leading = 0
        for phase, gap in digits:
            cycle = self.cycles[phase]
            whole, part = divmod(calls, len(cycle))
            rows = self.prefixes[phase]
            used, given, sent = (whole * rows[-1][i] + rows[part][i] for i in range(3))
            assert used <= gap
            if out:
                out[-1][1] += given
            else:
                leading = given
            out.append([cycle[part], gap - used])
            calls = sent
        assert calls == 0
        return leading, out

    def batch_clocks(self, leading, calls, digits):
        # Count wall visits separately from work done inside digits. The
        # triangular terms sum prior complete periods of the same digit.
        wall_visits = leading * calls
        ref = self.reset_clock[0] * calls
        weighted = self.reset_clock[1] * calls
        for phase, gap in digits:
            if not calls:
                break
            rows = self.prefixes[phase]
            period = len(rows) - 1
            cycles, part = divmod(calls, period)
            used, given, sent, work, weight, prior, sent_used = rows[-1]
            _, _, sent_part, work_part, weight_part, prior_part, su_part = rows[part]
            pairs = cycles * (cycles - 1) // 2
            prior_sum = pairs * period * given + cycles * prior + part * cycles * given + prior_part
            su_sum = pairs * sent * used + cycles * sent_used + sent_part * cycles * used + su_part
            calls = cycles * sent + sent_part
            wall_visits += prior_sum + gap * calls - su_sum
            ref += cycles * work + work_part
            weighted += cycles * weight + weight_part
        assert calls == 0 and wall_visits >= 0
        return ref + self.wall_clock[0] * wall_visits, weighted + self.wall_clock[1] * wall_visits
