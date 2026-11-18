// Fuse several line-17 digits and compute the exact order of a complete
// source period on their physical trits and pending bits.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
#ifdef __AVX512F__
#include <immintrin.h>
#endif
#include <string>
namespace bm {
using U=uint32_t;using B=uint64_t;
struct Out{B bits=0;unsigned n=0,end=6;};
Out digit(unsigned s,B input,unsigned n) {
    Out x;unsigned v=s/2,p=s%2;
    for(unsigned i=0;i<n;++i){
        unsigned bit=(input>>i)&1;
        if(p&&bit)return {};
        if(p||bit){
            if(v==1)x.bits|=B(2)<<x.n;
            x.n+=v?2:1;p=v!=0;v=(v+2)%3;
        }else{if(v==2)++x.n;v=(v+1)%3;}
        if(x.n>61)throw std::runtime_error("fused token exceeds 61 slots");
    }
    x.end=2*v+p;return x;
}
struct Table {
    unsigned depth,invalid;
    std::array<U,7> pow{};
    std::vector<std::vector<U>> tables;
    std::array<std::array<unsigned short,250>,17> ids{};
    std::array<unsigned,250> masks{};
    explicit Table(unsigned d):depth(d) {
        if(!d||d>6)throw std::runtime_error("fused depth must be 1 through 6");
        pow[0]=1;for(unsigned i=1;i<=d;++i)pow[i]=6*pow[i-1];invalid=pow[d];
        unsigned k=0;
        for(unsigned w=0;w<65536;++w)if(!(w&((w>>1)|(w>>2)|(w>>3))))masks.at(k++)=w;
        if(k!=250)throw std::logic_error("bad 16-slot alphabet");
        for(unsigned n=1;n<=16;++n)for(unsigned c=0;c<250;++c){
            auto w=masks[c]&((1u<<n)-1);
            auto canon=std::lower_bound(masks.begin(),masks.end(),w)-masks.begin();
            if(unsigned(canon)==c){
                ids[n][c]=tables.size();tables.emplace_back(invalid+1,invalid);
                compile(tables.back(),0,0,0,w,n);
            }else ids[n][c]=ids[n][canon];
        }
    }
    void compile(std::vector<U>& table,unsigned d,U pos,U finish,B bits,unsigned n){
        if(d==depth){table[pos]=finish;return;}
        for(unsigned s=0;s<6;++s){
            auto x=digit(s,bits,n);
            if(x.end<6)compile(table,d+1,pos+pow[d]*s,finish+pow[d]*x.end,x.bits,x.n);
        }
    }
};
using Tokens=std::vector<unsigned short>;
void apply(U* dst,size_t count,const U* table){
    size_t i=0;
#ifdef __AVX512F__
    for(;i+16<=count;i+=16){
        auto ix=_mm512_loadu_si512(dst+i);
        _mm512_storeu_si512(dst+i,_mm512_i32gather_epi32(ix,table,4));
    }
#endif
    for(;i<count;++i)dst[i]=table[dst[i]];
}
std::vector<U> transfer(const Table& tbl,const Tokens& tokens,unsigned& rank) {
    const unsigned n=tbl.invalid+1;
    std::vector<U> image(n);std::iota(image.begin(),image.end(),0);
    // A short prefix often identifies distinct physical states. One lane is
    // sufficient for each surviving image, including the rejecting sink.
    size_t prefix=std::min<size_t>(16,tokens.size());
    for(size_t i=0;i<prefix;++i)apply(image.data(),n,tbl.tables[tokens[i]].data());
    std::vector<U> dest(n,n),live;
    for(auto& x:image){
        if(dest[x]==n){dest[x]=live.size();live.push_back(x);}
        x=dest[x];
    }
    rank=live.size();
    for(size_t i=prefix;i<tokens.size();++i)apply(live.data(),live.size(),tbl.tables[tokens[i]].data());
    for(auto& x:image)x=live[x];
    return image;
}
std::vector<U> scan(const std::string& path,const Table& tbl,unsigned workers) {
    std::ifstream f(path,std::ios::binary);
    if(!f)throw std::runtime_error("cannot open coded frames");
    const U n=tbl.invalid+1;
    std::vector<U> whole(n);std::iota(whole.begin(),whole.end(),0);
    std::vector<Tokens> group;
    Tokens tok;unsigned width=0,rank_min=n,rank_max=0;uint64_t slots=0,frames=0;
    auto flush=[&]{
        if(group.empty())return;
        std::vector<std::vector<U>> maps(group.size());std::vector<unsigned> ranks(group.size());
        #pragma omp parallel for num_threads(workers) schedule(static)
        for(size_t j=0;j<group.size();++j)maps[j]=transfer(tbl,group[j],ranks[j]);
        for(size_t j=0;j<maps.size();++j){
            apply(whole.data(),whole.size(),maps[j].data());
            rank_min=std::min(rank_min,ranks[j]);rank_max=std::max(rank_max,ranks[j]);
        }
        group.clear();
    };
    std::vector<unsigned char> bytes;
    std::array<unsigned char,4> size{};
    while(f.peek()!=std::char_traits<char>::eof()){
        if(!f.read(reinterpret_cast<char*>(size.data()),size.size()))throw std::runtime_error("short frame header");
        width=U(size[0])|(U(size[1])<<8)|(U(size[2])<<16)|(U(size[3])<<24);
        if(!width||width>4194304)throw std::runtime_error("bad frame length");
        slots+=width;++frames;bytes.resize((width+15)/16);
        if(!f.read((char*)bytes.data(),bytes.size()))throw std::runtime_error("truncated frame");
        for(unsigned i=0;i<bytes.size();++i){
            unsigned c=bytes[i];if(c>=250)throw std::runtime_error("bad coded symbol");
            auto nslots=std::min(16u,width-16*i);tok.push_back(tbl.ids[nslots][c]);
        }
        if(tok.size()>=65536){group.push_back(std::move(tok));tok=Tokens{};}
        if(group.size()>=workers*3)flush();
    }
    if(!f.eof())throw std::runtime_error("base read failed");
    if(!tok.empty())group.push_back(std::move(tok));flush();
    std::cerr<<"source slots "<<slots<<" frames "<<frames<<" stripe ranks "<<rank_min<<' '<<rank_max<<'\n';
    return whole;
}
}
int main(int argc,char** argv)try{
    using namespace bm;
    if(argc!=5)throw std::runtime_error("block-map CODED_FILE BASE_CUT DEPTH THREADS");
    auto natural=[](const std::string& s){
        if(s.empty()||s.find_first_not_of("0123456789")!=std::string::npos)
            throw std::runtime_error("expected an unsigned decimal argument");
        return std::stoull(s);
    };
    const auto cut=natural(argv[2]),d=natural(argv[3]),workers=natural(argv[4]);
    if(d<1||d>6||cut>424-d||workers<1||workers>64)throw std::runtime_error("invalid dimensions");
    Table table(d);auto t=std::chrono::steady_clock::now();auto m=scan(argv[1],table,workers);
    unsigned initial=0;
    for(unsigned i=0;i<d;++i)initial+=2*table.pow[i];
    std::vector<unsigned> orbit;
    std::vector<int> seen(table.invalid,-1);
    for(unsigned s=initial;;s=m[s]){
        if(s==table.invalid)throw std::runtime_error("invalid full-period input");
        if(seen[s]>=0){if(seen[s]!=0)throw std::runtime_error("nonzero macro preperiod");break;}
        seen[s]=orbit.size();orbit.push_back(s);
    }
    for(unsigned i=1;i<=d;++i){
        unsigned h=1;
        while(h<orbit.size() && (orbit[h]%table.pow[i])!=(initial%table.pow[i]))++h;
        std::cout<<cut+i<<" source-copies "<<h<<'\n';
    }
    std::cout<<"orbit";for(auto s:orbit)std::cout<<' '<<s;std::cout<<'\n';
    std::cerr<<"seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count()<<'\n';
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 2;}
