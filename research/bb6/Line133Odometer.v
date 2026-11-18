(** Blank-start transfer and checkpoint for the 608-list line 133 (ID 35069).
    The odometer and its soundness theorem are from BusyCoq PR 76.
    See line133-odometer.md for the pinned dependency and replay commands. *)
From Coq Require Import String Lists.List NArith PArith.Pnat Lia.
From BusyCoq Require Import Individual62 M_1RB1RD_1RC1RB_1LD0RA_1RA0LE_1LF0LC_HHH1LE.
Import ListNotations.
Module Odo := M172044.

Definition line133 := Eval compute in
  (TM_from_str "1RB0LC_1LC0RE_1LD1LB_1LA1LD_1RF0RA_---1RE"%string).

Definition rename_state (q : Q) : Q :=
  match q with A => C | B => D | C => A | D => B | E => E | F => F end.

Definition reflect_config (c : Q * tape) : Q * tape :=
  let '(q, t) := flip_conf c in (rename_state q, t).

Lemma to_line133 : Perm (flip Odo.tm) line133 rename_state.
Proof.
  split.
  - intros [] [] H; discriminate H || reflexivity.
  - intros [] [] s d q H; inversion H; reflexivity.
Qed.

Lemma from_line133 : Perm (flip line133) Odo.tm rename_state.
Proof.
  split.
  - intros [] [] H; discriminate H || reflexivity.
  - intros [] [] s d q H; inversion H; reflexivity.
Qed.

Definition seed := Odo.MC true [] [] C.

Theorem line133_halts_iff : halts line133 c0 <-> halts Odo.tm (Odo.semc seed).
Proof.
  split; intro H.
  - apply (perm_halts _ _ _ A tape0 from_line133).
    exact (flip_halts _ _ H).
  - apply (perm_halts _ _ _ C tape0 to_line133).
    exact (flip_halts _ _ H).
Qed.

Lemma transfer_steps n c c' :
  c -[ Odo.tm ]->> n / c' -> reflect_config c -[ line133 ]->> n / reflect_config c'.
Proof.
  intro H. pose proof (flip_multistep _ _ _ _ H) as Hf.
  unfold reflect_config. destruct (flip_conf c), (flip_conf c').
  eapply perm_multistep; [apply to_line133 | exact Hf].
Qed.

(** At a fresh cell on the left in the original machine, an arbitrary
    untouched right tail survives any batch whose counters pass both guards. *)
Theorem line133_jump ps top tail visits :
  Odo.ovf visits ps = 0%N -> Odo.goodN (Odo.after visits ps) top = true ->
  0inf <{{C}} (Odo.zoneN ps top tail) -[line133]->*
  0inf <{{C}} (Odo.zoneN (Odo.after visits ps) top tail).
Proof.
  intros Ho Hg. destruct (evstep_multistep _ _ _ (Odo.jump ps top tail visits Ho Hg)) as [n Hn].
  apply multistep_evstep_iff. exists n. exact (transfer_steps _ _ _ Hn).
Qed.

(** A missing case of the ordinary odometer. Bits are written in physical
    order from the head to the right. The unknown suffix is never inspected. *)
Definition recovery_in a b (tail : side) :=
  0inf <{{C}} ([1;1;0] ^^ (2+b) *> [1;1] *> [1;1;0] ^^ (1+a) *> [1;0;1;1;1] *> tail).
Definition recovery_out a b (tail : side) :=
  0inf <{{C}} ([0] *> [1;1;0] ^^ 7 *> [1;0] *> [1;1;0] ^^ b *>
    [1;1] *> [1;1;0] ^^ a *> [1;1] *> [1;1;0] *> tail).

Theorem line133_recover a b tail :
  recovery_in a b tail -[line133]->* recovery_out a b tail.
Proof. unfold recovery_in, recovery_out. es. Qed.

(** An elementary transition writes a single cell. Bound the number of ones
    in every finite window, allowing different lengths on the two sides. *)
Definition bit_weight (s : Sym) : N := if Odo.is1 s then 1%N else 0%N.

Fixpoint prefix_ones (k : nat) (s : side) : N :=
  match k with O => 0%N | S k' => (bit_weight (hd s) + prefix_ones k' (tl s))%N end.

