(** Unbounded switch accounting for the line-36 suffix beyond a known halo. *)
From Coq Require Import Bool List Arith Lia ZArith.
From BusyCoq Require Import Line36Right Line36Word.
Import ListNotations.

(** All zero runs in a [paired_mask] have even length. *)
Inductive paired_mask : list bool -> Prop :=
| pm_nil : paired_mask []
| pm_one : forall u, paired_mask u -> paired_mask (true :: u)
| pm_zeros : forall u, paired_mask u -> paired_mask (false :: false :: u).

Lemma pair_prefix_zeros : forall z u,
  Nat.odd z = false -> paired_mask u -> paired_mask (repeat false z ++ u).
Proof.
  fix IH 1. intros [|[|z]] u Ev P.
  - exact P.
  - discriminate.
  - cbn [repeat app]. apply pm_zeros. apply IH; [|assumption].
    now rewrite Nat.odd_succ_succ in Ev.
Qed.

Definition starts_paired u := u = [] \/ exists t, u = true :: t /\ paired_mask t.

Lemma starts_paired_paired u : starts_paired u -> paired_mask u.
Proof. intros [->|[t [-> H]]]; constructor; assumption. Qed.

Lemma nat_odd_succ n : Nat.odd (S n) = negb (Nat.odd n).
Proof. rewrite Nat.odd_succ, Nat.negb_odd. reflexivity. Qed.

Theorem marked_shape w :
  let '(d,bits) := mark36 w 0 in
  exists z r, bits = repeat false z ++ r /\
             Nat.odd z = Nat.odd d /\ starts_paired r.
Proof.
  induction w as [|a w IH].
  - exists 0, []. repeat split; now left.
  - cbn [mark36]. destruct (mark36 w 0) as [d bits].
    destruct IH as [z [r [-> [Ev R]]]]. destruct a.
    + destruct d as [|d].
      * exists 0,(true :: repeat false z ++ r). repeat split.
        right. eexists; split; [reflexivity|].
        apply pair_prefix_zeros; [exact Ev|now apply starts_paired_paired].
      * exists (S z),r. split; [reflexivity|]. split; [|exact R].
        rewrite nat_odd_succ, Ev, nat_odd_succ. apply negb_involutive.
    + exists (S z),r. split; [reflexivity|]. split; [|exact R].
      now rewrite !nat_odd_succ, Ev.
Qed.

Definition body36 (prev : bool) (bits : list bool) :=
  deriv36 prev bits ++ carry36 prev bits.

Lemma body36_nil p : body36 p [] = if p then [false] else [].
Proof. reflexivity. Qed.

Lemma body36_cons p a w : body36 p (a::w) = Bool.eqb p a :: body36 a w.
Proof. unfold body36, carry36. cbn [deriv36 app]. now rewrite last36_cons. Qed.

Lemma paired_body u : paired_mask u ->
  (forall g, gap_cost (body36 true u) g =
     run_cost u (negb g) + bit_cost (negb (last u true))) /\
  gap_cost (body36 false u) true =
     run_cost u false + bit_cost (negb (last u false)).
Proof.
  intros P. induction P as [|u P [T F]|u P [T F]].
  - split; [intros []|]; reflexivity.
  - rewrite !body36_cons, !last36_cons. split.
    + intros []; cbn [Bool.eqb gap_cost run_cost negb bit_cost]; apply T.
    + cbn [Bool.eqb gap_cost run_cost negb bit_cost]. apply (T false).
  - rewrite !body36_cons, !last36_cons. split.
    + intros []; cbn [Bool.eqb gap_cost run_cost negb bit_cost]; lia.
    + cbn [Bool.eqb gap_cost run_cost negb bit_cost]. exact F.
Qed.

Definition cell_fee (opening gap : bool) :=
  if opening then 0 else bit_cost (negb gap).
Definition cell_gap (opening gap : bool) :=
  if opening then negb gap else false.

Lemma gap_cost_cons x w g :
  gap_cost (x::w) g = cell_fee x g + gap_cost w (cell_gap x g).
