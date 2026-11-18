// Evaluate chronological rightward calls to line 15, seven physical cells at
// a time. Each speculative strip assumes A from the right and must return A
// to the left on every call. Write WORD ENTRIES RAW OUTGOING for each completed strip.
#include <algorithm>
#include <array>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

using Count = std::uint64_t;
constexpr Count visit_limit = 10000;
constexpr char machine[] = "1RB3RB1LA2LA3RA_1LB2RA4RB0LA---";
constexpr char period[] = "BABAABBABBABAAAB";
constexpr unsigned width = 7;
using Cells = std::array<unsigned, width>;

struct Bits {
    std::vector<std::uint32_t> words;
    Count size = 0;
    // The final partial word remains addressable while appending or reading.
    void append(std::uint32_t bits, unsigned length) {
        if (!length) return;
        auto shift = unsigned(size % 32);
        if (!shift) words.push_back(bits);
        else {
            words.back() |= bits << shift;
            if (length > 32-shift) words.push_back(bits >> (32-shift));
        }
        size += length;
    }
    unsigned bit(Count i) const { return (words[i/32] >> (i%32)) & 1; }
    unsigned byte(Count i) const { return (words[i/32] >> (i%32)) & 255; }
    void clear() { words.clear(); size = 0; }
};

struct Rule { unsigned write; int move; unsigned state; };
using Rules = std::array<std::array<Rule, 5>, 2>;
Rules rules() {
    Rules result{};
    for (unsigned q=0; q<2; ++q) for (unsigned s=0; s<5; ++s) {
        const char* r = machine + 16*q + 3*s;
        if (*r != '-') result[q][s] = {unsigned(r[0]-'0'), r[1]=='L' ? -1 : 1, unsigned(r[2]-'A')};
    }
    return result;
}

Count literal(const Rules& tm, Cells& tape, unsigned state, Bits& outgoing) {
    int head = 0;
    Count steps = 0;
    while (head >= 0) {
        const Rule rule = tm[state][tape[head]];
        if (!rule.move) throw std::runtime_error("undefined instruction inside candidate strip");
        tape[head] = rule.write;
        head += rule.move;
        state = rule.state;
        ++steps;
        if (head == int(width)) {
            outgoing.append(state, 1);
            head = width-1;
            state = 0;
        }
        if (steps >= visit_limit) throw std::runtime_error("strip first-exit work limit");
    }
    if (state != 0) throw std::runtime_error("candidate strip returned B");
    return steps;
}

int mature(const Cells& tape) {
    unsigned mask = 0;
    for (unsigned j=0; j<width; ++j) {
        if (tape[j] != 1 && tape[j] != 2) return -1;
        mask |= (tape[j]-1) << j;
    }
    return int(mask);
}

struct Image {
    std::uint32_t bits = 0;
    std::uint16_t steps = 0;
    std::uint8_t length = 0, state = 0;
};
using Table = std::array<std::array<Image, 256>, 1<<width>;
// For a whole input byte the changed state bits depend only on the first
// five cells. Check this against every literal image while building the table.
using Changes = std::array<std::array<std::uint8_t, 256>, 32>;
void make_table(const Rules& tm, Table& table, Changes& changes) {
    std::array<std::array<Image, 2>, 1<<width> single{};
    for (unsigned mask=0; mask<single.size(); ++mask) for (unsigned input=0; input<2; ++input) {
        Cells cells{};
        for (unsigned j=0; j<width; ++j) cells[j] = 1 + ((mask >> j) & 1);
        Bits out;
        Count steps = literal(tm, cells, input, out);
        int final = mature(cells);
        if (out.size > 32 || steps > UINT16_MAX || final < 0) throw std::logic_error("mature strip failed to close");
        single[mask][input] = {out.size ? out.words[0] : 0, std::uint16_t(steps),
                               std::uint8_t(out.size), std::uint8_t(final)};
    }
    for (unsigned mask=0; mask<table.size(); ++mask) for (unsigned byte=0; byte<256; ++byte) {
        unsigned state=mask, length=0, steps=0;
        std::uint32_t bits=0;
        for (unsigned j=0; j<8; ++j) {
            auto v=single[state][(byte >> j) & 1];
            if (length + v.length > 32) throw std::logic_error("output byte table overflow");
            if (v.length) bits |= v.bits << length;
            length += v.length;
            steps += v.steps;
            state = v.state;
        }
        if (steps > UINT16_MAX) throw std::logic_error("output byte clock overflow");
        const auto delta = std::uint8_t(mask ^ state);
        if (mask < changes.size()) changes[mask][byte] = delta;
        else if (changes[mask & 31][byte] != delta) throw std::logic_error("byte state change differs");
        table[mask][byte] = {bits, std::uint16_t(steps), std::uint8_t(length), std::uint8_t(state)};
    }
}

void check_letters(const Bits& input, std::string_view anchor) {
    for (unsigned j=0; j<anchor.size() && j<input.size; ++j)
        if (input.bit(j) != unsigned(anchor[j]=='B'))
            throw std::runtime_error("request letters differ from the proposed prefix");
}

