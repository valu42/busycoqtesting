"""Check the elementary-depth annular skip against literal first returns."""
from fractions import Fraction
from annular_skip_758 import partition, run
from check_bb33 import first_return


def elementary_cut(x):
    depth, power = 0, 1
    while power < x:
        depth, power = depth+1, 3*power
    return depth


def verify():
    # alpha is the positive root of t^2-t-4. These rational bounds prove
    # 3^delta < 2.4 < alpha < 3^0.857, using delta < 3/4.
    assert Fraction(12,5)**2-Fraction(12,5)-4 < 0
    assert 3**3 < Fraction(12,5)**4
    # Upper bounds for the fourth roots (1/3)^(3/4) and (4/9)^(3/4).
    a,b = Fraction(44,100),Fraction(55,100)
    assert 27*a**4 >= 1 and 729*b**4 >= 64 and a+b < 1
    c = Fraction(25616,10000)
    assert c*c-c-4 > 0 and c**1000 < 3**857

    for x in (100,497,3**7,3**9,3**11):
        depth = elementary_cut(x)
        cells = list(partition(x,depth,(1,2)))
        for start in (x,x+1,x+19):
            exit_seed, returns, queries = run(cells,start)
            seed, count = start,0
            while seed is not None and seed <= 3*x:
                seed = first_return(seed)
                count += 1
            assert (seed,count) == (exit_seed,returns)
        print(f'[{x:,}, {3*x:,}] matches literal iteration at all three starts '
              f'using {len(cells):,} elementary-depth cells.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with integer assertions enabled.')
    verify()
