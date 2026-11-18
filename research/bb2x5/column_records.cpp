// Enumerate successive new deepest Q stops on the ordinary blank orbit.
// All indices are full physical pair indices, including the three low pairs.
#include "column_calendar.hpp"
#include <algorithm>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

namespace {
struct Transfer {
    Integer safe;
    unsigned digit;
    bool danger;
};

Transfer transfer(unsigned digit, Integer gap, bool danger) {
    unsigned u = digit / 2, e = digit % 2;
    const auto half = gap / 2 + ((gap & 1) && !u);
    if (!e && half > std::numeric_limits<Integer>::max()/2)
        throw std::overflow_error("pair output");
    const Integer safe = (2-e)*half;
    u ^= gap & 1;
    const bool passed = danger && (u || e);
    e ^= danger && !u;
    return {safe, 2*u+e, passed};
}

Transfer block(unsigned state, Integer gap, bool danger, unsigned length) {
    unsigned next = 0;
    for (unsigned j=0; j<length; ++j) {
        const auto move = transfer((state>>(2*j))&3, gap, danger);
        next |= move.digit<<(2*j);
        gap = move.safe;
        danger = move.danger;
    }
    return {gap, next, danger};
}

void add(Integer& total, Integer extra) {
    if (std::numeric_limits<Integer>::max()-total < extra)
        throw std::overflow_error("calendar counter");
    total += extra;
}

struct Packet {
    Integer pending = 0;
    unsigned state = 0;
};

class Records {
    static constexpr unsigned small = 256;
    struct Entry { std::uint16_t gap; std::uint8_t state, danger; };
    std::vector<Entry> lookup;
    std::vector<Packet> packets;
    unsigned partial = 0, length = 0;
    Integer gap_at_record = 0;
    unsigned cut;

    void append(unsigned digit) {
        partial |= digit<<(2*length);
        if (++length == 4) {
            packets.push_back({0,partial});
            partial = length = 0;
        }
    }

public:
    Integer width;
    unsigned depth() const { return cut+4*packets.size()+length; }
    Records(unsigned base, Integer first_gap) : lookup(256*small), cut(base),
            width(first_gap/2+(first_gap&1)) {
        for (unsigned state=0; state<256; ++state) {
            for (unsigned g=0; g<small; ++g) {
                const auto t=block(state,g,true,4);
                lookup[state*small+g] = {std::uint16_t(t.safe),std::uint8_t(t.digit),
                                         std::uint8_t(t.danger)};
            }
        }
        if (first_gap&1) append(2);
        if (depth()>=width) throw std::runtime_error("unsafe initial record");
    }

    void consume(Integer gap, Integer tick) {
        for (std::size_t i=0; i<packets.size(); ++i) {
            auto& packet=packets[i];
            add(packet.pending,gap);
            const Integer input=packet.pending;
            packet.pending=0;
            bool danger;
            if (input<small) {
                const auto m=lookup[packet.state*small+input];
                packet.state=m.state; gap=m.gap; danger=m.danger;
            } else {
                const auto m=block(packet.state,input,true,4);
                packet.state=m.digit; gap=m.safe; danger=m.danger;
            }
            if (!danger) {
                // Forward the safe output before the next dangerous input.
                if (i+1<packets.size()) add(packets[i+1].pending,gap);
                else {
                    const auto tail=block(partial,gap,false,length);
                    partial=tail.digit; add(gap_at_record,tail.safe);
                }
                return;
            }
        }
        const auto tail=block(partial,gap,true,length);
        partial=tail.digit;
        add(gap_at_record,tail.safe);
        if (!tail.danger) return;

        const Integer b=gap_at_record;
        gap_at_record=0;
        const unsigned residue=b%4;
        const auto previous=depth();
        append((b&1) ? 3 : 0);
        if (residue==1 || residue==2) append(2);
        add(width,b/4+(residue!=0));
        std::cout << tick << ' ' << previous << ' ' << b << ' ' << depth()
                  << ' ' << width << '\n';
        if (depth()>=width) throw std::runtime_error("candidate blank halt; replay B3");
    }
};
}

int main(int argc,char** argv) {
    if (argc!=3) { std::cerr<<"usage: column-records calendar-cut last-record-depth\n"; return 2; }
    const unsigned cut=std::stoul(argv[1]), goal=std::stoul(argv[2]);
    if (cut<3 || cut>18 || goal>1000000) throw std::invalid_argument("cut or goal");
    Integer period;
    const auto gaps=calendar(cut,period);
    Records orbit(cut,gaps.front().p);
    std::cout<<"# tick old_depth safe_gap new_depth width\n";
    std::cout<<"# seed "<<gaps.front().tick<<' '<<orbit.depth()<<' '<<orbit.width<<'\n';
    Integer start=0;
    std::size_t first=1;
    while (orbit.depth()<goal) {
        for (std::size_t i=first; i<gaps.size(); ++i) {
            if (start>std::numeric_limits<Integer>::max()-gaps[i].tick)
                throw std::overflow_error("tick");
            orbit.consume(gaps[i].p,start+gaps[i].tick);
            if (orbit.depth()>=goal) break;
        }
        first=0;
        if (orbit.depth()<goal) add(start,period);
    }
}
