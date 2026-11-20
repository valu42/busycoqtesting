(* A regular parser for the complete leftward phase of normalized line 429.
   Each row reads nearest-first, and works for all opposite tapes. *)
From BusyCoq Require Import Individual62 Line429Engine.
From BusyCoq Require Import Line429RightSweep.
From Coq Require Import List Arith Lia.
Import ListNotations Bell429.
Open Scope list_scope.
Open Scope sym_scope.

Module LeftLanguage429.
Inductive mode := ML | MJ.
Definition at_left m := match m with ML => CfgL | MJ => CfgJ end.
Inductive outcome := Stop | Turn.
(* No source of a step in this path is in state A. *)
Inductive before : Q*tape -> Q*tape -> Prop :=
| before_refl c : before c c
| before_cons c d z : fst c <> A -> c -[src_tm]-> d -> before d z -> before c z.
Lemma before_join c d z : before c d -> before d z -> before c z.
Proof. induction 1; eauto using before_cons. Qed.
Lemma before_path c d : before c d -> c -[src_tm]->* d.
Proof. induction 1; eauto. Qed.
Definition first (o : outcome) (c : Q*tape) :=
  match o with
  | Stop => exists z, before c z /\ halted src_tm z
  | Turn => exists l r, before c (AR l r)
  end.
Definition first_shape (o : outcome) (c : Q*tape) :=
  match o with
  | Stop => first Stop c
  | Turn => exists y v, before c (AR (0 >> y) (1 >> v))
  end.
Lemma compose o c d : before c d -> first_shape o d -> first_shape o c.
Proof.
  destruct o; cbn.
  - intros H [z [P Q]]. exists z. split; eauto using before_join.
  - intros H [l [r K]]. exists l, r. eauto using before_join.
Qed.
Ltac left_step := eapply before_cons; [discriminate | prove_step | simpl_tape].

Fixpoint copies (b : Sym) (n : nat) (s : side) : side :=
  match n with O => s | S k => b >> copies b k s end.
Lemma copies_push b n s : copies b n (b >> s) = b >> copies b n s.
Proof. induction n; simpl; congruence. Qed.
Lemma e_erase n : forall l r,
  before ((copies S1 n l) <{{E}} r) (l <{{E}} (copies S0 n r)).
Proof.
  induction n as [|n IH]; intros l r; [constructor |].
  cbn [copies]. left_step. eapply before_join; [apply IH |].
  rewrite copies_push. constructor.
Qed.

(* After the initial 00 in ML or 0 in MJ, D scans the first one.
   Erasing all n+1 ones reaches B, scanning the symbol after the next zero. *)
Lemma d_run n l r :
  before ((1 >> copies S1 n (0 >> l)) <{{D}} r)
      (l <{{B}} (0 >> copies S0 n (0 >> r))).
Proof.
  left_step. eapply before_join; [apply e_erase |]. left_step. constructor.
Qed.

(* The prefix is deliberately explicit, including the first one of a run. *)
Inductive accepts : mode -> side -> outcome -> Prop :=
| L01 x o : accepts ML x o -> accepts ML ([0;1] *> x) o
| L10 x o : accepts MJ x o -> accepts ML ([1;0] *> x) o
| Lrun0 n x o : accepts MJ x o ->
    accepts ML ([0;0;1] *> copies S1 n ([0;0] *> x)) o
| J1 x o : accepts ML x o -> accepts MJ (1 >> x) o
| Jrun0 n x o : accepts MJ x o ->
    accepts MJ ([0;1] *> copies S1 n ([0;0] *> x)) o
| Lbad x : accepts ML ([0;0;0;1] *> x) Stop
| Jbad x : accepts MJ ([0;0;1] *> x) Stop
| L11 x : accepts ML ([1;1] *> x) Turn
| L0000 x : accepts ML ([0;0;0;0] *> x) Turn
| Lrun1 n x : accepts ML ([0;0;1] *> copies S1 n ([0;1] *> x)) Turn
| J000 x : accepts MJ ([0;0;0] *> x) Turn
| Jrun1 n x : accepts MJ ([0;1] *> copies S1 n ([0;1] *> x)) Turn.

