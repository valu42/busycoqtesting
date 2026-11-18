// Finite prefix of the aligned ordinary-cell streams of line 31.
// Compile with C++20. OpenMP is optional. See line31-phase.md.
#include <algorithm>
#include <array>
#include <bit>
#include <charconv>
#include <cstdint>
#include <fstream>
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

// The last word is zero padded. The file uses little-endian uint64 words.
class Archive {
    std::ofstream file;
    Word buffer;
    Writer writer{buffer};

    void flush() {
        if constexpr (std::endian::native == std::endian::little) {
            file.write(reinterpret_cast<const char*>(buffer.data.data()),
                       std::streamsize(buffer.data.size() * sizeof(Count)));
        } else {
            for (Count value : buffer.data)
                for (unsigned i = 0; i < 8; ++i)
                    file.put(char((value >> (8 * i)) & 255));
        }
        buffer.data.clear();
    }

public:
    void open(const char* path) {
        file.exceptions(std::ios::failbit | std::ios::badbit);
        file.open(path, std::ios::binary);
    }
    void append(const Word& word) {
        for (Count pos = 0; pos < word.size; pos += 64)
            writer.append(word.data[pos / 64], unsigned(std::min<Count>(64, word.size - pos)));
        if (buffer.data.size() >= 32768) flush();
    }
    void finish() {
        if (writer.used) buffer.data.push_back(writer.pending);
        flush();
        file.close();
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

// Read complete packed words in sequence and preserve the true length at wrap.
class DiskPeriod {
    std::ifstream file;
    const Count period_length;
    Word buffer;
    Count pos = 0, file_pos = 0;

    void refill() {
        if (file_pos == period_length) {
            file.seekg(0);
            file_pos = 0;
        }
        buffer.size = std::min(Count{1} << 20, period_length - file_pos);
        buffer.data.resize((buffer.size + 63) / 64);
        file.read(reinterpret_cast<char*>(buffer.data.data()),
                  std::streamsize(8 * buffer.data.size()));
        if constexpr (std::endian::native != std::endian::little) {
            for (Count& word : buffer.data) {
                auto* bytes = reinterpret_cast<unsigned char*>(&word);
                std::reverse(bytes, bytes + sizeof(word));
            }
        }
        pos = 0;
        file_pos += buffer.size;
    }

public:
    DiskPeriod(const char* path, Count length) : period_length(length) {
        file.exceptions(std::ios::failbit | std::ios::badbit);
        file.open(path, std::ios::binary | std::ios::ate);
        if (file.tellg() != std::streamoff(8 * ((length + 63) / 64)))
            throw std::runtime_error("incorrect packed period length");
        file.seekg(0);
    }

    void fill(std::vector<Tile>& tiles, Count total) {
        for (auto& tile : tiles) {
            Count needed = std::min(total, tile_size);
            total -= needed;
            Writer out{tile.word};
            tile.word.data.reserve((needed + 63) / 64);
            while (needed) {
                if (pos == buffer.size) refill();
                unsigned k = unsigned(std::min({Count{64}, needed, buffer.size - pos}));
                Count bits = buffer.read(pos, k);
                tile.bs += std::popcount(bits);
                out.append(bits, k);
                pos += k;
                needed -= k;
            }
            out.finish();
        }
    }
};

void fill_memory(const Word& base, Count offset, std::vector<Tile>& tiles, Count total) {
    #pragma omp parallel for schedule(static)
    for (unsigned j = 0; j < tiles.size(); ++j) {
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
}

// Input at the split is the first n letters of base repeated. Each tile
// keeps its chronological place. Displacement n - 2b equals n + b mod 3,
// so starting phases are known before any of the tile images are evaluated.
template<class Fill>
void finish_tail(Count n, unsigned split, Count last_cell, std::vector<Row>& rows, Archive* archive, Fill fill) {
    while (n) {
        Count total = std::min(n, batch_size);
        unsigned num = unsigned((total + tile_size - 1) / tile_size);
        std::vector<Tile> tiles(num), next(num);
        fill(tiles, total);
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
            if (x == last_cell) {
                if (archive)
                    for (const auto& tile : tiles) archive->append(tile.word);
                break;
            }
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

void print_rows(const std::vector<Row>& rows, unsigned start) {
    for (unsigned x = start; x < rows.size() && rows[x].length; ++x)
        std::cout << x << ' ' << rows[x].length << ' ' << rows[x].phase
                  << ' ' << rows[x].prefix << '\n';
}

#include "line31_edits.hpp"

int main(int argc, char** argv) try {
    if (argc == 6 && std::string_view(argv[1]) == "--capture-edits")
        return edits31::search(number(argv[2]), number(argv[3]), number(argv[4]), number(argv[5]));
    if (argc == 6 && (std::string_view(argv[1]) == "--postpone-band" ||
                      std::string_view(argv[1]) == "--literal-shift")) {
        Count cut = number(argv[2]), last = number(argv[3]);
        if (cut > std::numeric_limits<unsigned>::max() || last > std::numeric_limits<unsigned>::max())
            throw std::runtime_error("cut too large");
        if (std::string_view(argv[1]) == "--literal-shift")
            return edits31::literal_shift(unsigned(cut), unsigned(last), number(argv[4]), number(argv[5]));
        return edits31::check_shift_band(unsigned(cut), unsigned(last), number(argv[4]), number(argv[5]));
    }
    if (argc == 5 && std::string_view(argv[1]) == "--postpone-edit") {
        Count cut = number(argv[2]);
        if (cut > std::numeric_limits<unsigned>::max()) throw std::runtime_error("cut too large");
        return edits31::postpone(unsigned(cut), number(argv[3]), number(argv[4]));
    }
    if (argc == 4 && std::string_view(argv[1]) == "--from56") {
        DiskPeriod disk(argv[2], 53'427'204'485);
        Count n = number(argv[3]);
        build_packets();
        std::vector<Row> rows(56);
        finish_tail(n, 56, std::numeric_limits<Count>::max(), rows, nullptr,
                    [&](auto& tiles, Count total) { disk.fill(tiles, total); });
        print_rows(rows, 56);
        return 0;
    }
    if (argc < 3 || argc > 5)
        throw std::runtime_error("usage: line31_phase GROUPS SPLIT_CELL [LAST_CELL [PACKED_OUTPUT]]");
    Count groups = number(argv[1]), split = number(argv[2]);
    Count last_cell = argc >= 4 ? number(argv[3]) : std::numeric_limits<Count>::max();
    if (!groups || groups > std::numeric_limits<Count>::max() / 5)
        throw std::runtime_error("5 * GROUPS must fit in a nonzero uint64");
    Archive archive;
    if (argc == 5) {
        archive.open(argv[4]);
        split = std::min(split, last_cell);
    }
    build_packets();
    Count n = 5 * groups;
    Word word{{4}, 5}; // AABAA, first letter in the low bit
    std::vector<Row> rows;
    bool periodic = true;
    for (unsigned x = 0; n; ++x) {
        if (x == split) {
            Count offset = 0;
            finish_tail(n, x, last_cell, rows, argc == 5 ? &archive : nullptr,
                        [&](auto& tiles, Count total) {
                            fill_memory(word, offset, tiles, total);
                            offset = (offset + total) % word.size;
                        });
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
        if (x == last_cell) break;
        word = std::move(image);
    }
    if (argc == 5) archive.finish();
    print_rows(rows, 0);
} catch (const std::exception& e) {
    std::cerr << e.what() << '\n';
    return 1;
}
