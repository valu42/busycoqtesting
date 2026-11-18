// Counts ordinary pair visits on line 26, for exact raw time and tape recovery.
#include "column_calendar.hpp"
#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <string>

struct Move {
    unsigned state, p, q;
};

Move one_pair(unsigned digit, unsigned p, unsigned q) {
    unsigned u = digit / 2, e = digit % 2;
    const unsigned sent = (2-e)*((p+1-u)/2);
    u ^= p%2;
    const unsigned passed = q && (u || e);
    if (q && !u) e ^= 1;
    return {2*u+e,sent,passed};
}

struct Prefix {
    Integer visits = 0;
    unsigned tail = 0;  // Ps after the last Q at this cut, through the requested tick.
    std::string digits;
};

Prefix low_prefix(unsigned cut, Integer ticks) {
    // Per tick the first three cuts contribute 32, 24 and 16 units.
    Prefix result{72*ticks,0,"000"};
    for (unsigned j=3; j<cut; ++j) {
        Integer period;
        const auto gaps = calendar(j,period);
        const Integer full = ticks/period, remainder = ticks%period;
        result.visits += full*11*gaps.size() + result.tail;
        unsigned state = 0, pending = 0;
        auto consume = [&](unsigned p, unsigned q) {
            const auto step = one_pair(state,p,q);
            state = step.state;
            pending += step.p;
            if (step.q) pending = 0;
        };
        // Four complete lower periods restore this pair and end in an emitted Q.
        for (unsigned copy=0; copy<full%4; ++copy)
            for (auto gap : gaps) consume(gap.p,1);
        for (auto gap : gaps) {
            if (gap.tick>remainder) break;
            result.visits += gap.p+2;
            consume(gap.p,1);
        }
        consume(result.tail,0);
        result.tail = pending;
        result.digits.push_back(char('0'+state));
    }
    return result;
}

struct Block {
    std::uint16_t p, weight;
    std::uint8_t q, state;
};

std::vector<Block> weighted_blocks(unsigned maximum) {
    std::vector<Block> table(256*(maximum+1)*2);
    for (unsigned state=0; state<256; ++state)
        for (unsigned g=0; g<=maximum; ++g)
            for (unsigned flag=0; flag<2; ++flag) {
                unsigned next=0, p=g, q=flag, weight=0;
                for (unsigned i=0; i<4; ++i) {
                    weight += p+2*q;
                    const auto step = one_pair((state>>(2*i))&3,p,q);
                    next |= step.state<<(2*i);
                    p=step.p; q=step.q;
                }
                assert(weight<65536 && p<65536);
                table[2*(state*(maximum+1)+g)+flag] = {
                    std::uint16_t(p),std::uint16_t(weight),std::uint8_t(q),std::uint8_t(next)};
            }
    return table;
}

void endpoint(unsigned cut, Integer ticks) {
    if (cut<3 || cut>18 || !ticks || ticks>1145205194028ULL)
        throw std::invalid_argument("use cut 3..18 and a tick in the certified blank interval");
    auto low = low_prefix(cut,ticks);
    Integer period;
    const auto gaps = calendar(cut,period);
    // The record-96 certificate bounds the tape width by 205 on the new interval.
    const unsigned accounting_width = ticks<=54306954019ULL ? 192 : 212;
    const unsigned blocks = (accounting_width-cut+3)/4;
    const unsigned length = cut+4*blocks;
    unsigned largest = low.tail;
    for (auto gap : gaps) largest = std::max(largest,gap.p);
    // Each pair increases the safe count in one input message by at most one.
    const unsigned maximum = largest+length;
    const auto table = weighted_blocks(maximum);
    std::vector<unsigned> states(blocks);
    Integer end_p=0;
    auto consume = [&](unsigned p, unsigned q) {
        for (auto& state : states) {
            if (!p && !q) return;
            assert(p<=maximum);
            const auto step = table[2*(state*(maximum+1)+p)+q];
            low.visits += step.weight;
            state=step.state; p=step.p; q=step.q;
        }
        if (q) throw std::runtime_error("selected accounting width was reached by Q");
        end_p += p;
    };
    for (Integer i=0; i<ticks/period; ++i)
        for (auto gap : gaps) consume(gap.p,1);
    for (auto gap : gaps) {
        if (gap.tick>ticks%period) break;
        consume(gap.p,1);
    }
    consume(low.tail,0);
    for (auto state : states)
        for (unsigned i=0; i<4; ++i) low.digits.push_back(char('0'+((state>>(2*i))&3)));
    const auto last = low.digits.find_last_not_of('0');
    if (end_p%2 || end_p/2>=length || (last!=std::string::npos && last>=end_p/2))
        throw std::runtime_error("invalid virgin suffix or width");
    std::cout << ticks << ' ' << length << ' ' << low.visits << ' ' << end_p/2 << ' '
              << low.digits.substr(0,end_p/2) << '\n';
}

int main(int argc,char** argv) {
    if (argc!=3) return 2;
    endpoint(std::stoul(argv[1]),std::stoull(argv[2]));
}
