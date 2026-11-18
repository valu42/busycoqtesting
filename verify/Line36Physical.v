(** Physical interpretation of a complete successful row-36 sweep. *)
From Coq Require Import Lists.Streams Lists.List Bool.Bool PeanoNat Lia.
From BusyCoq Require Import Line36Machine Line36Word.
Import ListNotations.
Local Open Scope list_scope.

(** The processed old data are stored nearest-first on the left. *)
Definition mark_symbol36 (b : bool) : sym := if b then S3 else S2.
Definition header_rev36 (d : nat) : list sym :=
  match d with
  | 0 => [S1] | 1 => [S3] | 2 => [S2]
  | n => [S2; match n with 3 => S1 | 4 => S3 | _ => S2 end; S4; S3; S3; S1]
  end.
Definition physical_row36 (d : nat) (p : list bool) : list sym :=
  List.map mark_symbol36 p ++ header_rev36 d.

(** Remove the nearest [n] remaining marks, or report the excess debt. *)
Fixpoint drain36 (p : list bool) (n : nat) : nat * list bool :=
  match p with
  | [] => (n, [])
  | b :: t =>
    let '(n', bit) := if b then match n with
                                  | 0 => (0,true) | S k => (k,false) end
                            else (n,false) in
    let '(excess, t') := drain36 t n' in (excess, bit :: t')
  end.

Lemma drain36_zero p : drain36 p 0 = (0,p).
Proof.
  induction p as [|b p IH]; [reflexivity|].
  destruct b; cbn; now rewrite IH.
Qed.

Lemma drain36_compose p a b e1 p1 e2 p2 :
  drain36 p a = (e1,p1) ->
  drain36 p1 b = (e2,p2) ->
  drain36 p (a+b) = (e1+e2,p2).
Proof.
  revert a b e1 p1 e2 p2.
  induction p as [|x p IH]; intros a b e1 p1 e2 p2 H1 H2.
  - inversion H1; subst. inversion H2. reflexivity.
  - destruct x; [destruct a as [|a]|].
    + rewrite drain36_zero in H1. inversion H1; subst. exact H2.
    + cbn [drain36] in H1.
      destruct (drain36 p a) as [k q] eqn:E. inversion H1; subst.
      cbn [drain36] in H2. destruct (drain36 q b) as [j t] eqn:F.
      inversion H2; subst. cbn [Nat.add drain36].
      now rewrite (IH a b _ _ _ _ E F).
    + cbn [drain36] in H1.
      destruct (drain36 p a) as [k q] eqn:E. inversion H1; subst.
      cbn [drain36] in H2. destruct (drain36 q b) as [j t] eqn:F.
      inversion H2; subst. cbn [drain36].
      now rewrite (IH a b _ _ _ _ E F).
Qed.

