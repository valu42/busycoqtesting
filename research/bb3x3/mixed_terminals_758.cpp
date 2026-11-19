// Exhaust ordinary reset excursions ending in L followed by an immediate halt.
// c++ -std=c++17 -O3 mixed_terminals_758.cpp -o mixed_terminals_758
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>

using Int = __int128_t;
using Word = std::uint32_t;
constexpr int gain[] = {5, 9, 7, 7};
constexpr int shift[] = {20, 35, 26, 29};

std::string decimal(Int n) {
    std::string s;
    do {
        s.push_back(char('0'+n%10));
        n /= 10;
    } while (n);
    std::reverse(s.begin(), s.end());
    return s;
}

Int floor_div(Int n, Int d) {
    return n/d - (n%d < 0);
}

struct Strip {
    Int a, den, low, high;  // low <= den*d - a*u <= high
    Strip inverse_jump() const {
        return {a+den, 3*den, low+2*a-den, high+2*a-den};
    }
    Strip inverse_bulk_pair() const {
        return {4*a, 9*den, 4*low+36*a-35*den, 4*high+20*a-20*den};
    }
};

class Search {
    int low_m, high_m, depth, base;
    bool exception;
    std::array<Int,77> power{};
    std::uint64_t words = 0, candidates = 0, hits = 0;

    void replay(Int h, Int t, int m, int even, Word word, int n) {
        if (t < h || t > 3*h-3) return;
        ++candidates;
        Int u=t, d=(t-h)/2;
        for (int i=0; i<n; ++i, word >>= 1) {
            if (word & 1) {
                int r=int(d%4);
                d=(9*d+shift[r])/4;
                u+=gain[r];
                if (2*d+1>u) return;
            } else {
                d=3*d-u+1;
                if (d<0) return;
                u+=2;
            }
            if (2*d+1==u) return;  // a=1 before the requested endpoint
        }
        Int a=2*u-4*d-1, q=(d+1)/2;
        if (exception) {
            if (3*d!=u-2 || !(d%2)) return;
        } else if (a!=10*q+9 && !(q%2 && a==10*q+11)) {
            return;
        }
        ++hits;
        std::cout << decimal(t-2*m-4*even) << ' ' << m << ' ' << even << ' '
                  << n << ' ' << decimal(a) << ' ' << decimal(2*d+1) << '\n';
    }

    void test(const Strip& strip, Word word, int n) {
        ++words;
        Int den=strip.den-2*strip.a;
        // Avoid the large product 3^m * strip.den at high exponents.
        Int initial=power[base]*strip.den;
        Int quotient=initial/den, remainder=initial%den;
        for (int m=base; m<=high_m; ++m) {
            if (m>=low_m) {
                for (int even=0; even<=1; ++even) {
                    Int b=1+even, h=b*power[m], whole=b*quotient, rem=b*remainder;
                    Int start=whole-floor_div(-rem-2*strip.low,den);
                    Int end=whole+floor_div(rem+2*strip.high,den);
                    if ((start-h)%2) ++start;
                    for (Int t=start; t<=end; t+=2) replay(h,t,m,even,word,n);
                }
            }
            // denominator > 0 and 0 <= remainder < denominator
            remainder*=3;
            quotient=3*quotient;
            while (remainder>=den) {
                remainder-=den;
                ++quotient;
            }
        }
    }

    void traverse(const Strip& strip, Word word, int n) {
        // The *first* symbol is the low bit. A nonempty word must begin with P
        // since the initial J run has already been maximized.
        if (!n || (word&1)) test(strip,word,n);
        if (n==depth) return;
        traverse(strip.inverse_jump(),word<<1,n+1);
        traverse(strip.inverse_bulk_pair(),(word<<1)|1,n+1);
    }

public:
    Search(int first, int last, int blocks, bool use_exception)
        : low_m(first), high_m(last), depth(blocks),
          base(std::min(first,75-2*(blocks+1))), exception(use_exception) {
        if (first<2 || first>last || last>76 || blocks<0 || blocks>30)
            throw std::invalid_argument("require 2 <= m_min <= m_max <= 76 and 0 <= depth <= 30");
        power[0]=1;
        for (unsigned i=1; i<power.size(); ++i) power[i]=3*power[i-1];
    }

    void run() {
        if (exception) traverse({1,3,-2,-2},0,0);
        else traverse({2,9,-17,-10},0,0);
        std::cerr << words << " words, " << candidates << " candidates, " << hits << " hits\n";
    }
};

int main(int argc, char** argv) {
    if (argc!=4 && !(argc==5 && std::string(argv[4])=="--exception")) {
        std::cerr << "usage: mixed_terminals_758 m_min m_max depth [--exception]\n";
        return 2;
    }
    try {
        Search(std::stoi(argv[1]),std::stoi(argv[2]),std::stoi(argv[3]),argc==5).run();
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