Proof. destruct x; reflexivity. Qed.

Lemma zeros_before_live n u g :
  gap_cost (body36 false (repeat false n ++ true :: u)) g =
  bit_cost (negb (xorb g (Nat.odd n))) + gap_cost (body36 true u) false.
Proof.
  revert g. induction n as [|n IH]; intros g.
  - cbn [repeat app]. rewrite body36_cons. destruct g; reflexivity.
  - cbn [repeat app]. rewrite body36_cons. cbn [Bool.eqb gap_cost].
    rewrite IH, nat_odd_succ. destruct g, (Nat.odd n); reflexivity.
Qed.

Lemma run_cost_distance w a b :
  run_cost w a <= run_cost w b + bit_cost (xorb a b).
Proof.
  pose proof (run_cost_toggle w). destruct a,b; cbn [xorb bit_cost]; lia.
Qed.

Lemma suffix_last_zero_head n u s :
  last (false :: repeat false n ++ true :: u) s = last u true.
Proof.
  rewrite last36_cons. induction n as [|n IH].
  - cbn [repeat app]. apply last36_cons.
  - cbn [repeat app]. rewrite last36_cons. exact IH.
Qed.

Lemma zeros_run_cost n u :
  run_cost (repeat false n ++ u) false = run_cost u false.
Proof. induction n; [reflexivity|]. cbn; exact IHn. Qed.

Lemma no_live_in_zeros n : ~ In true (repeat false n).
Proof. induction n as [|n IH]; cbn; firstorder discriminate. Qed.

Lemma live_prefix_no_debt w d t :
  mark36 w 0 = (d,true::t) -> d = 0.
Proof.
  destruct w as [|x w]; [discriminate|]. cbn [mark36].
  destruct (mark36 w 0) as [j m]. destruct x; [destruct j|]; congruence.
Qed.

Definition debt_fee d (e : bool) :=
  match d with
  | 0 => bit_cost e
  | S k => S k - bit_cost e
  end.

(** Extend the left anchor by the one formal opening realizing [e]. *)
Lemma anchor_charge_aligned p u (e:bool) :
  let w := p ++ false :: u in
  let a := if e then [true] else [] in
  let '(d,bits) := mark36 (a ++ w) 0 in
  d + odd_runs bits + cap_loss u <= gap_cost w e.
Proof.
  cbv zeta. rewrite <- aligned_gap_cost.
  replace ((if e then [true] else []) ++ p ++ false :: u) with
      (((if e then [true] else []) ++ p) ++ false :: u) by (symmetry; apply app_assoc).
  apply anchored_cancellation.
Qed.

Lemma aligned_nonsurvivor p u d t e :
  mark36 (p ++ false :: u) 0 = (d,false::t) ->
  odd_runs (false::t) + debt_fee d e + cap_loss u <=
    gap_cost (p ++ false::u) e.
Proof.
  intros M. pose proof (anchor_charge_aligned p u e) as H; cbv zeta in H.
  destruct e.
  - change (let '(v,m) := mark36 (true::(p ++ false::u)) 0 in
        v + odd_runs m + cap_loss u <= gap_cost (p ++ false::u) true) in H.
    cbn [mark36] in H. rewrite M in H. destruct d;
      cbn [odd_runs run_cost debt_fee bit_cost negb] in *; lia.
  - change (let '(v,m) := mark36 (p ++ false::u) 0 in
        v + odd_runs m + cap_loss u <= gap_cost (p ++ false::u) false) in H.
    rewrite M in H. destruct d; cbn [debt_fee bit_cost] in *; lia.
Qed.

Lemma aligned_survivor p u d t e :
  mark36 (p ++ false :: u) 0 = (d,true::t) ->
  run_cost t (negb e) + cap_loss u <= gap_cost (p ++ false::u) e.
