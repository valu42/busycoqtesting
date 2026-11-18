// Ordinary line-33 requests with bulk stable-pair transfers. Compile with GMP.
#include <algorithm>
#include <cstdint>
#include <deque>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <gmpxx.h>

namespace {
const std::string phase_words[3] = {"21", "14", "24"};

int phase(char a, char b) {
    if (a == '2' && b == '1') return 0;
    if (a == '1' && b == '4') return 1;
    if (a == '2' && b == '4') return 2;
    return -1;
}

struct Token {
    char digit = 0;
    mpz_class requests = 0;
    explicit Token(char d) : digit(d) {}
    explicit Token(mpz_class count) : requests(std::move(count)) {}
};

class Transfer {
    const std::string &source;
    size_t pos = 0;
    std::deque<Token> queue;
    std::string output;

    void schedule(mpz_class n) {
        if (!n) return;
        if (!queue.empty() && !queue.front().digit) queue.front().requests += n;
        else queue.emplace_front(std::move(n));
    }

    // Compute F^n on a virgin suffix by converting n to balanced ternary.
    void virgin(const mpz_class &n) {
        const auto ternary = n.get_str(3);
        unsigned carry = 0;
        size_t digits = 0, minus = 0;
        for (auto it = ternary.rbegin(); it != ternary.rend(); ++it) {
            unsigned value = unsigned(*it - '0') + carry;
            carry = (value + 1) / 3;
            unsigned remainder = value % 3;
            output += phase_words[(remainder + 2) % 3];
            minus += remainder == 2;
            ++digits;
        }
        if (carry) { output += "21"; ++digits; }
        cost += 5*n + 4*mpz_class(minus) - 2*mpz_class(digits);
    }

    // One available digit. A pending F on the unprocessed suffix is a token.
    char digit() {
        while (!queue.empty()) {
            auto t = std::move(queue.front());
            queue.pop_front();
            if (t.digit) return t.digit;
            auto &n = t.requests;
            char a = digit();
            if (a == 0) {
                cost += 3;
                queue.emplace_front('1'); queue.emplace_front('2'); schedule(n-1);
            } else if (a == '1' || a == '4') {
                cost += (a == '1' ? 1 : 2);
                if (a == '4') schedule(1);
                queue.emplace_front('2'); schedule(n-1);
            } else {
                char b = digit();
                if (b == 0) throw std::runtime_error("exceptional solitary 2");
                if (b == '2') {
                    cost += 7*n; schedule(2*n);
                    queue.emplace_front('2'); queue.emplace_front('2');
                } else {
                    int p = phase('2',b);
                    mpz_class m = (n + (p+2)%3)/3;
                    int q = (p + mpz_fdiv_ui(n.get_mpz_t(),3)) % 3;
                    cost += 5*(n-m) + 4*((q==1)-(p==1));
                    schedule(std::move(m));
                    queue.emplace_front(phase_words[q][1]); queue.emplace_front(phase_words[q][0]);
                }
            }
        }
        return pos == source.size() ? 0 : source[pos++];
    }

    void transfer_stable(mpz_class n) {
        if (source.compare(pos,2,"22") == 0) {
            size_t k = 0;
            while (source.compare(pos,2,"22") == 0) { pos += 2; ++k; }
            output.append(2*k,'2');
            mpz_class m = n << k;
            cost += 7*(m-n);
            schedule(std::move(m));
            return;
        }
        // 3^39 and every affine offset fit in one 64-bit unsigned long.
        static_assert(sizeof(unsigned long) >= 8);
        unsigned long power = 1, offset = 0;
        unsigned k = 0, before = 0;
        while (k < 39 && pos+1 < source.size()) {
            int p = phase(source[pos], source[pos+1]);
            if (p < 0) break;
            before += p == 1;
            offset += power * ((p+2)%3);
            power *= 3; ++k; pos += 2;
        }
        mpz_class m = n + offset;
        auto residues = mpz_fdiv_q_ui(m.get_mpz_t(),m.get_mpz_t(),power);
        unsigned after = 0;
        while (k-- > 0) {
            int q = (residues%3+1)%3;
            output += phase_words[q];
            after += q == 1;
            residues /= 3;
        }
        cost += 5*(n-m) + 4*(int(after)-int(before));
        schedule(std::move(m));
    }

public:
    mpz_class cost = 0;
    explicit Transfer(const std::string &word) : source(word) {}
    std::string run(mpz_class n) {
        schedule(std::move(n));
        while (true) {
            if (queue.empty()) { output.append(source,pos,std::string::npos); return output; }
            if (queue.size() == 1 && !queue.front().digit) {
                if (pos == source.size()) { virgin(queue.front().requests); return output; }
                if (pos+1 < source.size() && (source.compare(pos,2,"22")==0 ||
                                               phase(source[pos],source[pos+1]) >= 0)) {
                    auto count = std::move(queue.front().requests); queue.pop_front();
                    transfer_stable(std::move(count)); continue;
                }
            }
            char next = digit();
            if (!next) return output;
            output += next;
        }
    }
};
}

int main() {
    std::string line;
    while (std::getline(std::cin,line)) {
        auto sep = line.find(' ');
        if (sep == std::string::npos) return 2;
        auto word = line.substr(sep+1);
        if (word.find_first_not_of("124") != std::string::npos) return 2;
        mpz_class n(line.substr(0,sep));
        if (n < 0) return 2;
        try {
            Transfer runner(word);
            auto result = runner.run(n);
            std::cout << runner.cost.get_str(16) << ' ' << result << '\n';
        } catch (const std::runtime_error &e) {
            std::cout << e.what() << '\n';
        }
        std::cout.flush();
    }
}
