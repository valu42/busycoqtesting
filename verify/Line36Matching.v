(** Right-to-left matching for the binary word at a line-36 checkpoint.
    [true] is an opening. Words and masks are in left-to-right tape order. *)
From Coq Require Import List Bool ZArith Lia.
Import ListNotations.

Fixpoint bal36 (w : list bool) : Z :=
  match w with
  | [] => 0%Z
  | b :: r => ((if b then 1 else -1) + bal36 r)%Z
  end.

Fixpoint mark36 (w : list bool) (incoming : nat) : nat * list bool :=
  match w with
  | [] => (incoming, [])
  | b :: r =>
      let '(d, bits) := mark36 r incoming in
      if b then
        match d with
        | 0 => (0, true :: bits)
        | S k => (k, false :: bits)
        end
      else (S d, false :: bits)
  end.

Fixpoint openings36 (bits : list bool) : nat :=
  match bits with
  | [] => 0
  | true :: r => S (openings36 r)
  | false :: r => openings36 r
  end.

Lemma bal36_app l r : bal36 (l ++ r) = (bal36 l + bal36 r)%Z.
Proof. induction l as [|[] l IH]; cbn [app bal36]; rewrite ?IH; lia. Qed.

Lemma mark36_app l r n :
  mark36 (l ++ r) n =
  let '(d, b) := mark36 r n in
  let '(e, a) := mark36 l d in (e, a ++ b).
Proof.
  induction l as [|x l IH]; cbn; destruct (mark36 r n) as [d b] eqn:E.
  - reflexivity.
  - rewrite IH. destruct (mark36 l d) as [e a]. destruct x, e; reflexivity.
Qed.

Lemma mark36_length w n : length (snd (mark36 w n)) = length w.
Proof.
  induction w as [|x w IH]; cbn; auto.
  destruct (mark36 w n) as [d bits]. destruct x, d; cbn in *; congruence.
Qed.

Lemma mark36_balance w n :
  (Z.of_nat (openings36 (snd (mark36 w n))) - Z.of_nat (fst (mark36 w n))
   = bal36 w - Z.of_nat n)%Z.
Proof.
  induction w as [|x w IH]; cbn; try lia.
  destruct (mark36 w n) as [d bits]. destruct x, d;
    cbn [fst snd openings36] in *; rewrite ?Nat2Z.inj_succ in *; lia.
Qed.

(** Erase the rightmost [extra] live openings, passing through all other cells. *)
Fixpoint erase36 (bits : list bool) (extra : nat) : nat * list bool :=
  match bits with
  | [] => (extra, [])
  | b :: r =>
      let '(d, tail) := erase36 r extra in
      if b then
        match d with
        | 0 => (0, true :: tail)
        | S k => (k, false :: tail)
        end
      else (d, false :: tail)
  end.

Lemma erase36_excess bits k :
  fst (erase36 bits k) = k - openings36 bits.
Proof.
  induction bits as [|b bits IH]; cbn; try lia.
  destruct (erase36 bits k) as [e tail]. cbn in IH.
  destruct b, e; cbn [fst openings36]; lia.
Qed.

Lemma mark36_more w n k :
  mark36 w (n+k) =
  let '(d,bits) := mark36 w n in
  let '(e,tail) := erase36 bits k in (d+e,tail).
Proof.
  induction w as [|b w IH]; cbn; auto.
  rewrite IH. destruct (mark36 w n) as [d bits].
  destruct b, d; cbn; destruct (erase36 bits k) as [e tail]; destruct e;
    cbn; reflexivity.
Qed.

Lemma mark36_shield w n :
  (Z.of_nat n <= bal36 w)%Z ->
  fst (mark36 w n) = fst (mark36 w 0).
Proof.
  intro H. pose proof (mark36_balance w 0) as HB.
  replace n with (0+n) at 1 by lia. rewrite mark36_more.
  destruct (mark36 w 0) as [d bits]. cbn [fst snd] in *.
  pose proof (erase36_excess bits n) as HE.
  destruct (erase36 bits n) as [e tail]. cbn in HE |- *; lia.
Qed.

(** An arbitrarily complicated left prefix receives exactly the same debt for
    all sufficiently small demands on the right. Its entire survivor mask is
    consequently determined before the exterior continuation is known. *)
Lemma mark36_prefix_shield l w n :
  (Z.of_nat n <= bal36 w)%Z ->
  mark36 (l++w) n =
  let '(e,a) := mark36 l (fst (mark36 w 0)) in
  (e, a ++ snd (mark36 w n)).
Proof.
  intros H. rewrite mark36_app. pose proof (mark36_shield w n H) as E.
  destruct (mark36 w n) as [d bits]; cbn in E |- *; rewrite E; reflexivity.
Qed.

Lemma erase36_all bits k :
  openings36 bits <= k ->
  erase36 bits k = (k - openings36 bits, repeat false (length bits)).
Proof.
  induction bits as [|b bits IH]; cbn; intros H.
  - f_equal; lia.
  - destruct b; cbn in H |- *; rewrite IH by lia.
    + destruct (k - openings36 bits) as [|e] eqn:E; [lia|].
      f_equal; lia.
    + reflexivity.
Qed.

(** The boundary of the affected segment is an actual opening, ranked from
    the right among the openings that survive with empty exterior. *)
Theorem mark36_rank w k :
  0 < k <= openings36 (snd (mark36 w 0)) ->
  exists l r, w = l ++ true :: r /\
    fst (mark36 r 0) = 0 /\
    bal36 (true :: r) = Z.of_nat k /\
    mark36 (true :: r) k = (0,repeat false (S (length r))).
Proof.
  induction w as [|x w IH]; [cbn; lia|].
  cbn [mark36]. destruct (mark36 w 0) as [d bits] eqn:E.
  intros H. destruct (le_dec k (openings36 bits)) as [K|K].
  - destruct IH as [l [r [-> Hrest]]].
    + cbn in *. destruct x,d; cbn in *; lia.
    + exists (x :: l), r; split; [reflexivity|exact Hrest].
  - destruct x,d; cbn [snd openings36] in H; try lia.
    assert (Eq : k = S (openings36 bits)) by lia.
    exists [],w. split; [reflexivity|]. rewrite E. split; [reflexivity|].
    pose proof (mark36_balance w 0) as HB. rewrite E in HB. cbn [snd fst] in HB.
    split; [cbn [bal36]; lia|].
    replace k with (0+k) at 1 by lia. rewrite mark36_more.
    cbn [mark36]; rewrite E. rewrite erase36_all by (cbn; lia).
    rewrite <- (mark36_length w 0), E. cbn [fst snd openings36 length].
    replace (k - openings36 bits) with 1 by lia. reflexivity.
Qed.
