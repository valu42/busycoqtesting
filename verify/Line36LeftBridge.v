(** Connecting the finite checker, absolute parities and the suffix ledger. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Left Line36LeftStep Line36Matching Line36Word
                            Line36Right Line36Halo.
Import ListNotations L36Left L36LeftStep.
Local Open Scope nat_scope.
Module L36LeftBridge.

Lemma physical_header_agrees d : physical_header d = guard36 d.
Proof. reflexivity. Qed.
Lemma derivative_agrees b m : derivative b m = deriv36 b m.
Proof. revert b; induction m as [|x r IH]; intros b; [reflexivity|]. cbn; now rewrite IH. Qed.

(** Uniformly renaming both checkerboard colours preserves every fee. *)
Lemma scan_translate w p a k shift :
  scan w (xorb p shift) (xorb a shift) k =
  let '(z,m) := scan w p a k in (xorb z shift,m).
Proof.
  revert p a k. induction w as [|x r IH]; intros p a k; [reflexivity|].
  destruct x,p,a,shift; cbn [scan xorb negb Bool.eqb];
  first [exact (IH true true k) | exact (IH true false k) |
         exact (IH false true k) | exact (IH false false k) |
         exact (IH true true (S k)) | exact (IH true false (S k)) |
         exact (IH false true (S k)) | exact (IH false false (S k))].
Qed.

Lemma scan_append l r p a k :
  scan (l++r) p a k =
  let '(b,j) := scan l p a k in scan r (xorb p (Nat.odd (length l))) b j.
Proof.
  revert p a k. induction l as [|v l IH]; intros p a k.
  - destruct p; reflexivity.
  - cbn [app length]. rewrite nat_odd_succ.
    destruct v; cbn [scan]; rewrite IH; destruct p,(Nat.odd (length l)); reflexivity.
Qed.

Lemma scan_initial_count w p a k :
  scan w p a k =
  let '(z,j) := scan w p a 0 in (z,k+j).
Proof.
  revert p a k. induction w as [|v w IH]; intros p a k.
  - cbn [scan]; now rewrite Nat.add_0_r.
  - destruct v; cbn [scan]; [apply IH|].
    destruct (Bool.eqb p a); [apply IH|].
    rewrite (IH _ _ (S k)), (IH _ _ 1). destruct (scan w (negb p) p 0); cbn. f_equal. lia.
Qed.

Lemma scan_closing_anchor w p a a' k k' :
  In false w -> fst (scan w p a k) = fst (scan w p a' k').
Proof.
  revert p a a' k k'. induction w as [|v w IH]; intros p a a' k k' I;
  [contradiction|].
  destruct v; cbn [scan].
  - destruct I as [I|I]; [discriminate|]. now apply IH.
  - rewrite (scan_initial_count w (negb p) p (if Bool.eqb p a then k else S k)) at 1.
    rewrite (scan_initial_count w (negb p) p (if Bool.eqb p a' then k' else S k')) at 1.
    destruct (scan w (negb p) p 0); reflexivity.
Qed.

(** At the cell of parity p, the gap ledger's current flag means that the
    last closing differs from the opposite parity. *)
Lemma scan_gap w p a k :
  let '(b,j) := scan w p a k in
  let '(n,g) := gap_scan w (xorb a (negb p)) in
  j=k+n /\ g=xorb b (negb (xorb p (Nat.odd (length w)))).
Proof.
  revert p a k. induction w as [|v w IH]; intros p a k.
  - destruct p,a; cbn; lia || auto.
  - cbn [length]. rewrite nat_odd_succ. destruct v.
    + cbn [scan gap_scan]. specialize (IH (negb p) a k).
      destruct p,a; cbn [xorb negb cell_gap cell_fee] in IH |- *;
      destruct (scan w _ _ _) as [b j], (gap_scan w _) as [n g];
      destruct b,(Nat.odd (length w)); cbn in *; tauto.
    + cbn [scan gap_scan]. specialize (IH (negb p) p (if Bool.eqb p a then k else S k)).
      destruct p,a; cbn [xorb negb cell_gap cell_fee Bool.eqb bit_cost] in IH |- *;
      destruct (scan w _ _ _) as [b j], (gap_scan w _) as [n g];
      destruct b,(Nat.odd (length w)); cbn in *; intuition lia.
Qed.

Definition rounded_debt (old beta bridge : bool) (d : nat) :=
  let low := d - (if negb (Bool.eqb old bridge) then 1 else 0) in
  if Bool.eqb (Nat.odd low) (xorb old beta) then low else S low.

Lemma rounded_debt_fee old bridge d :
  rounded_debt old (xorb bridge (Nat.odd d)) bridge d =
  debt_fee d (xorb old bridge).
Proof.
  destruct d as [|m]; [destruct old,bridge; reflexivity|].
  unfold rounded_debt, debt_fee.
  destruct old,bridge; cbn [Bool.eqb xorb negb bit_cost];
  rewrite ?Nat.sub_0_r; cbn [Nat.sub]; rewrite ?Nat.sub_0_r, !nat_odd_succ;
  destruct (Nat.odd m); cbn; lia.
Qed.

Lemma bridge_cost_ledger old last bridge d previous q :
  (q = true -> d=0) ->
  let e := xorb old bridge in
  let g := xorb last (negb bridge) in
  let open := Bool.eqb previous q in
  (Z.of_nat (cell_fee open g) +
   Z.of_nat (bit_cost (xorb (cell_gap open g) (if q then e else Nat.odd d))) -
   Z.of_nat (if q then 0 else debt_fee d e) <=
   bridge_cost old last (xorb bridge (Nat.odd d)) bridge d previous)%Z.
Proof.
  intros Q. cbv zeta.
  unfold bridge_cost. fold (rounded_debt old (xorb bridge (Nat.odd d)) bridge d).
  rewrite rounded_debt_fee.
  destruct d as [|m].
  - destruct old,last,bridge,previous,q; vm_compute; discriminate || lia.
  - assert (q=false) by (destruct q; [specialize (Q eq_refl); discriminate|reflexivity]).
    subst q. cbn [Nat.eqb]. destruct old,last,bridge,previous,(Nat.odd (S m));
    cbn [Bool.eqb xorb negb cell_fee cell_gap change bit_cost]; lia.
Qed.
End L36LeftBridge.
