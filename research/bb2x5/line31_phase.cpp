// Finite prefix of the aligned ordinary-cell streams of line 31.
// Compile with C++20. OpenMP is optional. See line31-phase.md.
#include <algorithm>
#include <array>
#include <bit>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

using Count = std::uint64_t;
constexpr unsigned trace_length = 16;
constexpr Count tile_size = 1 << 16;
constexpr Count batch_size = Count{1} << 28;

unsigned initial_phase(unsigned x) {
    constexpr std::array<unsigned, 6> head{0, 0, 2, 2, 1, 1};
    return x < head.size() ? head[x] : 2 * (x % 2);
}

struct Word {
    std::vector<Count> data;
    Count size = 0;

    Count read(Count pos, unsigned width) const {
        unsigned shift = pos % 64;
        Count value = data[pos / 64] >> shift;
        if (shift + width > 64)
            value |= data[pos / 64 + 1] << (64 - shift);
        return width == 64 ? value : value & ((Count{1} << width) - 1);
    }
};

struct Writer {
    Word& word;
    Count pending = 0;
    unsigned used = 0;

    void append(Count value, unsigned width) {
        pending |= value << used;
        if (used + width >= 64) {
            word.data.push_back(pending);
            pending = used ? value >> (64 - used) : 0;
        }
        used = (used + width) % 64;
    }

    Count size() const { return 64 * word.data.size() + used; }

    void finish() {
        word.size = size();
        if (used) word.data.push_back(pending);
    }
};

struct Packet {
    std::uint16_t bits;
    std::uint8_t size, phase;
};
std::array<std::array<Packet, 65536>, 3> packets;

void build_packets() {
    for (unsigned p = 0; p < 3; ++p) {
        for (unsigned v = 0; v < 65536; ++v) {
            unsigned phase = p, bits = 0, length = 0;
            for (unsigned j = 0; j < 16; ++j) {
                unsigned b = (v >> j) & 1;
                if (!b || phase == 0)
                    bits |= unsigned(!b && phase == 0) << length++;
                phase = (phase + 1 + b) % 3;
            }
            packets[p][v] = {std::uint16_t(bits), std::uint8_t(length), std::uint8_t(phase)};
        }
    }
}

// Read a piece in time order. Return the number of B emissions.
Count project(const Word& word, Count pos, Count end, unsigned& phase, Writer& out) {
    Count bs = 0;
    while (end - pos >= 16) {
        const auto& packet = packets[phase][word.read(pos, 16)];
        out.append(packet.bits, packet.size);
        bs += std::popcount(packet.bits);
        phase = packet.phase;
        pos += 16;
    }
    while (pos < end) {
        unsigned b = word.read(pos++, 1);
        if (!b || !phase) {
            unsigned y = !b && !phase;
            out.append(y, 1);
            bs += y;
        }
        phase = (phase + 1 + b) % 3;
    }
    return bs;
}

struct Row {
    Count length = 0;
    unsigned phase = 0;
    std::string prefix;

    void observe(const Word& word, Count limit) {
        for (Count i = 0; i < limit && prefix.size() < trace_length; ++i)
            prefix.push_back("AB"[word.read(i % word.size, 1)]);
    }
};

struct Tile {
    Word word;
    Count bs = 0;
    unsigned start = 0;
};

