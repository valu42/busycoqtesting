(** Decide from the right half of a canonical sweep whether the next left pass
    can inherit its stopping outcome from the former left half. *)
From BusyCoq Require Import Individual62 Line429Engine Line429RightSweep Line429LeftLanguage Line429Round.
From Coq Require Import List Arith Lia.
Import ListNotations Bell429 LeftLanguage429 Round429.
Open Scope sym_scope.
Module Gate429.

Inductive phase := fresh | seen0 | seen01.

(** Read each symbol once, allowing implicit trailing zeroes at end of input.
    a and b are the two parser outcomes that can still be inherited. *)
Fixpoint gate (h:phase) (a b:bool) (w:list Sym) : bool :=
  match w with
  | [] => a
  | d::v =>
    match h,d with
    | fresh,S1  => gate fresh false a v
    | fresh,S0  => gate seen0 a b v
    | seen0,S0  => a
    | seen0,S1  => gate seen01 a b v
    | seen01,S0 => gate fresh a a v
    | seen01,S1 => gate seen0 b b v
    end
  end.

Definition parsed w a b s y := exists l r (t:nat),
    (3 <= t <= 4*length w+3)%nat /\
    AR s (w *> 0inf) -[src_tm]->> t / CfgL l r /\
    forall o, accepts MJ y o -> accepts ML l (choose (gate fresh a b w) o).

Lemma prepend w v a b a' b' s s' y (n:nat) :
  (n + 4*length v <= 4*length w)%nat ->
  AR s (w *> 0inf) -[src_tm]->> n / AR s' (v *> 0inf) ->
  gate fresh a b w = gate fresh a' b' v ->
  parsed v a' b' s' y -> parsed w a b s y.
Proof.
  intros N R E [l [r [t [K [M G]]]]]. exists l,r,(n+t)%nat.
  split; [lia|]. split; [eapply multistep_trans; eassumption|now rewrite E].
Qed.

Lemma parse_general w : forall a b s y, layer a b s y -> parsed w a b s y.
Proof.
  remember (length w) as n eqn:N. revert w N.
  induction n as [n IH] using lt_wf_ind. intros [|c w] N a b s y H.
  - exists s,(1 >> 0inf),3%nat. split; [cbn; lia|]. split.
    + pose proof (ar_zerozero s 0inf) as R.
      cbn [Str_app] in R. repeat rewrite <- (const_unfold _ S0) in R. exact R.
    + intros o P. apply (proj1 (proj2 H o P)).
  - destruct c.
    + destruct w as [|d w].
      * exists s,(1 >> 0inf),3%nat. split; [cbn; lia|]. split.
        -- pose proof (ar_zerozero s 0inf) as R. cbn [Str_app].
           rewrite <- (const_unfold _ S0). cbn [Str_app] in R.
           repeat rewrite <- (const_unfold _ S0) in R. exact R.
        -- intros o P. apply (proj1 (proj2 H o P)).
      * destruct d.
        -- exists s,(1 >> (w *> 0inf)),3%nat. split; [cbn; lia|].
           split; [apply ar_zerozero|intros o P; apply (proj1 (proj2 H o P))].
        -- destruct w as [|e w].
           ++ exists ([1;0;1] *> s),(1 >> 0inf),8%nat. split; [cbn; lia|]. split.
              ** eapply (multistep_trans _ 5 3).
                 --- pose proof (ar_010 s 0inf) as R.
                     cbn [Str_app] in R |- *. rewrite <- (const_unfold _ S0) in R. exact R.
                 --- pose proof (ar_zerozero ([1;0;1] *> s) 0inf) as R.
                     cbn [Str_app] in R. repeat rewrite <- (const_unfold _ S0) in R. exact R.
              ** intros o P. apply (proj1 (proj2 (write_101 a b s y H) o P)).
           ++ destruct e.
              ** eapply (prepend _ w _ _ a a _ ([1;0;1] *> s) _ 5); [cbn; lia|apply ar_010|reflexivity|].
                 apply (IH (length w) ltac:(cbn in N; lia) w eq_refl), (write_101 a b); exact H.
              ** eapply (prepend _ (S0::w) _ _ b b _ ([1;0] *> s) _ 8); [cbn; lia|apply ar_011|reflexivity|].
                 apply (IH (length (S0::w)) ltac:(cbn in N |- *; lia) (S0::w) eq_refl), (write_10 a); exact H.
    + eapply (prepend _ w _ _ false a _ (1 >> s) _ 1); [cbn; lia|apply ar_one|reflexivity|].
      apply (IH (length w) ltac:(cbn in N; lia) w eq_refl), (write_one a b); exact H.
Qed.

Theorem filtered_parse w u : exists l r (t:nat),
    (4<=t)%nat /\
    AR (0 >> (u *> 0inf)) (1 >> (w *> 0inf)) -[src_tm]->> t / CfgL l r /\
    forall o, accepts MJ (u *> 0inf) o ->
              accepts ML l (choose (gate fresh true true w) o).
Proof.
  destruct (parse_general w _ _ _ _ (initial (u *> 0inf))) as [l [r [t [time [R G]]]]].
  exists l,r,(S t); split; [lia|]. split; [eapply multistep_S; [unfold AR; prove_step|exact R]|exact G].
Qed.

Theorem filtered_round w u : exists l r (t:nat),
    (4<=t)%nat /\
    AR (0 >> (u *> 0inf)) (1 >> (w *> 0inf)) -[src_tm]->> t / CfgL l r /\
    forall o, accepts MJ (u *> 0inf) o ->
              first (choose (gate fresh true true w) o) (CfgL l r).
Proof.
  destruct (filtered_parse w u) as [l [r [t [N [R P]]]]]. exists l,r,t.
  split; [exact N|]. split; [exact R|]. intros o H. apply (accepts_first ML),P,H.
Qed.
End Gate429.
Print Assumptions Gate429.filtered_parse.
Print Assumptions Gate429.filtered_round.