Definition bounded_by (b : N) (c : Q * tape) :=
  let '(_, (l, s, r)) := c in
  forall i j, (prefix_ones i l + bit_weight s + prefix_ones j r <= b)%N.

Lemma blank_prefix k : prefix_ones k 0inf = 0%N.
Proof. induction k; simpl; assumption || reflexivity. Qed.

Lemma weight_step tm c c' b : c -[tm]-> c' -> bounded_by b c -> bounded_by (b+1) c'.
Proof.
  intro H. destruct H as [q q' s w l r H | q q' s w l r H]; cbn [bounded_by move_left move_right]; intros Hb i j.
  - destruct j as [|j]; [specialize (Hb (S i) O) | specialize (Hb (S i) j)];
      cbn [prefix_ones hd tl] in *; destruct w; cbv [bit_weight Odo.is1] in *; lia.
  - destruct i as [|i]; [specialize (Hb O (S j)) | specialize (Hb i (S j))];
      cbn [prefix_ones hd tl] in *; destruct w; cbv [bit_weight Odo.is1] in *; lia.
Qed.

Lemma weight_run tm n c c' : c -[tm]->> n / c' ->
  forall b, bounded_by b c -> bounded_by (b + N.of_nat n) c'.
Proof.
  intro H. induction H as [c | n c m c' Hstep Hrest IH]; intros b Hb.
  - rewrite N.add_0_r. exact Hb.
  - rewrite Nat2N.inj_succ. replace (b + N.succ (N.of_nat n))%N with ((b+1) + N.of_nat n)%N by lia.
    apply IH. eapply weight_step; eassumption.
Qed.

Fixpoint word_ones (w : list Sym) : N :=
  match w with [] => 0%N | s :: w' => (bit_weight s + word_ones w')%N end.

Fixpoint stack_ones (b : list Odo.item) : N :=
  match b with
  | [] => 0%N
  | Odo.Bit s :: xs => (bit_weight s + stack_ones xs)%N
  | Odo.Run w p :: xs => (Npos p * word_ones w + stack_ones xs)%N
  end.

Lemma word_app u v : word_ones (u ++ v) = (word_ones u + word_ones v)%N.
Proof. induction u; simpl; [reflexivity | rewrite IHu; lia]. Qed.

Lemma word_power w n : word_ones (w ^^ n) = (N.of_nat n * word_ones w)%N.
Proof.
  induction n as [|n IH]; [reflexivity |].
  rewrite Nat2N.inj_succ. cbn [lpow]. rewrite word_app, IH, N.mul_succ_l. lia.
Qed.

Lemma prefix_app w s k : prefix_ones (List.length w + k) (w *> s) =
  (word_ones w + prefix_ones k s)%N.
Proof. induction w; simpl; [reflexivity | rewrite IHw; lia]. Qed.

Lemma den_count b : exists k, prefix_ones k (Odo.den b 0inf) = stack_ones b.
Proof.
  induction b as [|[s|w p] b [k IH]].
  - exists O. reflexivity.
  - exists (S k). cbn [Odo.den prefix_ones hd tl stack_ones]. now rewrite IH.
  - exists (List.length (w ^^ Pos.to_nat p) + k)%nat.
    assert (Hp : N.of_nat (Pos.to_nat p) = Npos p) by exact (N2Nat.id (Npos p)).
    cbn [Odo.den stack_ones]. now rewrite prefix_app, word_power, IH, Hp.
Qed.

(** The observation reads only compressed counters. The previous lemmas
    relate their sum to actual tape cells and hence to elementary steps. *)
Definition gate (a b : positive) : list Odo.item :=
  [Odo.Run Odo.W (Pos.succ (Pos.succ b)); Odo.Bit S1; Odo.Bit S1;
   Odo.Run Odo.W (Pos.succ a); Odo.Bit S1; Odo.Bit S0; Odo.Bit S1; Odo.Bit S1; Odo.Bit S1].

