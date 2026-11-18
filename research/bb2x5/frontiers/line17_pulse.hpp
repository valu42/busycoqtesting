// One-symbol and small-word transfers shared by the two packed line-17 workers.
#pragma once
#include <algorithm>
#include <charconv>
#include <cstdint>
#include <stdexcept>
#include <string>

using Count = std::uint64_t;
constexpr unsigned invalid = 6;

inline Count number(const char* str) {
    Count x;
    auto end = str + std::char_traits<char>::length(str);
    auto v = std::from_chars(str, end, x);
    if (v.ec!=std::errc{} || v.ptr!=end) throw std::runtime_error("invalid integer");
    return x;
}

struct Packet {
    std::uint8_t state=0, width=0, calls=0, interior=0;
    std::uint32_t bits=0;
    static Packet compile(unsigned initial, unsigned bits, unsigned width) {
        Packet out;
        unsigned v=initial/2, pending=initial%2;
        for (unsigned i=0;i<width;++i) {
            bool mark=(bits>>i)&1;
            if (pending && mark) { out.state=invalid; return out; }
            if (pending || mark) {
                out.calls+=v ? 3 : 4;
                out.interior+=v==0 ? 2 : (v==1 ? 6 : 4);
                if (v==1) out.bits |= 2U<<out.width;
                out.width+=v ? 2 : 1;
                pending=v!=0;
                v=(v+2)%3;
            } else {
                ++out.calls;
                if (v==2) { ++out.width; out.interior+=2; }
                v=(v+1)%3;
            }
        }
        out.state=2*v+pending;
        return out;
    }
};
