// Batch the line 411 right call on a run-length encoded tape.
#include <algorithm>
#include <cstdlib>
#include <cassert>
#include <cstdint>
#include <cstring>
#include <limits>
#include <string>
#include <vector>

using Count = std::uint64_t;
using Limb = std::uint64_t;

class Pulses {
    std::vector<Limb> a;
    size_t start = 0;
    size_t top = 0;
    void trim() {
        while (!a.empty() && a.back() == 0) a.pop_back();
        top = a.empty() ? 0 : 64*a.size() - __builtin_clzll(a.back());
    }
public:
    Pulses(const unsigned char *bytes, size_t size): a((size+7)/8,0) {
        for(size_t i=0;i<size;i++) a[i/8] |= Limb(bytes[i])<<(8*(i%8));
        trim();
    }
    bool high(size_t i=0) const { return start+i < top; }
    void shift(size_t n) { start+=n; }
    unsigned bit(size_t i) const {
        size_t j=start+i;
        return j<top ? (a[j/64]>>(j%64))&1 : 0;
    }
    void add(size_t i) {
        size_t j=start+i, k=j/64;
        Limb u=Limb(1)<<(j%64);
        do {
            if(k==a.size()) a.push_back(0);
            a[k]+=u;
            if(a[k]>=u) break;
            ++k;u=1;
        } while(true);
        if(k+1==a.size()) top=64*a.size()-__builtin_clzll(a.back());
    }
    void sub(size_t i) {
        size_t j=start+i, k=j/64;
        Limb u=Limb(1)<<(j%64);
        while(a[k]<u) { a[k]-=u;++k;u=1; }
        a[k]-=u;
        if(k+1==a.size()) trim();
    }
};

struct Word {
    std::vector<Count> lengths;
    int first=0;
    Count extent=0;
    void clear() {lengths.clear();first=0;extent=0;}
    void put(unsigned bit, Count count=1) {
        if(!count)return;
        if(count>std::numeric_limits<Count>::max()-extent) std::abort();
        if(lengths.empty()){first=bit;lengths.push_back(count);}
        else if((first ^ ((lengths.size()-1)&1))==bit) lengths.back()+=count;
        else lengths.push_back(count);
        extent+=count;
    }
    void finish() {
        if(!lengths.empty() && !(first ^ ((lengths.size()-1)&1))) {
            extent-=lengths.back();lengths.pop_back();
        }
        if(lengths.empty())first=0;
    }
};

class Source {
    const Word *source;
    size_t next=0;
    unsigned cell=0;
    Count rest=0;
    // These ones stand before the untouched suffix. An overwritten first
    // bit is represented by consuming its old value before inserting a one.
    Count prefix=0;
    void load() {
        if(next<source->lengths.size()) {
            cell=source->first ^ (next&1);
            rest=source->lengths[next++];
        } else {cell=0;rest=std::numeric_limits<Count>::max();}
    }
public:
    Source(const Word &w):source(&w){load();}
    void ones(Count n){prefix+=n;}
    unsigned get(){
        if(prefix){--prefix;return 1;}
        unsigned val=cell;
        if(--rest==0)load();
        return val;
    }
    unsigned read(unsigned n){
        unsigned x=0;
        for(unsigned j=0;j<n;j++)x=x*2+get();
        return x;
    }
    Count ones_run() const {
        return prefix+(cell==1?rest:0);
    }
    void consume_ones(Count n) {
        Count pre=std::min(n,prefix);prefix-=pre;n-=pre;
        if(n) {
            assert(cell==1 && n<=rest);
            rest-=n;
            if(!rest)load();
        }
    }
    void append_to(Word &w) const {
        if(prefix)w.put(1,prefix);
        if(rest!=std::numeric_limits<Count>::max() && (next<source->lengths.size() || cell==1))
            w.put(cell,rest);
        for(size_t k=next;k<source->lengths.size();k++)w.put(source->first ^ (k&1),source->lengths[k]);
    }
};

static void block(Word &out, size_t m, const Pulses &sum, bool closed) {
    assert(m>0 && (!closed || m>=2));
    out.put(sum.bit(0));out.put(0);
    for(size_t i=1;i<m;i++){
        unsigned bit=sum.bit(i);
        out.put(0);out.put(bit);
        bool last=closed && i+1==m;
        out.put(bit || last);out.put(last);
    }
}

// Write the m pending binary digits once their outgoing carry is determined.
static void power(Source src, Pulses count, Word &out){
    out.clear();
    while(count.high()) {
        Count ones=src.ones_run()&~Count(1);
        if(ones){out.put(1,ones);src.consume_ones(ones);continue;}
        unsigned root=src.read(2);
        if(root==1) {out.put(1,2);count.sub(0);continue;}
        assert(root==0 || root==2);
        if(root==2)count.add(0);
        size_t m=1;
        bool emitted=false;
        while(count.high(m)) {
            Source after=src;
            unsigned group=after.read(4);
            if(group==0 || group==6 || group==3 || group==7) {
                if(group&4)count.add(m);
                ++m;src=after;
                if((group&3)==3) {
                    block(out,m,count,true);count.shift(m);emitted=true;break;
                }
                continue;
            }
            if(group&8) {
                if(m==1){out.put(1,2);count.sub(1);}
                else {block(out,m,count,true);count.shift(m);count.sub(0);}
                emitted=true;break;
            }
            if(group==1 || group==2) {
                ++m;src=after;
                if(group==1){block(out,m,count,true);count.shift(m);emitted=true;break;}
                continue;
            }
            assert(group==4 || group==5);
            out.put(1,4*m);count.sub(m);
            src.read(3);src.ones(1);
            emitted=true;break;
        }
        if(!emitted){block(out,m,count,false);src.append_to(out);out.finish();return;}
    }
    src.append_to(out);out.finish();
}

static Word tape, result;
extern "C" {
void set_word(const char *bits) {
    tape.clear();
    while(*bits)tape.put(*bits++=='1');
    tape.finish();
}
void exponentiate(const unsigned char *data,size_t size){
    power(Source(tape),Pulses(data,size),result);
    std::swap(tape,result);
}
int take_boundary(const unsigned char *data,size_t size,Count *skipped){
    Source src(tape);
    Count p=0;
    for(;;) {
        Source copy=src;
        if(copy.read(4)!=9)break;
        src=copy;p+=4;
    }
    *skipped=p;
    if(src.get()==0) {
        src.ones(p);power(src,Pulses(data,size),result);std::swap(tape,result);return 0;
    }
    if(src.get()==1){
        unsigned char one=1;power(src,Pulses(&one,1),result);std::swap(tape,result);return 1;
    }
    Source copy=src;
    if(copy.get()==1) {
        result.clear();src.append_to(result);result.finish();std::swap(tape,result);return 2;
    }
    return 3;
}
Count width(){return tape.extent;}
Count runs(){return tape.lengths.size();}
const char *word_prefix(Count length) {
    static std::string s;
    s.clear();
    for(size_t i=0;i<tape.lengths.size() && length;i++){
        Count take=std::min(length,tape.lengths[i]);
        s.append(take,(tape.first^(i&1))?'1':'0');length-=take;
    }
    return s.c_str();
}
}
extern "C" {
int leading(){return tape.first;}
const Count *run_data(){return tape.lengths.data();}
}
