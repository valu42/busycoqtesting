// Exhaust ordinary rational direction cycles and their bounded integer deviations.
// Requires C++17, signed and unsigned 128-bit arithmetic, and no external libraries.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <set>
#include <stdexcept>
#include <vector>

using Word = std::uint64_t;
using Signed = std::int64_t;
using Wide = __uint128_t;
using Direction = std::pair<Word,Word>;  // denominator, smallest numerator
constexpr Word default_limit = 14984528;
constexpr Word largest_limit = 1290157064;
constexpr std::array<Signed,4> gains = {5,9,7,7};
constexpr std::array<Signed,4> offsets = {20,35,26,29};

Word inverse_four(Word x, Word modulus) {
    for (int bit=0; bit<2; ++bit)
        x=x/2+(x%2)*(modulus/2+1);
    return x;
}

Word successor(Word q, Word k) {
    if (3*k>q && 2*k<q) return 3*k-q;
    if (9*k<2*q && k%4==0) return 9*(k/4);
    return 0;
}

class DirectionSearch {
    Word limit, modulus=1;
    int length=0;
    std::array<std::array<Word,32>,64> coefficient{};
    std::set<Direction> result;

    void recover(Word residue) {
        ++leaves;
        // Adjacent Euclidean vectors form a basis of r = residue*t (mod modulus).
        Word previous=modulus, r=residue;
        __int128_t last_t=0, t=1;
        while (r>limit/2) {
            Word quotient=previous/r;
            Word remainder=previous-quotient*r;
            previous=r;
            r=remainder;
            auto next=last_t-__int128_t(quotient)*t;
            last_t=t;
            t=next;
        }
        if (r==0 || t<=0 || t>limit) return;
        Word q=Word(t);
        // Choose the phase just after P and just before J in a mixed cycle.
        if (3*r<=q || 2*r>=q || q%2==0 || q%3==0 || std::gcd(r,q)!=1) return;
        Word smallest=r, k=r;
        do {
            k=successor(q,k);
            if (!k) return;
            smallest=std::min(smallest,k);
        } while (k!=r);  // injectivity prevents entry into a different cycle
        result.emplace(q,smallest);
    }

    void past(int n, int pairs, Word residue) {
        if (n>=length) {
            recover(residue);
            return;
        }
        // Adding an earlier J subtracts 3^n / 4^pairs. An earlier P
        // leaves the constant unchanged. Both relations are modulo 3^length.
        Word drop=coefficient[n][pairs];
        past(n+1,pairs,residue>=drop ? residue-drop : modulus-(drop-residue));
        past(n+2,pairs+1,residue);
    }

public:
    Word leaves=0;
    explicit DirectionSearch(Word q_limit) : limit(q_limit) {
        if (limit<5 || limit>largest_limit) throw std::invalid_argument("unsupported limit");
        while (Wide(modulus)<=Wide(limit)*limit) {
            modulus*=3;
            ++length;
        }
        Word power=1;
        for (int n=0; n<length; ++n) {
            Word value=power;
            for (int p=0; p<=length/2; ++p) {
                coefficient[n][p]=value;
                value=inverse_four(value,modulus);
            }
            power*=3;
        }
    }

    const std::set<Direction>& run() {
        past(2,1,0);  // The most recent block is P.
        return result;
    }
};

struct Counts {
    Word suffix_words=0;
    Word deviations=0;
};

struct Phase {
    Word k;
    bool jump;
};

std::vector<Phase> build_cycle(Word q, Word first) {
    std::vector<Phase> cycle;
    Word k=first;
    do {
        cycle.push_back({k,3*k>q});
        k=successor(q,k);
        if (!k) throw std::logic_error("invalid normalized cycle");
    } while (k!=first);
    return cycle;
}

// Choose any phase with the fewest P blocks in a long-enough backward suffix.
struct Suffix { int reference=0, count=0, pairs=100; };
Suffix choose_suffix(const std::vector<Phase>& cycle, Word q) {
    int need=0;
    for (Word power=1; power<=7*q; power*=3) ++need;
    Suffix best;
    int phases=int(cycle.size());
    for (int ref=0; ref<phases; ++ref) {
        int cursor=ref, calls=0, pairs=0, count=0;
        while (calls<need) {
            cursor=cursor ? cursor-1 : phases-1;
            bool jump=cycle[cursor].jump;
            calls+=jump ? 1 : 2;
            pairs+=!jump;
            ++count;
        }
        if (pairs<best.pairs) best={ref,count,pairs};
    }
    return best;
}

