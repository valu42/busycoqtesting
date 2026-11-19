"""Check exact #758 returns against the unbatched Python counter map."""
from argparse import ArgumentParser
from pathlib import Path
from random import Random
from subprocess import PIPE, run
from tempfile import TemporaryDirectory

from check_bb33 import first_return


def test_inputs():
    rng = Random(758)
    cases = [(3, 8192, seed) for seed in range(3, 8193)]
    def window(center, width):
        lo = max(3, center-width)
        hi = min(10**17, center+width)
        if lo > hi:
            return
        points = {lo, hi, (lo+hi)//2}
        for p in range(80):
            points.add(rng.randint(lo,hi))
        for s in range(max(lo, center-4), min(hi, center+4)+1):
            points.add(s)
        cases.extend((lo,hi,s) for s in sorted(points))
    for center in (1_326_438_094_216_110,2_031_355_966_425_479,3_335_436_339_933_243,10**17):
        for width in (0,1,29,1000,1_000_000_000):
            window(center,width)
    for _ in range(700):
        center=rng.randrange(3,10**17)
        width=rng.choice((1,37,1023,524288,1<<30,1<<33))
        b=rng.choice((0,19,31))
        center=(center>>b)<<b
        window(center,width)
    for i in range(1,37):
        for u, adjust in ((4,3),(6,0)):
            center=u*(3**i-1)//2-adjust
            for width in (10, 2000):
                window(center,width)
    # A deliberately non-monotone visit order across both coarse bit boundaries.
    for _ in range(10):
        keys = [rng.randrange(1,10**17) for j in range(5)]
        cases.extend((3,10**17,s) for s in keys+list(reversed(keys)))
    return cases


def check(driver):
    cases = test_inputs()
    data = "".join(f"{lo} {hi} {seed}\n" for lo,hi,seed in cases)
    output = run([driver], input=data, stdout=PIPE, text=True, check=True)
    actual = list(map(int, output.stdout.splitlines()))
    assert len(actual) == len(cases)
    for (_, _, seed), value in zip(cases, actual):
        expected = first_return(seed, batch=False)
        assert value == (-1 if expected is None else expected), (seed, value, expected)
    assert (len(cases), actual.count(-1)) == (65294, 50)
    print("65,294 seed/range cases match the unbatched map, including 50 halting cases.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so verification checks execute.")
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--driver", type=Path, help="use an already compiled audit driver")
    args = parser.parse_args()
    if args.driver is not None:
        check(args.driver.resolve())
    else:
        with TemporaryDirectory() as tmp:
            driver = Path(tmp)/"audit_returns"
            source = Path(__file__).with_suffix(".cpp")
            run(["c++", "-O2", "-std=c++17", source, "-o", driver], check=True)
            check(driver)