Ltac self_turn :=
  match goal with
  | |- first_shape Turn (A,(S0 >> ?y,S1,?v)) => exists y, v; constructor
  end.
Theorem accepts_first_shape m s o : accepts m s o -> forall r, first_shape o (at_left m s r).
Proof.
  induction 1; intro r; cbn [at_left] in *.
  - eapply compose; [unfold CfgL; do 2 left_step; apply before_refl | apply IHaccepts].
  - eapply compose; [unfold CfgL; do 4 left_step; apply before_refl | apply IHaccepts].
  - eapply compose; [unfold CfgL; do 2 left_step; eapply before_join;
      [apply d_run | left_step; apply before_refl] | rewrite copies_push; apply IHaccepts].
  - eapply compose; [unfold CfgJ; left_step; apply before_refl | apply IHaccepts].
  - eapply compose; [unfold CfgJ; left_step; eapply before_join;
      [apply d_run | left_step; apply before_refl] | rewrite copies_push; apply IHaccepts].
  - eapply (compose Stop); [unfold CfgL; do 3 left_step; apply before_refl |].
    eexists. split; [constructor | reflexivity].
  - eapply (compose Stop); [unfold CfgJ; do 2 left_step; apply before_refl |].
    eexists. split; [constructor | reflexivity].
  - eapply (compose Turn); [unfold CfgL; do 6 left_step; apply before_refl | self_turn].
  - eapply (compose Turn); [unfold CfgL; do 4 left_step; apply before_refl | self_turn].
  - eapply (compose Turn); [unfold CfgL; do 2 left_step; eapply before_join;
      [apply d_run | do 3 left_step; apply before_refl] | self_turn].
  - eapply (compose Turn); [unfold CfgJ; do 3 left_step; apply before_refl | self_turn].
  - eapply (compose Turn); [unfold CfgJ; left_step; eapply before_join;
      [apply d_run | do 3 left_step; apply before_refl] | self_turn].
Qed.

Corollary accepts_turn_shape m s : accepts m s Turn -> forall r,
  exists y v, before (at_left m s r) (AR (0 >> y) (1 >> v)).
Proof. exact (accepts_first_shape m s Turn). Qed.

Corollary accepts_first m s o : accepts m s o -> forall r, first o (at_left m s r).
Proof.
  intros P r. pose proof (accepts_first_shape _ _ _ P r) as H.
  destruct o; [exact H |]. destruct H as [y [v path]].
  exists (0 >> y), (1 >> v). exact path.
Qed.

Lemma ar_live l r : ~halted src_tm (AR l r).
Proof. destruct r as [[|] r]; discriminate. Qed.
Lemma first_exclusive c : first Stop c -> first Turn c -> False.
Proof.
  intros [z [P Z]] [l [r T]]. remember (AR l r) as a eqn:E.
  revert l r E T. induction P as [u|u v z U uv P IH]; intros l r E T.
  - inversion T; subst.
    + eapply ar_live; eauto.
    + eapply halted_no_step; eauto.
  - inversion T; subst.
    + apply U; reflexivity.
    + match goal with
      | K : u -[src_tm]-> ?v2, T2 : before ?v2 (AR l r) |- _ =>
          assert (v = v2) by (eapply step_deterministic; eauto);
          subst v2; eapply IH; eauto
      end.
Qed.

Definition reaches (o : outcome) (c : Q*tape) :=
  match o with
  | Stop => halts src_tm c
  | Turn => exists l r, c -[src_tm]->* AR l r
  end.
Corollary accepts_sound m s o : accepts m s o -> forall r, reaches o (at_left m s r).
Proof.
  intros H r. pose proof (accepts_first _ _ _ H r) as E.
  destruct o.
  - destruct E as [z [P Q]]. eapply evstep_halts; [apply before_path, P | apply halted_halts, Q].
  - destruct E as [l [r1 P]]. exists l,r1. apply before_path, P.