(* The two exponents in recovery_in are a+1 and b+2. *)
Definition checkpoint_a := 404277775835677427574742439536721155021%positive.
Definition checkpoint_b := 310982904488982636595955722720554739540%positive.
Definition checkpoint_gate := gate checkpoint_a checkpoint_b.
Definition checkpoint_ones := 1802104644690770721432339129424760388912%N.
Definition checkpoint_rounds := 4195051%positive.

Definition observed (r : Odo.rr) : option N :=
  match r with
  | Odo.RNext (Odo.MC true [] b A) =>
      if Odo.items_eqb (firstn (List.length checkpoint_gate) (Odo.canonL b)) checkpoint_gate
      then Some (stack_ones b) else None
  | _ => None
  end.

Lemma observed_spec r n : observed r = Some n -> exists b,
  r = Odo.RNext (Odo.MC true [] b A) /\ stack_ones b = n /\
  exists rest, Odo.canonL b = checkpoint_gate ++ rest.
Proof.
  destruct r as [|[[] [|x f] b []]]; cbn [observed]; intro H; try discriminate H.
  destruct (Odo.items_eqb _ _) eqn:He; inversion H; subst.
  exists b. split; [reflexivity |]. split; [reflexivity |].
  apply Odo.items_eqb_eq in He. exists (skipn (List.length checkpoint_gate) (Odo.canonL b)).
  pose proof (firstn_skipn (List.length checkpoint_gate) (Odo.canonL b)) as Hsplit.
  now rewrite He in Hsplit.
Qed.

Lemma gate_config a b data rest : Odo.canonL data = gate a b ++ rest ->
  reflect_config (Odo.semc (Odo.MC true [] data A)) =
  recovery_in (Pos.to_nat a) (Pos.to_nat b) (Odo.den rest 0inf).
Proof.
  intro H. change ((0inf <{{C}} Odo.den data 0inf) =
    recovery_in (Pos.to_nat a) (Pos.to_nat b) (Odo.den rest 0inf)).
  rewrite <- (Odo.den_canonL data 0inf), H.
  cbn [gate List.app Odo.den]. rewrite !Pos2Nat.inj_succ. reflexivity.
Qed.

Lemma checkpoint_observed : observed (Odo.run checkpoint_rounds seed) = Some checkpoint_ones.
Proof. vm_cast_no_check (eq_refl (Some checkpoint_ones)). Qed.

Theorem line133_blank_checkpoint : exists n tail,
  c0 -[line133]->> n / recovery_in (Pos.to_nat checkpoint_a) (Pos.to_nat checkpoint_b) tail /\
  (checkpoint_ones <= N.of_nat n)%N.
Proof.
  destruct (observed_spec _ _ checkpoint_observed) as [b [Hr [Hones [rest Hgate]]]].
  pose proof (Odo.run_sound checkpoint_rounds seed) as Hrun. rewrite Hr in Hrun.
  destruct (evstep_multistep _ _ _ Hrun) as [n Hn].
  exists n, (Odo.den rest 0inf). split.
  - rewrite <- (gate_config _ _ _ _ Hgate). exact (transfer_steps _ _ _ Hn).
  - assert (Hblank : bounded_by 0 (Odo.semc seed)).
    { change (forall i j, (prefix_ones i 0inf + 0 + prefix_ones j 0inf <= 0)%N).
      intros i j; rewrite !blank_prefix; reflexivity. }
    pose proof (weight_run _ _ _ _ Hn 0%N Hblank) as Hbound.
    destruct (den_count b) as [k Hk]. specialize (Hbound k O).
    change (prefix_ones k (Odo.den b 0inf) + 0 + 0 <= N.of_nat n)%N in Hbound.
    rewrite Hk, Hones in Hbound. lia.
Qed.

Corollary line133_no_early_halt k : (N.of_nat k < checkpoint_ones)%N -> ~halts_in line133 c0 k.
Proof.
  intros Hk Hhalt. destruct line133_blank_checkpoint as [n [tail [Hpath Hbound]]].
  eapply exceeds_halt; [exact Hhalt | | exact Hpath]. lia.
Qed.

Print Assumptions line133_halts_iff.
Print Assumptions line133_jump.
Print Assumptions line133_recover.
Print Assumptions line133_blank_checkpoint.
Print Assumptions line133_no_early_halt.
