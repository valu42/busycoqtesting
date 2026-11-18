#pragma once
#include <deque>
// Exact ordered action of a marked period on a block of drained trits.
// A marked pulse finishes its burst immediately. Following ordinary inputs
// catch up before the next mark. Every local trit action is a permutation.
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

namespace ternary17 {
using U=uint32_t;using B=uint64_t;
struct Action{U state=0;unsigned n=0;B bits=0;};
Action stepword(U s,B bits,unsigned n){
    Action o;o.state=s;
    for(unsigned i=0;i<n;++i){
        auto v=o.state;
        if((bits>>i)&1) {
            if(v) o.bits|=B(1)<<(o.n+2*v-1);
            o.n+=1+2*v;o.state=(5*(v+1))%3;
        }else{if(v==2)++o.n;o.state=(v+1)%3;}
        if(o.n>61)throw std::runtime_error("ternary packet too long");
    }
    return o;
}
struct Tables{
    U depth,count;std::array<U,10> powers{};
    std::array<unsigned,250> mask{};
    std::array<unsigned char,65536> code{};
    std::array<std::array<unsigned short,250>,17> token{};
    std::vector<std::vector<U>> rows;
    std::vector<std::vector<unsigned char>> bytes;
    std::vector<std::array<std::array<unsigned char,256>,5>> sections;
    static unsigned action_code(U x,U y) {
        const unsigned delta=(y+3-x)%3;
        if(!delta)throw std::logic_error("nonpermuting upper trit");
        return x+(delta==2?3:0);
    }
    Tables(unsigned d):depth(d){
        if(!d||d>8)throw std::runtime_error("depth must be 1 through 8");
        powers[0]=1;for(unsigned i=1;i<=d;++i)powers[i]=3*powers[i-1];count=powers[d];
        unsigned k=0;code.fill(255);
        for(unsigned w=0;w<65536;++w)if(!(w&((w>>1)|(w>>2)|(w>>3)))){mask.at(k)=w;code[w]=k++;}
        for(unsigned n=1;n<=16;++n)for(unsigned c=0;c<250;++c){
            unsigned w=mask[c]&((1U<<n)-1);unsigned canon=code[w];
            if(canon!=c){token[n][c]=token[n][canon];continue;}
            token[n][c]=rows.size();rows.emplace_back(count);
            compile(rows.back(),0,0,0,w,n);
            if(count<=256){bytes.emplace_back((count+63)/64*64);std::copy(rows.back().begin(),rows.back().end(),bytes.back().begin());}
        }
        if(count==729||count==2187){
            const unsigned low=243;
            sections.resize(rows.size());
            for(size_t token=0;token<rows.size();++token){
                auto& part=sections[token];const auto& map=rows[token];
                for(unsigned v=0;v<low;++v){
                    part[0][v]=map[v]%low;
                    auto high=[&](unsigned s){return map[v+low*s]/low;};
                    part[1][v]=6*action_code(high(0)%3,high(1)%3);
                    if(count==2187)for(unsigned a=0;a<3;++a)
                        part[2+a][v]=6*action_code(high(a)/3,high(a+3)/3);
                }
            }
        }
    }
    void compile(std::vector<U>& dst,unsigned d,U pos,U end,B w,unsigned n){
        if(d==depth){dst[pos]=end;return;}
        for(unsigned v=0;v<3;++v){auto y=stepword(v,w,n);compile(dst,d+1,pos+v*powers[d],end+y.state*powers[d],y.bits,y.n);}
    }
};
using Tokens=std::vector<unsigned short>;
void apply(U* dst,size_t n,const U* t){
    size_t j=0;
#ifdef __AVX512F__
    for(;j+16<=n;j+=16){
        auto q=_mm512_loadu_si512(dst+j);_mm512_storeu_si512(dst+j,_mm512_i32gather_epi32(q,t,4));
    }
#endif
    for(;j<n;++j)dst[j]=t[dst[j]];
}
std::vector<U> act(const Tables& t,const Tokens& z){
    std::vector<U> r(t.count);std::iota(r.begin(),r.end(),0);
#ifdef __AVX512VBMI__
    if(t.count==729||t.count==2187) {
        alignas(64) unsigned char aux[256];
        for(unsigned i=0;i<256;++i)aux[i]=i;
        __m512i q[4],top[4],section[3][4];
        for(unsigned k=0;k<4;++k){q[k]=_mm512_load_si512(aux+64*k);top[k]=_mm512_setzero_si512();
            for(auto& x:section)x[k]=top[k];}
        alignas(64) unsigned char products[64]{},images[3][64]{};
        auto eval=[](unsigned g,unsigned x){return (g%3+(g>=3?2*x:x))%3;};
        for(unsigned a=0;a<6;++a)for(unsigned x=0;x<3;++x)images[x][a]=eval(a,x);
        for(unsigned a=0;a<6;++a)for(unsigned b=0;b<6;++b)
            products[6*b+a]=Tables::action_code(eval(b,eval(a,0)),eval(b,eval(a,1)));
        auto mult=_mm512_load_si512(products);
        __m512i im[3];for(unsigned i=0;i<3;++i)im[i]=_mm512_load_si512(images[i]);
        for(auto c:z){
            const auto& data=t.sections[c];
            __m512i tables[5][4];
            unsigned fields=t.count==729?2:5;
            for(unsigned i=0;i<fields;++i)for(unsigned j=0;j<4;++j)
                tables[i][j]=_mm512_loadu_si512(data[i].data()+64*j);
            for(unsigned k=0;k<4;++k){
                auto index=q[k];auto hi=_mm512_movepi8_mask(index);
                auto lookup=[&](unsigned i){
                    auto lo=_mm512_permutex2var_epi8(tables[i][0],index,tables[i][1]);
                    auto up=_mm512_permutex2var_epi8(tables[i][2],index,tables[i][3]);
                    return _mm512_mask_blend_epi8(hi,lo,up);
                };
                q[k]=lookup(0);auto u=lookup(1);
                if(t.count==2187){
                    __m512i v[3];for(unsigned j=0;j<3;++j)v[j]=lookup(2+j);
                    for(unsigned j=0;j<3;++j){
                        auto a=_mm512_permutexvar_epi8(top[k],im[j]);
                        auto g=_mm512_mask_blend_epi8(_mm512_cmpeq_epi8_mask(a,_mm512_set1_epi8(1)),v[0],v[1]);
                        g=_mm512_mask_mov_epi8(g,_mm512_cmpeq_epi8_mask(a,_mm512_set1_epi8(2)),v[2]);
                        section[j][k]=_mm512_permutexvar_epi8(_mm512_add_epi8(section[j][k],g),mult);
                    }
                }
                top[k]=_mm512_permutexvar_epi8(_mm512_add_epi8(top[k],u),mult);
            }
        }
        alignas(64) unsigned char high[256],sec[3][256];
        for(unsigned k=0;k<4;++k){_mm512_store_si512(aux+64*k,q[k]);_mm512_store_si512(high+64*k,top[k]);
            if(t.count==2187)for(unsigned j=0;j<3;++j)_mm512_store_si512(sec[j]+64*k,section[j][k]);}
        for(unsigned i=0;i<t.count;++i){unsigned v=i%243,a=i/243%3,b=i/729;
            unsigned upper=eval(high[v],a);
            if(t.count==2187)upper+=3*eval(sec[a][v],b);
            r[i]=aux[v]+243*upper;
        }
        return r;
    }
    if(t.count<=256) {
        alignas(64) unsigned char store[256];
        for(unsigned i=0;i<256;++i)store[i]=i;
        unsigned lanes=(t.count+63)/64;
        __m512i a[4];
        for(unsigned k=0;k<lanes;++k)a[k]=_mm512_load_si512(store+64*k);
        if(lanes==1){
            for(auto c:z){auto x=_mm512_loadu_si512(t.bytes[c].data());a[0]=_mm512_permutexvar_epi8(a[0],x);}
        }else if(lanes==2){
            for(auto c:z){auto p=t.bytes[c].data();auto x=_mm512_loadu_si512(p),y=_mm512_loadu_si512(p+64);
                a[0]=_mm512_permutex2var_epi8(x,a[0],y);a[1]=_mm512_permutex2var_epi8(x,a[1],y);}
        }else{
            for(auto c:z){auto p=t.bytes[c].data();auto x=_mm512_loadu_si512(p),y=_mm512_loadu_si512(p+64);
                auto v=_mm512_loadu_si512(p+128),w=_mm512_loadu_si512(p+192);
                for(auto& s:a){auto lo=_mm512_permutex2var_epi8(x,s,y),hi=_mm512_permutex2var_epi8(v,s,w);
                    s=_mm512_mask_blend_epi8(_mm512_movepi8_mask(s),lo,hi);}
            }
        }
        for(unsigned k=0;k<lanes;++k)_mm512_store_si512(store+64*k,a[k]);
        std::copy_n(store,t.count,r.begin());return r;
    }
#endif
    for(auto c:z)apply(r.data(),r.size(),t.rows[c].data());
    return r;
}
std::vector<U> scan(const std::string& path,const Tables& t,unsigned workers,std::deque<std::pair<unsigned,unsigned>>& suffix){
    std::ifstream f(path,std::ios::binary);if(!f)throw std::runtime_error("cannot open source");
    std::vector<U> result(t.count);std::iota(result.begin(),result.end(),0);
    std::vector<Tokens> group;Tokens tok;
    auto finish=[&](){
        if(group.empty())return;std::vector<std::vector<U>> out(group.size());
        #pragma omp parallel for num_threads(workers) schedule(static)
        for(size_t j=0;j<group.size();++j)out[j]=act(t,group[j]);
        for(const auto& row:out)apply(result.data(),result.size(),row.data());group.clear();
    };
    U width;B slots=0;
    std::vector<unsigned char> bytes;
    while(tiled::coded::read_frame_size(f,width)){
        if(!width||width>4194304)throw std::runtime_error("bad frame");
        bytes.resize((width+15)/16);if(!f.read((char*)bytes.data(),bytes.size()))throw std::runtime_error("truncated frame");
        for(size_t i=0;i<bytes.size();++i){
            if(bytes[i]>=250)throw std::runtime_error("bad alphabet code");
            tok.push_back(t.token[std::min(16u,width-16*unsigned(i))][bytes[i]]);
        }
        unsigned from=bytes.size()>128 ? bytes.size()-128 : 0;
        if(from) suffix.clear();
        for(unsigned j=from;j<bytes.size();++j){
            suffix.emplace_back(t.mask[bytes[j]],std::min(16u,width-16*j));
            if(suffix.size()>128)suffix.pop_front();
        }
        slots+=width;
        if(tok.size()>=65536){group.push_back(std::move(tok));tok=Tokens{};}
        if(group.size()>=workers*4)finish();
    }
    if(!f.eof())throw std::runtime_error("source read error");
    if(!tok.empty())group.push_back(std::move(tok));finish();
    std::cerr<<"source slots "<<slots<<'\n';return result;
}
}
