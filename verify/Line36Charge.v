(** The moving-cut charge in the native finite enumerator is an upper
    bound on the change of the physical, anchored switch count. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Word Line36Right Line36Halo Line36CapModel Line36CapHalo
  Line36Left Line36Tiles Line36LeftStep Line36LeftBridge Line36Seed Line36CapBridge.
Import ListNotations.
Import L36LeftStep L36LeftBridge.
Local Open Scope nat_scope.

Definition charge_scan (flip : bool) (p w : list bool) :=
  let anchor := fst (scan p flip false 0) in
  scan w (xorb (Nat.odd (length p)) flip) anchor 0.

Lemma scan_last_color w pos a k :
  fst (scan w pos a k) = L36Seed.last_color w pos a.
Proof.
  revert pos a k. induction w as [|b w IH]; intros pos a k; [reflexivity|].
  destruct b; cbn [scan L36Seed.last_color]; apply IH.
Qed.

Lemma scanner_anchor flip p : In false p ->
  fst (scan p flip false 0) = xorb (L36Seed.last_color p false true) flip.
Proof.
  intros H. rewrite (scan_closing_anchor p flip false (xorb true flip) 0 0 H).
  replace flip with (xorb false flip) at 1 by (destruct flip; reflexivity).
  rewrite scan_translate, <- (scan_last_color p false true 0).
  destruct (scan p false true 0); reflexivity.
Qed.

Definition budget_align (p : list bool) :=
  Bool.eqb (L36Seed.last_color p false true) (Nat.odd (length p)).

Lemma charge_scan_gap flip p w : In false p ->
  let '(color,k) := charge_scan flip p w in
  let '(j,g) := gap_scan w (budget_align p) in
  j=k /\ g = xorb color (negb (xorb flip (Nat.odd (length (p++w))))).
Proof.
  intros H. unfold charge_scan. rewrite scanner_anchor by exact H.
  set (pos:=Nat.odd (length p)). set (old:=L36Seed.last_color p false true).
  pose proof (scan_gap w (xorb pos flip) (xorb old flip) 0) as L.
  unfold budget_align. fold pos old.
  replace (xorb (xorb old flip) (negb (xorb pos flip))) with (Bool.eqb old pos) in L
    by (destruct pos,old,flip; reflexivity).
  destruct (scan w (xorb pos flip) (xorb old flip) 0) as [color k].
  destruct (gap_scan w (Bool.eqb old pos)) as [j g]. destruct L as [E ->].
  rewrite length_app, Nat.odd_add. fold pos.
  split; [lia|]. destruct pos, flip, (Nat.odd (length w)); reflexivity.
Qed.

Lemma charge_tail_gap w pos prev :
  L36Seed.tail_charge w pos prev = gap_cost w (Bool.eqb prev pos).
Proof.
  revert pos prev. induction w as [|b w IH]; intros [] [];
    try reflexivity; destruct b; cbn [L36Seed.tail_charge gap_cost]; rewrite IH; reflexivity.
Qed.

Lemma budget_gap_eq p w : L36Seed.budget p w = gap_cost w (budget_align p).
Proof. apply charge_tail_gap. Qed.

Definition checked_charge p halo p' exposed h d :=
  let '(old,k) := charge_scan false p halo in
  let '(final,k') := charge_scan (Nat.even h) p' exposed in
  let y := length p + 3 in
  let prev := andb (Nat.eqb d 0) (last (p++halo) false) in
  (Z.of_nat k' + bridge_cost old final (Nat.odd (y+d+1)) (Nat.odd (y+1)) d prev
   - Z.of_nat k)%Z.

Lemma bridge_parity y d : Nat.odd (y+d+1) = xorb (Nat.odd (y+1)) (Nat.odd d).
Proof. rewrite !Nat.odd_add. destruct (Nat.odd y), (Nat.odd d); reflexivity. Qed.

Lemma bridge_odd y : Nat.odd (y+1) = negb (Nat.odd y).
Proof. rewrite Nat.odd_add. destruct (Nat.odd y); reflexivity. Qed.

Lemma flip_image h y :
  negb (xorb (Nat.even h) (Nat.odd (h+y))) = Nat.odd y.
Proof. rewrite Nat.odd_add, <- Nat.negb_odd. destruct (Nat.odd h),(Nat.odd y); reflexivity. Qed.

