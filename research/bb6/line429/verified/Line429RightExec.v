(* The right sweep of normalized line 429 as a finite-word transducer.
   Input and output words are ordered nearest to farthest from the head. *)
From BusyCoq Require Import Individual62 Line429Engine Line429RightSweep.
From Coq Require Import List Arith Lia.
Import ListNotations Bell429.
Open Scope list_scope.
Open Scope sym_scope.

Module RightExec429.
Inductive phase := fresh | pending0 | pending01.
Definition buffer h : list Sym :=
  match h with fresh => [] | pending0 => [0] | pending01 => [0;1] end.

Record answer := out { left_prefix : list Sym; right_remainder : list Sym; moves : nat }.
Definition add_moves (k:nat) a := out (left_prefix a) (right_remainder a) (k+moves a)%nat.

(* Pending symbols have been inspected but their Turing moves have not been
   charged yet. Completing a token adds its output at the front of the stack. *)
Fixpoint scan (w:list Sym) h (a:list Sym) : answer :=
  match w,h with
  | [],fresh | [],pending0 => out a [1] 3
  | [],pending01 => out (1::0::1::a) [1] 8
  | S1::v,fresh => add_moves 1 (scan v fresh (1::a))
  | S0::v,fresh => scan v pending0 a
  | S0::v,pending0 => out a (1::v) 3
  | S1::v,pending0 => scan v pending01 a
  | S0::v,pending01 => add_moves 5 (scan v fresh (1::0::1::a))
  | S1::v,pending01 => add_moves 8 (scan v pending0 (1::0::a))
  end.

Definition result_spec w h a res :=
  (3 <= moves res)%nat /\ forall l,
     AR (a *> l) (buffer h *> w *> 0inf) -[src_tm]->> moves res /
         CfgL (left_prefix res *> l) (right_remainder res *> 0inf).

Lemma pay w h a v j b n res :
  (forall l, AR (a *> l) (buffer h *> w *> 0inf) -[src_tm]->> n /
             AR (b *> l) (buffer j *> v *> 0inf)) ->
  result_spec v j b res -> result_spec w h a (add_moves n res).
Proof.
  intros edge [positive path]. split; [cbn; lia|].
  intro l. apply multistep_trans with (c':=AR (b *> l) (buffer j *> v *> 0inf)); auto.
Qed.

Lemma blank_pair l : AR l 0inf -[src_tm]->> 3 / CfgL l ([1] *> 0inf).
Proof.
  pose proof (ar_zerozero l 0inf) as P. cbn [Str_app] in P.
  repeat rewrite <-(const_unfold _ S0) in P. exact P.
Qed.

Theorem scan_correct w : forall h a, result_spec w h a (scan w h a).
Proof.
  induction w as [|x w IH]; intros h a.
  - destruct h; split; try (cbn; lia); intro l.
    + apply blank_pair.
    + change (AR (a *> l) (0 >> 0inf) -[src_tm]->> 3 / CfgL (a *> l) ([1] *> 0inf)).
      rewrite <-(const_unfold _ S0). apply blank_pair.
    + cbn [scan left_prefix right_remainder moves].
      eapply (multistep_trans _ 5 3).
      * pose proof (ar_010 (a *> l) 0inf) as P.
        cbn [buffer Str_app] in P |- *. rewrite <-(const_unfold _ S0) in P. exact P.
      * apply blank_pair.
  - destruct x, h; cbn [scan].
    + exact (IH pending0 a).
    + split; [cbn; lia|]. intro l. apply ar_zerozero.
    + eapply (pay _ _ _ w fresh); [|apply IH]. intro l. apply ar_010.
    + eapply (pay _ _ _ w fresh); [|apply IH]. intro l. apply ar_one.
    + exact (IH pending01 a).
    + eapply (pay _ _ _ w pending0); [|apply IH]. intro l. apply ar_011.
Qed.

Definition right_run w := scan w fresh [].
Definition right_words w := (left_prefix (right_run w), right_remainder (right_run w)).

Theorem right_run_spec w : (3 <= moves (right_run w))%nat /\ forall l,
  AR l (w *> 0inf) -[src_tm]->> moves (right_run w) /
       CfgL (left_prefix (right_run w) *> l) (right_remainder (right_run w) *> 0inf).
Proof. exact (scan_correct w fresh []). Qed.

Theorem right_words_spec w l : let '(p,q) := right_words w in
  AR l (w *> 0inf) -[src_tm]->+ CfgL (p *> l) (q *> 0inf).
Proof.
  destruct (right_run_spec w) as [positive path].
  unfold right_words. specialize (path l).
  destruct (moves (right_run w)) as [|k]; [lia |].
  eapply multistep_progress; exact path.
Qed.
End RightExec429.
Print Assumptions RightExec429.right_words_spec.
