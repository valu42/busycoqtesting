// Finite one-based mark timestamps in a homogeneous trit register.
// The Python worker checks words outside this band and assembles physical TM steps.
#include <algorithm>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

using Count = std::uint64_t;
constexpr Count limit = std::numeric_limits<Count>::max() / 16;
struct Digit {
    unsigned trit = 1;
    bool pending = false;
    Count slots = 0, calls = 0, interior = 0;
};
Count number(const char* str) {
    Count value;
    auto end = str + std::char_traits<char>::length(str);
    auto parsed = std::from_chars(str, end, value);
    if (parsed.ec != std::errc{} || parsed.ptr != end) throw std::runtime_error("invalid integer");
    return value;
}

// A mark's image requires only its timestamp and the cell's current trit.
// Pass bounded chunks through all digits. The final partial burst is
// trimmed once the preceding digit's exact output length becomes known.
struct StreamingDigit {
    Count used=0, pending_mark=0;
    Digit d;
    void ordinary(Count amount) {
        Count sum=d.trit+amount;
        d.trit=sum%3;
        d.slots+=sum/3;
        d.interior+=2*(sum/3);
    }
    void burst(Count t, Count take, std::vector<Count>& out) {
        ordinary(t-used-1);
        for (Count j=0; j<take; ++j) {
            if (d.trit==1) out.push_back(d.slots+2);
            d.calls+=d.trit==0?3:2;
            d.interior+=d.trit==0?2:(d.trit==1?6:4);
            d.slots+=d.trit==0?1:2;
            d.pending=d.trit!=0;
            d.trit=(d.trit+2)%3;
        }
        used=t+take-1;
    }
    void feed(const std::vector<Count>& in, std::vector<Count>& out) {
        for (Count t : in) {
            if (!t || t>limit || (pending_mark && t<=pending_mark)) throw std::runtime_error("invalid timestamp");
            // The following mark certifies the preceding burst completed.
            if (pending_mark) {
                if (pending_mark<=used) throw std::runtime_error("overlapping C bursts");
                Count r=(d.trit+(pending_mark-used-1)%3)%3;
                burst(pending_mark,r+1,out);
                if (used>=t || d.pending || d.slots>limit) throw std::runtime_error("overlap or arithmetic limit");
            }
            pending_mark=t;
        }
    }
    void finish(Count length,std::vector<Count>& out) {
        if (length>limit || used>length) throw std::runtime_error("slot arithmetic limit");
        if (pending_mark) {
            if (pending_mark<=used || pending_mark>length) throw std::runtime_error("invalid final mark");
            Count r=(d.trit+(pending_mark-used-1)%3)%3;
            burst(pending_mark,std::min<Count>(r+1,length-pending_mark+1),out);
        }
        ordinary(length-used);
        d.calls+=length;
    }
};

int main(int argc, char** argv) try {
    if (argc != 5 && argc != 6) throw std::runtime_error("usage: line17-marks SLOTS PERIOD DIGITS MARK_BUDGET [BLOCK]");
    Count n=number(argv[1]), period=number(argv[2]), digits=number(argv[3]), budget=number(argv[4]);
    Count block = argc == 6 ? number(argv[5]) : 65536;
    if (!period || !digits || digits>424 || n>limit || !budget || !block || block>10000000)
        throw std::runtime_error("invalid limits");
    std::vector<Count> times;
    Count t, previous=0;
    while (std::cin >> t) {
        if (!t || t<=previous || t>period) throw std::runtime_error("invalid source period");
        times.push_back(t);
        previous=t;
    }
    if (!std::cin.eof()) throw std::runtime_error("invalid source input");
    // Check the work budget before expanding any full copies of the source.
    auto partial = static_cast<Count>(std::upper_bound(times.begin(),times.end(),n%period)-times.begin());
    if (partial>budget || (times.size() && n/period > (budget-partial)/times.size()))
        throw std::runtime_error("finite mark budget");
    std::vector<StreamingDigit> registers(digits);
    std::vector<Count> incoming, outgoing, marks;
    auto propagate = [&](Count start) {
        for (Count i=start; i<digits && !incoming.empty(); ++i) {
            outgoing.clear();
            registers[i].feed(incoming,outgoing);
            incoming.swap(outgoing);
        }
        marks.insert(marks.end(),incoming.begin(),incoming.end());
        incoming.clear();
    };
    for (Count base=0; base<n && !times.empty(); base+=std::min(period,n-base)) {
        for (Count t : times) {
            if (t>n-base) break;
            incoming.push_back(base+t);
            if (incoming.size()==block) propagate(0);
        }
    }
    propagate(0);
    for (Count i=0; i<digits; ++i) {
        auto& scan=registers[i];
        scan.finish(n,incoming);
        propagate(i+1);
        Digit d=scan.d;
        std::cout << d.trit << ' ' << d.pending << ' ' << d.slots << ' ' << d.calls << ' ' << d.interior << '\n';
        n=d.slots;
    }
    std::cout << "marks";
    for (auto x : marks) std::cout << ' ' << x;
    std::cout << '\n';
    return 0;
} catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 2; }
