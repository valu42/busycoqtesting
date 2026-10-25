(* Racheline's two-counter rules for supplied holdout 26, independently
   checked with BusyCoq's execution tactics. Source:
   https://wiki.bbchallenge.org/wiki/1RB1LC_1LC1RD_1LA0LB_0RB1RE_1RF0RA_---0RC
   Small unused configurations are excluded from the diagonal rules. The
   final recurrence theorem covers the invariant domain of the blank run.
   This does not classify that run. AI-assisted by Codex. *)
From BusyCoq Require Import Individual62 ES_v2 ES_v3.
From Coq Require Import List String Lia Arith.
Import ListNotations.
Open Scope sym_scope.

Module Cubic26.
Definition tm := Eval compute in
 (TM_from_str "1RB1LC_1LC1RD_1LA0LB_0RB1RE_1RF0RA_---0RC").
Definition config a b := 0inf <* [1]^^a <* [0] {{C}}> [1]^^b *> 0inf.
Notation "c -->* c'" := (c -[tm]->* c') (at level 40).
Notation "c -->+ c'" := (c -[tm]->+ c') (at level 40).

Definition S a b c := 0inf <* [1]^^a <{{B}} [0;1]^^b *> [1]^^(2+c) *> 0inf.
Lemma enter a c : config (1+a) (4+c) -->+ S a 2 c.
Proof. unfold config,S; es. Qed.
Lemma transfer a b c : S (1+a) b (1+c) -->* S a (1+b) c.
Proof. unfold S; es. Qed.
Lemma transfers n : forall a b c, S (n+a) b (n+c) -->* S a (n+b) c.
Proof.
 induction n; intros a b c; [simpl; finish|].
 change (S (1+(n+a)) b (1+(n+c)) -->* S a (1+(n+b)) c).
 eapply evstep_trans; [apply transfer|].
 applys_eq (IHn a (1+b) c); flia.
Qed.
Lemma exit_odd n c : S 0 (n*2+1) c -->* config (n*4+4) (c+2).
Proof. unfold S,config; es. Qed.
Lemma exit_even n c : S 0 (n*2+2) (1+c) -->* config (n*4+5) (c+4).
Proof. unfold S,config; es. Qed.
Lemma exit_even_zero n : S 0 (n*2+2) 0 -->* config (n*4+3) 9.
Proof. unfold S,config; es. Qed.
Lemma exit_one n : S 1 n 0 -->* config 1 (n*2+7).
Proof. unfold S,config; es. Qed.
Lemma exit_two n : S 2 (n+1) 0 -->* config 4 (n*2+8).
Proof. unfold S,config; es. Qed.
Lemma exit_right a b : S (3+a) b 0 -->* config (1+a) (b*2+7).
Proof. unfold S,config; es. Qed.
Lemma left_even n m :
 config (n*2+2) (n*2+5+m) -->+ config (n*4+8) (2+m).
Proof.
 eapply progress_evstep_trans.
 - applys_eq (enter (n*2+1) (n*2+1+m)); flia.
 - eapply evstep_trans.
   + applys_eq (transfers (n*2+1) 0 2 m); flia.
   + applys_eq (exit_odd (n+1) m); flia.
Qed.

Lemma left_odd n m :
 config (n*2+1) (n*2+5+m) -->+ config (n*4+5) (4+m).
Proof.
 eapply progress_evstep_trans.
 - applys_eq (enter (n*2) (n*2+1+m)); flia.
 - eapply evstep_trans.
   + applys_eq (transfers (n*2) 0 2 (1+m)); flia.
   + applys_eq (exit_even n m); flia.
Qed.

Lemma diagonal_three n :
 config (n*2+1) (n*2+4) -->+ config (n*4+3) 9.
Proof.
 eapply progress_evstep_trans.
 - applys_eq (enter (n*2) (n*2)); flia.
 - eapply evstep_trans.
   + applys_eq (transfers (n*2) 0 2 0); flia.
   + applys_eq (exit_even_zero n); flia.
Qed.

Lemma diagonal_two n :
 config (n+2) (n+4) -->+ config 1 (n*2+11).
Proof.
 eapply progress_evstep_trans.
 - applys_eq (enter (n+1) n); flia.
 - eapply evstep_trans.
   + applys_eq (transfers n 1 2 0); flia.
   + applys_eq (exit_one (n+2)); flia.
Qed.

Lemma diagonal_one n :
 config (n+3) (n+4) -->+ config 4 (n*2+10).
Proof.
 eapply progress_evstep_trans.
 - applys_eq (enter (n+2) n); flia.
 - eapply evstep_trans.
   + applys_eq (transfers n 2 2 0); flia.
   + applys_eq (exit_two (n+1)); flia.
Qed.

Lemma right n m :
 config (4+n+m) (4+n) -->+ config (m+1) (n*2+11).
Proof.
 eapply progress_evstep_trans.
 - applys_eq (enter (3+n+m) n); flia.
 - eapply evstep_trans.
   + applys_eq (transfers n (3+m) 2 0); flia.
   + applys_eq (exit_right m (n+2)); flia.
Qed.

Lemma halt n : halts tm (config (2+n) 3).
Proof. unfold config; esx. Qed.

Lemma restart n : config (4+n) 2 -->+ config (1+n) 7.
Proof. unfold config; es. Qed.

Lemma initial : c0 -->+ config 2 9.
Proof. unfold config; es. Qed.

Open Scope nat_scope.

Definition valid (p : nat*nat) :=
  1 <= fst p /\ 2 <= snd p /\ 11 <= fst p + snd p.

Definition next (p : nat*nat) : option (nat*nat) :=
  let '(a,b) := p in
  if b <=? a then
    if b =? 2 then Some (a-3,7) else
    if b =? 3 then None else Some (a-b+1,b*2+3)
  else match b-a with
    | 0 => None (* impossible in the valid domain *)
    | 1 => Some (4,a*2+4)
    | 2 => Some (1,a*2+7)
    | 3 => if a mod 2 =? 0 then Some (a*2+4,2) else Some (a*2+1,9)
    | _ => if a mod 2 =? 0 then Some (a*2+4,b-a-1) else Some (a*2+3,b-a)
    end.

Definition pair_config (p : nat*nat) := config (fst p) (snd p).

Lemma next_spec p : valid p ->
  match next p with
  | Some p' => pair_config p -->+ pair_config p' /\ valid p'
  | None => halts tm (pair_config p)
  end.
Proof.
  destruct p as [a b]; unfold valid; cbn [fst snd]; intros [Ha [Hb Hsum]].
  unfold next; cbn [pair_config fst snd].
  destruct (Nat.leb_spec b a).
  - destruct (Nat.eqb_spec b 2); subst.
    + cbn [pair_config fst snd]; split;
      [applys_eq (restart (a-4)); unfold pair_config; cbn [fst snd]; flia
      |repeat split; cbn [fst snd]; lia].
    + destruct (Nat.eqb_spec b 3); subst.
      * cbn [pair_config fst snd]; applys_eq (halt (a-2)); unfold pair_config; cbn [fst snd]; flia.
      * cbn [pair_config fst snd]; split;
      [applys_eq (right (b-4) (a-b)); unfold pair_config; cbn [fst snd]; flia
      |repeat split; cbn [fst snd]; lia].
  - pose proof (Nat.div_mod a 2 ltac:(lia)) as Hdiv.
    pose proof (Nat.mod_upper_bound a 2 ltac:(lia)) as Hmod.
    remember (b-a) as gap eqn:Egap.
    destruct gap as [|[|[|[|gap]]]]; try lia.
    + cbn [pair_config fst snd]; split;
      [applys_eq (diagonal_one (a-3)); unfold pair_config; cbn [fst snd]; flia
      |repeat split; cbn [fst snd]; lia].
    + cbn [pair_config fst snd]; split;
      [applys_eq (diagonal_two (a-2)); unfold pair_config; cbn [fst snd]; flia
      |repeat split; cbn [fst snd]; lia].
    + destruct (Nat.eqb_spec (a mod 2) 0).
      * cbn [pair_config fst snd]; split;
      [applys_eq (left_even (a/2-1) 0); unfold pair_config; cbn [fst snd]; flia
      |repeat split; cbn [fst snd]; lia].
      * cbn [pair_config fst snd]; split;
      [applys_eq (diagonal_three (a/2)); unfold pair_config; cbn [fst snd]; flia
      |repeat split; cbn [fst snd]; lia].
    + destruct (Nat.eqb_spec (a mod 2) 0).
      * cbn [pair_config fst snd]; split;
      [applys_eq (left_even (a/2-1) (1+gap)); unfold pair_config; cbn [fst snd]; flia
      |repeat split; cbn [fst snd]; lia].
      * cbn [pair_config fst snd]; split;
      [applys_eq (left_odd (a/2) gap); unfold pair_config; cbn [fst snd]; flia
      |repeat split; cbn [fst snd]; lia].
Qed.

Theorem blank_halts_iff_recurrence :
  halts tm c0 <-> iter_halts next (2,9).
Proof.
  transitivity (halts tm (pair_config (2,9))).
  - apply halts_evstep_iff, progress_evstep, initial.
  - eapply (halts_iff tm (nat*nat) (2,9) next pair_config valid).
    + exact next_spec.
    + unfold valid; cbn; lia.
Qed.

Print Assumptions left_even.
Print Assumptions left_odd.
Print Assumptions diagonal_three.
Print Assumptions diagonal_two.
Print Assumptions diagonal_one.
Print Assumptions right.
Print Assumptions halt.
Print Assumptions restart.
Print Assumptions initial.
Print Assumptions next_spec.
Print Assumptions blank_halts_iff_recurrence.
End Cubic26.