Proof.
  intros M. rewrite (live_prefix_no_debt _ _ _ M) in M.
  pose proof (anchor_charge_aligned p u e) as H; cbv zeta in H.
  destruct e.
  - change (let '(v,m) := mark36 (true::(p ++ false::u)) 0 in
        v + odd_runs m + cap_loss u <= gap_cost (p ++ false::u) true) in H.
    cbn [mark36] in H. rewrite M in H. exact H.
  - change (let '(v,m) := mark36 (p ++ false::u) 0 in
        v + odd_runs m + cap_loss u <= gap_cost (p ++ false::u) false) in H.
    rewrite M in H. exact H.
Qed.

(** [e] is the old alignment at y: old last closing differs from y-1.
    [g] is the new alignment at y+h: normalized last closing differs from y.
    The first output cell is open iff [previous=q].  Its possible switch is
    [cell_fee], and [cell_gap] is the new alignment just after that cell. *)
Theorem halo_tail_bound p u d bits (e g previous : bool) :
  mark36 (p ++ false :: u) 0 = (d,bits) -> In true bits ->
  let q := hd false bits in
  let open := Bool.eqb previous q in
  gap_cost (body36 previous bits) g + cap_loss u
    + (if q then 0 else debt_fee d e) <=
  gap_cost (p ++ false :: u) e + bit_cost (negb (last bits previous))
    + cell_fee open g
    + bit_cost (xorb (cell_gap open g) (if q then e else Nat.odd d)).
Proof.
  intros M Live. pose proof (marked_shape (p ++ false::u)) as Shape.
  rewrite M in Shape. destruct Shape as [z [r [-> [Ev R]]]].
  destruct R as [->|[t [-> P]]].
  - rewrite app_nil_r in Live. now exfalso; apply (no_live_in_zeros z).
  - destruct z as [|n].
    + cbn [repeat app] in M |- *. cbn [hd].
      pose proof (aligned_survivor _ _ _ _ e M) as A.
      rewrite body36_cons, gap_cost_cons, last36_cons.
      rewrite (proj1 (paired_body _ P)).
      pose proof (run_cost_distance t (negb (cell_gap (eqb previous true) g))
                                      (negb e)) as B.
      replace (xorb (negb (cell_gap (eqb previous true) g)) (negb e)) with
              (xorb (cell_gap (eqb previous true) g) e) in B
        by (destruct (cell_gap (eqb previous true) g),e; reflexivity).
      lia.
    + cbn [repeat app] in M |- *. cbn [hd].
      pose proof (aligned_nonsurvivor _ _ _ _ e M) as A.
      rewrite body36_cons, gap_cost_cons, zeros_before_live, suffix_last_zero_head.
      rewrite (proj1 (paired_body _ P)).
      unfold odd_runs in A. cbn [run_cost bit_cost] in A.
      rewrite zeros_run_cost in A. cbn [run_cost negb] in A.
      rewrite nat_odd_succ in Ev. rewrite <- Ev.
      destruct (cell_gap (eqb previous false) g), (Nat.odd n);
        cbn [xorb negb bit_cost] in *; lia.
Qed.

(** Split off any finite known output/full-word portion to recover the
    moving-cut inequality.  Run [gap_scan] keeps the current alignment at
    the cut, without paying the unclosed terminal gap twice. *)
Fixpoint gap_scan (w : list bool) (g : bool) : nat * bool :=
  match w with
  | [] => (0,g)
  | a :: t =>
      let '(k,b) := gap_scan t (cell_gap a g) in (cell_fee a g + k,b)
  end.

Lemma gap_cost_append x t g :
  let '(n,f) := gap_scan x g in gap_cost (x ++ t) g = n + gap_cost t f.
Proof.
  revert g. induction x as [|a x IH]; intros g; [reflexivity|].
  cbn [gap_scan app]. rewrite gap_cost_cons.
  specialize (IH (cell_gap a g)). destruct (gap_scan x (cell_gap a g)).
  lia.
Qed.