Qed.

Definition short (n : nat) (s : side) :=
  exists w : list Sym, (length w <= n)%nat /\ s = w *> 0inf.
Lemma short_step n b s : short (S n) (b >> s) -> short n s.
Proof.
  intros [[|c w] [N E]].
  - exists (@nil Sym). split; [cbn; lia | exact (f_equal (@Streams.tl _) E)].
  - exists w. split; [cbn in N; lia | exact (f_equal (@Streams.tl _) E)].
Qed.
Lemma short_tail n b s : short n (b >> s) -> short n s.
Proof.
  intros [w [N E]]. apply (short_step n b). exists w. split; [lia | exact E].
Qed.
Lemma split_ones n s : short n s ->
  exists k x, s = copies S1 k (0 >> x) /\ short n x.
Proof.
  intros [w [N ->]]. revert N. induction w as [|b w IH]; intro N.
  - exists O, 0inf. split; [apply const_unfold | exists (@nil Sym); auto].
  - destruct b.
    + exists O, (w *> 0inf). split; [reflexivity | exists w; cbn in N; auto with arith].
    + destruct IH as [k [x [E H]]]; [cbn in N; lia |].
      exists (S k),x. split; [cbn; now rewrite E | exact H].
Qed.

Theorem accepts_total_bounded n : forall s, short n s -> forall m, exists o, accepts m s o.
Proof.
  induction n as [|n IH]; intros s H m.
  - destruct H as [[|b w] [N ->]]; [|cbn in N; lia].
    destruct m; exists Turn.
    + exact (eq_ind _ (fun z => accepts ML z Turn) (L0000 0inf) _
        ltac:(cbn [Str_app]; repeat rewrite <-const_unfold; reflexivity)).
    + exact (eq_ind _ (fun z => accepts MJ z Turn) (J000 0inf) _
        ltac:(cbn [Str_app]; repeat rewrite <-const_unfold; reflexivity)).
  - destruct s as [a s]. apply short_step in H. destruct m.
    + destruct a, s as [b s]; apply short_tail in H.
      * destruct b.
        -- destruct s as [[|] s]; apply short_tail in H.
           ++ destruct s as [[|] s]; [exists Turn; apply L0000 | exists Stop; apply Lbad].
           ++ destruct (split_ones _ _ H) as [k [[b x] [-> K]]].
              apply short_tail in K. destruct b.
              ** destruct (IH _ K MJ) as [o P]. exists o. now apply Lrun0.
              ** exists Turn. apply Lrun1.
        -- destruct (IH _ H ML) as [o P]. exists o. now apply L01.
      * destruct b.
        -- destruct (IH _ H MJ) as [o P]. exists o. now apply L10.
        -- exists Turn. apply L11.
    + destruct a.
      * destruct s as [b s]. apply short_tail in H. destruct b.
        -- destruct s as [[|] s]; [exists Turn; apply J000 | exists Stop; apply Jbad].
        -- destruct (split_ones _ _ H) as [k [[b x] [-> K]]].
           apply short_tail in K. destruct b.
           ++ destruct (IH _ K MJ) as [o P]. exists o. now apply Jrun0.
           ++ exists Turn. apply Jrun1.
      * destruct (IH _ H ML) as [o P]. exists o. now apply J1.
Qed.

Corollary accepts_total w m : exists o, accepts m (w *> 0inf) o.
Proof. apply (accepts_total_bounded (length w)). exists w. auto. Qed.
Theorem accepts_exact w m r o :
  accepts m (w *> 0inf) o <-> first o (at_left m (w *> 0inf) r).
Proof.
  split; [intros P; apply accepts_first,P |].
  intro F. destruct (accepts_total w m) as [o' P].
  pose proof (accepts_first _ _ _ P r) as F'.
  destruct o, o'; try exact P; exfalso; eapply first_exclusive; eauto.
Qed.
End LeftLanguage429.
Print Assumptions LeftLanguage429.accepts_exact.
