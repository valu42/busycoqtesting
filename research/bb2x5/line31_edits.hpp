// One A-to-B edit of the physical root word. Included after the packed cell
// worker in line31_phase.cpp. All event counts here use one-based root requests.
namespace edits31 {
constexpr std::string_view root_word = "AABAA";
constexpr std::string_view fixed_word = "AAAABBA";

struct History {
    Count count = 0;
    unsigned phase = 0;
    bool matches_fixed = true;
    bool safe_fourth = true;
};

void push(std::vector<History>& strip, char letter, std::vector<History>* saved = nullptr) {
    for (auto& cell : strip) {
        if (saved) saved->push_back(cell);
        cell.matches_fixed &= letter == fixed_word[cell.count % 7];
        if (cell.count == 3) cell.safe_fourth = letter == 'A';
        ++cell.count;
        unsigned p = cell.phase;
        cell.phase = (p + 1 + (letter == 'B')) % 3;
        if (letter == 'B' && p != 0) break;
        letter = (letter == 'A' && p == 0) ? 'B' : 'A';
    }
}

struct Future {
    Word word;
    Count count, bs;
    bool periodic;

    bool bit(Count pos) const { return word.read(pos % word.size, 1); }

    unsigned advance(unsigned p) {
        Word next;
        Writer output{next};
        Count next_bs = 0;
        unsigned end;
        if (periodic) {
            Count copies = (word.size % 3 + bs % 3) % 3 ? 3 : 1;
            periodic = count / word.size >= copies;
            Count cycle = periodic ? copies * word.size : count;
            Count remainder = periodic ? count % cycle : count;
            next.data.reserve(cycle / 64 + 1);
            Count pos = 0;
            auto take = [&](Count n) {
                while (n) {
                    Count part = std::min(n, word.size - pos);
                    next_bs += project(word, pos, pos + part, p, output);
                    pos += part;
                    if (pos == word.size) pos = 0;
                    n -= part;
                }
            };
            take(remainder);
            end = p;
            Count partial = output.size();
            take(cycle - remainder);
            output.finish();
            count = periodic ? count / cycle * next.size + partial : partial;
        } else {
            next.data.reserve(count / 64 + 1);
            next_bs = project(word, 0, count, p, output);
            end = p;
            output.finish();
            count = next.size;
        }
        word = std::move(next);
        bs = next_bs;
        return end;
    }