Theorem checked_charge_bound p halo p' exposed head pre cap d bits :
  length halo = 3 -> In false p -> In false p' ->
  length (p'++exposed) = head + length (p++halo) ->
  existsb negb cap = true -> existsb id (snd (mark36 cap 0)) = true ->
  mark36 (pre++cap) 0 = (d,bits) ->
  let prev := andb (Nat.eqb d 0) (last (p++halo) false) in
  (Z.of_nat (L36Seed.budget p' (exposed++body36 prev bits)) <=
    Z.of_nat (L36Seed.budget p (halo++pre++cap)) +
    checked_charge p halo p' exposed head d +
    Z.of_nat (bit_cost (negb (last bits prev))) -
    Z.of_nat (cap_loss (cap_after_anchor cap)))%Z.
Proof.
  intros Hh Hp Hp' L Anchor Live M.
  destruct (cap_halo_inputs pre cap Anchor Live) as [before [Et InBits]].
  rewrite M in InBits. cbn [snd] in InBits. rewrite Et in M.
  set (prev := andb (Nat.eqb d 0) (last (p++halo) false)).
  pose proof (halo_moving_cut halo exposed before (cap_after_anchor cap) d bits
      (budget_align p) (budget_align p') prev M InBits) as Bound.
  cbv zeta in Bound |- *. rewrite !budget_gap_eq.
  rewrite <- Et in Bound.
  unfold checked_charge. fold prev.
  pose proof (charge_scan_gap false p halo Hp) as O.
  pose proof (charge_scan_gap (Nat.even head) p' exposed Hp') as N.
  destruct (charge_scan false p halo) as [old k].
  destruct (charge_scan (Nat.even head) p' exposed) as [final k'].
  destruct (gap_scan halo (budget_align p)) as [k0 e].
  destruct (gap_scan exposed (budget_align p')) as [k1 g].
  destruct O as [-> ->]. destruct N as [-> ->].
  rewrite L, flip_image in Bound.
  assert (Len : length (p++halo) = length p + 3) by now rewrite length_app,Hh.
  rewrite Len in Bound.
  set (y := length p + 3) in *.
  assert (Q : hd false bits = true -> d = 0).
  { destruct bits as [|b t]; [discriminate|]. destruct b;
      [intros _; exact (live_prefix_no_debt _ _ _ M)|discriminate]. }
  pose proof (bridge_cost_ledger old final (Nat.odd (y+1)) d prev (hd false bits) Q) as Fee.
  cbv zeta in Fee. rewrite bridge_odd in Fee.
  rewrite bridge_parity,bridge_odd. cbn [xorb negb] in Bound.
  rewrite negb_involutive in Fee.
  lia.
Qed.

Definition known_image (known : list bool) (d:nat) :=
  let '(guard,bits) := mark36 known d in
  guard36 guard ++ deriv36 (Nat.eqb guard 1) bits.

Lemma known_update_split known tail out d bits :
  known <> [] -> mark36 tail 0 = (d,bits) -> step36 (known++tail) = Some out ->
  let prev := andb (Nat.eqb d 0) (last known false) in
  out = known_image known d ++ body36 prev bits.
Proof.
  intros Non M. unfold step36, known_image. rewrite mark36_app, M.
  destruct (mark36 known d) as [guard kb] eqn:K.
  destruct (guard <? 6); [|discriminate]. intros [= <-].
  unfold output36, body36, carry36. rewrite deriv36_app, last36_app.
  pose proof (L36CapBridge.final_mask known d (guard =? 1) Non) as E.
  rewrite K in E. cbn [snd] in E. rewrite E, (andb_comm (last known false)).
  now rewrite !app_assoc.
Qed.

Lemma known_image_length w d :
  length (known_image w d) = length (guard36 (fst (mark36 w d))) + length w.
Proof.
  unfold known_image. pose proof (mark36_length w d) as L.
  destruct (mark36 w d). cbn [fst snd] in *. rewrite length_app,L36CapBridge.derivative_length,L.
  reflexivity.
Qed.

Theorem physical_charge_bound p halo pre cap out z d :
  length halo = 3 -> In false p ->
  existsb negb cap = true -> existsb id (snd (mark36 cap 0)) = true ->
  fst (mark36 (pre++cap) 0) = d ->
  step36 ((p++halo) ++ (pre++cap)) = Some out ->
  let old := p ++ halo in
  let shown := known_image old d in
  let head := length (guard36 (fst (mark36 old d))) in
  z <= length shown -> In false (firstn z shown) ->
  (Z.of_nat (L36Seed.budget (firstn z out) (skipn z out)) <=
    Z.of_nat (L36Seed.budget p (halo++pre++cap)) +
    checked_charge p halo (firstn z shown) (skipn z shown) head d +
    Z.of_nat (bit_cost (negb (last (pre++cap) false))) -
    Z.of_nat (cap_loss (cap_after_anchor cap)))%Z.
Proof.
  intros Hh Hp A Live Hd Step. cbv zeta.
  set (old:=p++halo) in *.
  set (shown:=known_image old d).
  intros Hz Hp'.
  destruct (mark36 (pre++cap) 0) as [de bits] eqn:M. cbn [fst] in Hd. subst de.
  assert (Nold : old<>[]) by (unfold old; intros E; apply app_eq_nil in E;
                              destruct E as [-> _]; contradiction).
  assert (Nt : pre++cap<>[]) by (intros E; apply app_eq_nil in E;
                                 destruct E as [_ ->]; discriminate).
  set (prev:=andb (d=?0) (last old false)).
  pose proof (known_update_split old (pre++cap) out d bits Nold M Step) as Image.
  cbv zeta in Image. fold shown prev in Image.
  pose proof (L36CapBridge.final_mask (pre++cap) 0 prev Nt) as Final.
  rewrite M in Final. cbn [snd Nat.eqb] in Final. rewrite andb_true_r in Final.
  assert (Z0 : z-length shown=0) by lia.
  assert (Pz : firstn z out = firstn z shown).
  { rewrite Image, firstn_app, Z0, firstn_O, app_nil_r. reflexivity. }
  assert (Tz : skipn z out = skipn z shown ++ body36 prev bits).
  { rewrite Image, skipn_app, Z0. reflexivity. }
  rewrite Pz,Tz.
  pose proof (checked_charge_bound p halo (firstn z shown) (skipn z shown)
            (length (guard36 (fst (mark36 old d)))) pre cap d bits Hh Hp Hp') as B.
  rewrite firstn_skipn in B. specialize (B (known_image_length old d) A Live M).
  cbv zeta in B. fold old prev in B. rewrite Final in B. exact B.
Qed.

(** A successful representative evaluation uses exactly the function above
    on its own known words.  The translation from a real prefix to its
    finite representative is independent of this evaluation identity. *)
Theorem evaluator_charge_projection s history d edge :
  L36LeftStep.step s history d = Some edge ->
  let p := representative s history in
  let halo := halo_word (L36Left.halo s) in
  let shown := known_image (p++halo) d in
  let head := length (guard36 (fst (mark36 (p++halo) d))) in
  exists z,
    L36Left.dx edge = (Z.of_nat z - Z.of_nat (length p))%Z /\
    L36Left.charge edge =
      checked_charge p halo (firstn z shown) (skipn z shown) head d.
Proof.
  unfold L36LeftStep.step,prepare,evaluate; cbv zeta.
  set (p := representative s history). set (halo := halo_word (L36Left.halo s)).
  set (o := fst (scan p false false 0)).
  destruct (scan halo (Nat.odd (length p)) o 0) as [old k] eqn:O.
  cbn [full x old_color old_switches]. unfold known_image.
  destruct (mark36 (p++halo) d) as [guard bits]. cbn [fst].
  destruct (negb (guard =? L36Tiles.phase_guard (L36Left.phase s))); [discriminate|].
  rewrite physical_header_agrees,derivative_agrees.
  set (head := length (guard36 guard)).
  set (shown := guard36 guard ++ deriv36 (guard =? 1) bits).
  destruct (read_piece (pre (S (L36Left.phase s) mod 6)) (firstn (length p+head) shown))
    as [n [r|]]; [|discriminate].
  destruct (reparse 24 (S (L36Left.phase s) mod 6) 0 0 false n r)
    as [parsed|]; [|discriminate].
  destruct (complete parsed <? piece_count (L36Left.kind s)-4); [discriminate|].
  destruct (encode_halo (skipn (cut parsed) shown) =? 8) eqn:Hsize; [discriminate|].
  set (z:=cut parsed). fold z.
  set (a:= fst (scan (firstn z shown) (Nat.even head) false 0)).
  destruct (scan (skipn z shown) (xorb (Nat.odd z) (Nat.even head)) a 0)
    as [final k'] eqn:N. intros [= <-].
  exists z. split; [reflexivity|].
  cbn [L36Left.charge]. unfold checked_charge,charge_scan. fold o.
  rewrite xorb_false_r, O. fold a.
  assert (Hz : z <= length shown).
  { destruct (le_dec z (length shown)); [assumption|].
    fold z in Hsize. rewrite skipn_all2 in Hsize by lia. discriminate. }
  rewrite firstn_length_le by exact Hz. rewrite N. reflexivity.
Qed.

Lemma anchor_splice flip a b common : In false common ->
  fst (scan (b++common) flip false 0) =
  xorb (fst (scan (a++common) flip false 0))
       (xorb (Nat.odd (length a)) (Nat.odd (length b))).
Proof.
  intro H. rewrite !scan_append.
  destruct (scan a flip false 0) as [ca ka], (scan b flip false 0) as [cb kb].
  set (shift:=xorb (Nat.odd (length a)) (Nat.odd (length b))).
  set (pa:=xorb flip (Nat.odd (length a))).
  replace (xorb flip (Nat.odd (length b))) with (xorb pa shift)
    by (unfold shift,pa; destruct flip,(Nat.odd (length a)),(Nat.odd (length b)); reflexivity).
  rewrite (scan_closing_anchor common (xorb pa shift) cb (xorb ca shift) kb ka H).
  rewrite scan_translate. destruct (scan common pa ca ka); reflexivity.
Qed.

Lemma charge_scan_splice flip a b common tail : In false common ->
  let shift := xorb (Nat.odd (length a)) (Nat.odd (length b)) in
  let '(v,k) := charge_scan flip (a++common) tail in
  charge_scan flip (b++common) tail = (xorb v shift,k).
Proof.
  intros H. unfold charge_scan. rewrite (anchor_splice flip a b common H).
  set (shift:=xorb (Nat.odd (length a)) (Nat.odd (length b))).
  set (start:=xorb (Nat.odd(length(a++common))) flip).
  replace (xorb (Nat.odd (length (b++common))) flip) with (xorb start shift)
    by (unfold start,shift; rewrite !length_app,!Nat.odd_add;
        destruct flip,(Nat.odd (length a)),(Nat.odd (length b)),(Nat.odd(length common));
        reflexivity).
  rewrite scan_translate. destruct (scan tail start _ 0); reflexivity.
Qed.

Lemma bridge_cost_splice old final beta bridge d prev shift :
  bridge_cost (xorb old shift) (xorb final shift) (xorb beta shift) (xorb bridge shift) d prev
  = bridge_cost old final beta bridge d prev.
Proof. destruct old,final,beta,bridge,shift; reflexivity. Qed.

Lemma last_behind_closing a b common halo : In false common ->
  last ((a++common)++halo) false = last ((b++common)++halo) false.
Proof.
  intro H. rewrite !last36_app. destruct common as [|x c]; [contradiction|].
  now rewrite !last36_cons.
Qed.

Lemma add_parity_shift (a b c:list bool) n :
  Nat.odd (length (b++c)+n) =
  xorb (Nat.odd (length (a++c)+n)) (xorb (Nat.odd (length a)) (Nat.odd (length b))).
Proof.
  rewrite !length_app,!Nat.odd_add. destruct (Nat.odd (length a)),(Nat.odd (length b)),
    (Nat.odd (length c)),(Nat.odd n); reflexivity.
Qed.

Theorem checked_charge_splice a b a' b' common common' halo exposed head d :
  length a'=length a -> length b'=length b ->
  In false common -> In false common' ->
  checked_charge (a++common) halo (a'++common') exposed head d =
  checked_charge (b++common) halo (b'++common') exposed head d.
Proof.
  intros La Lb Old New. unfold checked_charge.
  pose proof (charge_scan_splice false a b common halo Old) as O.
  pose proof (charge_scan_splice (Nat.even head) a' b' common' exposed New) as N.
  cbv zeta in O,N. rewrite La,Lb in N.
  destruct (charge_scan false (a++common) halo) as [old k].
  destruct (charge_scan (Nat.even head) (a'++common') exposed) as [final k'].
  rewrite O,N, <- (last_behind_closing a b common halo Old).
  rewrite <- !Nat.add_assoc.
  rewrite (add_parity_shift a b common (3+(d+1))), (add_parity_shift a b common (3+1)).
  rewrite bridge_cost_splice. reflexivity.
Qed.

Lemma checked_positive_debt p halo p' exposed head d :
  0 < d -> In false p' -> closing_count exposed <= 1 ->
  (checked_charge p halo p' exposed head d <= 3-Z.of_nat d)%Z.
Proof.
  intros D A Few. unfold checked_charge.
  pose proof (charge_scan_gap (Nat.even head) p' exposed A) as Eq.
  pose proof (gap_scan_charges_closings exposed (budget_align p')) as Kbound.
  destruct (charge_scan false p halo) as [old k].
  destruct (charge_scan (Nat.even head) p' exposed) as [final k'].
  destruct (gap_scan exposed (budget_align p')) as [j g].
  destruct Eq as [-> _]; cbn [fst] in Kbound.
  destruct d as [|d]; [lia|]. unfold bridge_cost.
  cbn [Nat.eqb andb]. unfold change.
  destruct (negb (Bool.eqb old (Nat.odd (length p + 3 + 1))));
  destruct (Bool.eqb (Nat.odd _) (xorb _ _));
  destruct (Bool.eqb final _); lia.
Qed.
