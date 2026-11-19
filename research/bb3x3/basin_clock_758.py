"""Bound the remaining raw clock after entry into a certified halting basin."""
import argparse
from decimal import Decimal

from angular_clock_758 import upper_prefix
from check_bb33 import HALTING_TARGET as H, WALL_NEAR, champion_step
from lower_clock_758 import certify_potential, lower_at_mass, make_graph
from lower_scale_gates_758 import GATES
from scale_clauses_758 import EVEN_WORD, PREFIX


def terminal_input(seed):
    state = (1, seed)
    for call in range(1, 308):
        successor = champion_step(*state)
        if successor is None:
            assert call == 307
            return state
        state = successor
    raise AssertionError("The candidate passed the expected halt")


def audit():
    # gateway_758.cpp admits k+1 < 310, then performs up to 10,000 calls.
    max_segment = max(len(EVEN_WORD), len(PREFIX) + 308 + 10_000)
    assert max_segment == 10_615
    assert 2*(H - WALL_NEAR) + 1 + 9*max_segment < 2*H

    a, c = terminal_input(H)
    assert (a, c) == terminal_input(H - 2)
    terminal_mass = a + 2*c
    assert terminal_mass == 2*H + 1258

    def remaining(distance):
        entry_mass = 2*(H-distance) + 1
        calls = (terminal_mass - entry_mass)//4 + 1  # includes the halt
        max_cost = (terminal_mass**2 + 30*terminal_mass + 195)//3
        return calls*max_cost

    outer_limit = remaining(GATES[10][1])
    connected_limit = remaining(GATES[7][1])
    assert outer_limit < 278*10**291
    assert connected_limit < 104*10**290
    # For the total blank clock, add the cost of the final transition block
    # to the prefix bound evaluated at the latest possible terminal input.
    total_limit = (upper_prefix(terminal_mass)
                   + (terminal_mass**2 + 30*terminal_mass + 195)//3)
    assert total_limit < 8206*10**413
    # Even an orbit that misses the target must halt or exceed its terminal
    # mass by this horizon. A first crossing can overshoot by at most nine.
    crossing_limit = upper_prefix(terminal_mass + 9)
    assert crossing_limit < 8206*10**413
    max_calls = (terminal_mass - 2)//4 + 1
    assert max_calls < 10724*10**135
    first_mass = 2*(H - GATES[10][1]) + 1
    lower_limit = lower_at_mass(first_mass, certify_potential(make_graph())) - 50_707
    assert lower_limit > 210448*10**409
    assert outer_limit*10**121 < 2*lower_limit
    return outer_limit, connected_limit, lower_limit, total_limit


def joined_clock(distance):
    """Bounds after entry anywhere in the joined halting basin."""
    a, c = terminal_input(H)
    last = a+2*c
    assert last == 2*H+1258
    initial = 2*(H-distance)+1
    call_cost = (last**2+30*last+195)//3
    remaining = ((last-initial)//4+1)*call_cost
    lower = lower_at_mass(initial,certify_potential(make_graph()))-50_707
    upper = upper_prefix(last)+call_cost
    assert lower > 210448*10**409 and upper < 8206*10**413
    return remaining,lower,upper


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Enable assertions to run the checks.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--joined', action='store_true', help='use the widest joined interval')
    args = parser.parse_args()
    if args.joined:
        from target_basin_758 import GATES_NEW
        distance = GATES_NEW[max(GATES_NEW)][1]
        remaining, lower, upper = joined_clock(distance)
        print(f"Mass-distance {distance:,}; raw remaining upper bound {remaining}.")
        print(f"Conditional blank bounds {lower} through {upper}.")
        raise SystemExit
    outer, connected, lower, total = audit()
    print(f"Time left from any of the covered basins: <= {Decimal(outer):.12E} (rounded)")
    print(f"Time left from the contiguous basin: <= {Decimal(connected):.12E} (rounded)")
    print(f"Total from blank if entry occurs (rounded bounds): "
          f"{Decimal(lower):.12E} to {Decimal(total):.12E}")