std::vector<Signed> possible_deviations(Word q, const std::vector<Phase>& cycle,
                                        Suffix suffix, Counts& counts) {
    const int phases=int(cycle.size());
    Word modulus=1;
    int cursor=suffix.reference;
    for (int i=0; i<suffix.count; ++i) {
        cursor=cursor ? cursor-1 : phases-1;
        modulus*=cycle[cursor].jump ? 3 : 9;
    }
    Word scale=1;
    std::vector<Word> values{0};
    cursor=suffix.reference;
    for (int i=0; i<suffix.count; ++i) {
        Word end_k=cycle[cursor].k;
        cursor=cursor ? cursor-1 : phases-1;
        if (cycle[cursor].jump) {
            Word term=Word(Wide(scale)*(q-2*end_k)%modulus);
            for (Word& v:values) v=(v+term)%modulus;
            scale=3*scale%modulus;
        } else {
            std::array<Word,4> terms;
            scale=inverse_four(scale,modulus);
            for (int r=0; r<4; ++r) {
                Word constant=q*offsets[r]-4*end_k*gains[r];
                terms[r]=Word(Wide(scale)*constant%modulus);
            }
            std::size_t old=values.size();
            values.resize(4*old);
            for (std::size_t j=old; j>0; --j) {
                Word v=values[j-1];
                for (int r=0; r<4; ++r) values[4*(j-1)+r]=(v+terms[r])%modulus;
            }
            scale=9*scale%modulus;
        }
    }
    counts.suffix_words+=values.size();
    std::vector<Signed> possible;
    for (Word v:values) {
        Signed e=v ? Signed(v)-Signed(modulus) : 0;
        if (e>=-7*Signed(q)) possible.push_back(e);
    }
    std::sort(possible.begin(),possible.end());
    possible.erase(std::unique(possible.begin(),possible.end()),possible.end());
    counts.deviations+=possible.size();
    return possible;
}

bool survives(Word q, Word first, Counts& counts) {
    auto cycle=build_cycle(q,first);
    Suffix suffix=choose_suffix(cycle,q);
    auto entries=possible_deviations(q,cycle,suffix,counts);
    std::vector<std::size_t> stamp(entries.size());
    for (std::size_t start=0; start<entries.size(); ++start) {
        std::size_t cursor=start, id=start+1;
        while (stamp[cursor]==0) {
            stamp[cursor]=id;
            Signed e=entries[cursor];
            int phase=suffix.reference;
            do {
                bool jump=cycle[phase].jump;
                phase=(phase+1)%int(cycle.size());
                Signed next_k=Signed(cycle[phase].k);
                if (jump) {
                    e=3*e+Signed(q)-2*next_k;
                } else {
                    int r=int((Word(e)*q)%4);
                    Signed numerator=9*e+Signed(q)*offsets[r];
                    if (numerator%4) throw std::logic_error("nonintegral pair");
                    e=numerator/4-next_k*gains[r];
                }
                if (e>0 || e< -7*Signed(q)) break;
            } while (phase!=suffix.reference);
            if (e>0 || e< -7*Signed(q)) break;
            auto found=std::lower_bound(entries.begin(),entries.end(),e);
            if (found==entries.end() || *found!=e) break;
            cursor=std::size_t(found-entries.begin());
            if (stamp[cursor]==id) {
                std::cerr << "repeated deviation q=" << q << " k=" << cycle[phase].k
                          << " e=" << e << '\n';
                return true;
            }
        }
    }
    return false;
}

int main(int argc, char** argv) {
    if (argc>2) return 2;
    try {
        Word bound=argc==2 ? std::stoull(argv[1]) : default_limit;
        DirectionSearch search(bound);
        const auto& cycles=search.run();
        Counts counts;
        for (auto [q,k]:cycles) if (survives(q,k,counts)) return 1;
        if (bound==default_limit && (cycles.size()!=400 || search.leaves!=1346269 ||
                                    counts.suffix_words!=494824 || counts.deviations!=98775))
            throw std::logic_error("unexpected default totals");
        std::cout << bound << " denominator limit, " << search.leaves << " words, "
                  << cycles.size() << " direction cycles, " << counts.suffix_words
                  << " fine suffixes, " << counts.deviations << " bounded deviations, no cycle.\n";
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 2;
    }
}
