// Shared sliding binary words. AI-assisted by Codex.
// Extracted without changing the arithmetic from soc25_deque.cpp.
#pragma once
#include <cstdint>
#include <deque>
#include <iomanip>
#include <sstream>
#include <stdexcept>
#include <string>
namespace sliding {
using u64=uint64_t;
// Stored positions are absolute; changing the logical low end does not shift
// or copy the remaining words. Bits below base are always zero.
struct Bits {
    std::deque<u64> words;
    u64 base=64, first=1;
    explicit Bits(u64 x=0) {if (x) words.push_back(x);}
    void clear() {words.clear();base=64;first=1;}
    void trim() {while (!words.empty() && words.back()==0) words.pop_back();}
    u64 length() const {
        if (words.empty()) return 0;
        return (first+words.size()-1)*64+64-static_cast<u64>(__builtin_clzll(words.back()))-base;
    }
    u64 block(u64& cursor) const {
        const u64 absolute=base+cursor;
        u64 index=(absolute>>6)-first;
        if (index>=words.size()) throw std::runtime_error("read past binary counter");
        u64 w=words[index] & (UINT64_MAX<<(absolute&63));
        while (!w) {
            if (++index>=words.size()) throw std::runtime_error("missing low block");
            w=words[index];
        }
        const u64 position=(first+index)*64+static_cast<u64>(__builtin_ctzll(w))-base;
        const u64 gap=position-cursor;
        cursor=position+1;
        return gap;
    }
    void right(u64 count) {
        if (count>=length()) {clear();return;}
        base+=count;
        while (first<(base>>6)) {words.pop_front();++first;}
        words.front() &= UINT64_MAX<<(base&63);
    }
    void left_one() {
        if (words.empty()) return;
        if (base==0) {base=64;++first;}
        --base;
        if ((base>>6)<first) {words.push_front(0);--first;}
    }
    void add_power(u64 p) {
        const u64 absolute=base+p;
        u64 index=(absolute>>6)-first;
        if (index>=words.size()) words.resize(index+1,0);
        const u64 old=words[index], value=u64(1)<<(absolute&63);
        words[index]+=value;
        if (words[index]>=old) return;
        while (true) {
            if (++index==words.size()) words.push_back(0);
            if (++words[index]) return;
        }
    }
    void subtract_power(u64 p) {
        const u64 absolute=base+p;
        u64 index=(absolute>>6)-first;
        if (index>=words.size()) throw std::runtime_error("negative counter");
        const u64 old=words[index], value=u64(1)<<(absolute&63);
        words[index]-=value;
        if (old>=value) return;
        while (true) {
            if (++index==words.size()) throw std::runtime_error("negative counter");
            const u64 before=words[index];--words[index];
            if (before) return;
        }
    }
    std::string hex() const {
        const u64 count=(length()+63)/64, offset=base&63;
        if (!count) return "0";
        std::ostringstream out;out<<std::hex<<std::setfill('0');
        for (u64 j=count;j-->0;) {
            u64 w=words[j]>>offset;
            if (offset && j+1<words.size()) w|=words[j+1]<<(64-offset);
            out<<std::setw(16)<<w;
        }
        return out.str();
    }
    u64 fingerprint() const {
        // Reproducibility aid, not a cryptographic certificate. Independent
        // validation compares the complete hexadecimal integer instead.
        u64 h=14695981039346656037ULL;
        const u64 count=(length()+63)/64,offset=base&63;
        for (u64 j=0;j<count;++j) {
            u64 w=words[j]>>offset;
            if (offset && j+1<words.size()) w|=words[j+1]<<(64-offset);
            for (unsigned b=0;b<8;++b) {h^=(w>>(8*b))&255;h*=1099511628211ULL;}
        }
        return h;
    }
};

} // namespace sliding
