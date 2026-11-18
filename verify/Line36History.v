(** Finite-history factorization for the row-36 left cut. The reference
    identities actually compose at each piece boundary, including boundaries
    that fall strictly inside one six-piece tile. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Word Line36Tiles Line36Reference Line36Left Line36LeftStep.
Import ListNotations L36Tiles.
Local Open Scope nat_scope.

Module L36History.
Definition deposit ph k := fst (mark36 (phase_pieces ph k false) 0).
Definition previous ph k :=
  last (snd (mark36 (phase_pieces ph ((k+5) mod 6) false) (deposit ph k))) false.
Definition overlap ph k :=
  firstn (phase_header ph) (phase_pieces (next ph) k false).
Fixpoint boundary k (bits : list bool) :=
  match bits with [] => k | _::r => boundary (next k) r end.

Lemma boundary_bounded k cs : k < 6 -> boundary k cs < 6.
Proof. revert k. induction cs; cbn; auto using next_bound. Qed.

Lemma piece_boundary ph k b (Hp : ph < 6) (Hk : k < 6) :
  let '(d,s) := mark36 (phase_pieces ph k b) (deposit ph (next k)) in
  d = deposit ph k /\ last s (previous ph k) = previous ph (next k) /\
  overlap ph k ++ deriv36 (previous ph k) s =
        phase_pieces (next ph) k b ++ overlap ph (next k).
Proof. cases_six ph; cases_six k; destruct b; vm_compute; auto. Qed.

Lemma piece_flat ph k b (Hp : ph < 6) (Hk : k < 6) :
  fst (mark36 (phase_pieces ph k b) 0) = deposit ph k /\
  deposit ph k <= 1 /\ (1 <= bal36 (phase_pieces ph k b))%Z /\
  length (phase_pieces (next ph) k b) = length (phase_pieces ph k b).
Proof. cases_six ph; cases_six k; destruct b; vm_compute; repeat split; try reflexivity; try discriminate; try lia. Qed.

Lemma initial_boundary ph (Hp : ph<6) :
  let '(g,s) := mark36 (phase_prefix ph) (deposit ph 0) in
  g = phase_guard ph /\
  last s (g =? 1) = previous ph 0 /\
  guard36 g ++ deriv36 (g =? 1) s = phase_prefix (next ph) ++ overlap ph 0.
Proof. cases_six ph; vm_compute; auto. Qed.

Lemma pieces_boundary ph k cs (Hp : ph<6) (Hk : k<6) :
  let j := boundary k cs in
  let '(d,s) := mark36 (segments ph k cs) (deposit ph j) in
  d = deposit ph k /\ last s (previous ph k) = previous ph j /\
  overlap ph k ++ deriv36 (previous ph k) s =
        segments (next ph) k cs ++ overlap ph j.
Proof.
  revert k Hk. induction cs as [|b cs IH]; intros k Hk.
  - cbn [boundary segments mark36 last deriv36 app]. rewrite app_nil_r; auto.
  - cbn [boundary segments]. rewrite mark36_app.
    specialize (IH (next k) (next_bound k Hk)).
    cbn zeta in IH. destruct (mark36 (segments ph (next k) cs) _) as [dr sr] eqn:Er.
    destruct IH as [-> [R T]].
    pose proof (piece_boundary ph k b Hp Hk) as P.
    destruct (mark36 (phase_pieces ph k b) _) as [df sf].
    destruct P as [-> [F P]]. split; [reflexivity|].
    rewrite last36_app, F. split; [exact R|].
    rewrite deriv36_app, F, app_assoc, P, <- app_assoc, T, app_assoc. reflexivity.
Qed.

Definition observed (known : list bool) (d : nat) :=
  let '(g,s) := mark36 known d in (g, guard36 g ++ deriv36 (g =? 1) s).

(** Every older complete piece can be removed from the input and inserted
    unchanged in choice and length in the NEXT-phase output. The remaining
    word starts at an exact physical piece boundary and is independent of
    every removed choice. *)
Theorem signature_factor ph cs tail d bits (Hp : ph<6)
  (E : mark36 tail d = (deposit ph (boundary 0 cs),bits)) :
  observed (phase_prefix ph ++ segments ph 0 cs ++ tail) d =
  (phase_guard ph, phase_prefix (next ph) ++ segments (next ph) 0 cs ++
      overlap ph (boundary 0 cs) ++ deriv36 (previous ph (boundary 0 cs)) bits).
Proof.
  unfold observed. rewrite mark36_app, mark36_app, E.
  pose proof (pieces_boundary ph 0 cs Hp ltac:(lia)) as P. cbn zeta in P.
  destruct (mark36 (segments ph 0 cs) _) as [dc sc].
  destruct P as [-> [Pc Oc]].
  pose proof (initial_boundary ph Hp) as I.
  destruct (mark36 (phase_prefix ph) _) as [g sp]. destruct I as [-> [Ip Io]].
  f_equal. rewrite !deriv36_app, Ip, Pc, !app_assoc, Io.
  rewrite <- (app_assoc (phase_prefix (next ph)) (overlap ph 0)), Oc.
  now repeat rewrite app_assoc.
Qed.

Lemma prefix_debt_le l r : fst (mark36 l 0) <= fst (mark36 (l++r) 0).
Proof.
  rewrite mark36_app. destruct (mark36 r 0) as [d bits].
  pose proof (mark36_more l 0 d) as M. change (0+d) with d in M. destruct (mark36 l 0) as [u s].
  destruct (erase36 s d) as [v t]. rewrite M. cbn. lia.
Qed.

Lemma partial_debt ph k b part (Hp:ph<6) (Hk:k<6)
  (P : prefix part (phase_pieces ph k b)) : fst (mark36 part 0) <= 1.
Proof.
  destruct P as [r E]. pose proof (prefix_debt_le part r) as H.
  rewrite <- E in H. pose proof (piece_flat ph k b Hp Hk). lia.
Qed.

Lemma pieces_small_debt ph k cs part n (Hp:ph<6) (Hk:k<6)
  (H : fst (mark36 part n) <= 1) :
  fst (mark36 (segments ph k cs ++ part) n) <= 1.
Proof.
  revert k Hk. induction cs as [|b cs IH]; intros k Hk; [exact H|].
  cbn [segments]. rewrite <- app_assoc, mark36_app.
  specialize (IH (next k) (next_bound _ Hk)).
  destruct (mark36 (segments ph (next k) cs ++ part) n) as [q tail].
  cbn [fst] in IH. pose proof (piece_flat ph k b Hp Hk) as [D [Z [A _]]].
  pose proof (mark36_shield (phase_pieces ph k b) q ltac:(lia)) as S.
  destruct (mark36 (phase_pieces ph k b) q); cbn [fst] in *. lia.
Qed.

Lemma exterior_halo_bound h d : fst (mark36 h d) <= length h+d.
Proof.
  induction h as [|b h IH]; [cbn; lia|].
  cbn [mark36]. destruct (mark36 h d) as [g t].
  destruct b, g; cbn in *; lia.
Qed.

Definition four_kind k := next (next (next (next k))).

Lemma four_halo_debt ph k u v w z choice part halo d
   (Hp:ph<6) (Hk:k<6)
   (P:prefix part (phase_pieces ph (four_kind k) choice))
   (Hhalo:length halo<=3) (Hd:d<=28) :
  fst (mark36 (segments ph k [u;v;w;z] ++ part ++ halo) d) <= 1.
Proof.
  pose proof (four_piece_shield ph k u v w z choice part [false;false;false]
               Hp Hk P ltac:(cbn;lia)) as H.
  rewrite !balance_app in H. cbn [balance bal36] in H.
  pose proof (exterior_halo_bound halo d).
  rewrite app_assoc, mark36_app. destruct (mark36 halo d) as [a t]; cbn [fst] in *.
  assert (HH : (Z.of_nat a <= bal36 (segments ph k [u;v;w;z] ++ part))%Z).
  { rewrite bal36_app. unfold balance in *. lia. }
  pose proof (mark36_shield _ _ HH) as S.
  pose proof (pieces_small_debt ph k [u;v;w;z] part 0 Hp Hk
              (partial_debt ph (four_kind k) choice part Hp
                 ltac:(unfold four_kind; auto using next_bound) P)) as B.
  destruct (mark36 (segments ph k [u;v;w;z] ++ part) a); cbn [fst] in *; lia.
Qed.

Definition five_tail ph k a b c e f part halo :=
  segments ph k [a;b;c;e;f] ++ part ++ halo.

Lemma five_tail_debt ph k a b c e f choice part halo d
   (Hp:ph<6) (Hk:k<6)
   (P:prefix part (phase_pieces ph (four_kind (next k)) choice))
   (Hhalo:length halo<=3) (Hd:d<=28) :
  fst (mark36 (five_tail ph k a b c e f part halo) d) = deposit ph k.
Proof.
  pose proof (four_halo_debt ph (next k) b c e f choice part halo d
                 Hp (next_bound k Hk) P Hhalo Hd) as B.
  pose proof (piece_flat ph k a Hp Hk) as [M [_ [A _]]].
  unfold five_tail.
  change (segments ph k [a;b;c;e;f]) with
    (phase_pieces ph k a ++ segments ph (next k) [b;c;e;f]).
  rewrite <- app_assoc, mark36_app.
  destruct (mark36 (segments ph (next k) [b;c;e;f] ++ part ++ halo) d)
    as [u s]; cbn [fst] in B.
  pose proof (mark36_shield (phase_pieces ph k a) u ltac:(lia)) as S.
  destruct (mark36 (phase_pieces ph k a) u); cbn [fst] in *; congruence.
Qed.

Definition front ph cs := phase_prefix ph ++ segments ph 0 cs.

(** The two true outputs agree from their respective cuts at the OLDEST
    shared piece, even when the physically older material has different
    length, different choices, or a different number of six-piece cycles.
    [local] contains the complete known output through the halo. *)
Theorem five_history_replacement ph actual padded k a b c e f choice part halo d
   (Hp:ph<6) (Ha:boundary 0 actual=k) (Hb:boundary 0 padded=k)
   (P:prefix part (phase_pieces ph (four_kind (next k)) choice))
   (Hhalo:length halo<=3) (Hd:d<=28) :
   let common := five_tail ph k a b c e f part halo in
   exists local,
    observed (front ph actual ++ common) d =
       (phase_guard ph, front (next ph) actual ++ local) /\
    observed (front ph padded ++ common) d =
       (phase_guard ph, front (next ph) padded ++ local).
Proof.
  cbn zeta. assert (Hk:k<6) by (rewrite <-Ha; apply boundary_bounded; lia).
  pose proof (five_tail_debt ph k a b c e f choice part halo d Hp Hk P Hhalo Hd) as H.
  destruct (mark36 (five_tail ph k a b c e f part halo) d) as [q mask] eqn:E.
  cbn in H; subst q.
  pose proof (signature_factor ph actual _ d mask Hp ltac:(rewrite Ha;exact E)) as A.
  pose proof (signature_factor ph padded _ d mask Hp ltac:(rewrite Hb;exact E)) as B.
  rewrite Ha in A. rewrite Hb in B. unfold front. repeat rewrite <- app_assoc.
  exists (overlap ph k ++ deriv36 (previous ph k) mask). repeat rewrite <- app_assoc. split; [exact A|exact B].
Qed.

Lemma segments_next_length ph k cs : ph<6 -> k<6 ->
  length (segments (next ph) k cs) = length (segments ph k cs).
Proof.
  intros Hp Hk. revert k Hk.
  induction cs as [|b cs IH]; intros k Hk; [reflexivity|].
  cbn [segments]. rewrite !length_app, (IH _ (next_bound k Hk)).
  pose proof (piece_flat ph k b Hp Hk). lia.
Qed.
Lemma front_next_length ph cs : ph<6 -> length (front (next ph) cs) = length (front ph cs).
Proof.
  intro Hp. unfold front. rewrite !length_app, !phase_prefix_length by auto using next_bound.
  now rewrite segments_next_length by lia.
Qed.

Import L36Left L36LeftStep.
Lemma next_mod k : k<6 -> S k mod 6 = next k.
Proof. intro H; cases_six k; reflexivity. Qed.
Lemma piece_exact ph k b : ph<6 -> k<6 -> piece ph k b = phase_pieces ph k b.
Proof. intros P K; cases_six ph; cases_six k; destruct b; reflexivity. Qed.
Lemma pre_exact ph : ph<6 -> pre ph = phase_prefix ph.
Proof. intro P; cases_six ph; reflexivity. Qed.

Lemma read_piece_word p w :
  let '(n,o) := read_piece p w in
  w = firstn n p ++ skipn n w /\
  match o with Some r => n = length p /\ w = p ++ r | None => True end.
Proof.
  revert w. induction p as [|a p IH]; intros [|b w]; cbn [read_piece length firstn skipn]; try tauto.
  destruct (Bool.eqb a b) eqn:E; [apply Bool.eqb_prop in E; subst b|]; cbn; [|auto].
  specialize (IH w). destruct (read_piece p w) as [n [r|]]; cbn in IH |- *.
  - destruct IH as [A [B C]]. rewrite <- A at 1. split; [reflexivity|].
    split; congruence.
  - destruct IH as [A _]. split; [now rewrite <- A|trivial].
Qed.

Lemma reparse_readback gas ph k n prev pos w p :
  ph<6 -> k<6 -> reparse gas ph k n prev pos w = Some p ->
  exists cs r,
    w = segments ph k cs ++ firstn (partial p) (piece ph (next_kind p) (next_bit p)) ++ r /\
    next_kind p = boundary k cs /\ prev_bit p = last cs prev /\
    complete p = n+length cs /\ cut p = pos + length (segments ph k cs) + partial p.
Proof.
  revert k n prev pos w p. induction gas as [|gas IH];
    intros k n prev pos w p Hp Hk P; cbn [reparse] in P; [discriminate|].
  pose proof (read_piece_word (piece ph k false) w) as F.
  destruct (read_piece (piece ph k false) w) as [nf [rf|]] eqn:Ef.
  - destruct F as [_ [-> ->]]. rewrite (next_mod k Hk) in P.
    destruct (IH _ _ _ _ _ _ Hp (next_bound k Hk) P) as [cs [r [W [K [B [N C]]]]]].
    exists (false::cs), r. cbn [segments boundary length]. rewrite last36_cons.
    rewrite (piece_exact ph k false Hp Hk) in *. split.
    + rewrite <- app_assoc, W. reflexivity.
    + rewrite length_app. repeat split; try assumption; lia.
  - pose proof (read_piece_word (piece ph k true) w) as T.
    destruct (read_piece (piece ph k true) w) as [nt [rt|]] eqn:Et.
    + destruct T as [_ [-> ->]]. rewrite (next_mod k Hk) in P.
      destruct (IH _ _ _ _ _ _ Hp (next_bound k Hk) P) as [cs [r [W [K [B [N C]]]]]].
      exists (true::cs), r. cbn [segments boundary length]. rewrite last36_cons.
      rewrite (piece_exact ph k true Hp Hk) in *. split.
      * rewrite <- app_assoc, W. reflexivity.
      * rewrite length_app. repeat split; try assumption; lia.
    + destruct (nf <? nt); inversion P; subst p; cbn.
      * exists [], (skipn nt w); cbn. split; [apply T|]. repeat split; lia.
      * exists [], (skipn nf w); cbn. split; [apply F|]. repeat split; lia.
Qed.

Lemma piece_disjoint ph k a b l r : ph<6 -> k<6 ->
  phase_pieces ph k a ++ l = phase_pieces ph k b ++ r -> a=b.
Proof.
  intros Hp Hk E. destruct a,b; try reflexivity;
    cases_six ph; cases_six k; vm_compute in E; discriminate.
Qed.

Lemma segments_app ph k cs ds : segments ph k (cs++ds) =
  segments ph k cs ++ segments ph (boundary k cs) ds.
Proof. revert k; induction cs; intro k; cbn; [reflexivity|]. now rewrite IHcs, app_assoc. Qed.
Lemma boundary_app k cs ds : boundary k (cs++ds) = boundary (boundary k cs) ds.
Proof. revert k; induction cs; intro k; cbn; auto. Qed.

Lemma cancel_piece_prefix ph k older parsed left_tail right_tail
  (Hp: ph<6) (Hk:k<6) (Le : length older <= length parsed)
  (E: segments ph k older ++ left_tail = segments ph k parsed ++ right_tail) :
  exists suffix, parsed = older ++ suffix /\
  left_tail = segments ph (boundary k older) suffix ++ right_tail.
Proof.
  revert k parsed left_tail right_tail Hk Le E.
  induction older as [|a older IH]; intros k parsed tl tr Hk Le E.
  - exists parsed. auto.
  - destruct parsed as [|b parsed]; [cbn in Le; lia|]. cbn [segments] in E.
    rewrite <- !app_assoc in E.
    pose proof (piece_disjoint ph k a b _ _ Hp Hk E) as ->.
    apply app_inv_head in E.
    destruct (IH (next k) parsed tl tr (next_bound k Hk) ltac:(cbn in Le;lia) E)
      as [ys [A B]]. exists ys. cbn. split; [now rewrite A|exact B].
Qed.
End L36History.
