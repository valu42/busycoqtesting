# BB(6) machine approach rankings

**520 fresh starts** · 3 open lines with existing campaigns · 85 verification targets. All 608 permanent lines are included.

The fresh queue orders campaigns by how precisely the next proof step is known and how many machines could use the work. The verification queue orders existing results by the evidence available to check.

[Existing campaigns](#existing-campaigns) · [Verification queue](#verification-queue) · [Ranking method and reproduction](#ranking-method-and-reproduction) · [Claim board](ROADMAP.md#claim-board)

| Fresh ranks | Approach | First line |
|---:|---|---:|
| 1 | [Adapt a decision argument](#adapt-a-decision-argument) | 448 |
| 2 | [Decide a representative](#decide-a-representative) | 117 |
| 3–12 | [Resume a checkpoint](#resume-a-checkpoint) | 396 |
| 13–73 | [Analyze a return map](#analyze-a-return-map) | 464 |
| 74–100 | [Use a structural reduction](#use-a-structural-reduction) | 185 |
| 101–117 | [Transfer a related model](#transfer-a-related-model) | 422 |
| 118–152 | [Test a repeating tape edge](#test-a-repeating-tape-edge) | 593 |
| 153–387 | [Compare blank starts](#compare-blank-starts) | 545 |
| 388–520 | [Collect the next edge records](#collect-the-next-edge-records) | 3 |

## Adapt a decision argument

A theorem or proposed proof supplies either a complete table match or a single changed instruction with the same blank entry. Check the entry or the altered branch before reusing the argument.

| Rank | Line | Machine ID | First check | Edge records · last signature and step | Other open starts |
|---:|---:|---:|---|---|---|
| 1 | [448](BB6_holdouts_608.txt#L448) | 127983 | Compare line 598 ([HALT_PR source](https://github.com/ccz181078/busycoq/pull/93)), `A → A`. At `F0` (first read at step 303), the candidate uses `0LC` and the aligned peer uses `0RD`. | 382 · `L/D/1101` at 65,307 | 247 (D mirrored), 539 (B) |

## Decide a representative

Follow the representative's blank orbit. A decision can also settle its linked lines once the equivalence is verified.

| Rank | Line | Machine ID | First check | Edge records · last signature and step | Other open starts |
|---:|---:|---:|---|---|---|
| 2 | [117](BB6_holdouts_608.txt#L117) | 30773 | Linked to [405 (EQUIVALENCE_PR)](https://github.com/ccz181078/busycoq/pull/77). [TailWord.f from cfg0](https://github.com/ccz181078/busycoq/blob/7e615fbe1d20a2424bbcdbca84dbafbb17929841/verify/Eqv_TailWord.v#L357) | 229 · `R/B/1010` at 63,339 | — |

## Resume a checkpoint

The cited work identifies the machine and a resumable calculation. Seek an invariant or a reachable halting case in the recorded model.

| Rank | Line | Machine ID | First check | Edge records · last signature and step | Other open starts |
|---:|---:|---:|---|---|---|
| 3 | [396](BB6_holdouts_608.txt#L396) | 112145 | [packet catalogue and 500,000-round checkpoint](https://github.com/valu42/busycoqtesting/blob/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623/PACKET_STREAM.md) · [compare the token invariant proposed for line 471](https://github.com/ccz181078/busycoq/pull/55) | 92 · `L/A/0101` at 51,456 | — |
| 4 | [26](BB6_holdouts_608.txt#L26) | 8084 | [Cubic Mess, test b = 3](https://github.com/valu42/busycoqtesting/blob/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623/CUBIC26.md) · [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LC_1LC1RD_1LA0LB_0RB1RE_1RF0RA_HHH0RC.lean#L729) | 149 · `L/A/1101` at 63,287 | — |
| 5 | [35](BB6_holdouts_608.txt#L35) | 9516 | [WF17 from (3, 0, 0)](https://github.com/valu42/busycoqtesting/blob/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623/CUBIC_FAMILY.md) · [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LE_1LC1RA_1RA1LD_0LC0LA_0RE1RF_0RCHHH.lean#L785) | 145 · `R/B/1101` at 65,360 | — |
| 6 | [135](BB6_holdouts_608.txt#L135) | 35167 | [WF35 from (0, 1, 1)](https://github.com/valu42/busycoqtesting/blob/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623/CUBIC_FAMILY.md) · [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RD_0LC1RA_1LA1LC_1RA1LE_1RF0LD_HHH0RE.lean#L796) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L99) | 159 · `R/B/1111` at 65,246 | — |
| 7 | [264](BB6_holdouts_608.txt#L264) | 70028 | [WF32 from (0, 1, 0)](https://github.com/valu42/busycoqtesting/blob/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623/CUBIC_FAMILY.md) · [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RD_0LC1RA_1RA1LC_0RB1LE_1RF0LD_HHH0RE.lean#L1359) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L120) | 155 · `R/B/1111` at 64,207 | — |
| 8 | [400](BB6_holdouts_608.txt#L400) | 113619 | [WF36 from (0, 0, 1)](https://github.com/valu42/busycoqtesting/blob/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623/CUBIC_FAMILY.md) · [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RD_0LC1RA_0RA1LC_1RA1LE_1RF0LD_HHH0RE.lean#L1278) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L151) | 163 · `R/B/1111` at 64,766 | — |
| 9 | [483](BB6_holdouts_608.txt#L483) | 137865 | [WF33 from (2, 2, 1)](https://github.com/valu42/busycoqtesting/blob/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623/CUBIC_FAMILY.md) · [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LE_1RC1RA_0LD1RB_1LE1LD_1RF0LA_HHH0RE.lean#L2089) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L444) | 157 · `L/E/1010` at 64,871 | — |
| 10 | [522](BB6_holdouts_608.txt#L522) | 150065 | [SOC25 from (2, 4)](https://github.com/valu42/busycoqtesting/blob/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623/SOC25_DEQUE.md) | 110 · `R/B/1111` at 44,407 | — |
| 11 | [558](BB6_holdouts_608.txt#L558) | 163183 | [SOC25 from (1, 3)](https://github.com/valu42/busycoqtesting/blob/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623/SOC25_DEQUE.md) | 94 · `R/B/1111` at 61,427 | — |
| 12 | [559](BB6_holdouts_608.txt#L559) | 163594 | [SOC25 from (1, 2)](https://github.com/valu42/busycoqtesting/blob/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623/SOC25_DEQUE.md) | 90 · `L/A/1111` at 41,532 | — |

## Analyze a return map

Start at the specified seed. Prove that its iterates reach a halting branch or stay in a closed set of continuing states.

| Rank | Line | Machine ID | First check | Edge records · last signature and step | Other open starts |
|---:|---:|---:|---|---|---|
| 13 | [464](BB6_holdouts_608.txt#L464) | 132148 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RF_1LCHHH_1LE1RD_1RA0RC_0LF0LA_0LD0RB.lean#L1002) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L381) | 270 · `L/D/0011` at 65,339 | 103 (F mirrored) |
| 14 | [51](BB6_holdouts_608.txt#L51) | 13743 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LC_0LC1RF_1LE1RD_0RC1RC_0LA1LA_HHH1RA.lean#L1489) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L244) | 261 · `R/C/0111` at 64,865 | — |
| 15 | [57](BB6_holdouts_608.txt#L57) | 15414 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RBHHH_0RC0LD_1LB1RC_0LE0LF_1RD1LE_1RF1RA.lean#L465) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L688) | 135 · `R/C/1011` at 63,295 | — |
| 16 | [81](BB6_holdouts_608.txt#L81) | 21883 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LF_1RC1RF_0LD1RE_HHH1LC_0RB1RE_1LA0LE.lean#L1749) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L319) | 117 · `R/C/1010` at 65,458 | — |
| 17 | [92](BB6_holdouts_608.txt#L92) | 25221 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RB_1RC0LE_1LD1LA_HHH0LC_1RF1LE_1RA0RA.lean#L667) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L586) | 168 · `R/C/1011` at 60,102 | — |
| 18 | [101](BB6_holdouts_608.txt#L101) | 25899 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RF_1LC1LF_HHH1LD_1LE0RA_1RE1LB_1RD0LD.lean#L706) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L711) | 362 · `L/F/1101` at 64,772 | — |
| 19 | [112](BB6_holdouts_608.txt#L112) | 28830 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LD_1RC0RA_1LA1RE_0LA0LB_0RB1RF_HHH1RD.lean#L1588) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L343) | 207 · `R/C/1101` at 64,442 | — |
| 20 | [136](BB6_holdouts_608.txt#L136) | 35366 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LF_0RC1RD_1LA1LD_1LE0RA_HHH1LC_0LA1LA.lean#L1424) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L190) | 281 · `L/A/1101` at 65,394 | — |
| 21 | [245](BB6_holdouts_608.txt#L245) | 66813 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LC_1RC0RF_1RD0LB_1RE0LD_1LFHHH_0RA1LA.lean#L3068) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L80) | 433 · `L/A/1100` at 65,217 | — |
| 22 | [296](BB6_holdouts_608.txt#L296) | 78424 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1LA_1LA0RC_1RD1RC_1LE0RC_HHH0LF_1LE0LA.lean#L566) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L568) | 187 · `R/D/1010` at 59,629 | — |
| 23 | [350](BB6_holdouts_608.txt#L350) | 97525 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0RC_1LC1RE_1RA1LD_0LC0LA_1RF1RD_HHH0RD.lean#L1560) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L359) | 163 · `L/C/0111` at 63,693 | — |
| 24 | [470](BB6_holdouts_608.txt#L470) | 133227 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LE_0RC1RC_0RD1LA_1LD0LA_1LF1LC_HHH0LA.lean#L1741) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L402) | 242 · `L/C/1010` at 65,421 | — |
| 25 | [496](BB6_holdouts_608.txt#L496) | 141594 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LD_1LC1RD_0LE1LA_0RB1RD_HHH0LF_1RA1LF.lean#L409) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L631) | 350 · `R/B/0111` at 58,747 | — |
| 26 | [514](BB6_holdouts_608.txt#L514) | 147851 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RA_1RC1LB_1LD0RA_HHH0LE_1LC0LF_1RE0LB.lean#L569) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L672) | 356 · `R/C/1110` at 63,875 | — |
| 27 | [520](BB6_holdouts_608.txt#L520) | 149707 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RF_1LC1LF_0RE1LD_0LB1LD_HHH1RC_1RA0RD.lean#L2089) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L465) | 113 · `L/C/1010` at 61,813 | — |
| 28 | [524](BB6_holdouts_608.txt#L524) | 151747 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RC_1LC1LC_1RE0LD_1LB1RF_HHH1RA_0RD1RD.lean#L1175) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L494) | 271 · `R/D/1101` at 64,620 | — |
| 29 | [548](BB6_holdouts_608.txt#L548) | 159080 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RB_1LC0RE_HHH1LD_0RA1LB_1RA1LF_0LE1LE.lean#L964) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L221) | 291 · `R/B/1101` at 65,313 | — |
| 30 | [565](BB6_holdouts_608.txt#L565) | 165234 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LF_1LC1RA_0RE0RD_HHH1LE_1LF1RC_1LC1LA.lean#L746) · [halting residue class](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/HardnessEvidence.lean#L520) | 329 · `R/B/1111` at 65,129 | — |
| 31 | [64](BB6_holdouts_608.txt#L64) | 18046 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RE_0RC1RE_1RD1LE_0LEHHH_1RA1LF_1RF0LC.lean#L789) | 438 · `L/E/1010` at 65,526 | 371 (E), 602 (B) |
| 32 | [186](BB6_holdouts_608.txt#L186) | 50372 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_HHH0RE.lean#L2963) | 338 · `L/E/1010` at 62,131 | 317 (B mirrored), 573 (B) |
| 33 | [317](BB6_holdouts_608.txt#L317) | 87254 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RE_1LC0RA_1RD0LB_1LB1RC_1LF0RD_HHH0LE.lean#L1205) | 340 · `R/E/1010` at 64,689 | 186 (D mirrored), 573 (D mirrored) |
| 34 | [573](BB6_holdouts_608.txt#L573) | 167198 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LC_1RC0LD_1LA0RB_1LB1LE_1RF0LA_HHH0RE.lean#L2963) | 373 · `L/B/1010` at 65,236 | 186 (C), 317 (D mirrored) |
| 35 | [103](BB6_holdouts_608.txt#L103) | 26350 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RBHHH_1RC1LE_0RD0RF_0RE0LA_1LF0LB_1LA1LD.lean#L2057) | 256 · `R/F/0111` at 65,460 | 464 (B mirrored) |
| 36 | [166](BB6_holdouts_608.txt#L166) | 44531 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RE_1LC0RC_1RA1LD_1RB0LA_0LC1RF_HHH1RD.lean#L595) | 352 · `L/D/1110` at 64,846 | 69 (B) |
| 37 | [180](BB6_holdouts_608.txt#L180) | 48788 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LB_1LC0RE_1LA1LD_0LCHHH_0RB0RF_1RE1RB.lean#L2865) | 383 · `R/B/1010` at 65,456 | 497 (C mirrored) |
| 38 | [497](BB6_holdouts_608.txt#L497) | 141950 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RBHHH.lean#L4924) | 416 · `L/A/1010` at 65,300 | 180 (B mirrored) |
| 39 | [36](BB6_holdouts_608.txt#L36) | 9785 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_HHH0RA.lean#L660) | 371 · `R/B/1111` at 65,450 | — |
| 40 | [48](BB6_holdouts_608.txt#L48) | 12891 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LD_0RC1RB_0RD0RA_1LE0RD_1LFHHH_0LA1LA.lean#L1098) | 170 · `R/D/0011` at 63,496 | — |
| 41 | [72](BB6_holdouts_608.txt#L72) | 20053 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_HHH0LE.lean#L1301) | 291 · `L/E/1111` at 65,230 | — |
| 42 | [82](BB6_holdouts_608.txt#L82) | 22247 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RBHHH_1LC0RF_0RA0LD_1LE1LA_1RF0LF_0LC0RA.lean#L1259) | 72 · `L/E/1011` at 40,129 | — |
| 43 | [89](BB6_holdouts_608.txt#L89) | 24009 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_HHH0LC.lean#L1421) | 335 · `L/E/1111` at 65,463 | — |
| 44 | [93](BB6_holdouts_608.txt#L93) | 25239 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LE_1LB1LC_1RD0LE_HHH0RB_1RF1LA_0RA0RD.lean#L1374) | 234 · `L/E/1111` at 45,612 | — |
| 45 | [120](BB6_holdouts_608.txt#L120) | 31371 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_HHH1LE.lean#L627) | 211 · `R/E/1111` at 65,192 | — |
| 46 | [153](BB6_holdouts_608.txt#L153) | 40361 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RF_1LC0RE_1RD0LC_0LB0RA_1LD1RD_1RBHHH.lean#L521) | 473 · `L/C/1011` at 65,143 | — |
| 47 | [179](BB6_holdouts_608.txt#L179) | 48709 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_HHH1LB.lean#L595) | 463 · `L/C/1111` at 65,478 | — |
| 48 | [189](BB6_holdouts_608.txt#L189) | 50923 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RA_0LC0RE_1LF1LD_1LA0LA_1LC1RB_HHH1LC.lean#L784) | 173 · `R/B/1111` at 65,268 | — |
| 49 | [198](BB6_holdouts_608.txt#L198) | 53489 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_HHH1LC.lean#L649) | 173 · `R/C/1111` at 65,455 | — |
| 50 | [211](BB6_holdouts_608.txt#L211) | 57056 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1LF_0RC0RB_0LD1RB_1LE0LB_0LA1LC_0LBHHH.lean#L260) | 127 · `L/A/0101` at 52,685 | — |
| 51 | [258](BB6_holdouts_608.txt#L258) | 69308 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RE_1LC0RA_HHH1LD_1LA0LF_0LB0LC_1RB0LB.lean#L772) | 243 · `L/A/1101` at 65,379 | — |
| 52 | [275](BB6_holdouts_608.txt#L275) | 72026 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LE_0RC0RA_1RD1RB_0LA0RB_1LFHHH_1LD1LF.lean#L310) | 595 · `L/A/0110` at 64,209 | — |
| 53 | [284](BB6_holdouts_608.txt#L284) | 74998 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LC_0LC0RF_1RD1LC_0RA1LE_HHH0LD_1LF1LA.lean#L895) | 295 · `L/D/0111` at 65,449 | — |
| 54 | [314](BB6_holdouts_608.txt#L314) | 86694 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0RB_1LB0LC_1RD1LC_1RE0RA_0RF1RA_HHH1LB.lean#L710) | 154 · `R/B/1111` at 64,880 | — |
| 55 | [320](BB6_holdouts_608.txt#L320) | 89542 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LE_0LC0LB_1RD1LC_1RD1RA_1RF0LA_HHH1RE.lean#L662) | 527 · `L/C/0000` at 65,058 | — |
| 56 | [321](BB6_holdouts_608.txt#L321) | 89641 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1LB_1LC1LA_1RD0LB_1RA1RE_1RF0RD_HHH1RD.lean#L1025) | 548 · `L/C/1110` at 65,243 | — |
| 57 | [325](BB6_holdouts_608.txt#L325) | 91443 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_HHH0RC.lean#L837) | 348 · `L/A/0101` at 64,577 | — |
| 58 | [355](BB6_holdouts_608.txt#L355) | 98995 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RE_1RC1RE_1LD1LC_0RB0LC_1RF0RB_HHH1RA.lean#L554) | 485 · `L/D/1011` at 65,275 | — |
| 59 | [366](BB6_holdouts_608.txt#L366) | 101957 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_HHH0LD.lean#L607) | 117 · `L/A/1111` at 65,060 | — |
| 60 | [383](BB6_holdouts_608.txt#L383) | 107208 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RE_1LC0RA_0RD1LB_HHH1RC_1LF1RE_0LB0LE.lean#L703) | 266 · `R/E/1111` at 65,174 | — |
| 61 | [399](BB6_holdouts_608.txt#L399) | 113170 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LE_1LC0RA_0RF0LD_1LE1LA_1RC0LB_HHH1RC.lean#L1446) | 236 · `L/C/1010` at 58,164 | — |
| 62 | [412](BB6_holdouts_608.txt#L412) | 116538 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RE_1LC1LD_HHH1LA_1LB1LE_0RF0RA_1LD1RF.lean#L906) | 660 · `R/F/0101` at 65,365 | — |
| 63 | [459](BB6_holdouts_608.txt#L459) | 130861 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1LA_1LC0RE_1LF1LD_1RE0LC_1LB1RA_HHH0LA.lean#L1541) | 245 · `L/A/1111` at 65,364 | — |
| 64 | [478](BB6_holdouts_608.txt#L478) | 135376 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RD_1LC0RD_1RF1RB_1LE0RA_0LB0LE_HHH0RC.lean#L1072) | 391 · `R/D/0101` at 64,765 | — |
| 65 | [492](BB6_holdouts_608.txt#L492) | 140043 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1LA_1LC0RE_HHH0LD_1RE0LF_1RA1RE_1LA0LB.lean#L711) | 215 · `R/B/1110` at 58,276 | — |
| 66 | [503](BB6_holdouts_608.txt#L503) | 144815 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0RF_1RC1RF_1LD0LE_HHH1LC_1RA1LE_1LC1RB.lean#L728) | 187 · `L/E/1111` at 60,839 | — |
| 67 | [508](BB6_holdouts_608.txt#L508) | 145825 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LE_1LB1RC_0RF0RD_1RE0LA_1LA1RE_HHH0RB.lean#L721) | 233 · `R/E/1111` at 64,929 | — |
| 68 | [525](BB6_holdouts_608.txt#L525) | 151878 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RF_0LC0RF_1RD1LC_HHH0LE_0RC1LF_1RA0LE.lean#L918) | 165 · `L/E/0101` at 65,305 | — |
| 69 | [536](BB6_holdouts_608.txt#L536) | 155226 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_HHH1RE.lean#L364) | 349 · `R/C/1111` at 65,302 | — |
| 70 | [569](BB6_holdouts_608.txt#L569) | 166535 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_HHH0RA.lean#L942) | 643 · `R/D/1010` at 64,356 | — |
| 71 | [587](BB6_holdouts_608.txt#L587) | 173741 | [highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1LD_0RC0LF_1LD1RE_0LA0RB_0RD1RB_0LDHHH.lean#L878) | 96 · `L/A/0101` at 64,852 | — |
| 72 | [591](BB6_holdouts_608.txt#L591) | 174634 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_HHH1RA.lean#L710) | 501 · `L/C/1010` at 65,128 | — |
| 73 | [595](BB6_holdouts_608.txt#L595) | 175628 | [next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RE_1LC1LB_1LE0LD_1LE1LC_0RF1RA_HHH1RA.lean#L448) | 512 · `L/E/1111` at 65,379 | — |

## Use a structural reduction

Use the cited stack, odometer or tape invariant to write the return rules for the reachable start and check their halting exits.

| Rank | Line | Machine ID | First check | Edge records · last signature and step | Other open starts |
|---:|---:|---:|---|---|---|
| 74 | [185](BB6_holdouts_608.txt#L185) | 50114 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RBHHH_0RC1RD_1LA0LA_1LE0RB_1LF1LE_1LC0LD.lean#L1856) | 380 · `R/D/1111` at 65,134 | 422 (C mirrored), 441 (B mirrored), 490 (E mirrored), 538 (D mirrored) |
| 75 | [62](BB6_holdouts_608.txt#L62) | 17454 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RBHHH_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA.lean#L1193) | 594 · `R/D/1101` at 64,417 | 212 (F), 369 (F mirrored), 377 (F) |
| 76 | [212](BB6_holdouts_608.txt#L212) | 58362 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RD_1LC0LE_1RA0LB_1RA1RF_0RA0RC_1REHHH.lean#L118) | 602 · `R/B/1101` at 64,911 | 62 (C), 369 (C mirrored), 377 (B) |
| 77 | [288](BB6_holdouts_608.txt#L288) | 75625 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RE_0RCHHH_1LD1LE_1LE1LD_1RF0LC_1RA1RF.lean#L1694) | 473 · `R/C/0111` at 65,474 | 23 (D mirrored), 215 (C), 502 (E mirrored) |
| 78 | [369](BB6_holdouts_608.txt#L369) | 103424 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LEHHH.lean#L120) | 538 · `L/A/1101` at 64,031 | 62 (D mirrored), 212 (B mirrored), 377 (C mirrored) |
| 79 | [377](BB6_holdouts_608.txt#L377) | 104936 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LC_1RC1RE_1LA0LD_0RB0RA_1RB1RF_1RDHHH.lean#L118) | 623 · `R/C/1101` at 64,541 | 62 (E), 212 (C), 369 (B mirrored) |
| 80 | [83](BB6_holdouts_608.txt#L83) | 22262 | [segmented tape](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RF_1RC0RA_1LD1RB_1LE0LD_0RA0LB_0RBHHH.lean#L730) | 130 · `R/C/1111` at 58,921 | 402 (E), 462 (C mirrored) |
| 81 | [402](BB6_holdouts_608.txt#L402) | 113824 | [segmented tape](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RE_1LC1RA_1LD0LC_0RE0LA_1RA1RF_0RAHHH.lean#L731) | 89 · `R/B/1111` at 40,711 | 83 (B), 462 (E mirrored) |
| 82 | [462](BB6_holdouts_608.txt#L462) | 131953 | [segmented tape](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RA_0LC0RE_1LE1LD_0LEHHH_1LF0LC_1RA1LE.lean#L730) | 120 · `L/F/1111` at 59,397 | 83 (D mirrored), 402 (C mirrored) |
| 83 | [425](BB6_holdouts_608.txt#L425) | 122751 | [odometer invariant](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LD_0LC0RE_1LA0RD_0RB0LD_1RC1RF_1RAHHH.lean#L533) | 68 · `R/C/1011` at 47,760 | 488 (B) |
| 84 | [488](BB6_holdouts_608.txt#L488) | 139516 | [odometer invariant](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RBHHH_1RC0LE_0LD0RF_1LB0RE_0RC0LE_1RD1RA.lean#L512) | 72 · `R/D/1011` at 45,070 | 425 (F) |
| 85 | [8](BB6_holdouts_608.txt#L8) | 2327 | [stack invariant](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LE_1LC0RE_0RA0LD_1LA1LF_0LC0RE_0LAHHH.lean#L1735) | 97 · `L/A/1011` at 50,804 | — |
| 86 | [9](BB6_holdouts_608.txt#L9) | 2336 | [mixed-radix odometer](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LD_0RCHHH_1LD0RF_0LE0RA_0RA1LF_0LA1LB.lean#L550) | 108 · `L/A/0101` at 60,680 | — |
| 87 | [22](BB6_holdouts_608.txt#L22) | 6741 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_HHH0LB.lean#L481) | 446 · `R/C/1111` at 65,283 | — |
| 88 | [34](BB6_holdouts_608.txt#L34) | 9169 | [stack invariant](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LE_1LC0RE_0RA0LD_1LA1LF_0LC0RE_0LCHHH.lean#L1532) | 94 · `L/A/1011` at 58,659 | — |
| 89 | [139](BB6_holdouts_608.txt#L139) | 36498 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RA_1LC0RC_HHH0LD_0LE0RF_1RE0RA_0LF1LB.lean#L1114) | 91 · `L/E/0011` at 62,298 | — |
| 90 | [156](BB6_holdouts_608.txt#L156) | 41157 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RC_1LC0LE_1RD1RC_1LB0RA_HHH0LF_1RD1LF.lean#L855) | 349 · `R/D/1111` at 50,935 | — |
| 91 | [164](BB6_holdouts_608.txt#L164) | 43701 | [stack invariant](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LE_1LC0RE_0RA0LD_1LA0LF_0LC0RA_0REHHH.lean#L1187) | 109 · `L/A/1011` at 54,316 | — |
| 92 | [206](BB6_holdouts_608.txt#L206) | 55410 | [stack invariant](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LD_0LC0RE_1LA0RD_0RB0LF_1RC1LA_0RBHHH.lean#L1183) | 109 · `R/C/1011` at 58,389 | — |
| 93 | [225](BB6_holdouts_608.txt#L225) | 60779 | [stack invariant](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LE_1LC0RE_0RA0LD_1LA1LF_0LC0RE_1LAHHH.lean#L1543) | 93 · `L/A/1011` at 53,148 | — |
| 94 | [226](BB6_holdouts_608.txt#L226) | 61234 | [stack invariant](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LE_1LC0RE_0RA0LD_1LA1LF_0LC0RA_0LEHHH.lean#L1458) | 83 · `L/A/1011` at 60,196 | — |
| 95 | [230](BB6_holdouts_608.txt#L230) | 64715 | [stack invariant](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LE_1LC0RE_0RA0LD_1LA1LF_0LC0RE_1LEHHH.lean#L1682) | 72 · `L/A/1011` at 44,919 | — |
| 96 | [242](BB6_holdouts_608.txt#L242) | 66280 | [stack invariant](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LE_1LC0RE_0RA0LD_1LA1LF_0LC0RA_0LBHHH.lean#L1469) | 83 · `L/A/1011` at 60,208 | — |
| 97 | [361](BB6_holdouts_608.txt#L361) | 100296 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LC_1LC0RE_1LD1LC_1LA1RD_HHH0RF_0LB0RD.lean#L454) | 315 · `L/A/1111` at 52,516 | — |
| 98 | [385](BB6_holdouts_608.txt#L385) | 107543 | [segmented tape](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0LD_0RC1RD_1LA1RA_1LE0LE_1RF0LA_0RAHHH.lean#L692) | 363 · `L/A/0100` at 65,100 | — |
| 99 | [416](BB6_holdouts_608.txt#L416) | 118184 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1LA_1RC0RF_1RDHHH_0LE1RB_HHH0LA_1LD1RF.lean#L434) | 155 · `L/A/1111` at 54,995 | — |
| 100 | [495](BB6_holdouts_608.txt#L495) | 141118 | [stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RA_1LC0RC_1RE0LD_0RE0LF_1RAHHH_1RB1LF.lean#L439) | 349 · `R/B/1111` at 53,321 | — |

## Transfer a related model

Translate the peer's model to the listed entry. Check each changed instruction on the new blank orbit.

| Rank | Line | Machine ID | First check | Edge records · last signature and step | Other open starts |
|---:|---:|---:|---|---|---|
| 101 | [422](BB6_holdouts_608.txt#L422) | 121862 | Compare line 185 ([stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RBHHH_0RC1RD_1LA0LA_1LE0RB_1LF1LE_1LC0LD.lean#L1856)), `A → F mirrored`, all 12 instructions match. | 406 · `L/E/1111` at 65,461 | 185 (F mirrored), 441 (F), 490 (C), 538 (B) |
| 102 | [441](BB6_holdouts_608.txt#L441) | 126123 | Compare line 185 ([stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RBHHH_0RC1RD_1LA0LA_1LE0RB_1LF1LE_1LC0LD.lean#L1856)), `A → C mirrored`, all 12 instructions match. | 383 · `L/D/1101` at 64,561 | 185 (C mirrored), 422 (B), 490 (D), 538 (C) |
| 103 | [490](BB6_holdouts_608.txt#L490) | 139893 | Compare line 185 ([stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RBHHH_0RC1RD_1LA0LA_1LE0RB_1LF1LE_1LC0LD.lean#L1856)), `A → D mirrored`, all 12 instructions match. | 398 · `L/A/1111` at 65,413 | 185 (D mirrored), 422 (E), 441 (D), 538 (F) |
| 104 | [538](BB6_holdouts_608.txt#L538) | 155803 | Compare line 185 ([stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RBHHH_0RC1RD_1LA0LA_1LE0RB_1LF1LE_1LC0LD.lean#L1856)), `A → E mirrored`, all 12 instructions match. | 391 · `L/F/1111` at 65,482 | 185 (E mirrored), 422 (F), 441 (E), 490 (B) |
| 105 | [23](BB6_holdouts_608.txt#L23) | 7085 | Compare line 288 ([stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RE_0RCHHH_1LD1LE_1LE1LD_1RF0LC_1RA1RF.lean#L1694)), `A → D mirrored`, all 12 instructions match. | 463 · `R/B/1111` at 65,507 | 215 (F mirrored), 288 (D mirrored), 502 (B) |
| 106 | [215](BB6_holdouts_608.txt#L215) | 58953 | Compare line 288 ([stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RE_0RCHHH_1LD1LE_1LE1LD_1RF0LC_1RA1RF.lean#L1694)), `A → E`, all 12 instructions match. | 465 · `L/A/1111` at 64,866 | 23 (B mirrored), 288 (E), 502 (C mirrored) |
| 107 | [502](BB6_holdouts_608.txt#L502) | 144803 | Compare line 288 ([stack reduction](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RE_0RCHHH_1LD1LE_1LE1LD_1RF0LC_1RA1RF.lean#L1694)), `A → C mirrored`, all 12 instructions match. | 480 · `R/C/1111` at 65,512 | 23 (F), 215 (E mirrored), 288 (C mirrored) |
| 108 | [371](BB6_holdouts_608.txt#L371) | 103901 | Compare line 64 ([highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RE_0RC1RE_1RD1LE_0LEHHH_1RA1LF_1RF0LC.lean#L789)), `A → C`, all 12 instructions match. | 469 · `L/C/1010` at 65,459 | 64 (C), 602 (D) |
| 109 | [602](BB6_holdouts_608.txt#L602) | 180268 | Compare line 64 ([highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB0RE_0RC1RE_1RD1LE_0LEHHH_1RA1LF_1RF0LC.lean#L789)), `A → E`, all 12 instructions match. | 556 · `L/A/1010` at 65,126 | 64 (E), 371 (C) |
| 110 | [69](BB6_holdouts_608.txt#L69) | 19219 | Compare line 166 ([highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RE_1LC0RC_1RA1LD_1RB0LA_0LC1RF_HHH1RD.lean#L595)), `A → C`, all 12 instructions match. | 358 · `L/D/1110` at 65,167 | 166 (C) |
| 111 | [194](BB6_holdouts_608.txt#L194) | 52677 | Compare line 492 ([next from start](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1LA_1LC0RE_HHH0LD_1RE0LF_1RA1RE_1LA0LB.lean#L711)), `A → A`. At `D0` (first read at step 3), the candidate uses `1LA` and the aligned peer uses `1RE`. | 212 · `R/B/1110` at 57,666 | — |
| 112 | [247](BB6_holdouts_608.txt#L247) | 67137 | Compare line 598 ([HALT_PR source](https://github.com/ccz181078/busycoq/pull/93)), `A → B mirrored`. At `F0` (first read at step 271), the candidate uses `0RB` and the aligned peer uses `0LC`. | 386 · `R/C/1101` at 64,887 | 448 (B mirrored), 539 (C mirrored) |
| 113 | [539](BB6_holdouts_608.txt#L539) | 155900 | Compare line 598 ([HALT_PR source](https://github.com/ccz181078/busycoq/pull/93)), `A → D`. At `F0` (first read at step 104), the candidate uses `0LD` and the aligned peer uses `0RA`. | 403 · `L/A/1101` at 64,979 | 247 (C mirrored), 448 (D) |
| 114 | [47](BB6_holdouts_608.txt#L47) | 12692 | Compare line 166 ([highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RE_1LC0RC_1RA1LD_1RB0LA_0LC1RF_HHH1RD.lean#L595)), `A → C`. At `F1` (first read at step 66), the candidate uses `1RB` and the aligned peer uses `1RD`. | 438 · `L/D/1110` at 65,341 | 91 (B mirrored) |
| 115 | [91](BB6_holdouts_608.txt#L91) | 24566 | Compare line 166 ([highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RE_1LC0RC_1RA1LD_1RB0LA_0LC1RF_HHH1RD.lean#L595)), `A → B mirrored`. At `F1` (first read at step 44), the candidate uses `1LC` and the aligned peer uses `1LE`. | 380 · `R/E/1110` at 64,756 | 47 (C mirrored) |
| 116 | [158](BB6_holdouts_608.txt#L158) | 41716 | Compare line 101 ([highLevelNext from highLevelStart](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/M_1RB1RF_1LC1LF_HHH1LD_1LE0RA_1RE1LB_1RD0LD.lean#L706)), `A → D mirrored`. At `B0` (first read at step 1), the candidate uses `1RC` and the aligned peer uses `1LB`. | 398 · `R/C/1101` at 64,521 | — |
| 117 | [337](BB6_holdouts_608.txt#L337) | 95121 | Compare line 559 ([SOC25 from (1, 2)](https://github.com/valu42/busycoqtesting/blob/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623/SOC25_DEQUE.md)), `A → F mirrored`. At `A1` (first read at step 10), the candidate uses `0RF` and the aligned peer uses `---`. | 86 · `R/C/1111` at 42,147 | — |

## Test a repeating tape edge

Derive a return rule for the repeated edge signature and test it against the full interior tape at the next extension.

| Rank | Line | Machine ID | First check | Edge records · last signature and step | Other open starts |
|---:|---:|---:|---|---|---|
| 118 | [593](BB6_holdouts_608.txt#L593) | 175438 | Period 2 across the last 724 edge records. | 809 · `R/C/0001` at 65,480 | — |
| 119 | [24](BB6_holdouts_608.txt#L24) | 7846 | Period 2 across the last 660 edge records. | 743 · `R/F/0001` at 65,092 | — |
| 120 | [564](BB6_holdouts_608.txt#L564) | 164904 | Period 2 across the last 656 edge records. | 734 · `R/F/0001` at 65,383 | — |
| 121 | [413](BB6_holdouts_608.txt#L413) | 117020 | Period 2 across the last 337 edge records. | 426 · `R/C/1111` at 65,488 | 280 (E) |
| 122 | [542](BB6_holdouts_608.txt#L542) | 157319 | Period 2 across the last 337 edge records. | 423 · `R/B/1101` at 65,073 | — |
| 123 | [516](BB6_holdouts_608.txt#L516) | 148224 | Period 2 across the last 335 edge records. | 429 · `L/C/1111` at 64,901 | 187 (E mirrored) |
| 124 | [99](BB6_holdouts_608.txt#L99) | 25821 | Period 2 across the last 334 edge records. | 459 · `R/C/1111` at 65,114 | — |
| 125 | [280](BB6_holdouts_608.txt#L280) | 73071 | Period 2 across the last 331 edge records. | 436 · `R/B/1111` at 65,190 | 413 (B) |
| 126 | [467](BB6_holdouts_608.txt#L467) | 132695 | Period 2 across the last 260 edge records. | 386 · `R/B/1010` at 64,760 | 283 (C mirrored) |
| 127 | [417](BB6_holdouts_608.txt#L417) | 118323 | Period 2 across the last 227 edge records. | 533 · `R/B/1010` at 64,935 | 217 (E mirrored), 387 (B) |
| 128 | [570](BB6_holdouts_608.txt#L570) | 166700 | Period 2 across the last 210 edge records. | 481 · `L/D/1010` at 65,148 | 54 (E), 200 (E), 272 (B mirrored), 545 (E mirrored) |
| 129 | [391](BB6_holdouts_608.txt#L391) | 110862 | Period 2 across the last 210 edge records. | 352 · `L/D/1110` at 64,846 | 543 (B) |
| 130 | [543](BB6_holdouts_608.txt#L543) | 157488 | Period 2 across the last 210 edge records. | 358 · `L/D/1110` at 65,167 | 391 (C) |
| 131 | [283](BB6_holdouts_608.txt#L283) | 74982 | Period 2 across the last 204 edge records. | 428 · `L/F/1010` at 65,517 | 467 (D mirrored) |
| 132 | [200](BB6_holdouts_608.txt#L200) | 54407 | Period 2 across the last 202 edge records. | 520 · `L/C/1010` at 65,234 | 54 (B), 272 (C mirrored), 545 (C mirrored), 570 (E) |
| 133 | [192](BB6_holdouts_608.txt#L192) | 51709 | Period 2 across the last 199 edge records. | 411 · `L/D/1111` at 65,429 | — |
| 134 | [544](BB6_holdouts_608.txt#L544) | 157503 | Period 2 across the last 181 edge records. | 383 · `R/B/1101` at 65,200 | — |
| 135 | [424](BB6_holdouts_608.txt#L424) | 122390 | Period 2 across the last 177 edge records. | 594 · `R/D/1010` at 65,394 | 251 (E), 353 (D) |
| 136 | [25](BB6_holdouts_608.txt#L25) | 8002 | Period 2 across the last 157 edge records. | 323 · `R/D/1010` at 64,923 | 37 (C mirrored), 336 (D) |
| 137 | [184](BB6_holdouts_608.txt#L184) | 49956 | Period 2 across the last 156 edge records. | 436 · `L/D/0111` at 65,250 | 510 (C mirrored) |
| 138 | [353](BB6_holdouts_608.txt#L353) | 98520 | Period 2 across the last 154 edge records. | 400 · `R/B/1010` at 64,767 | 251 (F), 424 (F) |
| 139 | [481](BB6_holdouts_608.txt#L481) | 136824 | Period 2 across the last 149 edge records. | 369 · `L/D/1111` at 65,229 | — |
| 140 | [387](BB6_holdouts_608.txt#L387) | 108865 | Period 2 across the last 145 edge records. | 500 · `R/C/1010` at 65,063 | 217 (F mirrored), 417 (F) |
| 141 | [187](BB6_holdouts_608.txt#L187) | 50378 | Period 2 across the last 126 edge records. | 437 · `R/B/1111` at 65,010 | 516 (B mirrored) |
| 142 | [70](BB6_holdouts_608.txt#L70) | 19442 | Period 3 across the last 369 edge records. | 430 · `L/B/1110` at 65,215 | 85 (F mirrored), 409 (F mirrored) |
| 143 | [409](BB6_holdouts_608.txt#L409) | 115779 | Period 3 across the last 366 edge records. | 433 · `R/D/1110` at 64,699 | 70 (D mirrored), 85 (B) |
| 144 | [85](BB6_holdouts_608.txt#L85) | 23154 | Period 3 across the last 357 edge records. | 463 · `R/E/1110` at 64,965 | 70 (C mirrored), 409 (E) |
| 145 | [7](BB6_holdouts_608.txt#L7) | 2090 | Period 3 across the last 302 edge records. | 649 · `R/E/1010` at 65,491 | 535 (B mirrored) |
| 146 | [505](BB6_holdouts_608.txt#L505) | 144992 | Period 3 across the last 239 edge records. | 469 · `L/D/0010` at 64,752 | 201 (D) |
| 147 | [232](BB6_holdouts_608.txt#L232) | 65180 | Period 3 across the last 194 edge records. | 529 · `R/C/0010` at 64,939 | 347 (D mirrored), 582 (B mirrored) |
| 148 | [347](BB6_holdouts_608.txt#L347) | 97302 | Period 3 across the last 191 edge records. | 558 · `L/A/0010` at 64,775 | 232 (C mirrored), 582 (D) |
| 149 | [577](BB6_holdouts_608.txt#L577) | 168919 | Period 3 across the last 144 edge records. | 401 · `R/C/1101` at 64,653 | — |
| 150 | [12](BB6_holdouts_608.txt#L12) | 3292 | Period 3 across the last 111 edge records. | 373 · `R/B/1100` at 65,465 | 84 (C mirrored), 440 (B) |
| 151 | [84](BB6_holdouts_608.txt#L84) | 22465 | Period 3 across the last 105 edge records. | 368 · `L/A/1100` at 64,103 | 12 (B mirrored), 440 (C mirrored) |
| 152 | [269](BB6_holdouts_608.txt#L269) | 70977 | Period 4 across the last 256 edge records. | 696 · `R/E/1010` at 64,744 | — |

## Compare blank starts

Use one transition table for the listed open lines. Compare the complete configurations reached from their distinct initial states.

| Rank | Line | Machine ID | First check | Edge records · last signature and step | Other open starts |
|---:|---:|---:|---|---|---|
| 153 | [545](BB6_holdouts_608.txt#L545) | 157647 | Compare the mapped starts at the next `R/B/1010` extension. | 579 · `R/B/1010` at 65,463 | 54 (C mirrored), 200 (B mirrored), 272 (D), 570 (F mirrored) |
| 154 | [54](BB6_holdouts_608.txt#L54) | 14847 | Compare the mapped starts at the next `L/A/1010` extension. | 534 · `L/A/1010` at 65,450 | 200 (C), 272 (E mirrored), 545 (B mirrored), 570 (D) |
| 155 | [272](BB6_holdouts_608.txt#L272) | 71372 | Compare the mapped starts at the next `R/E/1010` extension. | 529 · `R/E/1010` at 64,695 | 54 (D mirrored), 200 (D mirrored), 545 (D), 570 (B mirrored) |
| 156 | [21](BB6_holdouts_608.txt#L21) | 5788 | Compare the mapped starts at the next `L/A/0110` extension. | 586 · `L/A/0110` at 65,409 | 106 (B mirrored), 182 (C mirrored), 214 (C) |
| 157 | [30](BB6_holdouts_608.txt#L30) | 9074 | Compare the mapped starts at the next `L/C/1011` extension. | 118 · `L/C/1011` at 46,834 | 73 (C mirrored), 169 (E mirrored), 354 (D mirrored) |
| 158 | [60](BB6_holdouts_608.txt#L60) | 16609 | Compare the mapped starts at the next `R/D/1100` extension. | 655 · `R/D/1100` at 64,719 | 146 (D mirrored), 218 (E), 485 (D mirrored) |
| 159 | [73](BB6_holdouts_608.txt#L73) | 20489 | Compare the mapped starts at the next `R/B/1011` extension. | 112 · `R/B/1011` at 41,473 | 30 (B mirrored), 169 (C), 354 (B) |
| 160 | [106](BB6_holdouts_608.txt#L106) | 26895 | Compare the mapped starts at the next `R/B/0110` extension. | 554 · `R/B/0110` at 64,652 | 21 (C mirrored), 182 (E), 214 (B mirrored) |
| 161 | [146](BB6_holdouts_608.txt#L146) | 37988 | Compare the mapped starts at the next `L/A/1100` extension. | 691 · `L/A/1100` at 65,286 | 60 (D mirrored), 218 (B mirrored), 485 (C) |
| 162 | [169](BB6_holdouts_608.txt#L169) | 44966 | Compare the mapped starts at the next `R/D/1011` extension. | 124 · `R/D/1011` at 44,300 | 30 (E mirrored), 73 (E), 354 (F) |
| 163 | [214](BB6_holdouts_608.txt#L214) | 58767 | Compare the mapped starts at the next `L/C/0110` extension. | 525 · `L/C/0110` at 65,285 | 21 (B), 106 (C mirrored), 182 (D mirrored) |
| 164 | [218](BB6_holdouts_608.txt#L218) | 59536 | Compare the mapped starts at the next `R/B/1100` extension. | 695 · `R/B/1100` at 65,437 | 60 (C), 146 (C mirrored), 485 (B mirrored) |
| 165 | [354](BB6_holdouts_608.txt#L354) | 98843 | Compare the mapped starts at the next `R/C/1011` extension. | 135 · `R/C/1011` at 56,374 | 30 (F mirrored), 73 (F), 169 (B) |
| 166 | [485](BB6_holdouts_608.txt#L485) | 139315 | Compare the mapped starts at the next `L/C/1100` extension. | 663 · `L/C/1100` at 65,110 | 60 (B mirrored), 146 (B), 218 (C mirrored) |
| 167 | [17](BB6_holdouts_608.txt#L17) | 4608 | Compare the mapped starts at the next `R/D/1010` extension. | 464 · `R/D/1010` at 64,805 | 168 (D mirrored), 332 (D), 342 (D mirrored) |
| 168 | [168](BB6_holdouts_608.txt#L168) | 44840 | Compare the mapped starts at the next `L/A/1010` extension. | 470 · `L/A/1010` at 64,700 | 17 (D mirrored), 332 (B mirrored), 342 (C) |
| 169 | [227](BB6_holdouts_608.txt#L227) | 63327 | Compare the mapped starts at the next `R/D/1111` extension. | 320 · `R/D/1111` at 64,262 | 138 (E), 308 (D), 358 (B mirrored) |
| 170 | [332](BB6_holdouts_608.txt#L332) | 93459 | Compare the mapped starts at the next `L/A/1101` extension. | 479 · `L/A/1101` at 65,404 | 17 (C), 168 (C mirrored), 342 (B mirrored) |
| 171 | [358](BB6_holdouts_608.txt#L358) | 99431 | Compare the mapped starts at the next `R/B/1101` extension. | 347 · `R/B/1101` at 63,220 | 138 (D mirrored), 227 (E mirrored), 308 (C mirrored) |
| 172 | [115](BB6_holdouts_608.txt#L115) | 29824 | Compare the mapped starts at the next `R/C/1111` extension. | 93 · `R/C/1111` at 51,009 | 144 (E), 456 (E mirrored), 537 (E mirrored) |
| 173 | [144](BB6_holdouts_608.txt#L144) | 37401 | Compare the mapped starts at the next `R/B/1111` extension. | 111 · `R/B/1111` at 52,026 | 115 (B), 456 (C mirrored), 537 (B mirrored) |
| 174 | [426](BB6_holdouts_608.txt#L426) | 123029 | Compare the mapped starts at the next `L/E/1111` extension. | 307 · `L/E/1111` at 61,038 | 188 (D mirrored), 415 (C mirrored), 429 (E mirrored) |
| 175 | [456](BB6_holdouts_608.txt#L456) | 130046 | Compare the mapped starts at the next `L/D/1111` extension. | 87 · `L/D/1111` at 63,685 | 115 (D mirrored), 144 (C mirrored), 537 (D) |
| 176 | [175](BB6_holdouts_608.txt#L175) | 47099 | Compare the mapped starts at the next `R/D/1010` extension. | 712 · `R/D/1010` at 64,843 | 297 (D), 410 (C), 507 (B mirrored) |
| 177 | [297](BB6_holdouts_608.txt#L297) | 78977 | Compare the mapped starts at the next `R/C/1010` extension. | 694 · `R/C/1010` at 65,260 | 175 (F), 410 (F), 507 (F mirrored) |
| 178 | [308](BB6_holdouts_608.txt#L308) | 83242 | Compare the mapped starts at the next `R/B/1111` extension. | 311 · `R/B/1111` at 64,786 | 138 (B), 227 (C), 358 (D mirrored) |
| 179 | [327](BB6_holdouts_608.txt#L327) | 92022 | Compare the mapped starts at the next `R/C/1111` extension. | 520 · `R/C/1111` at 64,762 | 40 (C), 250 (D mirrored), 540 (E) |
| 180 | [410](BB6_holdouts_608.txt#L410) | 116343 | Compare the mapped starts at the next `R/B/1010` extension. | 731 · `R/B/1010` at 64,401 | 175 (C), 297 (B), 507 (D mirrored) |
| 181 | [154](BB6_holdouts_608.txt#L154) | 40600 | Compare the mapped starts at the next `R/B/1010` extension. | 615 · `R/B/1010` at 65,163 | 126 (D mirrored), 370 (C), 463 (E mirrored) |
| 182 | [342](BB6_holdouts_608.txt#L342) | 95984 | Compare the mapped starts at the next `L/C/1010` extension. | 545 · `L/C/1010` at 65,480 | 17 (E mirrored), 168 (B), 332 (C mirrored) |
| 183 | [126](BB6_holdouts_608.txt#L126) | 32883 | Compare the mapped starts at the next `L/A/1010` extension. | 615 · `L/A/1010` at 65,262 | 154 (B mirrored), 370 (D mirrored), 463 (B) |
| 184 | [138](BB6_holdouts_608.txt#L138) | 36364 | Compare the mapped starts at the next `L/E/1101` extension. | 345 · `L/E/1101` at 65,339 | 227 (B), 308 (E), 358 (C mirrored) |
| 185 | [188](BB6_holdouts_608.txt#L188) | 50436 | Compare the mapped starts at the next `R/C/1111` extension. | 301 · `R/C/1111` at 65,321 | 415 (E), 426 (C mirrored), 429 (B) |
| 186 | [370](BB6_holdouts_608.txt#L370) | 103746 | Compare the mapped starts at the next `R/D/1010` extension. | 615 · `R/D/1010` at 65,119 | 126 (B mirrored), 154 (C), 463 (C mirrored) |
| 187 | [415](BB6_holdouts_608.txt#L415) | 117546 | Compare the mapped starts at the next `L/D/1101` extension. | 313 · `L/D/1101` at 65,321 | 188 (B), 426 (D mirrored), 429 (C) |
| 188 | [429](BB6_holdouts_608.txt#L429) | 123915 | Compare the mapped starts at the next `L/A/1101` extension. | 301 · `L/A/1101` at 65,109 | 188 (E), 415 (D), 426 (B mirrored) |
| 189 | [463](BB6_holdouts_608.txt#L463) | 131976 | Compare the mapped starts at the next `L/B/1010` extension. | 615 · `L/B/1010` at 65,403 | 126 (E), 154 (D mirrored), 370 (E mirrored) |
| 190 | [507](BB6_holdouts_608.txt#L507) | 145615 | Compare the mapped starts at the next `R/B/1010` extension. | 625 · `R/B/1010` at 65,087 | 175 (D mirrored), 297 (C mirrored), 410 (B mirrored) |
| 191 | [537](BB6_holdouts_608.txt#L537) | 155590 | Compare the mapped starts at the next `L/C/1111` extension. | 89 · `L/C/1111` at 60,157 | 115 (E mirrored), 144 (D mirrored), 456 (B) |
| 192 | [182](BB6_holdouts_608.txt#L182) | 49413 | Compare the mapped starts at the next `R/C/0110` extension. | 598 · `R/C/0110` at 64,351 | 21 (E mirrored), 106 (F), 214 (E mirrored) |
| 193 | [40](BB6_holdouts_608.txt#L40) | 10690 | Compare the mapped starts at the next `L/A/1001` extension. | 493 · `L/A/1001` at 64,918 | 250 (B mirrored), 327 (D), 540 (C) |
| 194 | [250](BB6_holdouts_608.txt#L250) | 67840 | Compare the mapped starts at the next `L/A/1111` extension. | 513 · `L/A/1111` at 64,872 | 40 (E mirrored), 327 (C mirrored), 540 (B mirrored) |
| 195 | [540](BB6_holdouts_608.txt#L540) | 156554 | Compare the mapped starts at the next `R/B/1111` extension. | 494 · `R/B/1111` at 64,753 | 40 (D), 250 (E mirrored), 327 (B) |
| 196 | [11](BB6_holdouts_608.txt#L11) | 3006 | Compare the mapped starts at the next `R/E/1010` extension. | 573 · `R/E/1010` at 65,139 | 287 (D), 423 (B mirrored) |
| 197 | [145](BB6_holdouts_608.txt#L145) | 37843 | Compare the mapped starts at the next `L/A/1010` extension. | 529 · `L/A/1010` at 65,390 | 310 (B mirrored), 313 (C) |
| 198 | [217](BB6_holdouts_608.txt#L217) | 59397 | Compare the mapped starts at the next `L/A/1010` extension. | 707 · `L/A/1010` at 65,286 | 387 (C mirrored), 417 (B mirrored) |
| 199 | [237](BB6_holdouts_608.txt#L237) | 65944 | Compare the mapped starts at the next `L/A/1011` extension. | 356 · `L/A/1011` at 65,126 | 442 (E), 556 (B mirrored) |
| 200 | [251](BB6_holdouts_608.txt#L251) | 67879 | Compare the mapped starts at the next `R/C/1010` extension. | 525 · `R/C/1010` at 65,218 | 353 (E), 424 (B) |
| 201 | [287](BB6_holdouts_608.txt#L287) | 75404 | Compare the mapped starts at the next `R/C/1010` extension. | 564 · `R/C/1010` at 65,201 | 11 (C), 423 (D mirrored) |
| 202 | [310](BB6_holdouts_608.txt#L310) | 84927 | Compare the mapped starts at the next `R/B/1010` extension. | 554 · `R/B/1010` at 65,145 | 145 (C mirrored), 313 (B mirrored) |
| 203 | [313](BB6_holdouts_608.txt#L313) | 86275 | Compare the mapped starts at the next `L/C/1010` extension. | 537 · `L/C/1010` at 65,144 | 145 (B), 310 (C mirrored) |
| 204 | [418](BB6_holdouts_608.txt#L418) | 119197 | Compare the mapped starts at the next `R/C/1111` extension. | 358 · `R/C/1111` at 65,495 | 234 (D), 290 (D mirrored) |
| 205 | [423](BB6_holdouts_608.txt#L423) | 122192 | Compare the mapped starts at the next `L/A/1010` extension. | 633 · `L/A/1010` at 65,491 | 11 (E mirrored), 287 (C mirrored) |
| 206 | [442](BB6_holdouts_608.txt#L442) | 126128 | Compare the mapped starts at the next `L/E/1011` extension. | 366 · `L/E/1011` at 65,263 | 237 (D), 556 (C mirrored) |
| 207 | [32](BB6_holdouts_608.txt#L32) | 9129 | Compare the mapped starts at the next `L/A/0010` extension. | 608 · `L/A/0010` at 65,448 | 170 (D), 333 (C mirrored) |
| 208 | [49](BB6_holdouts_608.txt#L49) | 12989 | Compare the mapped starts at the next `R/C/0010` extension. | 597 · `R/C/0010` at 65,303 | 100 (D mirrored), 248 (B mirrored) |
| 209 | [52](BB6_holdouts_608.txt#L52) | 13768 | Compare the mapped starts at the next `L/D/0010` extension. | 631 · `L/D/0010` at 64,722 | 263 (C), 541 (E mirrored) |
| 210 | [65](BB6_holdouts_608.txt#L65) | 18251 | Compare the mapped starts at the next `R/C/1100` extension. | 531 · `R/C/1100` at 65,437 | 381 (E), 590 (C) |
| 211 | [68](BB6_holdouts_608.txt#L68) | 18495 | Compare the mapped starts at the next `L/D/0010` extension. | 564 · `L/D/0010` at 65,355 | 97 (E mirrored), 334 (C) |
| 212 | [71](BB6_holdouts_608.txt#L71) | 19849 | Compare the mapped starts at the next `L/D/0010` extension. | 546 · `L/D/0010` at 65,454 | 105 (E mirrored), 338 (C) |
| 213 | [78](BB6_holdouts_608.txt#L78) | 21561 | Compare the mapped starts at the next `L/C/0010` extension. | 555 · `L/C/0010` at 65,212 | 403 (F mirrored), 408 (F) |
| 214 | [97](BB6_holdouts_608.txt#L97) | 25702 | Compare the mapped starts at the next `R/C/0010` extension. | 597 · `R/C/0010` at 65,181 | 68 (B mirrored), 334 (D mirrored) |
| 215 | [100](BB6_holdouts_608.txt#L100) | 25839 | Compare the mapped starts at the next `L/A/0010` extension. | 623 · `L/A/0010` at 65,068 | 49 (C mirrored), 248 (D) |
| 216 | [105](BB6_holdouts_608.txt#L105) | 26817 | Compare the mapped starts at the next `R/C/0010` extension. | 588 · `R/C/0010` at 65,477 | 71 (B mirrored), 338 (D mirrored) |
| 217 | [109](BB6_holdouts_608.txt#L109) | 28031 | Compare the mapped starts at the next `R/B/1111` extension. | 574 · `R/B/1111` at 56,973 | 372 (C mirrored), 572 (D mirrored) |
| 218 | [150](BB6_holdouts_608.txt#L150) | 39511 | Compare the mapped starts at the next `L/A/0100` extension. | 360 · `L/A/0100` at 65,446 | 160 (E), 349 (C mirrored) |
| 219 | [160](BB6_holdouts_608.txt#L160) | 42011 | Compare the mapped starts at the next `L/E/0100` extension. | 349 · `L/E/0100` at 65,104 | 150 (B), 349 (D mirrored) |
| 220 | [170](BB6_holdouts_608.txt#L170) | 45197 | Compare the mapped starts at the next `L/D/0010` extension. | 543 · `L/D/0010` at 65,355 | 32 (C), 333 (E mirrored) |
| 221 | [248](BB6_holdouts_608.txt#L248) | 67596 | Compare the mapped starts at the next `L/D/0010` extension. | 570 · `L/D/0010` at 65,107 | 49 (E mirrored), 100 (C) |
| 222 | [249](BB6_holdouts_608.txt#L249) | 67635 | Compare the mapped starts at the next `R/C/0010` extension. | 600 · `R/C/0010` at 65,343 | 298 (D mirrored), 340 (B mirrored) |
| 223 | [252](BB6_holdouts_608.txt#L252) | 67956 | Compare the mapped starts at the next `R/B/1101` extension. | 540 · `R/B/1101` at 65,013 | 443 (B mirrored), 557 (B) |
| 224 | [257](BB6_holdouts_608.txt#L257) | 69016 | Compare the mapped starts at the next `L/D/0010` extension. | 549 · `L/D/0010` at 64,367 | 267 (E mirrored), 427 (C) |
| 225 | [263](BB6_holdouts_608.txt#L263) | 69987 | Compare the mapped starts at the next `L/A/0010` extension. | 676 · `L/A/0010` at 64,867 | 52 (D), 541 (C mirrored) |
| 226 | [267](BB6_holdouts_608.txt#L267) | 70490 | Compare the mapped starts at the next `R/C/0010` extension. | 597 · `R/C/0010` at 65,248 | 257 (B mirrored), 427 (D mirrored) |
| 227 | [298](BB6_holdouts_608.txt#L298) | 79009 | Compare the mapped starts at the next `L/A/0010` extension. | 626 · `L/A/0010` at 65,188 | 249 (C mirrored), 340 (D) |
| 228 | [326](BB6_holdouts_608.txt#L326) | 91503 | Compare the mapped starts at the next `L/A/1110` extension. | 460 · `L/A/1110` at 65,211 | 174 (B mirrored), 604 (D) |
| 229 | [333](BB6_holdouts_608.txt#L333) | 93836 | Compare the mapped starts at the next `R/C/0010` extension. | 585 · `R/C/0010` at 65,198 | 32 (D mirrored), 170 (B mirrored) |
| 230 | [334](BB6_holdouts_608.txt#L334) | 94115 | Compare the mapped starts at the next `L/A/0010` extension. | 623 · `L/A/0010` at 65,306 | 68 (D), 97 (C mirrored) |
| 231 | [335](BB6_holdouts_608.txt#L335) | 95020 | Compare the mapped starts at the next `L/A/0010` extension. | 623 · `L/A/0010` at 65,258 | 468 (C mirrored), 474 (D) |
| 232 | [338](BB6_holdouts_608.txt#L338) | 95740 | Compare the mapped starts at the next `L/A/0010` extension. | 608 · `L/A/0010` at 65,372 | 71 (D), 105 (C mirrored) |
| 233 | [340](BB6_holdouts_608.txt#L340) | 95904 | Compare the mapped starts at the next `L/D/0010` extension. | 567 · `L/D/0010` at 64,867 | 249 (E mirrored), 298 (C) |
| 234 | [346](BB6_holdouts_608.txt#L346) | 97237 | Compare the mapped starts at the next `L/D/0010` extension. | 567 · `L/D/0010` at 64,869 | 480 (C), 550 (E mirrored) |
| 235 | [349](BB6_holdouts_608.txt#L349) | 97509 | Compare the mapped starts at the next `R/C/0100` extension. | 359 · `R/C/0100` at 64,953 | 150 (D mirrored), 160 (C mirrored) |
| 236 | [359](BB6_holdouts_608.txt#L359) | 99697 | Compare the mapped starts at the next `L/D/0010` extension. | 631 · `L/D/0010` at 64,698 | 580 (E mirrored), 586 (C) |
| 237 | [367](BB6_holdouts_608.txt#L367) | 102105 | Compare the mapped starts at the next `R/B/1101` extension. | 342 · `R/B/1101` at 54,571 | 114 (D), 378 (B mirrored) |
| 238 | [372](BB6_holdouts_608.txt#L372) | 103931 | Compare the mapped starts at the next `L/A/1111` extension. | 503 · `L/A/1111` at 65,058 | 109 (B mirrored), 572 (B) |
| 239 | [381](BB6_holdouts_608.txt#L381) | 106698 | Compare the mapped starts at the next `R/B/1100` extension. | 493 · `R/B/1100` at 64,628 | 65 (B), 590 (D) |
| 240 | [403](BB6_holdouts_608.txt#L403) | 114051 | Compare the mapped starts at the next `R/C/0010` extension. | 600 · `R/C/0010` at 65,027 | 78 (E mirrored), 408 (D mirrored) |
| 241 | [408](BB6_holdouts_608.txt#L408) | 115768 | Compare the mapped starts at the next `L/A/0010` extension. | 626 · `L/A/0010` at 64,992 | 78 (C), 403 (C mirrored) |
| 242 | [427](BB6_holdouts_608.txt#L427) | 123261 | Compare the mapped starts at the next `L/A/0010` extension. | 623 · `L/A/0010` at 65,279 | 257 (D), 267 (C mirrored) |
| 243 | [440](BB6_holdouts_608.txt#L440) | 126070 | Compare the mapped starts at the next `R/C/1100` extension. | 373 · `R/C/1100` at 65,443 | 12 (C), 84 (B mirrored) |
| 244 | [443](BB6_holdouts_608.txt#L443) | 126204 | Compare the mapped starts at the next `L/A/1101` extension. | 558 · `L/A/1101` at 65,176 | 252 (B mirrored), 557 (C mirrored) |
| 245 | [468](BB6_holdouts_608.txt#L468) | 132708 | Compare the mapped starts at the next `R/C/0010` extension. | 597 · `R/C/0010` at 65,267 | 335 (D mirrored), 474 (B mirrored) |
| 246 | [474](BB6_holdouts_608.txt#L474) | 134083 | Compare the mapped starts at the next `L/D/0010` extension. | 555 · `L/D/0010` at 65,223 | 335 (C), 468 (E mirrored) |
| 247 | [480](BB6_holdouts_608.txt#L480) | 136458 | Compare the mapped starts at the next `L/A/0010` extension. | 626 · `L/A/0010` at 65,190 | 346 (D), 550 (C mirrored) |
| 248 | [541](BB6_holdouts_608.txt#L541) | 156951 | Compare the mapped starts at the next `R/C/0010` extension. | 650 · `R/C/0010` at 65,270 | 52 (B mirrored), 263 (D mirrored) |
| 249 | [550](BB6_holdouts_608.txt#L550) | 159639 | Compare the mapped starts at the next `R/C/0010` extension. | 600 · `R/C/0010` at 65,345 | 346 (B mirrored), 480 (D mirrored) |
| 250 | [557](BB6_holdouts_608.txt#L557) | 162730 | Compare the mapped starts at the next `R/C/1101` extension. | 542 · `R/C/1101` at 65,382 | 252 (D), 443 (E mirrored) |
| 251 | [572](BB6_holdouts_608.txt#L572) | 167030 | Compare the mapped starts at the next `R/C/1110` extension. | 394 · `R/C/1110` at 65,282 | 109 (D mirrored), 372 (D) |
| 252 | [580](BB6_holdouts_608.txt#L580) | 170624 | Compare the mapped starts at the next `R/C/0010` extension. | 650 · `R/C/0010` at 65,256 | 359 (B mirrored), 586 (D mirrored) |
| 253 | [586](BB6_holdouts_608.txt#L586) | 173562 | Compare the mapped starts at the next `L/A/0010` extension. | 676 · `L/A/0010` at 64,853 | 359 (D), 580 (C mirrored) |
| 254 | [590](BB6_holdouts_608.txt#L590) | 174393 | Compare the mapped starts at the next `R/E/1100` extension. | 499 · `R/E/1100` at 64,900 | 65 (D), 381 (C) |
| 255 | [438](BB6_holdouts_608.txt#L438) | 125786 | Compare the mapped starts at the next `R/C/1110` extension. | 527 · `R/C/1110` at 64,628 | 66 (B), 532 (E) |
| 256 | [556](BB6_holdouts_608.txt#L556) | 162473 | Compare the mapped starts at the next `L/D/1001` extension. | 336 · `L/D/1001` at 65,161 | 237 (B mirrored), 442 (F mirrored) |
| 257 | [114](BB6_holdouts_608.txt#L114) | 29687 | Compare the mapped starts at the next `L/B/0100` extension. | 332 · `L/B/0100` at 64,737 | 367 (E), 378 (F mirrored) |
| 258 | [162](BB6_holdouts_608.txt#L162) | 42815 | Compare the mapped starts at the next `R/D/1011` extension. | 194 · `R/D/1011` at 64,893 | 202 (E mirrored), 477 (F) |
| 259 | [364](BB6_holdouts_608.txt#L364) | 101395 | Compare the mapped starts at the next `R/B/0110` extension. | 325 · `R/B/0110` at 65,508 | 380 (C mirrored), 521 (B mirrored) |
| 260 | [477](BB6_holdouts_608.txt#L477) | 135173 | Compare the mapped starts at the next `R/B/1011` extension. | 200 · `R/B/1011` at 64,259 | 162 (C), 202 (C mirrored) |
| 261 | [37](BB6_holdouts_608.txt#L37) | 10442 | Compare the mapped starts at the next `R/B/1010` extension. | 332 · `R/B/1010` at 59,741 | 25 (D mirrored), 336 (B mirrored) |
| 262 | [90](BB6_holdouts_608.txt#L90) | 24506 | Compare the mapped starts at the next `R/C/0100` extension. | 293 · `R/C/0100` at 64,960 | 203 (F mirrored), 292 (F mirrored) |
| 263 | [174](BB6_holdouts_608.txt#L174) | 46435 | Compare the mapped starts at the next `R/B/1110` extension. | 411 · `R/B/1110` at 64,464 | 326 (D mirrored), 604 (C mirrored) |
| 264 | [178](BB6_holdouts_608.txt#L178) | 48565 | Compare the mapped starts at the next `L/A/0100` extension. | 283 · `L/A/0100` at 65,018 | 205 (C mirrored), 491 (E) |
| 265 | [205](BB6_holdouts_608.txt#L205) | 55079 | Compare the mapped starts at the next `R/C/0100` extension. | 291 · `R/C/0100` at 64,334 | 178 (F mirrored), 491 (F mirrored) |
| 266 | [336](BB6_holdouts_608.txt#L336) | 95029 | Compare the mapped starts at the next `L/C/1010` extension. | 302 · `L/C/1010` at 56,971 | 25 (C), 37 (E mirrored) |
| 267 | [378](BB6_holdouts_608.txt#L378) | 105641 | Compare the mapped starts at the next `R/D/0100` extension. | 302 · `R/D/0100` at 64,849 | 114 (C mirrored), 367 (B mirrored) |
| 268 | [380](BB6_holdouts_608.txt#L380) | 105740 | Compare the mapped starts at the next `R/C/1101` extension. | 316 · `R/C/1101` at 65,455 | 364 (B mirrored), 521 (C) |
| 269 | [521](BB6_holdouts_608.txt#L521) | 149962 | Compare the mapped starts at the next `R/B/1101` extension. | 336 · `R/B/1101` at 65,472 | 364 (C mirrored), 380 (B) |
| 270 | [546](BB6_holdouts_608.txt#L546) | 157718 | Compare the mapped starts at the next `R/C/1111` extension. | 358 · `R/C/1111` at 63,271 | 210 (C mirrored), 439 (B) |
| 271 | [202](BB6_holdouts_608.txt#L202) | 54596 | Compare the mapped starts at the next `L/F/1011` extension. | 170 · `L/F/1011` at 65,236 | 162 (E mirrored), 477 (D mirrored) |
| 272 | [285](BB6_holdouts_608.txt#L285) | 75094 | Compare the mapped starts at the next `R/C/1101` extension. | 184 · `R/C/1101` at 61,497 | 362 (E), 561 (C mirrored) |
| 273 | [362](BB6_holdouts_608.txt#L362) | 100684 | Compare the mapped starts at the next `L/D/1010` extension. | 178 · `L/D/1010` at 55,775 | 285 (B), 561 (E mirrored) |
| 274 | [203](BB6_holdouts_608.txt#L203) | 54866 | Compare the mapped starts at the next `L/E/0101` extension. | 308 · `L/E/0101` at 65,163 | 90 (D mirrored), 292 (D) |
| 275 | [292](BB6_holdouts_608.txt#L292) | 76942 | Compare the mapped starts at the next `L/C/0101` extension. | 298 · `L/C/0101` at 63,961 | 90 (F mirrored), 203 (C) |
| 276 | [491](BB6_holdouts_608.txt#L491) | 139962 | Compare the mapped starts at the next `L/E/0101` extension. | 292 · `L/E/0101` at 64,593 | 178 (B), 205 (D mirrored) |
| 277 | [553](BB6_holdouts_608.txt#L553) | 160345 | Compare the mapped starts at the next `R/D/1011` extension. | 261 · `R/D/1011` at 57,635 | 161 (D), 562 (B) |
| 278 | [562](BB6_holdouts_608.txt#L562) | 164391 | Compare the mapped starts at the next `R/E/1011` extension. | 261 · `R/E/1011` at 58,877 | 161 (C), 553 (E) |
| 279 | [576](BB6_holdouts_608.txt#L576) | 168752 | Compare the mapped starts at the next `L/C/1101` extension. | 287 · `L/C/1101` at 64,683 | 46 (F mirrored), 526 (F mirrored) |
| 280 | [604](BB6_holdouts_608.txt#L604) | 180438 | Compare the mapped starts at the next `L/D/1110` extension. | 435 · `L/D/1110` at 65,421 | 174 (C mirrored), 326 (B) |
| 281 | [210](BB6_holdouts_608.txt#L210) | 56722 | Compare the mapped starts at the next `L/E/1111` extension. | 287 · `L/E/1111` at 63,570 | 439 (E mirrored), 546 (D mirrored) |
| 282 | [234](BB6_holdouts_608.txt#L234) | 65352 | Compare the mapped starts at the next `R/C/1111` extension. | 400 · `R/C/1111` at 64,966 | 290 (C mirrored), 418 (E) |
| 283 | [439](BB6_holdouts_608.txt#L439) | 126068 | Compare the mapped starts at the next `L/A/1101` extension. | 289 · `L/A/1101` at 64,883 | 210 (B mirrored), 546 (E) |
| 284 | [532](BB6_holdouts_608.txt#L532) | 154101 | Compare the mapped starts at the next `L/C/1011` extension. | 121 · `L/C/1011` at 62,170 | 66 (C), 438 (B) |
| 285 | [561](BB6_holdouts_608.txt#L561) | 164326 | Compare the mapped starts at the next `R/B/1010` extension. | 192 · `R/B/1010` at 60,415 | 285 (D mirrored), 362 (C mirrored) |
| 286 | [582](BB6_holdouts_608.txt#L582) | 172498 | Compare the mapped starts at the next `L/D/0010` extension. | 513 · `L/D/0010` at 64,501 | 232 (E mirrored), 347 (C) |
| 287 | [161](BB6_holdouts_608.txt#L161) | 42170 | Compare the mapped starts at the next `L/C/0110` extension. | 283 · `L/C/0110` at 65,494 | 553 (C), 562 (D) |
| 288 | [66](BB6_holdouts_608.txt#L66) | 18358 | Compare the mapped starts at the next `R/D/1110` extension. | 198 · `R/D/1110` at 55,081 | 438 (E), 532 (D) |
| 289 | [526](BB6_holdouts_608.txt#L526) | 152108 | Compare the mapped starts at the next `L/E/1101` extension. | 297 · `L/E/1101` at 65,369 | 46 (B), 576 (F mirrored) |
| 290 | [290](BB6_holdouts_608.txt#L290) | 76238 | Compare the mapped starts at the next `L/A/1111` extension. | 376 · `L/A/1111` at 64,889 | 234 (C mirrored), 418 (C mirrored) |
| 291 | [447](BB6_holdouts_608.txt#L447) | 127908 | Compare the mapped starts at the next `R/B/1101` extension. | 417 · `R/B/1101` at 64,556 | 319 (B), 469 (D) |
| 292 | [46](BB6_holdouts_608.txt#L46) | 12600 | Compare the mapped starts at the next `L/A/1111` extension. | 303 · `L/A/1111` at 65,534 | 526 (E), 576 (E mirrored) |
| 293 | [319](BB6_holdouts_608.txt#L319) | 88925 | Compare the mapped starts at the next `L/E/0101` extension. | 429 · `L/E/0101` at 62,882 | 447 (F), 469 (C) |
| 294 | [469](BB6_holdouts_608.txt#L469) | 132972 | Compare the mapped starts at the next `R/E/1101` extension. | 431 · `R/E/1101` at 64,134 | 319 (E), 447 (D) |
| 295 | [129](BB6_holdouts_608.txt#L129) | 34042 | Compare the mapped starts at the next `R/E/1010` extension. | 321 · `R/E/1010` at 65,482 | 465 (B mirrored) |
| 296 | [465](BB6_holdouts_608.txt#L465) | 132224 | Compare the mapped starts at the next `L/A/1010` extension. | 296 · `L/A/1010` at 65,453 | 129 (E mirrored) |
| 297 | [13](BB6_holdouts_608.txt#L13) | 3389 | Compare the mapped starts at the next `L/D/1111` extension. | 247 · `L/D/1111` at 65,226 | 243 (C mirrored) |
| 298 | [77](BB6_holdouts_608.txt#L77) | 21494 | Compare the mapped starts at the next `L/F/1010` extension. | 326 · `L/F/1010` at 63,658 | 498 (D mirrored) |
| 299 | [113](BB6_holdouts_608.txt#L113) | 29537 | Compare the mapped starts at the next `R/C/0101` extension. | 454 · `R/C/0101` at 65,254 | 453 (D mirrored) |
| 300 | [132](BB6_holdouts_608.txt#L132) | 34590 | Compare the mapped starts at the next `L/C/1010` extension. | 559 · `L/C/1010` at 65,423 | 143 (C mirrored) |
| 301 | [165](BB6_holdouts_608.txt#L165) | 44149 | Compare the mapped starts at the next `L/C/0100` extension. | 504 · `L/C/0100` at 64,860 | 373 (B) |
| 302 | [243](BB6_holdouts_608.txt#L243) | 66567 | Compare the mapped starts at the next `R/F/1111` extension. | 241 · `R/F/1111` at 64,998 | 13 (E mirrored) |
| 303 | [299](BB6_holdouts_608.txt#L299) | 79385 | Compare the mapped starts at the next `R/F/1010` extension. | 547 · `R/F/1010` at 65,387 | 357 (C) |
| 304 | [315](BB6_holdouts_608.txt#L315) | 87181 | Compare the mapped starts at the next `L/A/1101` extension. | 328 · `L/A/1101` at 64,611 | 141 (E mirrored) |
| 305 | [324](BB6_holdouts_608.txt#L324) | 91338 | Compare the mapped starts at the next `L/A/1010` extension. | 486 · `L/A/1010` at 65,055 | 152 (E) |
| 306 | [453](BB6_holdouts_608.txt#L453) | 129771 | Compare the mapped starts at the next `L/C/0101` extension. | 446 · `L/C/0101` at 65,235 | 113 (D mirrored) |
| 307 | [80](BB6_holdouts_608.txt#L80) | 21851 | Compare the mapped starts at the next `L/F/0101` extension. | 506 · `L/F/0101` at 65,457 | 270 (D) |
| 308 | [108](BB6_holdouts_608.txt#L108) | 27795 | Compare the mapped starts at the next `R/B/1101` extension. | 145 · `R/B/1101` at 45,759 | 163 (D) |
| 309 | [116](BB6_holdouts_608.txt#L116) | 29825 | Compare the mapped starts at the next `R/B/1010` extension. | 456 · `R/B/1010` at 65,012 | 513 (F mirrored) |
| 310 | [141](BB6_holdouts_608.txt#L141) | 36703 | Compare the mapped starts at the next `R/E/1101` extension. | 330 · `R/E/1101` at 64,914 | 315 (D mirrored) |
| 311 | [172](BB6_holdouts_608.txt#L172) | 45361 | Compare the mapped starts at the next `L/E/0110` extension. | 374 · `L/E/0110` at 65,492 | 311 (D mirrored) |
| 312 | [201](BB6_holdouts_608.txt#L201) | 54516 | Compare the mapped starts at the next `L/A/0010` extension. | 575 · `L/A/0010` at 65,513 | 505 (D) |
| 313 | [216](BB6_holdouts_608.txt#L216) | 59221 | Compare the mapped starts at the next `L/D/0010` extension. | 631 · `L/D/0010` at 64,720 | 219 (E mirrored) |
| 314 | [219](BB6_holdouts_608.txt#L219) | 59893 | Compare the mapped starts at the next `R/C/0010` extension. | 650 · `R/C/0010` at 65,268 | 216 (B mirrored) |
| 315 | [270](BB6_holdouts_608.txt#L270) | 71111 | Compare the mapped starts at the next `L/F/0101` extension. | 503 · `L/F/0101` at 64,729 | 80 (B) |
| 316 | [277](BB6_holdouts_608.txt#L277) | 72232 | Compare the mapped starts at the next `L/D/0011` extension. | 78 · `L/D/0011` at 35,759 | 190 (B) |
| 317 | [281](BB6_holdouts_608.txt#L281) | 73584 | Compare the mapped starts at the next `R/B/1110` extension. | 514 · `R/B/1110` at 64,938 | 454 (B mirrored) |
| 318 | [301](BB6_holdouts_608.txt#L301) | 81504 | Compare the mapped starts at the next `R/B/1111` extension. | 307 · `R/B/1111` at 65,355 | 329 (D mirrored) |
| 319 | [329](BB6_holdouts_608.txt#L329) | 92364 | Compare the mapped starts at the next `L/E/1111` extension. | 306 · `L/E/1111` at 65,045 | 301 (C mirrored) |
| 320 | [373](BB6_holdouts_608.txt#L373) | 104106 | Compare the mapped starts at the next `L/A/0100` extension. | 421 · `L/A/0100` at 65,280 | 165 (C) |
| 321 | [398](BB6_holdouts_608.txt#L398) | 112769 | Compare the mapped starts at the next `L/C/1011` extension. | 467 · `L/C/1011` at 64,710 | 530 (C mirrored) |
| 322 | [406](BB6_holdouts_608.txt#L406) | 114464 | Compare the mapped starts at the next `L/A/0010` extension. | 608 · `L/A/0010` at 65,434 | 575 (D) |
| 323 | [454](BB6_holdouts_608.txt#L454) | 129887 | Compare the mapped starts at the next `R/B/1111` extension. | 437 · `R/B/1111` at 63,083 | 281 (C mirrored) |
| 324 | [513](BB6_holdouts_608.txt#L513) | 147837 | Compare the mapped starts at the next `L/A/1010` extension. | 455 · `L/A/1010` at 64,977 | 116 (B mirrored) |
| 325 | [530](BB6_holdouts_608.txt#L530) | 152969 | Compare the mapped starts at the next `R/B/1011` extension. | 435 · `R/B/1011` at 65,355 | 398 (B mirrored) |
| 326 | [534](BB6_holdouts_608.txt#L534) | 154700 | Compare the mapped starts at the next `L/A/1110` extension. | 345 · `L/A/1110` at 63,799 | 224 (C mirrored) |
| 327 | [535](BB6_holdouts_608.txt#L535) | 154944 | Compare the mapped starts at the next `L/A/1010` extension. | 633 · `L/A/1010` at 65,190 | 7 (E mirrored) |
| 328 | [575](BB6_holdouts_608.txt#L575) | 168729 | Compare the mapped starts at the next `L/D/0010` extension. | 543 · `L/D/0010` at 65,341 | 406 (C) |
| 329 | [222](BB6_holdouts_608.txt#L222) | 60438 | Compare the mapped starts at the next `R/D/1111` extension. | 513 · `R/D/1111` at 64,936 | 31 (B mirrored) |
| 330 | [393](BB6_holdouts_608.txt#L393) | 111043 | Compare the mapped starts at the next `L/F/1101` extension. | 508 · `L/F/1101` at 64,326 | 295 (E) |
| 331 | [472](BB6_holdouts_608.txt#L472) | 133770 | Compare the mapped starts at the next `R/C/1101` extension. | 108 · `R/C/1101` at 43,742 | 151 (F) |
| 332 | [33](BB6_holdouts_608.txt#L33) | 9146 | Compare the mapped starts at the next `L/A/1110` extension. | 401 · `L/A/1110` at 65,134 | 39 (D mirrored) |
| 333 | [39](BB6_holdouts_608.txt#L39) | 10681 | Compare the mapped starts at the next `R/D/1110` extension. | 405 · `R/D/1110` at 63,880 | 33 (B mirrored) |
| 334 | [79](BB6_holdouts_608.txt#L79) | 21606 | Compare the mapped starts at the next `R/C/0111` extension. | 89 · `R/C/0111` at 48,518 | 282 (B mirrored) |
| 335 | [143](BB6_holdouts_608.txt#L143) | 37222 | Compare the mapped starts at the next `R/B/1010` extension. | 604 · `R/B/1010` at 65,077 | 132 (B mirrored) |
| 336 | [149](BB6_holdouts_608.txt#L149) | 39050 | Compare the mapped starts at the next `L/E/1111` extension. | 356 · `L/E/1111` at 64,926 | 328 (C mirrored) |
| 337 | [151](BB6_holdouts_608.txt#L151) | 39952 | Compare the mapped starts at the next `R/B/1101` extension. | 92 · `R/B/1101` at 59,855 | 472 (B) |
| 338 | [224](BB6_holdouts_608.txt#L224) | 60575 | Compare the mapped starts at the next `L/D/1010` extension. | 311 · `L/D/1010` at 64,273 | 534 (D mirrored) |
| 339 | [282](BB6_holdouts_608.txt#L282) | 74449 | Compare the mapped starts at the next `L/E/0111` extension. | 89 · `L/E/0111` at 52,572 | 79 (D mirrored) |
| 340 | [328](BB6_holdouts_608.txt#L328) | 92170 | Compare the mapped starts at the next `R/B/1111` extension. | 344 · `R/B/1111` at 63,333 | 149 (D mirrored) |
| 341 | [352](BB6_holdouts_608.txt#L352) | 98225 | Compare the mapped starts at the next `R/B/1111` extension. | 67 · `R/B/1111` at 43,642 | 493 (C) |
| 342 | [357](BB6_holdouts_608.txt#L357) | 99408 | Compare the mapped starts at the next `R/B/1010` extension. | 495 · `R/B/1010` at 65,455 | 299 (E) |
| 343 | [386](BB6_holdouts_608.txt#L386) | 108051 | Compare the mapped starts at the next `R/E/1111` extension. | 122 · `R/E/1111` at 64,855 | 487 (C) |
| 344 | [450](BB6_holdouts_608.txt#L450) | 128426 | Compare the mapped starts at the next `L/C/0111` extension. | 150 · `L/C/0111` at 58,504 | 555 (E mirrored) |
| 345 | [493](BB6_holdouts_608.txt#L493) | 140108 | Compare the mapped starts at the next `R/D/1111` extension. | 66 · `R/D/1111` at 51,369 | 352 (F) |
| 346 | [555](BB6_holdouts_608.txt#L555) | 162010 | Compare the mapped starts at the next `R/D/0111` extension. | 116 · `R/D/0111` at 61,949 | 450 (D mirrored) |
| 347 | [147](BB6_holdouts_608.txt#L147) | 38215 | Compare the mapped starts at the next `L/C/0011` extension. | 66 · `L/C/0011` at 35,192 | 394 (C) |
| 348 | [163](BB6_holdouts_608.txt#L163) | 43527 | Compare the mapped starts at the next `R/E/1101` extension. | 129 · `R/E/1101` at 44,808 | 108 (F) |
| 349 | [240](BB6_holdouts_608.txt#L240) | 66058 | Compare the mapped starts at the next `L/D/1110` extension. | 411 · `L/D/1110` at 63,030 | 592 (B mirrored) |
| 350 | [259](BB6_holdouts_608.txt#L259) | 69417 | Compare the mapped starts at the next `R/D/1111` extension. | 158 · `R/D/1111` at 61,498 | 578 (F) |
| 351 | [306](BB6_holdouts_608.txt#L306) | 83065 | Compare the mapped starts at the next `R/C/1010` extension. | 509 · `R/C/1010` at 65,452 | 461 (B mirrored) |
| 352 | [311](BB6_holdouts_608.txt#L311) | 85142 | Compare the mapped starts at the next `R/C/0110` extension. | 375 · `R/C/0110` at 64,594 | 172 (C mirrored) |
| 353 | [437](BB6_holdouts_608.txt#L437) | 125689 | Compare the mapped starts at the next `L/A/0110` extension. | 349 · `L/A/0110` at 65,188 | 501 (D) |
| 354 | [455](BB6_holdouts_608.txt#L455) | 129932 | Compare the mapped starts at the next `L/A/1101` extension. | 379 · `L/A/1101` at 65,206 | 98 (B mirrored) |
| 355 | [461](BB6_holdouts_608.txt#L461) | 131775 | Compare the mapped starts at the next `L/D/1010` extension. | 527 · `L/D/1010` at 65,153 | 306 (D mirrored) |
| 356 | [501](BB6_holdouts_608.txt#L501) | 144461 | Compare the mapped starts at the next `L/D/0110` extension. | 340 · `L/D/0110` at 64,541 | 437 (D) |
| 357 | [592](BB6_holdouts_608.txt#L592) | 175040 | Compare the mapped starts at the next `R/D/1110` extension. | 402 · `R/D/1110` at 62,455 | 240 (C mirrored) |
| 358 | [152](BB6_holdouts_608.txt#L152) | 40254 | Compare the mapped starts at the next `L/E/1010` extension. | 514 · `L/E/1010` at 65,525 | 324 (B) |
| 359 | [519](BB6_holdouts_608.txt#L519) | 149506 | Compare the mapped starts at the next `L/A/1010` extension. | 297 · `L/A/1010` at 65,518 | 376 (D mirrored) |
| 360 | [588](BB6_holdouts_608.txt#L588) | 173888 | Compare the mapped starts at the next `L/D/1101` extension. | 394 · `L/D/1101` at 65,438 | 20 (F) |
| 361 | [597](BB6_holdouts_608.txt#L597) | 176216 | Compare the mapped starts at the next `L/C/0111` extension. | 355 · `L/C/0111` at 65,330 | 67 (B) |
| 362 | [67](BB6_holdouts_608.txt#L67) | 18397 | Compare the mapped starts at the next `R/C/1110` extension. | 367 · `R/C/1110` at 65,358 | 597 (C) |
| 363 | [274](BB6_holdouts_608.txt#L274) | 71717 | Compare the mapped starts at the next `L/A/1010` extension. | 465 · `L/A/1010` at 64,490 | 518 (D mirrored) |
| 364 | [318](BB6_holdouts_608.txt#L318) | 87823 | Compare the mapped starts at the next `R/D/1011` extension. | 491 · `R/D/1011` at 64,173 | 322 (E) |
| 365 | [322](BB6_holdouts_608.txt#L322) | 89727 | Compare the mapped starts at the next `R/B/1010` extension. | 465 · `R/B/1010` at 64,476 | 318 (C) |
| 366 | [506](BB6_holdouts_608.txt#L506) | 145349 | Compare the mapped starts at the next `L/D/0111` extension. | 88 · `L/D/0111` at 45,734 | 547 (B) |
| 367 | [510](BB6_holdouts_608.txt#L510) | 147121 | Compare the mapped starts at the next `R/F/0111` extension. | 618 · `R/F/0111` at 65,396 | 184 (F mirrored) |
| 368 | [518](BB6_holdouts_608.txt#L518) | 149064 | Compare the mapped starts at the next `R/D/1011` extension. | 491 · `R/D/1011` at 64,173 | 274 (B mirrored) |
| 369 | [547](BB6_holdouts_608.txt#L547) | 158007 | Compare the mapped starts at the next `L/A/0111` extension. | 86 · `L/A/0111` at 45,677 | 506 (D) |
| 370 | [20](BB6_holdouts_608.txt#L20) | 5380 | Compare the mapped starts at the next `L/C/1010` extension. | 398 · `L/C/1010` at 64,840 | 588 (B) |
| 371 | [31](BB6_holdouts_608.txt#L31) | 9123 | Compare the mapped starts at the next `R/D/0001` extension. | 445 · `R/D/0001` at 63,319 | 222 (D mirrored) |
| 372 | [98](BB6_holdouts_608.txt#L98) | 25733 | Compare the mapped starts at the next `R/B/1010` extension. | 400 · `R/B/1010` at 64,973 | 455 (F mirrored) |
| 373 | [190](BB6_holdouts_608.txt#L190) | 51101 | Compare the mapped starts at the next `L/A/0011` extension. | 71 · `L/A/0011` at 55,700 | 277 (D) |
| 374 | [363](BB6_holdouts_608.txt#L363) | 100726 | Compare the mapped starts at the next `L/F/0001` extension. | 268 · `L/F/0001` at 63,918 | 560 (C mirrored) |
| 375 | [394](BB6_holdouts_608.txt#L394) | 111363 | Compare the mapped starts at the next `L/A/0011` extension. | 71 · `L/A/0011` at 55,700 | 147 (C) |
| 376 | [487](BB6_holdouts_608.txt#L487) | 139327 | Compare the mapped starts at the next `L/D/0101` extension. | 123 · `L/D/0101` at 63,567 | 386 (D) |
| 377 | [498](BB6_holdouts_608.txt#L498) | 142609 | Compare the mapped starts at the next `L/A/1010` extension. | 325 · `L/A/1010` at 64,342 | 77 (E mirrored) |
| 378 | [560](BB6_holdouts_608.txt#L560) | 163738 | Compare the mapped starts at the next `R/F/0001` extension. | 268 · `R/F/0001` at 64,348 | 363 (D mirrored) |
| 379 | [578](BB6_holdouts_608.txt#L578) | 169745 | Compare the mapped starts at the next `R/B/1111` extension. | 164 · `R/B/1111` at 61,827 | 259 (C) |
| 380 | [384](BB6_holdouts_608.txt#L384) | 107251 | Compare the mapped starts at the next `L/A/1111` extension. | 439 · `L/A/1111` at 64,706 | 431 (B mirrored) |
| 381 | [431](BB6_holdouts_608.txt#L431) | 124153 | Compare the mapped starts at the next `R/B/1111` extension. | 433 · `R/B/1111` at 64,556 | 384 (B mirrored) |
| 382 | [127](BB6_holdouts_608.txt#L127) | 33448 | Compare the mapped starts at the next `L/A/0100` extension. | 216 · `L/A/0100` at 61,739 | 291 (E mirrored) |
| 383 | [291](BB6_holdouts_608.txt#L291) | 76289 | Compare the mapped starts at the next `R/E/0100` extension. | 233 · `R/E/0100` at 62,844 | 127 (E mirrored) |
| 384 | [376](BB6_holdouts_608.txt#L376) | 104920 | Compare the mapped starts at the next `R/D/1010` extension. | 287 · `R/D/1010` at 64,285 | 519 (B mirrored) |
| 385 | [260](BB6_holdouts_608.txt#L260) | 69718 | Compare the mapped starts at the next `L/A/1000` extension. | 277 · `L/A/1000` at 65,358 | 397 (E mirrored) |
| 386 | [295](BB6_holdouts_608.txt#L295) | 78071 | Compare the mapped starts at the next `L/D/1101` extension. | 527 · `L/D/1101` at 65,428 | 393 (C) |
| 387 | [397](BB6_holdouts_608.txt#L397) | 112382 | Compare the mapped starts at the next `L/D/1000` extension. | 224 · `L/D/1000` at 64,980 | 260 (E mirrored) |

## Collect the next edge records

Replay through the last extension shown. Compare the interior tape at the next occurrence of that side, state and four-bit word.

| Rank | Line | Machine ID | First check | Edge records · last signature and step | Other open starts |
|---:|---:|---:|---|---|---|
| 388 | [3](BB6_holdouts_608.txt#L3) | 726 | 1 different signatures in the last 24 records. | 298 · `R/B/1010` at 65,368 | — |
| 389 | [118](BB6_holdouts_608.txt#L118) | 30875 | 1 different signatures in the last 24 records. | 354 · `L/A/1101` at 65,523 | — |
| 390 | [596](BB6_holdouts_608.txt#L596) | 176107 | 1 different signatures in the last 24 records. | 308 · `L/A/1101` at 64,847 | — |
| 391 | [18](BB6_holdouts_608.txt#L18) | 4905 | 2 different signatures in the last 24 records. | 413 · `R/D/1010` at 64,970 | — |
| 392 | [86](BB6_holdouts_608.txt#L86) | 23160 | 2 different signatures in the last 24 records. | 386 · `L/F/1111` at 65,018 | — |
| 393 | [148](BB6_holdouts_608.txt#L148) | 38519 | 2 different signatures in the last 24 records. | 435 · `L/A/1111` at 64,676 | — |
| 394 | [167](BB6_holdouts_608.txt#L167) | 44742 | 2 different signatures in the last 24 records. | 433 · `R/B/1011` at 65,356 | — |
| 395 | [204](BB6_holdouts_608.txt#L204) | 55074 | 2 different signatures in the last 24 records. | 380 · `R/B/1111` at 64,885 | — |
| 396 | [208](BB6_holdouts_608.txt#L208) | 55875 | 2 different signatures in the last 24 records. | 354 · `R/D/1010` at 65,342 | — |
| 397 | [241](BB6_holdouts_608.txt#L241) | 66128 | 2 different signatures in the last 24 records. | 419 · `L/B/1111` at 65,464 | — |
| 398 | [289](BB6_holdouts_608.txt#L289) | 75665 | 2 different signatures in the last 24 records. | 325 · `L/E/1010` at 65,246 | — |
| 399 | [309](BB6_holdouts_608.txt#L309) | 83770 | 2 different signatures in the last 24 records. | 594 · `L/B/1010` at 64,849 | — |
| 400 | [351](BB6_holdouts_608.txt#L351) | 97939 | 2 different signatures in the last 24 records. | 404 · `L/E/0110` at 65,073 | — |
| 401 | [392](BB6_holdouts_608.txt#L392) | 111009 | 2 different signatures in the last 24 records. | 282 · `L/A/0101` at 65,489 | — |
| 402 | [452](BB6_holdouts_608.txt#L452) | 129533 | 2 different signatures in the last 24 records. | 547 · `R/B/1010` at 65,362 | — |
| 403 | [479](BB6_holdouts_608.txt#L479) | 136111 | 2 different signatures in the last 24 records. | 426 · `R/C/0111` at 65,512 | — |
| 404 | [594](BB6_holdouts_608.txt#L594) | 175626 | 2 different signatures in the last 24 records. | 504 · `L/A/1010` at 65,159 | — |
| 405 | [606](BB6_holdouts_608.txt#L606) | 181043 | 2 different signatures in the last 24 records. | 411 · `L/D/1111` at 64,801 | — |
| 406 | [1](BB6_holdouts_608.txt#L1) | 279 | 3 different signatures in the last 24 records. | 557 · `L/C/1101` at 64,296 | — |
| 407 | [45](BB6_holdouts_608.txt#L45) | 12189 | 3 different signatures in the last 24 records. | 407 · `R/B/1011` at 65,264 | — |
| 408 | [157](BB6_holdouts_608.txt#L157) | 41677 | 3 different signatures in the last 24 records. | 315 · `R/B/1111` at 65,491 | — |
| 409 | [196](BB6_holdouts_608.txt#L196) | 53104 | 3 different signatures in the last 24 records. | 72 · `R/B/1111` at 34,183 | — |
| 410 | [213](BB6_holdouts_608.txt#L213) | 58579 | 3 different signatures in the last 24 records. | 588 · `R/C/0010` at 65,533 | — |
| 411 | [231](BB6_holdouts_608.txt#L231) | 65140 | 3 different signatures in the last 24 records. | 70 · `R/B/1111` at 47,955 | — |
| 412 | [239](BB6_holdouts_608.txt#L239) | 65987 | 3 different signatures in the last 24 records. | 275 · `L/D/0101` at 63,221 | — |
| 413 | [246](BB6_holdouts_608.txt#L246) | 67116 | 3 different signatures in the last 24 records. | 70 · `R/B/1111` at 47,352 | — |
| 414 | [262](BB6_holdouts_608.txt#L262) | 69875 | 3 different signatures in the last 24 records. | 366 · `R/D/0100` at 65,085 | — |
| 415 | [265](BB6_holdouts_608.txt#L265) | 70169 | 3 different signatures in the last 24 records. | 62 · `R/B/1111` at 45,727 | — |
| 416 | [276](BB6_holdouts_608.txt#L276) | 72107 | 3 different signatures in the last 24 records. | 600 · `R/C/0010` at 65,025 | — |
| 417 | [356](BB6_holdouts_608.txt#L356) | 99198 | 3 different signatures in the last 24 records. | 371 · `R/D/1111` at 65,393 | — |
| 418 | [404](BB6_holdouts_608.txt#L404) | 114206 | 3 different signatures in the last 24 records. | 72 · `R/B/1111` at 34,183 | — |
| 419 | [407](BB6_holdouts_608.txt#L407) | 114477 | 3 different signatures in the last 24 records. | 62 · `R/B/1111` at 45,723 | — |
| 420 | [466](BB6_holdouts_608.txt#L466) | 132322 | 3 different signatures in the last 24 records. | 68 · `R/B/1111` at 50,354 | — |
| 421 | [529](BB6_holdouts_608.txt#L529) | 152797 | 3 different signatures in the last 24 records. | 83 · `R/B/1111` at 44,191 | — |
| 422 | [549](BB6_holdouts_608.txt#L549) | 159355 | 3 different signatures in the last 24 records. | 417 · `R/C/1010` at 65,396 | — |
| 423 | [563](BB6_holdouts_608.txt#L563) | 164766 | 3 different signatures in the last 24 records. | 676 · `L/A/0010` at 64,867 | — |
| 424 | [4](BB6_holdouts_608.txt#L4) | 1125 | 4 different signatures in the last 24 records. | 370 · `R/C/0101` at 65,000 | — |
| 425 | [16](BB6_holdouts_608.txt#L16) | 4320 | 4 different signatures in the last 24 records. | 78 · `R/C/1111` at 45,726 | — |
| 426 | [74](BB6_holdouts_608.txt#L74) | 21160 | 4 different signatures in the last 24 records. | 232 · `L/C/1100` at 60,100 | — |
| 427 | [130](BB6_holdouts_608.txt#L130) | 34090 | 4 different signatures in the last 24 records. | 485 · `L/A/1111` at 64,995 | — |
| 428 | [159](BB6_holdouts_608.txt#L159) | 41852 | 4 different signatures in the last 24 records. | 139 · `L/E/1111` at 62,714 | — |
| 429 | [193](BB6_holdouts_608.txt#L193) | 52486 | 4 different signatures in the last 24 records. | 535 · `R/E/1011` at 64,027 | — |
| 430 | [197](BB6_holdouts_608.txt#L197) | 53125 | 4 different signatures in the last 24 records. | 295 · `R/B/1000` at 65,261 | — |
| 431 | [273](BB6_holdouts_608.txt#L273) | 71477 | 4 different signatures in the last 24 records. | 308 · `R/C/0101` at 64,886 | — |
| 432 | [411](BB6_holdouts_608.txt#L411) | 116372 | 4 different signatures in the last 24 records. | 282 · `R/D/0000` at 65,100 | — |
| 433 | [436](BB6_holdouts_608.txt#L436) | 125234 | 4 different signatures in the last 24 records. | 124 · `L/A/1101` at 53,437 | — |
| 434 | [457](BB6_holdouts_608.txt#L457) | 130302 | 4 different signatures in the last 24 records. | 373 · `L/C/1111` at 65,492 | — |
| 435 | [482](BB6_holdouts_608.txt#L482) | 137602 | 4 different signatures in the last 24 records. | 316 · `L/A/0110` at 62,944 | — |
| 436 | [500](BB6_holdouts_608.txt#L500) | 144438 | 4 different signatures in the last 24 records. | 576 · `L/E/1111` at 64,923 | — |
| 437 | [504](BB6_holdouts_608.txt#L504) | 144929 | 4 different signatures in the last 24 records. | 438 · `R/C/1101` at 64,232 | — |
| 438 | [509](BB6_holdouts_608.txt#L509) | 147101 | 4 different signatures in the last 24 records. | 352 · `L/F/0101` at 64,998 | — |
| 439 | [515](BB6_holdouts_608.txt#L515) | 148028 | 4 different signatures in the last 24 records. | 117 · `L/A/1101` at 61,391 | — |
| 440 | [554](BB6_holdouts_608.txt#L554) | 161169 | 4 different signatures in the last 24 records. | 105 · `L/A/1101` at 62,135 | — |
| 441 | [2](BB6_holdouts_608.txt#L2) | 696 | 5 different signatures in the last 24 records. | 368 · `L/A/1111` at 65,305 | — |
| 442 | [14](BB6_holdouts_608.txt#L14) | 3919 | 5 different signatures in the last 24 records. | 102 · `L/A/0010` at 65,307 | — |
| 443 | [43](BB6_holdouts_608.txt#L43) | 11545 | 5 different signatures in the last 24 records. | 110 · `R/B/0101` at 62,895 | — |
| 444 | [53](BB6_holdouts_608.txt#L53) | 14216 | 5 different signatures in the last 24 records. | 59 · `L/A/1111` at 45,991 | — |
| 445 | [63](BB6_holdouts_608.txt#L63) | 17826 | 5 different signatures in the last 24 records. | 89 · `L/A/1010` at 58,624 | — |
| 446 | [128](BB6_holdouts_608.txt#L128) | 33818 | 5 different signatures in the last 24 records. | 116 · `R/D/0111` at 58,457 | — |
| 447 | [142](BB6_holdouts_608.txt#L142) | 36869 | 5 different signatures in the last 24 records. | 113 · `L/A/1001` at 51,041 | — |
| 448 | [183](BB6_holdouts_608.txt#L183) | 49767 | 5 different signatures in the last 24 records. | 88 · `L/A/1111` at 53,790 | — |
| 449 | [268](BB6_holdouts_608.txt#L268) | 70770 | 5 different signatures in the last 24 records. | 146 · `L/C/0000` at 62,821 | — |
| 450 | [271](BB6_holdouts_608.txt#L271) | 71252 | 5 different signatures in the last 24 records. | 115 · `L/D/1101` at 62,511 | — |
| 451 | [307](BB6_holdouts_608.txt#L307) | 83189 | 5 different signatures in the last 24 records. | 111 · `R/B/1011` at 53,877 | — |
| 452 | [348](BB6_holdouts_608.txt#L348) | 97431 | 5 different signatures in the last 24 records. | 97 · `L/A/1011` at 60,766 | — |
| 453 | [389](BB6_holdouts_608.txt#L389) | 110453 | 5 different signatures in the last 24 records. | 150 · `L/A/1111` at 60,875 | — |
| 454 | [434](BB6_holdouts_608.txt#L434) | 124869 | 5 different signatures in the last 24 records. | 113 · `R/D/1111` at 51,267 | — |
| 455 | [446](BB6_holdouts_608.txt#L446) | 127566 | 5 different signatures in the last 24 records. | 323 · `R/E/0101` at 65,301 | — |
| 456 | [458](BB6_holdouts_608.txt#L458) | 130321 | 5 different signatures in the last 24 records. | 150 · `L/C/0111` at 61,462 | — |
| 457 | [494](BB6_holdouts_608.txt#L494) | 140963 | 5 different signatures in the last 24 records. | 399 · `L/E/0110` at 65,260 | — |
| 458 | [517](BB6_holdouts_608.txt#L517) | 149024 | 5 different signatures in the last 24 records. | 77 · `R/B/1011` at 65,309 | — |
| 459 | [571](BB6_holdouts_608.txt#L571) | 166820 | 5 different signatures in the last 24 records. | 152 · `L/B/1111` at 59,899 | — |
| 460 | [599](BB6_holdouts_608.txt#L599) | 179721 | 5 different signatures in the last 24 records. | 251 · `L/F/0110` at 50,080 | — |
| 461 | [107](BB6_holdouts_608.txt#L107) | 27281 | 6 different signatures in the last 24 records. | 80 · `R/B/1011` at 60,368 | — |
| 462 | [171](BB6_holdouts_608.txt#L171) | 45336 | 6 different signatures in the last 24 records. | 297 · `R/D/0011` at 63,103 | — |
| 463 | [256](BB6_holdouts_608.txt#L256) | 68492 | 6 different signatures in the last 24 records. | 139 · `R/D/1101` at 64,413 | — |
| 464 | [435](BB6_holdouts_608.txt#L435) | 124880 | 6 different signatures in the last 24 records. | 106 · `R/B/1011` at 59,173 | — |
| 465 | [475](BB6_holdouts_608.txt#L475) | 134427 | 6 different signatures in the last 24 records. | 199 · `L/A/1101` at 64,136 | — |
| 466 | [523](BB6_holdouts_608.txt#L523) | 151599 | 6 different signatures in the last 24 records. | 339 · `R/C/1111` at 63,206 | — |
| 467 | [533](BB6_holdouts_608.txt#L533) | 154458 | 6 different signatures in the last 24 records. | 394 · `L/B/1101` at 64,508 | — |
| 468 | [608](BB6_holdouts_608.txt#L608) | 181655 | 6 different signatures in the last 24 records. | 342 · `L/E/1111` at 63,720 | — |
| 469 | [10](BB6_holdouts_608.txt#L10) | 2968 | 7 different signatures in the last 24 records. | 354 · `L/A/1101` at 65,249 | — |
| 470 | [15](BB6_holdouts_608.txt#L15) | 4176 | 7 different signatures in the last 24 records. | 126 · `R/B/1011` at 47,049 | — |
| 471 | [19](BB6_holdouts_608.txt#L19) | 5088 | 7 different signatures in the last 24 records. | 104 · `L/A/1011` at 48,910 | — |
| 472 | [76](BB6_holdouts_608.txt#L76) | 21414 | 7 different signatures in the last 24 records. | 362 · `L/A/1010` at 65,085 | — |
| 473 | [95](BB6_holdouts_608.txt#L95) | 25604 | 7 different signatures in the last 24 records. | 117 · `L/D/0110` at 64,152 | — |
| 474 | [102](BB6_holdouts_608.txt#L102) | 26127 | 7 different signatures in the last 24 records. | 442 · `L/D/1101` at 65,187 | — |
| 475 | [137](BB6_holdouts_608.txt#L137) | 35717 | 7 different signatures in the last 24 records. | 312 · `L/A/0010` at 64,447 | — |
| 476 | [209](BB6_holdouts_608.txt#L209) | 56057 | 7 different signatures in the last 24 records. | 109 · `L/A/1101` at 46,772 | — |
| 477 | [229](BB6_holdouts_608.txt#L229) | 64598 | 7 different signatures in the last 24 records. | 298 · `L/B/1011` at 63,701 | — |
| 478 | [261](BB6_holdouts_608.txt#L261) | 69753 | 7 different signatures in the last 24 records. | 343 · `L/E/0101` at 64,500 | — |
| 479 | [266](BB6_holdouts_608.txt#L266) | 70273 | 7 different signatures in the last 24 records. | 66 · `L/A/1111` at 60,395 | — |
| 480 | [379](BB6_holdouts_608.txt#L379) | 105737 | 7 different signatures in the last 24 records. | 134 · `R/B/1101` at 64,151 | — |
| 481 | [382](BB6_holdouts_608.txt#L382) | 106785 | 7 different signatures in the last 24 records. | 317 · `L/A/0111` at 61,735 | — |
| 482 | [388](BB6_holdouts_608.txt#L388) | 110152 | 7 different signatures in the last 24 records. | 281 · `L/A/1010` at 65,413 | — |
| 483 | [444](BB6_holdouts_608.txt#L444) | 126530 | 7 different signatures in the last 24 records. | 141 · `R/B/1001` at 64,531 | — |
| 484 | [484](BB6_holdouts_608.txt#L484) | 138104 | 7 different signatures in the last 24 records. | 385 · `L/D/0101` at 65,479 | — |
| 485 | [499](BB6_holdouts_608.txt#L499) | 143478 | 7 different signatures in the last 24 records. | 349 · `L/E/1111` at 65,092 | — |
| 486 | [41](BB6_holdouts_608.txt#L41) | 10753 | 8 different signatures in the last 24 records. | 350 · `L/E/0010` at 64,543 | — |
| 487 | [50](BB6_holdouts_608.txt#L50) | 13552 | 8 different signatures in the last 24 records. | 302 · `L/A/0101` at 62,645 | — |
| 488 | [294](BB6_holdouts_608.txt#L294) | 77933 | 8 different signatures in the last 24 records. | 157 · `R/D/0011` at 60,391 | — |
| 489 | [316](BB6_holdouts_608.txt#L316) | 87199 | 8 different signatures in the last 24 records. | 367 · `R/B/1010` at 65,497 | — |
| 490 | [344](BB6_holdouts_608.txt#L344) | 96840 | 8 different signatures in the last 24 records. | 155 · `L/E/0111` at 62,700 | — |
| 491 | [360](BB6_holdouts_608.txt#L360) | 100124 | 8 different signatures in the last 24 records. | 318 · `L/D/0100` at 59,620 | — |
| 492 | [365](BB6_holdouts_608.txt#L365) | 101586 | 8 different signatures in the last 24 records. | 141 · `L/A/1001` at 62,971 | — |
| 493 | [420](BB6_holdouts_608.txt#L420) | 120990 | 8 different signatures in the last 24 records. | 443 · `R/B/0101` at 65,534 | — |
| 494 | [579](BB6_holdouts_608.txt#L579) | 170561 | 8 different signatures in the last 24 records. | 159 · `L/E/0111` at 51,936 | — |
| 495 | [583](BB6_holdouts_608.txt#L583) | 172963 | 8 different signatures in the last 24 records. | 375 · `L/C/1010` at 64,983 | — |
| 496 | [585](BB6_holdouts_608.txt#L585) | 173433 | 8 different signatures in the last 24 records. | 325 · `L/B/0110` at 62,680 | — |
| 497 | [589](BB6_holdouts_608.txt#L589) | 174142 | 8 different signatures in the last 24 records. | 288 · `R/D/1011` at 64,799 | — |
| 498 | [601](BB6_holdouts_608.txt#L601) | 180047 | 8 different signatures in the last 24 records. | 320 · `L/A/0011` at 64,957 | — |
| 499 | [29](BB6_holdouts_608.txt#L29) | 8805 | 9 different signatures in the last 24 records. | 368 · `R/E/1010` at 64,342 | — |
| 500 | [111](BB6_holdouts_608.txt#L111) | 28668 | 9 different signatures in the last 24 records. | 360 · `L/F/1101` at 65,082 | — |
| 501 | [119](BB6_holdouts_608.txt#L119) | 31128 | 9 different signatures in the last 24 records. | 307 · `L/A/1001` at 64,084 | — |
| 502 | [155](BB6_holdouts_608.txt#L155) | 40644 | 9 different signatures in the last 24 records. | 143 · `R/B/0111` at 64,324 | — |
| 503 | [254](BB6_holdouts_608.txt#L254) | 68273 | 9 different signatures in the last 24 records. | 173 · `L/A/1010` at 64,596 | — |
| 504 | [511](BB6_holdouts_608.txt#L511) | 147183 | 9 different signatures in the last 24 records. | 148 · `R/B/1111` at 65,302 | — |
| 505 | [531](BB6_holdouts_608.txt#L531) | 153488 | 9 different signatures in the last 24 records. | 397 · `R/B/1101` at 65,471 | — |
| 506 | [605](BB6_holdouts_608.txt#L605) | 180739 | 9 different signatures in the last 24 records. | 639 · `R/B/1110` at 64,706 | — |
| 507 | [27](BB6_holdouts_608.txt#L27) | 8646 | 10 different signatures in the last 24 records. | 420 · `R/B/1101` at 65,381 | — |
| 508 | [233](BB6_holdouts_608.txt#L233) | 65208 | 10 different signatures in the last 24 records. | 187 · `L/A/1011` at 64,196 | — |
| 509 | [238](BB6_holdouts_608.txt#L238) | 65980 | 10 different signatures in the last 24 records. | 241 · `R/B/1010` at 58,693 | — |
| 510 | [345](BB6_holdouts_608.txt#L345) | 97059 | 10 different signatures in the last 24 records. | 147 · `L/A/0011` at 65,458 | — |
| 511 | [527](BB6_holdouts_608.txt#L527) | 152404 | 10 different signatures in the last 24 records. | 285 · `L/A/1011` at 63,861 | — |
| 512 | [96](BB6_holdouts_608.txt#L96) | 25624 | 11 different signatures in the last 24 records. | 152 · `R/D/0011` at 63,477 | — |
| 513 | [304](BB6_holdouts_608.txt#L304) | 82729 | 11 different signatures in the last 24 records. | 395 · `L/A/0010` at 64,552 | — |
| 514 | [341](BB6_holdouts_608.txt#L341) | 95916 | 11 different signatures in the last 24 records. | 179 · `L/A/0111` at 59,725 | — |
| 515 | [368](BB6_holdouts_608.txt#L368) | 103399 | 11 different signatures in the last 24 records. | 381 · `L/A/0101` at 52,486 | — |
| 516 | [460](BB6_holdouts_608.txt#L460) | 131324 | 11 different signatures in the last 24 records. | 281 · `L/A/1110` at 63,641 | — |
| 517 | [486](BB6_holdouts_608.txt#L486) | 139325 | 11 different signatures in the last 24 records. | 167 · `L/C/1110` at 63,774 | — |
| 518 | [195](BB6_holdouts_608.txt#L195) | 52729 | 13 different signatures in the last 24 records. | 419 · `R/B/1100` at 64,551 | — |
| 519 | [584](BB6_holdouts_608.txt#L584) | 173393 | 13 different signatures in the last 24 records. | 486 · `L/D/1111` at 65,155 | — |
| 520 | [191](BB6_holdouts_608.txt#L191) | 51276 | 14 different signatures in the last 24 records. | 433 · `L/A/1101` at 65,210 | — |

## Existing campaigns

Coordinate on the [claim board](ROADMAP.md#claim-board). The position shown is where each line would enter the fresh queue if that campaign alone were released.

| Position if released | Line | Machine ID | Campaign | Current proof question |
|---:|---:|---:|---|---|
| 1 | [173](BB6_holdouts_608.txt#L173) | 45924 | BB6-173-REPLAY (claimed) | Check whether the merged upstream `FIBv7.v` theorem applies to ID 45924 from blank A. Match all twelve instructions, replay the kernel proof, and record the proven outcome and attribution. [Rocq TM3.nonhalt](https://github.com/ccz181078/busycoq/blob/33209bc7dc282b38c8cd6be507bfc551fea56108/verify/FIBv7.v#L2678) |
| 1 | [133](BB6_holdouts_608.txt#L133) | 35069 | BB6-133-ODOMETER (claimed) | ID 35069. Match the reflected table to line 581, identify the actual blank-start entry and test whether its odometer reaches F0 or a closed return family. [Sibling proof](https://github.com/ccz181078/busycoq/pull/76) |
| 118 | [110](BB6_holdouts_608.txt#L110) | 28035 | BB6-110-VISIT (claimed) | Decide ID 28035 from blank. Derive its rightward visit rules from its own table and compare them with the three halters in [upstream PR 59](https://github.com/ccz181078/busycoq/pull/59). Determine which input first reaches F1 or find a closed set of safe returns. |

## Verification queue

First cross-check rows with a second theorem source, then review proposed decisions, reported simulation halts and proposed equivalences. Within each group, prefer sources covering more pending rows so one checkout can serve several machines. Ties go to the earliest line in the source batch, then the permanent line.

| Review rank | Line | Machine ID | Register status | Evidence to check |
|---:|---:|---:|---|---|
| 1 | [528](BB6_holdouts_608.txt#L528) | 152765 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/44) · [Lean nonhalting theorem](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/NonHalt/M_1RB1RA_0LC0RA_1RC1LD_0LB1LE_1LF0RC_HHH0LD.lean#L4469) |
| 2 | [28](BB6_holdouts_608.txt#L28) | 8754 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/49) · [Lean halting theorem](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Halt/M_1RB0RE_1RC0RA_0LD0LB_0LA1LE_1LC1LF_0LAHHH.lean#L276) |
| 3 | [430](BB6_holdouts_608.txt#L430) | 124060 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/49) · [Lean halting theorem](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Halt/M_1RB1RF_0RC0RE_0RD1RA_1LE0LA_1LB0LD_0RDHHH.lean#L377) |
| 4 | [177](BB6_holdouts_608.txt#L177) | 48098 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/50) · [Lean nonhalting theorem](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/NonHalt/M_1RB0RA_0RC0LD_1LA1RF_1LE1LD_1LB1RE_HHH1RA.lean#L45) |
| 5 | [574](BB6_holdouts_608.txt#L574) | 168016 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/50) · [Lean nonhalting theorem](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/NonHalt/M_1RB1RA_1RC1LB_0LD0RA_1RF1LE_HHH1LF_1LC0LF.lean#L277) |
| 6 | [207](BB6_holdouts_608.txt#L207) | 55861 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/47) · [Lean halting theorem](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Halt/M_1RB0LC_1LC0RE_1RF1LD_1LA0LB_1RD1RA_1LBHHH.lean#L553) |
| 7 | [512](BB6_holdouts_608.txt#L512) | 147335 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/47) · [Lean halting theorem](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Halt/M_1RB1RC_1LC0LF_1RF0LD_0RE1LB_1RCHHH_1LD0RA.lean#L379) |
| 8 | [94](BB6_holdouts_608.txt#L94) | 25358 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/52) · [Lean nonhalting theorem](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/NonHalt/M_1RB0LC_1LC0RB_0LE0LD_1LCHHH_0RA1LF_1LA1LF.lean#L3882) |
| 9 | [199](BB6_holdouts_608.txt#L199) | 54294 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/53) · [Lean nonhalting theorem](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/NonHalt/M_1RB0RA_0RC0LE_1LD1RF_1LB1RD_1LD1LE_HHH1RA.lean#L6654) |
| 10 | [330](BB6_holdouts_608.txt#L330) | 92633 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/51) · [Lean nonhalting theorem](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/M_1RB0LF_1RC0RA_1LD0RB_0LE0LC_0LA0LC_0LBHHH.lean#L383) |
| 11 | [603](BB6_holdouts_608.txt#L603) | 180313 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/48) · [Lean nonhalting theorem](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/NonHalt/M_1RB0RA_1RC0LC_0LD1RF_1RA1LE_1LD0LB_0REHHH.lean#L2309) |
| 12 | [61](BB6_holdouts_608.txt#L61) | 16925 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/55) |
| 13 | [181](BB6_holdouts_608.txt#L181) | 48815 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/55) |
| 14 | [255](BB6_holdouts_608.txt#L255) | 68358 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/55) |
| 15 | [278](BB6_holdouts_608.txt#L278) | 72270 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/55) |
| 16 | [343](BB6_holdouts_608.txt#L343) | 96519 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/55) |
| 17 | [374](BB6_holdouts_608.txt#L374) | 104518 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/55) |
| 18 | [471](BB6_holdouts_608.txt#L471) | 133258 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/55) |
| 19 | [253](BB6_holdouts_608.txt#L253) | 68184 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/54) |
| 20 | [432](BB6_holdouts_608.txt#L432) | 124651 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/54) |
| 21 | [451](BB6_holdouts_608.txt#L451) | 128933 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/54) |
| 22 | [567](BB6_holdouts_608.txt#L567) | 166072 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/54) |
| 23 | [88](BB6_holdouts_608.txt#L88) | 23933 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/59) |
| 24 | [312](BB6_holdouts_608.txt#L312) | 85227 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/59) |
| 25 | [449](BB6_holdouts_608.txt#L449) | 128126 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/59) |
| 26 | [305](BB6_holdouts_608.txt#L305) | 82928 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/44) |
| 27 | [401](BB6_holdouts_608.txt#L401) | 113677 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/44) |
| 28 | [375](BB6_holdouts_608.txt#L375) | 104840 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/43) |
| 29 | [414](BB6_holdouts_608.txt#L414) | 117456 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/43) |
| 30 | [433](BB6_holdouts_608.txt#L433) | 124655 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/43) |
| 31 | [56](BB6_holdouts_608.txt#L56) | 15252 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/67) |
| 32 | [445](BB6_holdouts_608.txt#L445) | 127123 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/67) |
| 33 | [59](BB6_holdouts_608.txt#L59) | 16554 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/62) |
| 34 | [124](BB6_holdouts_608.txt#L124) | 32304 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/62) |
| 35 | [176](BB6_holdouts_608.txt#L176) | 48016 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/80) |
| 36 | [600](BB6_holdouts_608.txt#L600) | 179725 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/80) |
| 37 | [244](BB6_holdouts_608.txt#L244) | 66704 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/82) |
| 38 | [279](BB6_holdouts_608.txt#L279) | 72859 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/82) |
| 39 | [323](BB6_holdouts_608.txt#L323) | 90097 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/60) |
| 40 | [395](BB6_holdouts_608.txt#L395) | 111805 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/60) |
| 41 | [339](BB6_holdouts_608.txt#L339) | 95765 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/84) |
| 42 | [473](BB6_holdouts_608.txt#L473) | 133909 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/84) |
| 43 | [489](BB6_holdouts_608.txt#L489) | 139727 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/93) |
| 44 | [598](BB6_holdouts_608.txt#L598) | 178401 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/93) |
| 45 | [5](BB6_holdouts_608.txt#L5) | 1309 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/91) |
| 46 | [6](BB6_holdouts_608.txt#L6) | 1965 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/46) |
| 47 | [38](BB6_holdouts_608.txt#L38) | 10642 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/61) |
| 48 | [42](BB6_holdouts_608.txt#L42) | 11019 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/70) |
| 49 | [44](BB6_holdouts_608.txt#L44) | 11596 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/87) |
| 50 | [55](BB6_holdouts_608.txt#L55) | 15053 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/58) |
| 51 | [58](BB6_holdouts_608.txt#L58) | 16113 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/79) |
| 52 | [87](BB6_holdouts_608.txt#L87) | 23376 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/75) |
| 53 | [104](BB6_holdouts_608.txt#L104) | 26463 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/78) |
| 54 | [121](BB6_holdouts_608.txt#L121) | 31480 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/92) |
| 55 | [122](BB6_holdouts_608.txt#L122) | 32070 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/96) |
| 56 | [123](BB6_holdouts_608.txt#L123) | 32161 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/72) |
| 57 | [125](BB6_holdouts_608.txt#L125) | 32641 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/74) |
| 58 | [131](BB6_holdouts_608.txt#L131) | 34517 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/63) |
| 59 | [134](BB6_holdouts_608.txt#L134) | 35160 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/45) |
| 60 | [140](BB6_holdouts_608.txt#L140) | 36670 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/69) |
| 61 | [220](BB6_holdouts_608.txt#L220) | 60274 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/83) |
| 62 | [221](BB6_holdouts_608.txt#L221) | 60424 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/68) |
| 63 | [223](BB6_holdouts_608.txt#L223) | 60498 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/73) |
| 64 | [228](BB6_holdouts_608.txt#L228) | 63822 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/89) |
| 65 | [235](BB6_holdouts_608.txt#L235) | 65692 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/94) |
| 66 | [236](BB6_holdouts_608.txt#L236) | 65826 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/71) |
| 67 | [286](BB6_holdouts_608.txt#L286) | 75248 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/88) |
| 68 | [293](BB6_holdouts_608.txt#L293) | 77294 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/64) |
| 69 | [300](BB6_holdouts_608.txt#L300) | 80070 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/95) |
| 70 | [302](BB6_holdouts_608.txt#L302) | 82139 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/90) |
| 71 | [390](BB6_holdouts_608.txt#L390) | 110703 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/85) |
| 72 | [428](BB6_holdouts_608.txt#L428) | 123390 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/86) |
| 73 | [551](BB6_holdouts_608.txt#L551) | 159749 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/57) |
| 74 | [566](BB6_holdouts_608.txt#L566) | 165799 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/81) |
| 75 | [568](BB6_holdouts_608.txt#L568) | 166286 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/66) |
| 76 | [581](BB6_holdouts_608.txt#L581) | 172044 | `HALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/76) |
| 77 | [607](BB6_holdouts_608.txt#L607) | 181063 | `NONHALT_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/56) |
| 78 | [75](BB6_holdouts_608.txt#L75) | 21328 | `SIMULATED_HALT` | [Register source](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/README.md) · [simulation log](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/orbits/O1/progress_halt_AhmerRaza.log) |
| 79 | [303](BB6_holdouts_608.txt#L303) | 82614 | `SIMULATED_HALT` | [Register source](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/README.md) · [simulation log](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/orbits/O4/progress_halt_AhmerRaza.log) |
| 80 | [331](BB6_holdouts_608.txt#L331) | 92948 | `SIMULATED_HALT` | [Register source](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/README.md) · [simulation log](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/orbits/O2/progress_halt_AhmerRaza.log) |
| 81 | [419](BB6_holdouts_608.txt#L419) | 119593 | `SIMULATED_HALT` | [Register source](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/README.md) · [simulation log](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/orbits/O2/progress_halt_AhmerRaza.log) |
| 82 | [421](BB6_holdouts_608.txt#L421) | 121010 | `SIMULATED_HALT` | [Register source](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/README.md) · [simulation log](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/orbits/O2/progress_halt_AhmerRaza.log) |
| 83 | [476](BB6_holdouts_608.txt#L476) | 134470 | `SIMULATED_HALT` | [Register source](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/README.md) · [simulation log](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/orbits/O4/progress_halt_AhmerRaza.log) |
| 84 | [552](BB6_holdouts_608.txt#L552) | 160156 | `SIMULATED_HALT` | [Register source](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/README.md) · [simulation log](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---/blob/main/orbits/O3/progress_halt_AhmerRaza.log) |
| 85 | [405](BB6_holdouts_608.txt#L405) | 114265 | `EQUIVALENCE_PR` | [Register source](https://github.com/ccz181078/busycoq/pull/77) · representative [117](BB6_holdouts_608.txt#L117) |

## Ranking method and reproduction

1. Only `OPEN` rows can enter the fresh queue. A `CLAIMED` or `BLOCKED` board row moves the line to existing campaigns. Check renewal dates and branches before claiming.
2. Use the first applicable approach in page order. Exact outcome replays take precedence over all transfers. The source catalogue matches machine identities across list editions. It links to individual theorem statements, return maps and checkpoints. Published models and machine-specific halt conditions still require an argument from the actual blank start.
3. Compare both read slots under state renaming and global left/right reflection, keeping symbol 0 blank. For a one-instruction match, substitute each possible instruction (including halt) into one candidate slot and compare all twelve again. `A → E` means candidate state A corresponds to E in the peer. A changed entry state can change the blank orbit. In the last column, `N (B mirrored)` means this line's blank A corresponds to line N's B on a reflected tape.
4. Run each open line from blank A for up to 65,536 elementary steps. A record is the first arrival outside the visited interval. `R/B/1011` means a new rightmost cell in state B with interior bits 1011 read inward, nearest first. The edge tier requires a period of 1–4 on a continuous suffix with at least 12 records in each half of the run. Only a local tape window repeats. A nonhalting proof must also cover the interior and establish infinite progress.
5. Within a transfer tier prefer fewer changed slots, the same entry and then verified or theorem-backed outcomes, proposed outcomes, simulation reports and models, in that order. Prefer representatives with more linked lines, checkpoints with a second proof comparison, and return maps with an explicit halting residue class. For edge repetitions prefer the smaller period, then the longer suffix. For shared tables prefer more other open starts. In the last two tiers prefer a full 24-record sample, then fewer distinct signatures. Remaining ties go to more other open starts on the same table, then the lower permanent line.

The [Lean BB(6) catalogue](https://github.com/google-deepmind/cryptids/tree/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6) supplies exact-machine theorem and model links. The [623-entry research diary](https://github.com/valu42/busycoqtesting/tree/632d9e666d26f9429aecfae44812cd4e69968703/research/holdouts-623) supplies earlier checkpoints. Their transition strings were matched to the 608-entry register, including the documented reflections for four cubic machines. All line numbers on this page use the 608-entry list.

From `research/bb6/`, run `python3 rank.py --write` to refresh this page or `python3 rank.py --check` to detect drift. The generator uses Python 3.10+ and the standard library. Edit the [source catalogue](ranking_sources.csv) to add a published lead. Use `python3 tracker.py --line N` for the register entry.