    bool agrees_with_fixed(Count offset) const {
        if (periodic && word.size % 7 != 0) return false;
        for (Count i = 0; i < word.size; ++i)
            if (bit(i) != (fixed_word[(offset % 7 + i % 7) % 7] == 'B')) return false;
        return true;
    }
};

struct CutPeriod {
    Future source;
    Count groups;
};

CutPeriod true_period(unsigned cut, Count max_copies) {
    if (cut < 6 || cut % 2 || !max_copies)
        throw std::runtime_error("use an even cut of at least six and a positive number of copies");
    build_packets();
    Future before{Word{{4}, 5}, 5, 1, true};
    Count groups = 1;
    for (unsigned x = 0; x < cut; ++x) {
        Count repeats = (before.word.size % 3 + before.bs % 3) % 3 ? 3 : 1;
        if (groups > std::numeric_limits<Count>::max() / 5 / repeats)
            throw std::runtime_error("period exceeds the supported source horizon");
        groups *= repeats;
        before.count = repeats * before.word.size;
        before.advance(initial_phase(x));
    }
    if (max_copies > std::numeric_limits<Count>::max() / 5 / groups)
        throw std::runtime_error("shift exceeds the supported source horizon");
    return {std::move(before), groups};
}

enum class ShiftStatus { halt, fixed, passed, unknown };
struct ShiftResult {
    ShiftStatus status;
    size_t at;
    std::string parent, prefix;
};

ShiftResult inspect_shift(Future before, unsigned cut, Count copies, Count budget, size_t last) {
    before.count = copies * before.word.size;
    Future after{Word{{48}, 7}, budget, 2, budget != 0};
    std::string parent;
    for (size_t x = cut;; ++x) {
        if (x % 2 == 0) {
            std::string prefix;
            for (Count i = 0; i < 16; ++i) {
                if (i < before.count) prefix += "AB"[before.bit(i)];
                else if (i - before.count < after.count)
                    prefix += "AB"[after.bit(i - before.count)];
                else break;
            }
            if (prefix.size() < 4) return {ShiftStatus::unknown, x, parent, prefix};
            if (prefix[3] == 'B') return {ShiftStatus::halt, x, parent, prefix};
            if (x == last) return {ShiftStatus::passed, x, {}, {}};
            if (after.periodic && after.agrees_with_fixed(before.count)) {
                // Periods of sizes L and 7 agree forever if they agree on L+7 letters.
                Count check = std::min(before.count, before.word.size + 7);
                Count i = 0;
                while (i < check && before.bit(i) == (fixed_word[i % 7] == 'B')) ++i;
                if (i == check) return {ShiftStatus::fixed, x, {}, {}};
            }
            parent = std::move(prefix);
        }
        unsigned p = before.advance(2 * (x % 2));
        after.advance(p);
    }
}

int postpone(unsigned cut, Count copies, Count budget) {
    if (!budget) throw std::runtime_error("use a positive future budget");
    auto period = true_period(cut, copies);
    std::cout << "Cut +" << cut << ", period length " << period.source.word.size
              << ", request shift " << 5 * period.groups * copies << ".\n";
    auto result = inspect_shift(std::move(period.source), cut, copies, budget,
                                std::numeric_limits<size_t>::max());
    if (result.status == ShiftStatus::unknown) {
        std::cout << "First unchecked fourth letter at +" << result.at << ".\n";
        return 2;
    }
    if (result.status == ShiftStatus::halt)
        std::cout << "A2 at +" << result.at << ", aligned parent " << result.parent
                  << ", failing prefix " << result.prefix << ".\n";
    else
        std::cout << "Fixed stream at +" << result.at << ".\n";
    return 0;
}

int check_shift_band(unsigned cut, unsigned last, Count max_copies, Count budget) {
    if (last < cut || last % 2 || !budget)
        throw std::runtime_error("use an even final cut at or beyond the start and a positive tail budget");
    auto period = true_period(cut, max_copies);
    auto before_tail = [&](Count k) { return inspect_shift(period.source, cut, k, 0, last); };
    auto upper = before_tail(max_copies);
    if (upper.status != ShiftStatus::passed) {
        std::cout << "Genuine prefix at " << max_copies << " copies "
                  << (upper.status == ShiftStatus::halt ? "fails" : "runs out") << " at +" << upper.at << ".\n";
        return 2;
    }
    // The true prefixes are nested. Once all fourth letters arrive, larger k
    // inherit every one of them before the edited tail has any effect.
    Count lo = 0, hi = max_copies;
    while (hi - lo > 1) {
        Count mid = lo + (hi - lo) / 2;
        if (before_tail(mid).status == ShiftStatus::passed) hi = mid;
        else lo = mid;
    }
    std::cout << "All k >= " << hi << " clear +" << cut << " through +" << last
              << " before the fixed tail.\n";
    Count halts = 0, unknown = 0;
    for (Count k = 1; k < hi; ++k) {
        auto result = inspect_shift(period.source, cut, k, budget, last);
        if (result.status == ShiftStatus::halt) {
            std::cout << "halt " << k << ' ' << result.at << '\n';
            ++halts;
        } else if (result.status == ShiftStatus::unknown) {
            std::cout << "unresolved " << k << ' ' << result.at << '\n';
            ++unknown;
        }
    }
    std::cout << "Positive shifts halting through +" << last << ": " << halts
              << ", unresolved shifts: " << unknown << ".\n";
    return unknown ? 2 : 0;
}

int literal_shift(unsigned cut, unsigned last, Count copies, Count limit) {
    if (last < cut || last % 2 || !limit || limit > std::numeric_limits<Count>::max() - 3)
        throw std::runtime_error("use an even final cut at or beyond the start and a positive request limit");
    auto period = true_period(cut, copies);
    Count prefix = copies * period.source.word.size;
    auto letter = [&](Count i) {
        return i < prefix ? period.source.bit(i) : fixed_word[(i - prefix) % 7] == 'B';
    };
    if (letter(0) || letter(1) || letter(2))
        throw std::runtime_error("a virgin physical suffix requires three introductory As");
    constexpr std::string_view machine = "1RB3RB---4RA2RA_2LA2RA3LB4LB1LB";
    std::vector<unsigned char> tape(1, 0);
    for (Count i = 0; i < limit; ++i) {
        size_t x = 0;
        bool state_b = letter(i + 3);
        for (;;) {
            if (x == last - cut && !state_b && !tape[x]) {
                std::cout << "First A0 at +" << last << " on physical request " << i + 1 << ".\n";
                return 0;
            }
            size_t pos = (state_b ? 16 : 0) + 3 * tape[x];
            if (machine[pos] == '-') {
                std::cout << "A2 at +" << cut + x << " on physical request " << i + 1 << ".\n";
                return 0;
            }
            tape[x] = machine[pos] - '0';
            state_b = machine[pos + 2] == 'B';
            if (machine[pos + 1] == 'R') {
                if (++x == tape.size()) tape.push_back(0);
            } else {
                if (x == 0) break;
                --x;
            }
        }
    }
    std::cout << "Request limit reached.\n";
    return 2;
}

enum class Result { excluded, capture, unknown };

Result classify(const std::vector<History>& strip, Count edit, Count budget, size_t& depth) {
    unsigned b = unsigned((7 - edit % 5) % 5); // Position of B in the unedited next block.
    Future tail{Word{{Count{1} << b}, 5}, budget, 1, true};
    bool guard_unknown = false, possible = false;
    for (size_t x = 0; x < strip.size(); ++x) {
        const auto& cell = strip[x];
        if (x % 2 == 0) {
            if (!cell.safe_fourth) return Result::excluded;
            if (cell.count < 4) {
                Count needed = 3 - cell.count;
                if (tail.periodic || tail.count > needed) {
                    if (tail.bit(needed)) return Result::excluded;
                } else {
                    guard_unknown = true;
                }
            }
            if (cell.matches_fixed && tail.agrees_with_fixed(cell.count)) {
                depth = x / 2;
                if (tail.periodic && !guard_unknown) return Result::capture;
                possible = true;
            }
        }
        if (x + 1 < strip.size()) tail.advance(cell.phase);
    }
    return possible ? Result::unknown : Result::excluded;
}

struct Trial {
    Count date;
    std::vector<History> strip;
    Result result = Result::unknown;
    size_t depth = 0;
};

Count check_trials(std::vector<Trial>& trials, Count first_budget, Count max_budget) {
    #pragma omp parallel for schedule(dynamic) if(trials.size() >= 32)
    for (size_t i = 0; i < trials.size(); ++i) {
        auto& t = trials[i];
        Count budget = first_budget;
        for (;;) {
            t.result = classify(t.strip, t.date, budget, t.depth);
            if (t.result != Result::unknown || budget == max_budget) break;
            budget = budget > max_budget / 4 ? max_budget : budget * 4;
        }
    }
    Count unresolved = 0;
    for (const auto& t : trials) {
        if (t.result == Result::capture) std::cout << "capture " << t.date << ' ' << t.depth << '\n';
        if (t.result == Result::unknown) {
            ++unresolved;
            std::cout << "unresolved " << t.date << '\n';
        }
    }
    trials.clear();
    return unresolved;
}

int search(Count pairs, Count last_edit, Count first_budget, Count max_budget) {
    if (pairs >= std::vector<History>().max_size() / 2 || last_edit < 2 ||
        last_edit > std::numeric_limits<Count>::max() - 4 || first_budget == 0 || first_budget > max_budget)
        throw std::runtime_error("invalid pair depth, edit limit or future budget");
    std::vector<History> strip(2 * pairs + 1), saved;
    for (size_t x = 0; x < strip.size(); ++x) strip[x].phase = 2 * (x % 2);
    for (int i = 0; i < 3; ++i) push(strip, 'A');
    build_packets();
    Count missing = pairs + 1, unresolved = 0, date = 0;
    std::vector<Trial> trials;
    for (Count n = 1; n <= last_edit; ++n) {
        char letter = root_word[(n - 1) % 5];
        if (n >= 2 && letter == 'A') {
            saved.clear();
            push(strip, 'B', &saved);
            trials.push_back({n, strip});
            std::copy(saved.begin(), saved.end(), strip.begin());
        }
        saved.clear();
        push(strip, letter, &saved);
        for (size_t x = 0; x < saved.size(); x += 2)
            if (saved[x].matches_fixed && !strip[x].matches_fixed) --missing;
        date = n;
        if (trials.size() == 256 || missing == 0 || n == last_edit)
            unresolved += check_trials(trials, first_budget, max_budget);
        if (missing == 0) break;
    }
    std::cout << "Last date tested " << date << ", unresolved edits " << unresolved
              << ", cuts still matching the genuine prefix " << missing << ".\n";
    return unresolved || missing ? 2 : 0;
}
} // namespace edits31
