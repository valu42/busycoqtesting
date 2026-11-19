"""Verify a global denominator cutoff for ordinary periodic excursions of #758."""
from itertools import pairwise


def word_counts(max_n):
    words = [1, 1]
    for _ in range(2, max_n+1):
        words.append(words[-1]+4*words[-2])
    return [0, 2]+[2*words[n-1]+28*words[n-2] for n in range(2,max_n+1)]


def multiplicity(q, n):
    modulus = 3**n
    return (q//(2*modulus)+1)*(3*q//modulus+1)


def verify(cut, first_n, last_n, merge_first_pair):
    """Bound each x in [cut,3*cut), then lift by arbitrary factors of three."""
    weights = word_counts(last_n+3)
    # The same inequality at all later n follows by the positive recurrence.
    assert all(weights[n] == weights[n-1]+4*weights[n-2]
               for n in range(4, len(weights)))
    for n in (6,7):
        assert weights[n+1] <= 3*weights[n]

    def bound(x,n):
        a,b = weights[n],4*weights[n-1]
        if merge_first_pair:
            a,b = a//2+3,b//2
        return a*multiplicity(x,n)+b*multiplicity(x,n+1)

    changes = {cut,3*cut}
    for n in range(first_n,last_n+2):
        for spacing in (2*3**n,3**(n-1)):
            for i in range(cut//spacing,3*cut//spacing+1):
                x = i*spacing
                if cut <= x <= 3*cut:
                    changes.add(x)
    cells = sorted(changes)
    least_slack = None
    for x,y in pairwise(cells):
        value = min(bound(x,n) for n in range(first_n,last_n+1))
        assert value < x, (x,y,value)
        # Both multiplicity factors are constant on [x,y).
        slack = x-value
        least_slack = slack if least_slack is None else min(least_slack,slack)
    print(f"q <= {cut-1:,}: {len(cells)-1} cells, minimum slack {least_slack}")


if __name__ == "__main__":
    verify(1_290_157_065,19,20,False)
    verify(14_984_529,15,16,True)