Local Notation "c ==>* c'" := (evstep line36 c c') (at level 70).
Local Notation "c ==> c'" := (step line36 c c') (at level 70).
Local Notation BR l r := (l {{ B }}> r).
Local Notation BL l r := (l <{{ B }} r).
Local Notation AL l r := (l <{{ A }} r).
Local Notation zeroes := (const S0).
Local Ltac one36 :=
  eapply evstep_step;
  [first [eapply step_right; reflexivity | eapply step_left; reflexivity] | ].
Local Ltac done36 := apply evstep_refl.

(** The exceptional guard transition is an actual 35-step excursion:
    one step across the spent guard, 33 on the blank half-line, and
    one restoring the old guard. Its entire right context is arbitrary. *)
Lemma physical_guard36 : forall d r, d < 5 ->
  BL (lift_side (header_rev36 d)) r ==>*
  BR (lift_side (header_rev36 (S d))) r.
Proof.
  intros d r H. destruct d as [|[|[|[|[|d]]]]]; try lia.
  - one36. done36.
  - one36. done36.
  - do 35 one36. done36.
  - one36. one36. one36. done36.
  - one36. one36. one36. done36.
Qed.

(** A closing searches backwards through previously paired ground cells,
    turns on the nearest mark (or at the guard), and restores the ground. *)
Lemma seek36 : forall p d e p' r,
  drain36 p 1 = (e,p') -> d+e < 6 ->
  BL (lift_side (physical_row36 d p)) r ==>*
  BR (lift_side (physical_row36 (d+e) p')) r.
Proof.
  induction p as [|b p IH]; intros d e p' r E H.
  - inversion E; subst. rewrite Nat.add_1_r. apply physical_guard36. lia.
  - destruct b.
    + cbn [drain36] in E. rewrite drain36_zero in E. inversion E; subst.
      rewrite Nat.add_0_r. one36. done36.
    + cbn [drain36] in E.
      destruct (drain36 p 1) as [a q] eqn:F. inversion E; subst.
      one36. eapply evstep_trans.
      * exact (IH d e q (Cons S3 r) eq_refl H).
      * one36. done36.
Qed.

Lemma rev36_cons_app {T} (x:T) w p :
  List.rev (x::w) ++ p = List.rev w ++ x::p.
Proof. cbn. now rewrite <- app_assoc. Qed.

(** Consume a finite input with an arbitrary right continuation. Its suffix
    matching debt is charged first to the stack, then to the physical guard. *)
Lemma outward36 : forall w p d e p' k bits (r : side),
  mark36 w 0 = (k,bits) -> drain36 p k = (e,p') -> d+e < 6 ->
  BR (lift_side (physical_row36 d p)) (Str_app (List.map data_symbol w) r) ==>*
  BR (lift_side (physical_row36 (d+e) (List.rev bits ++ p'))) r.
Proof.
  induction w as [|x w IH]; intros p d e p' k bits r M D H.
  - inversion M; subst. rewrite drain36_zero in D. inversion D; subst.
    rewrite Nat.add_0_r. done36.
  - cbn [mark36] in M. destruct (mark36 w 0) as [n t] eqn:W.
    destruct x.
    + destruct n as [|n]; inversion M; subst; rewrite rev36_cons_app; one36.
      * eapply (IH (true::p) d e (true::p') 0 t r eq_refl).
        -- cbn [drain36]. rewrite D. reflexivity.
        -- exact H.
      * eapply (IH (true::p) d e (false::p') (S k) t r eq_refl).
        -- cbn [drain36]. rewrite D. reflexivity.
        -- exact H.
    + inversion M; subst. rewrite rev36_cons_app.
      destruct (drain36 p 1) as [u q] eqn:U.
      destruct (drain36 q n) as [v t'] eqn:V.
      pose proof (drain36_compose p 1 n u q v t' U V) as C.
      change (drain36 p (S n) = (u+v,t')) in C.
      rewrite D in C. inversion C; subst.
      one36. eapply evstep_trans.
      * eapply (seek36 p d u q (Cons S3 (Str_app (List.map data_symbol w) r)) U). lia.
      * one36. replace (d + (u + v)) with ((d+u)+v) by lia.
        eapply (IH (false::q) (d+u) v (false::t') n t r eq_refl).
        -- cbn [drain36]. rewrite V. reflexivity.
        -- lia.
Qed.

Definition flip_first36 (w : list bool) : list bool :=
  match w with [] => [false] | b::t => negb b :: t end.
Definition ground36 (x : sym) : bool :=
  match x with S2 => true | _ => false end.
Definition live36 (x : sym) : bool :=
  match x with S3 => true | _ => false end.
Fixpoint render36 (previous : bool) (v : list sym) : list bool :=
  match v with
  | [] => if previous then [false] else []
  | x::t => xorb (ground36 x) previous :: render36 (live36 x) t
  end.

Lemma render36_toggle v :
  flip_first36 (render36 false v) = render36 true v.
Proof. destruct v as [|[] t]; reflexivity. Qed.

(** At a 3 the head briefly visits one already processed right neighbor.
    At a rightmost 3 the same excursion creates the appended 2. *)
Lemma return_cell36 : forall x q rs, x <> S0 ->
  AL (lift_side (x::q)) (lift_side (List.map data_symbol rs)) ==>*
  AL (lift_side q) (lift_side (List.map data_symbol
       (ground36 x :: if live36 x then flip_first36 rs else rs))).
Proof.
  intros x q rs H. destruct x; try contradiction.
  - one36. done36.
  - one36. done36.
  - destruct rs as [|b t].
    + do 5 one36.
      change (AL (lift_side q) (Cons S2 (Cons S2 (Cons S0 zeroes))) ==>*
              AL (lift_side q) (Cons S2 (Cons S2 zeroes))).
      rewrite <- (const_unfold _ S0). done36.
    + destruct b; do 3 one36; done36.
  - one36. done36.
Qed.

Lemma return_word36 : forall v q, Forall (fun x => x <> S0) v ->
  AL (lift_side (List.rev v ++ q)) zeroes ==>*
  AL (lift_side q) (lift_side (List.map data_symbol (render36 false v))).
Proof.
  induction v as [|x v IH]; intros q valid.
  - done36.
  - inversion valid as [|? ? X V]; subst. rewrite rev36_cons_app.
    eapply evstep_trans; [apply (IH (x::q) V)|].
    assert (K : render36 false (x::v) =
      ground36 x :: if live36 x then flip_first36 (render36 false v) else render36 false v).
    { destruct x; cbn [render36 live36 ground36 xorb]; try reflexivity.
      now rewrite render36_toggle. }
    rewrite K. apply return_cell36. exact X.
Qed.

Lemma render36_binary previous bits :
  render36 previous (List.map mark_symbol36 bits) =
    deriv36 previous bits ++ carry36 previous bits.
Proof.
  revert previous. induction bits as [|b t IH]; intros prev.
  - destruct prev; reflexivity.
  - unfold carry36. rewrite last36_cons.
    destruct b, prev; cbn [List.map mark_symbol36 render36 live36 ground36 deriv36
      Bool.eqb xorb app]; rewrite IH; reflexivity.
Qed.

Definition raw36 d bits := List.rev (header_rev36 d) ++ List.map mark_symbol36 bits.
Lemma raw36_stack d bits : List.rev (raw36 d bits) = physical_row36 d (List.rev bits).
Proof.
  unfold raw36, physical_row36. rewrite rev_app_distr, rev_involutive, map_rev.
  reflexivity.
Qed.

Lemma raw36_nonblank d bits : Forall (fun x => x <> S0) (raw36 d bits).
Proof.
  unfold raw36. apply Forall_app. split.
  - destruct d as [|[|[|[|[|d]]]]]; cbn; repeat constructor; discriminate.
  - induction bits as [|[] t IH]; cbn; constructor; congruence.
Qed.

Lemma render36_header d bits :
  render36 false (raw36 d bits) = output36 d bits.
Proof.
  destruct d as [|[|[|[|[|d]]]]]; unfold raw36, output36;
    cbn [header_rev36 guard36 List.rev app render36 ground36 live36 xorb Nat.eqb];
    now rewrite render36_binary.
Qed.

Lemma lift_side_prepend36 (xs : list sym) :
  Str_app xs zeroes = lift_side xs.
Proof. induction xs as [|x t IH]; [reflexivity|]. cbn. now rewrite IH. Qed.

Theorem step36_physical w v :
  step36 w = Some v -> progress line36 (checkpoint w) (checkpoint v).
Proof.
  unfold step36.
  destruct (mark36 w 0) as [d bits] eqn:M.
  destruct (d <? 6) eqn:D; [|discriminate]. apply Nat.ltb_lt in D.
  intro E. inversion E; subst. clear E.
  eapply progress_intro.
  - eapply step_right. reflexivity.
  - eapply evstep_trans.
    + pose proof (outward36 w [] 0 d [] d bits zeroes M eq_refl D) as O.
      rewrite app_nil_r, lift_side_prepend36 in O. exact O.
    + eapply evstep_step; [eapply step_left; reflexivity|].
      change (AL (lift_side (physical_row36 d (List.rev bits))) (Cons S0 zeroes) ==>*
              checkpoint (output36 d bits)).
      rewrite <- (const_unfold _ S0), <- raw36_stack.
      pose proof (return_word36 (raw36 d bits) [] (raw36_nonblank d bits)) as Ret.
      rewrite app_nil_r, render36_header in Ret. exact Ret.
Qed.
