// Independent single shifted-epoch checker for the two terminal phases in the report.
// Input is one clean y word per line, output is raw probe cost (hex), space, full output F(y).
#include <algorithm>
#include <array>
#include <iostream>
#include <stdexcept>
#include <string>
#include <gmpxx.h>

namespace {
const std::array<std::string,3> pairs = {"21","14","24"};

std::string transfer(const std::string &pair,mpz_class &count,mpz_class &time) {
    if (pair=="22") {
        time += 7*count;
        count *= 2;
        return pair;
    }
    auto it = std::find(pairs.begin(),pairs.end(),pair);
    if (it == pairs.end()) throw std::runtime_error("not aligned");
    int h = int(it-pairs.begin());
    mpz_class next = count + (h+2)%3;
    unsigned long residue = mpz_fdiv_q_ui(next.get_mpz_t(),next.get_mpz_t(),3);
    int g = int((residue+1)%3);
    time += 5*(count-next) + 4*((g==1)-(h==1));
    count.swap(next);
    return pairs[g];
}

void append_virgin(std::string &out, const mpz_class &n, size_t reserve, mpz_class &time) {
    // Add n to the ordinary ternary repunit of a sufficiently large fixed width.
    // Digit 0 denotes -1, digit 1 denotes zero, digit 2 denotes +1.
    if (n!=0) {
        auto width = mpz_sizeinbase(n.get_mpz_t(),3)+1;
        mpz_class power;
        mpz_ui_pow_ui(power.get_mpz_t(),3,width);
        mpz_class biased = n + (power-1)/2;
        auto digits = biased.get_str(3);
        auto first = digits.find_first_not_of('1');
        if (first == std::string::npos || digits[first]!='2') throw std::runtime_error("biased ternary");
        auto k = digits.size()-first;
        size_t negative = 0;
        for (size_t j=digits.size();j-->first;) {
            switch(digits[j]) {
            case '0': out += "14"; ++negative; break;
            case '1': out += "24"; break;
            case '2': out += "21"; break;
            }
        }
        time += 5*n + 4*mpz_class(negative) + (6*mpz_class(reserve)-2)*k;
    }
    for (size_t i=0;i<reserve;++i) out += "421";
}

void epoch(const std::string& y) {
    if(y.empty()) throw std::runtime_error("empty input");
    size_t end=y.size(),r=0;
    while (end>=3 && y.compare(end-3,3,"421")==0) { end-=3; ++r; }
    if (end%2==0) {
        if (!r) throw std::runtime_error("unaligned suffix");
        --r; end+=3;
    }
    if (!end) throw std::runtime_error("missing displaced digit");
    char d=y[0];
    mpz_class n=1,s=0,time=0;
    std::string out;
    for (size_t i=1;i<end;i+=2) {
        if (!n) throw std::runtime_error("outer count exhausted");
        auto p=transfer(y.substr(i,2),s,time);
        std::string lead; char next=p[1];
        if(d=='2') lead=std::string("2")+p[0];
        else if(d=='1') { --n; ++time; lead=std::string("2")+p[0]; }
        else if(p[0]=='1') { --n; time+=3; lead="22"; }
        else {
            --n;
            switch(p[1]) {
            case '1': lead="21"; next='4'; ++s; time+=6; break;
            case '2': lead="22"; next='2'; s+=2; time+=9; break;
            case '4': lead="22"; next='1'; time+=7; break;
            default: throw std::runtime_error("transient");
            }
        }
        out += transfer(lead,n,time);
        d=next;
    }
    if(d=='4' && s==1) { time+=6*r+3; ++r; }
    else if(d=='1' && s==0 && r>0) {
        --r;
        out+=transfer("14",n,time);
        out+=transfer("21",n,time);
    } else throw std::runtime_error("unverified phase");
    append_virgin(out,n,r,time);
    std::cout << time.get_str(16) << ' ' << out << '\n' << std::flush;
}
}

int main() {
    std::string y;
    while(std::getline(std::cin,y)) epoch(y);
}
