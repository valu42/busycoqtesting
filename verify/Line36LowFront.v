(** A certified finite-debt edge advances an actual normalized machine word. *)
From Coq Require Import List Arith ZArith Lia.
From BusyCoq Require Import Line36FiniteHistory Line36History Line36HistoryParse
  Line36Realize Line36Front Line36Left Line36LeftStep Line36LeftParse
  Line36Word Line36Tiles Line36Charge.
Import ListNotations L36FiniteHistory L36History L36HistoryParse
       L36Left L36LeftStep L36LeftParse L36Tiles.
Local Open Scope nat_scope.

Theorem low_front36 f w'
  (Valid:fvalid f) (Pieces:5<=length (fchoices f))
  (Advanced:step36 (fword f)=Some w') :
  let h:= firstn 3 (ftail f) in let tail:=skipn 3 (ftail f) in
  let d:=fst (mark36 tail 0) in d<=28 ->
  exists hist, hist<16 /\ forall e,
  L36LeftStep.step (fstate f) hist d=Some e ->
  exists g exposed rest,
    fvalid g /\ fword g=w' /\ fstate g=target e /\ fphase g=next (fphase f) /\
    ftail g=exposed++rest /\ In false (fprefix g) /\
    known_image (fprefix f++h) d=fprefix g++exposed /\
    fst (mark36 (fprefix f++h) d)=phase_guard (fphase f) /\
    dx e = (Z.of_nat (length (fprefix g))-Z.of_nat (length (fprefix f)))%Z /\
    charge e = checked_charge (fprefix f) h (fprefix g) exposed
                    (length (guard36 (phase_guard (fphase f)))) d.
Proof.
  intros h tail d Small.
  destruct (finite_history_semantics f d Valid Pieces Small) as [hist [Hi Transfer]].
  exists hist. split; [exact Hi|]. intros edge Step.
  destruct (Transfer edge Step) as [cs [exposed Info]].
  set (dest:=target edge) in *.
  set (p:=parsed_front (phase dest) cs (partial_choice dest) (partial_len dest)).
  cbv zeta in Info; fold dest p h in Info.
  destruct Info as [Shown [Ph [K [L [H [N [Closing [Dx C]]]]]]]].
  assert (Hp:fphase f<6) by apply Valid.
  destruct (step_success_wf (fstate f) hist d edge Hp Step) as [W X].
  change (phase (fstate f)) with (fphase f) in X.
  assert (HG : length (guard36 (phase_guard (fphase f)))=phase_header (fphase f)).
  { remember (fphase f) as ph. cases_six ph; reflexivity. }
  assert (Size:length p<=length (fprefix f)+length (guard36 (phase_guard (fphase f)))).
  { rewrite HG. lia. }
  assert (Split:ftail f=h++tail) by (unfold h,tail; symmetry;apply firstn_skipn).
  destruct (realize_front36 f dest cs h tail w' (phase_guard (fphase f)) exposed
             Valid Split Advanced Shown W K L H N Size)
    as [g [rest [G [S [P [Tail [Word [Cs Phg]]]]]]]].
  fold p in P. exists g,exposed,rest.
  destruct (observed_image _ _ _ _ Shown) as [Image Guard].
  rewrite P. repeat split; try assumption; try congruence. all: apply G.
Qed.
