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
    void whole_burst(Count t, std::vector<Count>& out) {
        // After the unmarked prefix, r is the trit on the marked slot.
        // A full burst runs at r,r-1,...,0 and always finishes at trit 2.
        ordinary(t-used-1);
        unsigned r=d.trit;
        if (r) out.push_back(d.slots+2*r);
        d.calls+=3+2*r;
        d.interior+=r==0?2:(r==1?8:12);
        d.slots+=1+2*r;
        d.trit=2;
        d.pending=false;
        used=t+r;
    }
    void feed(const std::vector<Count>& in, std::vector<Count>& out) {
        for (Count t : in) {
            if (!t || t>limit || (pending_mark && t<=pending_mark)) throw std::runtime_error("invalid timestamp");
            // The following mark certifies the preceding burst completed.
            if (pending_mark) {
                if (pending_mark<=used) throw std::runtime_error("overlapping C bursts");
                whole_burst(pending_mark,out);
                if (used>=t || d.slots>limit) throw std::runtime_error("overlap or arithmetic limit");
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

// Lift a whole periodic mark stream and exactly time a finite prefix in the
// same pass. At most three input copies restore the coefficient phase of a
// homogeneous digit. Full-copy summaries cover all three trits and
// a pending C at the copy boundary.
Digit prefix_state(const std::vector<Count>& times, Count length, unsigned trit, bool pending) {
    StreamingDigit reg;
    reg.d.trit = trit;
    reg.d.pending = pending;
    std::vector<Count> ignored;
    if (pending && length) {
        // A pending C on the first slot is an initial burst.
        Count take = std::min<Count>(length,trit+1);
        if (!times.empty() && times[0]<=take) throw std::runtime_error("initial C conflict");
        reg.burst(1,take,ignored);
    }
    for (Count t : times) {
        if (t>length) break;
        if (t<=reg.used) throw std::runtime_error("overlapping C bursts in period");
        if (length-t>=2) {
            reg.whole_burst(t,ignored);
        } else {
            unsigned r=(reg.d.trit+(t-reg.used-1)%3)%3;
            reg.burst(t,std::min<Count>(r+1,length-t+1),ignored);
        }
        ignored.clear();
    }
    reg.finish(length,ignored);
    return reg.d;
}

void periodic_band(Count& n, Count& period, std::vector<Count>& marks, Count levels, Count budget) {
    for (Count depth=0; depth<levels; ++depth) {
        if (!period || period>limit/64 || n>limit || marks.size()>budget) throw std::runtime_error("period limit");
        Count copies=0, coefficient=0;
        std::vector<Count> children;
        do {
            if (copies==3) throw std::runtime_error("period did not close");
            for (Count t : marks) {
                Count x=copies*period+t+coefficient;
                unsigned r=x%3;
                if (r) {
                    if (children.size()>=budget) throw std::runtime_error("period mark budget");
                    children.push_back((x+5*r)/3);
                }
                coefficient+=4*(1+r);
            }
            ++copies;
        } while ((copies*period+coefficient)%3);
        Count new_period=(copies*period+coefficient)/3;
        if (!children.empty() && children.back()>new_period) throw std::runtime_error("invalid output period");

        struct Totals { Count periods=0, slots=0, calls=0, interior=0; };
        Totals history[6]{};
        bool seen[6]{};
        Digit current;
        Count j=0, whole=n/period;
        auto add = [&](const Digit& d) {
            current.trit=d.trit; current.pending=d.pending;
            current.slots+=d.slots; current.calls+=d.calls; current.interior+=d.interior;
        };
        while (j<whole) {
            unsigned key=2*current.trit+current.pending;
            if (seen[key]) {
                const Totals& old=history[key];
                Count k=(whole-j)/(j-old.periods);
                if (k) {
                    current.slots+=k*(current.slots-old.slots);
                    current.calls+=k*(current.calls-old.calls);
                    current.interior+=k*(current.interior-old.interior);
                    j+=k*(j-old.periods);
                    continue;
                }
            } else {
                seen[key]=true;
                history[key]={j,current.slots,current.calls,current.interior};
            }
            add(prefix_state(marks,period,current.trit,current.pending));
            ++j;
        }
        if (n%period) add(prefix_state(marks,n%period,current.trit,current.pending));
        std::cout << current.trit << ' ' << current.pending << ' ' << current.slots << ' '
                  << current.calls << ' ' << current.interior << '\n';
        n=current.slots; period=new_period; marks.swap(children);
    }
}

// Finite direct suffix from an arbitrary physically saved register. There is no
// homogeneous-cell assumption here. The fast periodic front end supplies the
// actual pending flags and trits at the cut.
void resume(const std::string& word, Count cut, Count n) {
    if (word.size()!=848 || cut>=424 || n>4000000) throw std::runtime_error("invalid resume prefix");
    std::vector<Count> marks,children;
    for (Count i=0; i<n; ++i) {
        int bit=std::cin.get();
        if (bit!=0 && bit!=1) throw std::runtime_error("invalid binary pulse");
        if (bit) marks.push_back(i+1);
    }
    if (std::cin.peek()!=std::char_traits<char>::eof()) throw std::runtime_error("trailing binary pulse");
    for (Count i=cut; i<424; ++i) {
        char symbol=word[2*i], flag=i ? word[2*i-1] : '2';
        if ((symbol!='1' && symbol!='0' && symbol!='2') || (flag!='2' && flag!='3'))
            throw std::runtime_error("invalid register digit");
        StreamingDigit reg;
        reg.d.trit=(symbol=='1'?0:(symbol=='0'?1:2));
        reg.d.pending=flag=='3';
        children.clear();
        if (reg.d.pending && n) {
            auto take=std::min<Count>(reg.d.trit+1,n);
            if (!marks.empty() && marks.front()<=take) throw std::runtime_error("initial C conflict");
            reg.burst(1,take,children);
        }
        reg.feed(marks,children);
        reg.finish(n,children);
        Digit d=reg.d;
        std::cout << d.trit << ' ' << d.pending << ' ' << d.slots << ' ' << d.calls << ' ' << d.interior << '\n';
        n=d.slots;
        marks.swap(children);
    }
}

int main(int argc, char** argv) try {
    if (argc==5 && std::string(argv[1])=="resume") {
        resume(argv[2],number(argv[3]),number(argv[4]));
        return 0;
    }
    if (argc<5 || argc>7) throw std::runtime_error("usage: line17-marks SLOTS PERIOD DIGITS MARK_BUDGET [BLOCK [PERIODIC_DIGITS]]");
    Count n=number(argv[1]), period=number(argv[2]), digits=number(argv[3]), budget=number(argv[4]);
    Count block = argc >= 6 ? number(argv[5]) : 65536;
    Count periodic = argc == 7 ? number(argv[6]) : 0;
    if (!period || !digits || digits>424 || periodic>=digits || n>limit || !budget || !block || block>10000000)
        throw std::runtime_error("invalid limits");
    std::vector<Count> times;
    Count t, previous=0;
    while (std::cin >> t) {
        if (!t || t<=previous || t>period) throw std::runtime_error("invalid source period");
        times.push_back(t);
        previous=t;
    }
    if (!std::cin.eof()) throw std::runtime_error("invalid source input");
    periodic_band(n,period,times,periodic,budget);
    digits-=periodic;
    // Check the work budget before expanding any full copies of the source.
    auto partial = static_cast<Count>(std::upper_bound(times.begin(),times.end(),n%period)-times.begin());
    if (partial>budget || (times.size() && n/period > (budget-partial)/times.size()))
        throw std::runtime_error("finite mark budget at cut with " + std::to_string(n) + " slots, "
                                 + std::to_string(times.size()) + " marks per " + std::to_string(period) + " slots");
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