// Input at the split is the first n letters of base repeated. Each tile
// keeps its chronological place. Displacement n - 2b equals n + b mod 3,
// so starting phases are known before any of the tile images are evaluated.
void finish_tail(const Word& base, Count n, unsigned split, std::vector<Row>& rows) {
    Count offset = 0;
    while (n) {
        Count total = std::min(n, batch_size);
        unsigned num = unsigned((total + tile_size - 1) / tile_size);
        std::vector<Tile> tiles(num), next(num);
        #pragma omp parallel for schedule(static)
        for (unsigned j = 0; j < num; ++j) {
            auto& tile = tiles[j];
            Count length = std::min(tile_size, total - tile_size * j);
            Count pos = (offset + tile_size * j) % base.size;
            tile.word.data.reserve((length + 63) / 64);
            Writer writer{tile.word};
            while (length) {
                unsigned k = unsigned(std::min({Count{64}, length, base.size - pos}));
                Count bits = base.read(pos, k);
                writer.append(bits, k);
                tile.bs += std::popcount(bits);
                length -= k;
                pos += k;
                if (pos == base.size) pos = 0;
            }
            writer.finish();
        }
        for (unsigned x = split;; ++x) {
            if (rows.size() == x) rows.emplace_back();
            Row& row = rows[x];
            unsigned phase = row.length ? row.phase : initial_phase(x);
            Count length = 0;
            for (auto& tile : tiles) {
                tile.start = phase;
                length += tile.word.size;
                if (tile.word.size && row.prefix.size() < trace_length)
                    row.observe(tile.word, tile.word.size);
                phase = (phase + tile.word.size % 3 + tile.bs % 3) % 3;
            }
            if (!length) break;
            row.length += length;
            row.phase = phase;
            #pragma omp parallel for schedule(static) if(length > 262144)
            for (unsigned j = 0; j < num; ++j) {
                auto& output = next[j];
                output.word.data.clear();
                output.word.data.reserve((tiles[j].word.size + 63) / 64);
                Writer writer{output.word};
                unsigned p = tiles[j].start;
                output.bs = project(tiles[j].word, 0, tiles[j].word.size, p, writer);
                writer.finish();
            }
            tiles.swap(next);
        }
        offset = (offset + total) % base.size;
        n -= total;
    }
}

Count number(std::string_view s) {
    Count n;
    auto [end, ec] = std::from_chars(s.data(), s.data() + s.size(), n);
    if (ec != std::errc{} || end != s.data() + s.size())
        throw std::runtime_error("expected an unsigned decimal integer");
    return n;
}

int main(int argc, char** argv) try {
    if (argc != 3) throw std::runtime_error("usage: line31_phase GROUPS SPLIT_CELL");
    Count groups = number(argv[1]), split = number(argv[2]);
    if (!groups || groups > std::numeric_limits<Count>::max() / 5)
        throw std::runtime_error("5 * GROUPS must fit in a nonzero uint64");
    build_packets();
    Count n = 5 * groups;
    Word word{{4}, 5}; // AABAA, first letter in the low bit
    std::vector<Row> rows;
    bool periodic = true;
    for (unsigned x = 0; n; ++x) {
        if (x == split) {
            finish_tail(word, n, x, rows);
            break;
        }
        rows.emplace_back();
        Row& row = rows.back();
        row.length = n;
        row.observe(word, n);
        unsigned phase = initial_phase(x);
        Word image;
        Writer writer{image};
        if (periodic) {
            Count bs = 0;
            for (Count bits : word.data) bs += std::popcount(bits);
            unsigned copies = (word.size % 3 + bs % 3) % 3 ? 3 : 1;
            // Test the comparison before multiplying to avoid overflow.
            periodic = n / word.size >= copies;
            Count cycle = periodic ? copies * word.size : n;
            Count remainder = periodic ? n % cycle : n;
            image.data.reserve(cycle / 64 + 1);
            Count pos = 0;
            auto take = [&](Count length) {
                while (length) {
                    Count k = std::min(length, word.size - pos);
                    project(word, pos, pos + k, phase, writer);
                    length -= k;
                    pos += k;
                    if (pos == word.size) pos = 0;
                }
            };
            take(remainder);
            row.phase = phase;
            Count partial = writer.size();
            take(cycle - remainder);
            writer.finish();
            n = periodic ? n / cycle * image.size + partial : partial;
        } else {
            image.data.reserve(n / 64 + 1);
            project(word, 0, n, phase, writer);
            writer.finish();
            row.phase = phase;
            n = image.size;
        }
        word = std::move(image);
    }
    for (unsigned x = 0; x < rows.size() && rows[x].length; ++x)
        std::cout << x << ' ' << rows[x].length << ' ' << rows[x].phase
                  << ' ' << rows[x].prefix << '\n';
} catch (const std::exception& e) {
    std::cerr << e.what() << '\n';
    return 1;
}
