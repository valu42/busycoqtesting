# Running the BB(2,5) simulations

[The simulation table](../SIMULATION_TABLE.md) tracks the largest counted blank-tape endpoint for each of the 37 encodings. Each file under `runs/` records a complete configuration and its checksum. Simulation can continue from any verified file. Checksums establish file integrity. The experiments use native code and Python.

From `research/bb2x5`, build the moving-window simulator with a C++17 compiler and replay or extend any line with Python 3.10 or later.

```sh
c++ -O3 -std=c++17 frontiers/window.cpp -o /tmp/bb25-window
python3 frontiers/survey.py --engine /tmp/bb25-window --line 14 --width 8 \
  --target 10000000000 --work 10000000000 --checkpoint /tmp/line14.json
python3 frontiers/survey.py --engine /tmp/bb25-window --line 14 \
  --resume frontiers/runs/window-14.json --target 12000000000 \
  --work 1000000000 --checkpoint /tmp/line14-next.json
```

A lookup starts at the join between two adjacent base-five words. The key includes both words, the side of entry and the control state. It composes literal first exits from individual words and stops at an exit, a halt or a local work cap. Even a capped lookup returns its precise intermediate position, symbols and defined-step count. The outer loop takes individual transitions when a jump would pass the target. Fixed-size caches replace old entries and compare complete keys on every hit. The native counter accepts absolute targets through 2^60. Word width may change on resume.

The initial window survey used width 8 and a limit of 10 billion window operations per machine. It targeted 100 billion raw steps on lines 7 and 13, 100 million on lines 3, 5, 17, 26, 29 and 30, and 10 billion elsewhere. Every target was reached. Each snapshot stores the occupied interval as compressed symbols, its left endpoint, and the absolute head, state and step count. Earlier, deeper results take precedence in the table where applicable. To refresh the table after saving checked results run `python3 frontiers/scoreboard.py`.
