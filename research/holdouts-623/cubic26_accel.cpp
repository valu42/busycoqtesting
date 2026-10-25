// Guarded composition of Racheline's two-counter rules for holdout 26.
// Source and derivation: CUBIC26.md. This executable is UNVERIFIED exploration.
// A halt is a candidate requiring proof; a budget is UNKNOWN.
// Counts are recurrence iterations, never raw TM steps. AI-assisted by Codex.
#include <algorithm>
#include <array>
#include <charconv>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <memory>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

using u64 = uint64_t;
using i64 = int64_t;
using u128 = __uint128_t;
using i128 = __int128_t;
using Clock = std::chrono::steady_clock;
constexpr const char* MACHINE = "1RB1LC_1LC1RD_1LA0LB_0RB1RE_1RF0RA_---0RC";
constexpr u64 SAFE_SUM = std::numeric_limits<u64>::max()/8;

struct State {
    u64 a, b;
    bool operator==(const State& other) const { return a == other.a && b == other.b; }
};

// Returns a branch number, -1 for halt, or -2 for an uncovered configuration.
// The caller checks a+b <= SAFE_SUM before arithmetic.
int scalar(State& s) {
    const u64 a = s.a, b = s.b;
    if (!(a&1) && b >= a+3) { s = {2*a+4, b-a-1}; return 0; }
    if ((a&1) && b >= a+4) { s = {2*a+3, b-a}; return 1; }
    if ((a&1) && b == a+3) { s = {2*a+1, 9}; return 2; }
    if (b == a+2) { s = {1, 2*a+7}; return 3; }
    if (b == a+1) { s = {4, 2*a+4}; return 4; }
    if (a >= b && b >= 4) { s = {a-b+1, 2*b+3}; return 5; }
    if (b == 3 && a >= 2) return -1;
    if (b == 2 && a >= 4) { s = {a-3, 7}; return 6; }
    return -2;
}

struct Table {
    unsigned k;
    u64 radix;
    std::array<std::vector<int32_t>, 4> corrections;

    explicit Table(unsigned bits): k(bits), radix(u64(1)<<bits) {
        if (bits < 1 || bits > 24) throw std::runtime_error("block bits outside 1..24");
        for (unsigned p=0; p<4; ++p) {
            corrections[p].resize(radix);
            build(p, 0, 0, 0, p&1, p>>1, 0);
        }
    }

    void build(unsigned seed, unsigned depth, u64 word, i64 c,
               unsigned a_parity, unsigned sum_parity, unsigned d) {
        if (depth == k) {
            if (c < INT32_MIN || c > INT32_MAX) throw std::runtime_error("table overflow");
            corrections[seed][word] = static_cast<int32_t>(c);
            return;
        }
        build(seed, depth+1, 2*word, 2*c+4-a_parity,
              a_parity, sum_parity^1, d+3);
        build(seed, depth+1, 2*word+1, 2*c-d+1,
              sum_parity^1, sum_parity, d+4);
    }

    bool jump(State& s) const {
        const u64 n = s.a+s.b;
        u64 word, remainder;
        if (s.a <= UINT64_MAX/radix) {
            const u64 x = s.a*radix;
            word = x/n;
            remainder = x%n;
        } else {
            const u128 x = u128(s.a)*radix;
            word = static_cast<u64>(x/n);
            remainder = static_cast<u64>(x%n);
        }
        // Sufficient conditions for EVERY intermediate branch to be regular.
        // Otherwise fall back, including all possible exceptional/halting cases.
        if (remainder < 3*radix || n-remainder < 4*radix) return false;
        const i128 a = i128(remainder) + corrections[(s.a&1)+2*(n&1)][word];
        const u64 sum = n + 3*k + __builtin_popcountll(word);
        if (a < 1 || a >= sum) throw std::runtime_error("invalid jump result");
        s = {static_cast<u64>(a), sum-static_cast<u64>(a)};
        return true;
    }
};

struct Checkpoint {
    State state{2,9};
    u64 iterations=0, jumps=0, jumped_iterations=0, scalar_iterations=0;
    double elapsed=0;
};

