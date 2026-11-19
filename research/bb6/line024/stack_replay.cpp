// Replay the original marker stack from the Lean theorem blankSecondRestart.
// Each cached excursion is computed exclusively by staying inside one byte.
#include <array>
#include <cstdint>
#include <cstdio>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
struct Action { int write, direction, state; };
constexpr Action table[6][2] = {
    {{1,1,1},{0,-1,0}}, {{1,1,2},{0,0,-1}}, {{0,-1,3},{1,1,3}},
    {{0,1,0},{0,1,4}}, {{0,1,5},{1,1,2}}, {{1,-1,5},{0,-1,0}}
};
struct Contact { int cell, state; std::int64_t time; };
// Times from the second restart. The final item is the separate four-one block.
constexpr Contact contacts[] = {
    {1324,2,101958LL},
    {9958,2,764156LL},
    {108006697,5,17588658509LL},
    {141561133,2,23364025905LL},
    {149949745,2,24829890625LL},
    {152046901,2,25216552879LL},
    {152571193,2,25318090789LL},
    {152702269,2,25344774893LL},
    {152735041,2,25351774019LL},
    {152743237,2,25353619839LL},
    {152745289,2,25354100129LL},
    {152745805,2,25354224567LL},
    {152745937,2,25354256449LL},
    {152745973,2,25354264287LL},
    {152745985,2,25354265165LL},
    {152745991,2,25354265171LL},
    {152745999,2,25354265197LL}
};
struct TileRun {
    int bits = 0, state = 0, end = 0, steps = 0;
};
constexpr int origin = 1024;
constexpr int size = 153000000;
constexpr int count = sizeof(contacts)/sizeof(contacts[0]);

class Replay {
    std::array<TileRun,256*6*2> cache{};
    std::vector<std::uint8_t> tape = std::vector<std::uint8_t>((size+7)/8);
    int head = origin, state = 0, next = 0;
    std::int64_t time = 0;

    static void set(int& bits, int offset, int bit) {
        bits = (bits & ~(1 << offset)) | (bit << offset);
    }
    void mark(int p) {
        p += origin;
        tape.at(p/8) |= 1 << (p%8);
    }
    void checkContact() {
        if (next == count || head-origin != contacts[next].cell) return;
        const auto& c = contacts[next];
        if (time != c.time || state != c.state || !((tape[head/8] >> (head%8)) & 1))
            throw std::runtime_error("first contact disagrees at cell "+std::to_string(c.cell));
        std::printf("%2d  %9d  %c  %lld\n",next+1,c.cell,'A'+state,static_cast<long long>(time));
        ++next;
    }
    void one() {
        const int offset = head%8;
        int bits = tape[head/8];
        const auto a = table[state][(bits>>offset)&1];
        if (a.state<0) throw std::runtime_error("B1");
        set(bits,offset,a.write);
        tape[head/8] = static_cast<std::uint8_t>(bits);
        head += a.direction;
        state = a.state;
        ++time;
    }
    const TileRun& excursion(int bits,int offset) {
        auto& r = cache[(bits*6+state)*2+(offset==7)];
        if (r.steps) return r;
        r.bits = bits;
        r.end = offset;
        r.state = state;
        while (0 <= r.end && r.end < 8) {
            const auto a = table[r.state][(r.bits>>r.end)&1];
            if (a.state<0) throw std::runtime_error("B1 within tile");
            set(r.bits,r.end,a.write);
            r.end += a.direction;
            r.state = a.state;
            if (++r.steps > 256*8*6) throw std::runtime_error("confined cycle");
        }
        return r;
    }
    int cell(int p) const { return (tape.at(p/8)>>(p%8))&1; }

public:
    Replay() {
        for (int j=0; j<12; ++j)
            if ("111110110111"[j]=='1') mark(-1-j);
        int p=4;
        for (int gap : {1320,8628,107996733,33554430,8388606,2097150,524286,131070,
                        32766,8190,2046,510,126,30,6,0}) {
            p += gap;
            for (int j=0; j<6; ++j) mark(p++);
        }
        p += 2;
        for (int j=0; j<4; ++j) mark(p++);
        // The suffix from the preceding restart starts at cell 18396801869163.
        // Every head access is checked against this much smaller allocated window.
    }
    void run(std::int64_t stop) {
        while (time < stop) {
            if (head<0 || head>=size) throw std::runtime_error("outside certified initial window");
            checkContact();
            int offset = head%8;
            if ((offset!=0 && offset!=7) || (next<count && head/8==(origin+contacts[next].cell)/8)) {
                one();
            } else {
                auto& bits = tape[head/8];
                const auto& r = excursion(bits,offset);
                if (r.steps>stop-time) { one(); continue; }
                bits = static_cast<std::uint8_t>(r.bits);
                state = r.state;
                head += r.end-offset;
                time += r.steps;
            }
        }
    }
    void verifyEndpoint() const {
        if (next!=count || head-origin!=152745817 || state!=3)
            throw std::runtime_error("wrong final state or head");
        int p=head-1;
        auto expect = [&](int bit,int width,int dir){
            for (int i=0; i<width; ++i,p+=dir)
                if (cell(p)!=bit) throw std::runtime_error("wrong endpoint tape");
        };
        int bit=0;
        for (int width : {1,15353093,1,2,1,137382806,1,2,1,8630,1,2,1,1322,1,5,1,2,1,3}) {
            expect(bit,width,-1);
            bit=1-bit;
        }
        expect(0,p+1,-1);
        p=head;
        expect(1,1,1);
        expect(0,1,1);
        for (int digit : {2,2,2,1,3,2,1,4,2,1,5,2,3,4,4,4,4,4,3,1,0,1,0}) {
            expect(1,3*digit,1);
            expect(0,1,1);
        }
        expect(1,7,1);
        if (18396801869163LL-(p-origin)!=18396649123149LL)
            throw std::runtime_error("wrong distance to remote debris");
        expect(0,size-p,1);
        std::puts("Final D visit at +25354268309, head 152745817. Both half-tapes match.");
    }
};
} // namespace

int main() {
    Replay replay;
    replay.run(25354268309LL);
    replay.verifyEndpoint();
}
