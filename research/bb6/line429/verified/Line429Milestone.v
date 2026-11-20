(** Link the checked line-279 theorem to the five-state trajectory. *)
From BusyCoq Require Import Individual62 Line429Sibling M_1RB0LC_1RC1RA_1LD0RE_1LA1LD_0RA1RF_0LCHHH.
Import Sibling429.
Theorem total_orbit_hits_279 : reaches guard279 start.
Proof. apply (proj1 blank279). exact M_1RB0LC_1RC1RA_1LD0RE_1LA1LD_0RA1RF_0LCHHH.halt. Qed.
Theorem blank_milestone : halts machine429 c0 \/
  exists x, guard279 x = true /\ c0 -[machine429]->* embed state429 x.
Proof. apply sibling_milestone. exact M_1RB0LC_1RC1RA_1LD0RE_1LA1LD_0RA1RF_0LCHHH.halt. Qed.
Print Assumptions total_orbit_hits_279.
Print Assumptions blank_milestone.