void validate(const Checkpoint& c) {
    if (c.state.a < 1 || c.state.b < 2 || c.state.a > SAFE_SUM ||
        c.state.b > SAFE_SUM-c.state.a || c.state.a+c.state.b < 11)
        throw std::runtime_error("checkpoint state outside supported domain");
    if (c.jumped_iterations > c.iterations ||
        c.scalar_iterations != c.iterations-c.jumped_iterations ||
        c.jumps > c.jumped_iterations || !std::isfinite(c.elapsed) || c.elapsed < 0)
        throw std::runtime_error("invalid checkpoint counters");
}

Checkpoint read_checkpoint(const std::string& path) {
    std::ifstream in(path);
    std::string schema, machine;
    Checkpoint c;
    if (!std::getline(in,schema) || !std::getline(in,machine) ||
        schema != "cubic26-v1" || machine != MACHINE)
        throw std::runtime_error("checkpoint identity mismatch");
    // Read integers as tokens: stream extraction into unsigned accepts '-1'.
    std::array<u64*,6> fields{&c.state.a,&c.state.b,&c.iterations,&c.jumps,
                              &c.jumped_iterations,&c.scalar_iterations};
    for (u64* field: fields) {
        std::string token;
        if (!(in >> token) || token.empty()) throw std::runtime_error("truncated checkpoint");
        auto result=std::from_chars(token.data(),token.data()+token.size(),*field);
        if (result.ec != std::errc() || result.ptr != token.data()+token.size())
            throw std::runtime_error("invalid checkpoint integer");
    }
    std::string extra;
    if (!(in >> c.elapsed) || (in >> extra)) throw std::runtime_error("invalid checkpoint tail");
    validate(c);
    return c;
}

void save_checkpoint(const std::string& path, const Checkpoint& c) {
    if (path.empty()) return;
    const std::string temporary=path+".tmp";
    {
        std::ofstream out(temporary,std::ios::trunc);
        out << "cubic26-v1\n" << MACHINE << '\n'
            << c.state.a << ' ' << c.state.b << ' ' << c.iterations << ' '
            << c.jumps << ' ' << c.jumped_iterations << ' ' << c.scalar_iterations << ' '
            << std::setprecision(17) << c.elapsed << '\n';
        out.close();
        if (!out) throw std::runtime_error("failed to write checkpoint");
    }
    if (std::rename(temporary.c_str(),path.c_str()))
        throw std::runtime_error("failed to replace checkpoint");
}

void compare_jump(const Table& table, State s, u64& tested) {
    State original=s;
    if (!table.jump(s)) return;
    for (unsigned i=0;i<table.k;++i)
        if (scalar(original)<0) throw std::runtime_error("jump skipped terminal case");
    if (!(s==original)) throw std::runtime_error("jump disagrees with scalar execution");
    ++tested;
}

void selftest(unsigned bits) {
    Table table(bits);
    std::mt19937_64 random(260026);
    u64 tested=0;
    for (unsigned i=0;i<1000000;++i) {
        const u64 n=11+random()%(SAFE_SUM-10);
        State s{1+random()%(n-2),0};s.b=n-s.a;
        compare_jump(table,s,tested);
    }
    // Small domains, including rejection near all exceptional branches.
    for (unsigned k=1;k<=8;++k) {
        Table small(k);
        for (u64 n=11;n<2000;++n)
            for (u64 a=1;a<n-1;++a) compare_jump(small,{a,n-a},tested);
    }
    // The complete orbit agrees, not just randomly selected local jumps.
    State fast{2,9}, reference=fast;
    u64 done=0;
    while (done<1000000) {
        if (1000000-done>=bits && table.jump(fast)) done+=bits;
        else { if (scalar(fast)<0) throw std::runtime_error("unexpected terminal"); ++done; }
    }
    for (u64 i=0;i<done;++i) if (scalar(reference)<0) throw std::runtime_error("unexpected terminal");
    if (!(fast==reference)) throw std::runtime_error("orbit mismatch");
    State halted{8,3}, gap{0,0};
    if (table.jump(halted) || scalar(halted)!=-1 || scalar(gap)!=-2)
        throw std::runtime_error("terminal control failed");
    std::cout << "{\"selftest\":\"passed\",\"accepted_jumps_checked\":" << tested
              << ",\"blank_iterations_compared\":1000000}\n";
}

u64 integer(const std::string& value) {
    u64 result;
    auto parsed=std::from_chars(value.data(),value.data()+value.size(),result);
    if (parsed.ec!=std::errc() || parsed.ptr!=value.data()+value.size())
        throw std::runtime_error("invalid unsigned integer: "+value);
    return result;
}