Theorem halo_moving_cut lo hi p u d bits old_align new_align previous :
  mark36 (p ++ false::u) 0 = (d,bits) -> In true bits ->
  let '(k,e) := gap_scan lo old_align in
  let '(k',g) := gap_scan hi new_align in
  let q := hd false bits in
  let open := Bool.eqb previous q in
  let charge :=
      (Z.of_nat k' - Z.of_nat k + Z.of_nat (cell_fee open g)
       + Z.of_nat (bit_cost (xorb (cell_gap open g) (if q then e else Nat.odd d)))
       - Z.of_nat (if q then 0 else debt_fee d e))%Z in
  (Z.of_nat (gap_cost (hi ++ body36 previous bits) new_align) <=
   Z.of_nat (gap_cost (lo ++ p ++ false::u) old_align)
    + charge + Z.of_nat (bit_cost (negb (last bits previous))) - Z.of_nat (cap_loss u))%Z.
Proof.
  intros M Live.
  pose proof (gap_cost_append lo (p ++ false::u) old_align) as B.
  pose proof (gap_cost_append hi (body36 previous bits) new_align) as B'.
  destruct (gap_scan lo old_align) as [k e].
  destruct (gap_scan hi new_align) as [k' g].
  pose proof (halo_tail_bound p u d bits e g previous M Live) as Bound.
  cbv zeta in Bound |- *. lia.
Qed.

Lemma bit_cost_at_most_one b : bit_cost b <= 1.
Proof. destruct b; cbn; lia. Qed.

Fixpoint closing_count (w : list bool) : nat :=
  match w with
  | [] => 0
  | true :: r => closing_count r
  | false :: r => S (closing_count r)
  end.

Lemma gap_scan_charges_closings w e : fst (gap_scan w e) <= closing_count w.
Proof.
  revert e. induction w as [|a w IH]; intros e; [reflexivity|].
  cbn [gap_scan]. specialize (IH (cell_gap a e)).
  destruct (gap_scan w (cell_gap a e)) as [k g]. cbn [fst] in *.
  destruct a; cbn [closing_count cell_fee]; [assumption|].
  pose proof (bit_cost_at_most_one (negb e)); lia.
Qed.

Lemma closing_count_app x y :
  closing_count (x++y) = closing_count x + closing_count y.
Proof. induction x as [|[] x IH]; cbn; lia. Qed.

Lemma all_open_no_closing n : closing_count (repeat true n) = 0.
Proof. induction n; cbn; assumption || reflexivity. Qed.

Lemma suffix_of_flat_output a n earlier later :
  a :: repeat true n = earlier ++ later -> closing_count later <= 1.
Proof.
  intros E. apply (f_equal closing_count) in E. rewrite closing_count_app in E.
  destruct a; cbn [closing_count] in E; rewrite all_open_no_closing in E; lia.
Qed.

(** A positive exterior demand makes the previous old cell a nonsurvivor.
    If at most one closing remains in the exposed image, [K' <= 1].
    This combines the derived charge, cancellation, and [C <= 3-d] without
    assuming anything about the two sentinel parities. *)
Theorem halo_high_debt lo hi p u d bits old_align new_align :
  mark36 (p ++ false::u) 0 = (d,bits) -> In true bits ->
  0 < d -> closing_count hi <= 1 ->
  (Z.of_nat (gap_cost (hi ++ body36 false bits) new_align) <=
   Z.of_nat (gap_cost (lo ++ p ++ false::u) old_align) +
   (3-Z.of_nat d) + Z.of_nat (bit_cost (negb (last bits false))) - Z.of_nat (cap_loss u))%Z.
Proof.
  intros M Live D Few.
  pose proof (halo_moving_cut lo hi p u d bits old_align new_align false M Live) as H.
  pose proof (gap_scan_charges_closings hi new_align) as K.
  destruct (gap_scan lo old_align) as [k e], (gap_scan hi new_align) as [k' g].
  cbn [fst] in K. destruct bits as [|q bits]; [contradiction|].
  destruct q; [apply live_prefix_no_debt in M; lia|].
  cbn [hd Bool.eqb cell_fee] in H. destruct d as [|d]; [lia|].
  cbn [debt_fee] in H.
  pose proof (bit_cost_at_most_one e).
  pose proof (bit_cost_at_most_one (xorb (cell_gap true g) (Nat.odd (S d)))).
  lia.
Qed.
