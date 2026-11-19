# A conditional upper bound on the #758 halting clock

**If blank reaches either A(1,H−2) or A(1,H), #758 halts in fewer than 8.206 × 10⁴¹⁶ raw steps.** Here H is the known 140-digit halting seed. Each seeded suffix uses 307 calls and about 2.79256 × 10²⁷⁹ raw steps. Most of the upper bound is the cost of reaching the seed. Whether the blank orbit reaches either seed remains open. [Two-counter map](check_bb33.py) · [Raw timings](timing_758.py) · [Exact verifier](angular_clock_758.py)

## A bound at any attained mass

Write W = a + 2c and x = a/W, and let t be one continuing call's raw cost. Every row in the timing table has leading term W²r(x), where r(x) = 3 min(x,(1−x)/2)², and the lower-order terms give t ≤ W²r(x) + 30W + 65. The blank run starts at A(0,1) after two raw steps. Subsequently c ≥ 1, and every even c occurs with a = 1. Each continuing call increases W by an integer g between 4 and 9.

The following table compares the true update with a homogeneous update having outgoing fraction y. Each phase is the parity of a. The bulk rows apply to odd c. Their actual gains are 5 or 9.

| Rule | Input phase | Input x in the homogeneous update | Output phase | y | Minimum g |
|---|---|---|---|---|---:|
| J, grow the left counter | Odd | [0,1/3] | Odd | 3x | 4 |
| Bulk | Odd | [1/3,1] | Even | (3x−1)/2 | 5 |
| Bulk | Even | [1/3,1] | Odd | (3x−1)/2 | 5 |
| Reset | Even | [0,1/3] | Odd | 0 | 5 |
| Exceptional boundary | Odd | {1/3} | Odd | 1 | 8 |

Let P be the piecewise-linear function given by the following knots, with linear interpolation separately within each phase. The x coordinates are numerators with denominator 23, and the heights are numerators with denominator 146004.

| Phase | x numerators | Height numerators |
|---|---|---|
| Odd | 0, 1, 2, 4, 5, 13, 15, 23 | 0, 5913, 11101, 20833, 25285, 24985, 22801, −37490 |
| Even | 0, 8, 10, 11, 23 | −713, 27055, 30751, 32323, −14720 |

For every row, writing i and j for the input and output phases,

$$r(x)+P_j(y)-P_i(x)\le \lambda g,\qquad \lambda=33/1058.$$

To check this with rational arithmetic, split each row's domain at its own knots and the preimages of the output knots. On each resulting interval the left side is a convex quadratic, so checking its two endpoints suffices. The same knot table shows that both functions have Lipschitz constant at most 2 and values between −1/2 and 1/2. In this relaxation the rate is sharp. The cycle of three fractions 5/23 → 15/23 → 11/23 → 5/23 uses gains 4, 5, 5 and has total reward (4+5+5)λ. Whether an integer orbit can sustain that rate is a separate question.

## Finite-coordinate corrections

Write x′ = a′/(W+g) for the true output. For J, |x′−3x| = |2−12x|/(W+4) ≤ 2/W. In a bulk call, a′ = Wy−δ with δ equal to 2 or 4, so |x′−y| ≤ 13/W. At reset x′ = 1/(W+5). At the exceptional boundary a=c+2, the actual input x is 1/3+4/(3W), the output is 1−2/(W+8), and r(x) ≤ r(1/3). The two Lipschitz corrections together cost at most 2(4/3+2)/W. Finally an even-c input has a=1, a′=3, g=8, and remains in the odd phase. It satisfies W²r(x) = 3 and |x′−x| ≤ 2/W. These cases give, for every continuing update,

$$t \le \lambda gW^2+W^2\big(P_i(x)-P_j(x')\big)+56W+65.$$

Stop at an attained live configuration of mass V. Summing gW² over the increasing mass intervals gives at most (V³−8)/3. Since g≥4, the corresponding sum of W is at most (V²−4)/8, and the number of calls is at most (V−2)/4. Translate all P values into [0,1] by adding 1/2. Summation by parts bounds the total potential difference weighted by W² by V², since each interior value has coefficient equal to the increase over the preceding squared mass and the final value has nonpositive coefficient. Including the first two raw steps and rounding down the cubic term gives

$$T_{\mathrm{prefix}}(V)\le 2+\left\lfloor\frac{11V^3}{1058}\right\rfloor+8V^2+17V.$$

For a seed s ∈ {H−2,H}, take V=2s+1 and add all 307 exact suffix costs, including the halt. Both upper bounds round to 8.205102528405 × 10⁴¹⁶, giving the strict bound in the opening paragraph. The established join transfers the result to #153, which uses 50,707 fewer raw steps. Run `python3 angular_clock_758.py` next to the two-counter map and timing table to reproduce the certificate and both integer comparisons.