int main(int argc,char** argv) try {
    unsigned bits=14;
    u64 budget=1000000000;
    double seconds=30;
    bool test=false, scalar_only=false;
    std::string resume, checkpoint;
    for (int i=1;i<argc;++i) {
        const std::string option=argv[i];
        if (option=="--selftest") {test=true;continue;}
        if (option=="--scalar") {scalar_only=true;continue;}
        if (option=="--help") {
            std::cout << "--bits 1..24 --iterations ADDITIONAL --seconds SECONDS "
                         "--resume PATH --checkpoint PATH --scalar --selftest\n";
            return 0;
        }
        if (++i==argc) throw std::runtime_error("missing option value");
        const std::string value=argv[i];
        if (option=="--bits") {
            const u64 n=integer(value);
            if (n<1 || n>24) throw std::runtime_error("bits outside 1..24");
            bits=static_cast<unsigned>(n);
        } else if (option=="--iterations") budget=integer(value);
        else if (option=="--seconds") {
            size_t end;seconds=std::stod(value,&end);
            if (end!=value.size()) throw std::runtime_error("invalid seconds");
        } else if (option=="--resume") resume=value;
        else if (option=="--checkpoint") checkpoint=value;
        else throw std::runtime_error("unknown option: "+option);
    }
    if (!std::isfinite(seconds) || seconds<=0) throw std::runtime_error("seconds must be finite and positive");
    if (test) {selftest(bits);return 0;}
    Checkpoint c=resume.empty()?Checkpoint{}:read_checkpoint(resume);
    const u64 base=c.iterations;
    const double elapsed_base=c.elapsed;
    if (budget>UINT64_MAX-base) throw std::runtime_error("iteration counter overflow");
    const u64 target=base+budget;
    std::unique_ptr<Table> table;
    if (!scalar_only) table=std::make_unique<Table>(bits);
    const auto start=Clock::now();
    double last_save=0;
    std::string status="iteration_limit";
    u64 terminal_checks=0;
    while (c.iterations<target) {
        if (((c.jumps+c.scalar_iterations)&65535)==0) {
            const double elapsed=std::chrono::duration<double>(Clock::now()-start).count();
            c.elapsed=elapsed_base+elapsed;
            if (elapsed-last_save>=30) {save_checkpoint(checkpoint,c);last_save=elapsed;}
            if (elapsed>=seconds) {status="time_limit";break;}
        }
        // Leave enough room for either a whole jump or any exceptional rule.
        // Stop at a still-valid, resumable state, before crossing the limit.
        const u64 growth = table ? std::max(u64(7),u64(4)*bits) : 7;
        if (c.state.a+c.state.b>SAFE_SUM-growth) {status="integer_limit";break;}
        if (table && target-c.iterations>=bits && table->jump(c.state)) {
            c.iterations+=bits;++c.jumps;c.jumped_iterations+=bits;
        } else {
            ++terminal_checks;
            const int result=scalar(c.state);
            if (result<0) {status=result==-1?"halt_candidate":"uncovered_configuration";break;}
            ++c.iterations;++c.scalar_iterations;
        }
    }
    // A halt reached exactly at a budget boundary should still be reported.
    if (c.state.b==3 && c.state.a>=2) status="halt_candidate";
    const double elapsed=std::chrono::duration<double>(Clock::now()-start).count();
    c.elapsed=elapsed_base+elapsed;
    save_checkpoint(checkpoint,c);
    std::cout << std::setprecision(17)
              << "{\"machine\":\"" << MACHINE << "\",\"status\":\"" << status
              << "\",\"verified\":false,\"backend\":\"" << (scalar_only?"scalar":"guarded_table")
              << "\",\"bits\":" << bits << ",\"iterations\":" << c.iterations
              << ",\"new_iterations\":" << c.iterations-base
              << ",\"a\":" << c.state.a << ",\"b\":" << c.state.b
              << ",\"jumps\":" << c.jumps << ",\"jumped_iterations\":" << c.jumped_iterations
              << ",\"scalar_iterations\":" << c.scalar_iterations
              << ",\"seconds\":" << elapsed << ",\"total_seconds\":" << c.elapsed
              << ",\"terminal_checks_this_run\":" << terminal_checks << "}\n";
    return 0;
} catch (const std::exception& e) {
    std::cerr << "error: " << e.what() << '\n';return 1;
}
