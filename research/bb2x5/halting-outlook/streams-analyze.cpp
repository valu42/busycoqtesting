// Instrument the existing exact finite-stream engine; no simulation rule changed.
#define main inherited_main
#include "../frontiers/longitudinal.cpp"
#undef main

struct Stats {
    mpz_class length=0, b=0, bb=0;
    int first=-1,last=-1;
};
Stats cat(Stats a, const Stats &b) {
    if (a.length==0) return b;
    if (b.length==0) return a;
    a.bb+=b.bb+(a.last==1 && b.first==1 ? 1:0);
    a.length+=b.length; a.b+=b.b; a.last=b.last; return a;
}
Stats stats(const Word &w) {
    Stats a;
    a.length=w.size;
    if (!w.size) return a;
    a.first=w.at(0,1); a.last=w.at(w.size-1,1);
    int last=-1;
    Count count_b=0,count_bb=0;
    for(Count k=0;k<w.size;++k) {
        int bit=w.at(k,1); count_b+=bit;
        if(last==1 && bit==1) ++count_bb;
        last=bit;
    }
    a.b=count_b; a.bb=count_bb; return a;
}
Stats repeat(Stats a, const mpz_class &n) {
    if(n==0 || a.length==0) return Stats{};
    a.bb=a.bb*n+(a.first==1&&a.last==1 ? n-1:mpz_class(0));
    a.b*=n; a.length*=n; return a;
}
std::string prefix(const Stream &s, unsigned limit) {
    std::string out;
    auto append=[&](const Word &w) {
        for(Count k=0;k<w.size && out.size()<limit;++k) out.push_back(w.at(k,1)?'B':'A');
    };
    append(s.prefix);
    for(mpz_class n=0;n<s.copies && out.size()<limit && s.period.size;++n) append(s.period);
    append(s.suffix); return out;
}
int main(int argc,char **argv) try {
    if(argc!=3) throw std::runtime_error("usage: streams-analyze groups max-materialized-bits");
    mpz_class groups(argv[1]); bit_limit=parse(argv[2]);
    std::string machine,period,first,seed;
    std::cin>>machine>>period>>first>>seed;
    if(seed==".") seed.clear();
    Stream input;
    if(seed.empty()) {
        input.prefix=letters("A"); input.period=letters(period); input.copies=groups-1;
        input.suffix=letters(period.substr(0,period.size()-1));
    } else {
        input.period=letters(period.back()+period.substr(0,period.size()-1)); input.copies=groups;
    }
    Transducer trans(machine,0,first);
    std::string tape=seed;
    for(unsigned depth=0;input.size()!=0;++depth) {
        auto a=cat(cat(stats(input.prefix),repeat(stats(input.period),input.copies)),stats(input.suffix));
        std::cout<<depth<<'\t'<<a.length<<'\t'<<a.b<<'\t'<<a.bb<<'\t'<<a.last<<'\t'<<prefix(input,128)<<'\n';
        unsigned symbol=depth<seed.size()?unsigned(seed[depth]-'0'):0U;
        unsigned state=2*symbol+(depth+1>=seed.size());
        input=trans.image(input,state);
        if(depth==tape.size()) tape.push_back(char('0'+state/2));
        else tape[depth]=char('0'+state/2);
    }
    std::cout<<"tape\t"<<tape<<'\n';
} catch(const std::exception &e) {std::cerr<<e.what()<<'\n';return 2;}
