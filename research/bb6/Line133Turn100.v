(** A second outward scan after the 100 turn of a full carry on line 133. *)
From Coq Require Import Lists.List.
From BusyCoq Require Import Individual62.
Require Import Line133Odometer Line133Carry.
Import ListNotations.

(** After the tokens 01 and 100, a further 01 brings E back to the
    unread suffix. None of the surrounding cells are needed for these
    22 transitions from D in the reflected table. *)
Definition rescan_word tail := cycle_word [Pair01] (exit_word Turn100 (0 >> 1 >> tail)).
Definition rescan_writes : list Sym := [0;1;0;0;1;0;0;1].

Lemma turn100_rescan_steps tail behind :
  (rescan_word tail) {{D}}> (1 >> behind) -[Odo.tm]->> 22 /
  tail <{{E}} (rescan_writes *> behind).
Proof. apply multistep_c_spec. reflexivity. Qed.

Theorem line133_turn100_rescan front levels cycles e tail :
  carry_input front levels (rescan_word (cycle_word cycles (exit_word e tail))) -[line133]->*
  reflect_config (exit_config e tail (cycle_writes cycles
    (rescan_writes *> return_path levels (front_path front)))).
Proof.
  pose proof (evstep_trans _ _ _ _ (enter_carry front levels _)
    (without_counter _ _ _ _ (turn100_rescan_steps (cycle_word cycles (exit_word e tail)) _))) as H.
  pose proof (evstep_trans _ _ _ _ H
    (evstep_trans _ _ _ _ (scan_cycles cycles _ _) (take_exit e tail _))) as path.
  destruct (with_counter path) as [n Hn].
  exact (without_counter _ _ _ _ (transfer_steps _ _ _ Hn)).
Qed.

Corollary line133_turn100_f0 front levels cycles tail :
  halts_at_trans line133
    (carry_input front levels (rescan_word (cycle_word cycles (exit_word Stop00 tail)))) (F, S0).
Proof.
  destruct (with_counter (line133_turn100_rescan front levels cycles Stop00 tail)) as [n Hn].
  exists n. econstructor; [exact Hn | reflexivity].
Qed.

(** The two inputs share one full level and the same 100 exit. Changing
    only the second cell after the exit gives different immediate outcomes. *)
Definition turn100_example tail := carry_input 0 [O] (cycle_word [Pair01] (exit_word Turn100 tail)).

Theorem line133_turn100_one_cell :
  halts_in line133 (turn100_example (0 >> 1 >> 0inf)) 34 /\
  turn100_example 0inf -[line133]->> 97 /
    0inf <{{C}} ([0;1;1;0;1;1;1;1;1;1;1;0;1;1;0;1;1;1] *> 0inf).
Proof.
  split.
  - apply halts_in_halts_in'. eexists. split; reflexivity.
  - do 97 (eapply multistep_S; [prove_step | simpl_tape]). apply multistep_0.
Qed.

Print Assumptions line133_turn100_rescan.
Print Assumptions line133_turn100_f0.
Print Assumptions line133_turn100_one_cell.