int main(int argc, char** argv) try {
    Count groups;
    const std::string_view mode = argc == 3 ? argv[2] : "";
    const bool resume_audit = mode == "--resume-check-prefix";
    const bool resume = mode == "--resume" || resume_audit;
    const bool check_prefix = mode == "--check-prefix", check_anchor = mode == "--check-anchor";
    if (argc != 2 && !resume && !check_prefix && !check_anchor)
        throw std::runtime_error("usage: line15_stream GROUPS [--resume|--check-prefix|--resume-check-prefix|--check-anchor]");
    const std::string arg = argv[1];
    auto parsed = std::from_chars(arg.data(), arg.data()+arg.size(), groups);
    if (parsed.ec != std::errc{} || parsed.ptr != arg.data()+arg.size() || groups > UINT32_MAX)
        throw std::runtime_error("invalid group count");
    if (!groups) return 0;

    Bits input, output;
    unsigned period_bits = 0;
    for (unsigned i=0; i<16; ++i) period_bits |= unsigned(period[i]=='B') << i;
    if (resume) {
        unsigned rotated = ((period_bits << 1) & 65535) | (period_bits >> 15);
        for (Count i=0; i<groups; ++i) input.append(rotated, 16);
    } else {
        for (char c : std::string("ABBBA")) input.append(c=='B', 1);
        for (Count i=1; i<groups; ++i) input.append(period_bits, 16);
        input.append(period_bits & 32767, 15);
    }

    const Rules tm = rules();
    Table table;
    Changes changes;
    make_table(tm, table, changes);
    std::ios::sync_with_stdio(false);
    Count strip = 0, fresh = 0, fifth = 0, completed_fringe = 0;
    // A previously certified complete period leaves only mature blocks and
    // the final AAAB fringe. These are the startup states before maturity.
    const std::array<Cells,5> transient = {Cells{0,0,0,0,0,0,0}, Cells{1,0,1,0,0,0,0},
        Cells{0,1,1,0,0,0,0}, Cells{2,1,2,1,0,1,1}, Cells{2,2,1,0,1,1,1}};
    while (input.size) {
        if (check_prefix) check_letters(input, strip ? "AAABB" : "ABBBA");
        if (check_anchor) {
            std::string_view expected = "AAABBABBABBABA";
            if (strip == 0) expected = "ABBBA";
            if (strip == 1) expected = "AAABBABBAB";
            // Two distinguished cuts witness the divergence on letter 15.
            if (strip == 2) expected = "AAABBABBABBABAA";
            if (strip == 2101) expected = "AAABBABBABBABAB";
            check_letters(input, expected);
        }
        // Both the local clock and the number of emitted calls are bounded
        // by the per-visit work limit times the number of incoming calls.
        if (input.size > UINT64_MAX / visit_limit) throw std::overflow_error("strip clock exceeds native range");
        Cells tape{};
        if (resume) {
            std::string word;
            if (std::cin >> word) {
                if (word.size() != width || word.find_first_not_of("01234") != std::string::npos)
                    throw std::runtime_error("invalid resume block");
                for (unsigned j=0; j<width; ++j) tape[j] = unsigned(word[j]-'0');
            } else if (!std::cin.eof()) {
                throw std::runtime_error("could not read resume block");
            }
        }
        if (resume_audit && mature(tape) < 0) {
            const auto at = std::find(transient.begin(), transient.end(), tape);
            if (!strip || at == transient.end()) throw std::runtime_error("unrecognized strip in resumed prefix audit");
            const unsigned prefix = unsigned(at - transient.begin());
            check_letters(input, std::string_view("AAABB").substr(prefix));
            if (!prefix) ++fresh;
            if (input.size >= 5-prefix) {
                ++fifth;
                if (prefix) ++completed_fringe;
            }
        }
        Count at = 0, cost = 0;
        // Start from the actual cells. Batch only on a byte boundary
        // where all seven are in {1,2}. A short or exceptional prefix is literal.
        while (at < input.size && (at%8 || mature(tape) < 0))
            cost += literal(tm, tape, input.bit(at++), output);
        int state = mature(tape);
        if (state >= 0) {
            // Each image has at most 32 output bits. Keep the partial word
            // in a register and reserve room for at most 1,024 images at once.
            auto word = output.size / 32;
            auto used = unsigned(output.size % 32);
            std::uint64_t pending = used ? output.words.back() : 0;
            while (at + 8 <= input.size) {
                const Count batch = std::min<Count>(1024, (input.size - at) / 8);
                output.words.resize(word + batch + 1);
                const Count end = at + 8 * batch;
                for (; at < end; at += 8) {
                    const auto byte = input.byte(at);
                    const auto image = table[state][byte];
                    state ^= changes[state & 31][byte];
                    cost += image.steps;
                    pending |= std::uint64_t(image.bits) << used;
                    used += image.length;
                    // An image crosses at most one word boundary. The next
                    // store overwrites this word if it is still incomplete.
                    output.words[word] = std::uint32_t(pending);
                    const unsigned full = used / 32;
                    word += full;
                    pending >>= 32 * full;
                    used %= 32;
                }
            }
            output.size = 32 * word + used;
            if (used) output.words[word] = std::uint32_t(pending);
            output.words.resize(word + (used != 0));
            for (unsigned j=0; j<width; ++j) tape[j] = 1 + ((state >> j) & 1);
        }
        while (at < input.size) cost += literal(tm, tape, input.bit(at++), output);
        for (auto digit : tape) std::cout << digit;
        std::cout << ' ' << input.size << ' ' << cost << ' ' << output.size << '\n';
        std::swap(input, output);
        output.clear();
        ++strip;
    }
    if (resume_audit)
        std::cerr << "fresh " << fresh << " fifth " << fifth << " old_fringe " << completed_fringe << '\n';
    std::cout.flush();
    if (!std::cout) throw std::runtime_error("could not write completed strip counts");
    return 0;
} catch (const std::exception& e) {
    std::cerr << e.what() << '\n';
    return 2;
}
