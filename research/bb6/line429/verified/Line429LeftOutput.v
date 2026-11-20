(** Exact half-tape output of a complete leftward pass. *)
From BusyCoq Require Import Individual62 Line429Engine Line429RightSweep Line429LeftLanguage.
From Coq Require Import List Arith.
Import ListNotations Bell429 LeftLanguage429.
Open Scope list_scope.
Open Scope sym_scope.
Module LeftOutput429.
Inductive result := stopped | returned (untouched:side) (prefix:list Sym).
Definition feed o (w:list Sym) := match o with
  | stopped=>stopped | returned u v=>returned u (v++w) end.
Definition denotation o c r :=
  match o with
  | stopped => first Stop c
  | returned y v => before c (AR (0 >> y) (1 >> (v *> r)))
  end.
Inductive emit : mode -> side -> result -> Prop :=
| l01 x o : emit ML x o -> emit ML ([0;1] *> x) (feed o [1;1])
| l10 x o : emit MJ x o -> emit ML ([1;0] *> x) o
| lrun0 n x o : emit MJ x o ->
    emit ML ([0;0;1] *> copies S1 n ([0;0] *> x)) (feed o (repeat S0 n ++ [1;1;1]))
| j1 x o : emit ML x o -> emit MJ (1 >> x) (feed o [1;0;0])
| jrun0 n x o : emit MJ x o ->
    emit MJ ([0;1] *> copies S1 n ([0;0] *> x)) (feed o (repeat S0 n ++ [1;1;0;0]))
| lbad x : emit ML ([0;0;0;1] *> x) stopped
| jbad x : emit MJ ([0;0;1] *> x) stopped
| l11 x : emit ML ([1;1] *> x) (returned x [0])
| l0000 x : emit ML ([0;0;0;0] *> x) (returned x [1;1;1])
| lrun1 n x : emit ML ([0;0;1] *> copies S1 n ([0;1] *> x))
    (returned x (S0 :: repeat S0 n ++ [1;1;1]))
| j000 x : emit MJ ([0;0;0] *> x) (returned x [1;1;0;0])
| jrun1 n x : emit MJ ([0;1] *> copies S1 n ([0;1] *> x))
    (returned x (S0 :: repeat S0 n ++ [1;1;0;0])).
Lemma carry o w c d r : before c d -> denotation o d (w *> r) -> denotation (feed o w) c r.
Proof.
 destruct o as [|y v]; cbn [feed denotation]; intros M F.
 - destruct F as [z [P T]]. exists z;split; eauto using before_join.
 - rewrite Str_app_assoc. eapply before_join;eassumption.
Qed.
Lemma copy_repeat b n r : copies b n r=(repeat b n) *> r.
Proof. induction n;cbn;congruence. Qed.
Ltac word := repeat rewrite Str_app_assoc; cbn [Str_app].
Theorem emit_correct m s o : emit m s o -> forall r, denotation o (at_left m s r) r.
Proof.
 induction 1; intro r; cbn [at_left] in *.
 - eapply carry; [unfold CfgL;do 2 left_step;apply before_refl|apply IHemit].
 - pose proof (IHemit r) as P. destruct o; cbn [denotation] in *.
   + destruct P as [z [K T]]. exists z;split; [unfold CfgL; do 4 left_step; exact K|exact T].
   + unfold CfgL;do 4 left_step;exact P.
 - eapply carry; [|apply IHemit]. unfold CfgL; do 2 left_step.
   eapply before_join; [apply d_run|left_step]. word. rewrite <-copy_repeat. rewrite copies_push. apply before_refl.
 - eapply carry; [unfold CfgJ; left_step; apply before_refl|apply IHemit].
 - eapply carry; [|apply IHemit]. unfold CfgJ; left_step. eapply before_join; [apply d_run|left_step].
   word. rewrite <-copy_repeat. rewrite copies_push. apply before_refl.
 - exact (accepts_first_shape _ _ _ (Lbad x) r).
 - exact (accepts_first_shape _ _ _ (Jbad x) r).
 - cbn [denotation]. unfold CfgL;do 6 left_step;constructor.
 - cbn [denotation]. unfold CfgL;do 4 left_step;constructor.
 - cbn [denotation]. unfold CfgL; do 2 left_step. eapply before_join; [apply d_run|do 3 left_step].
   word. rewrite <-copy_repeat. rewrite copies_push. apply before_refl.
 - cbn [denotation]. unfold CfgJ;do 3 left_step;constructor.
 - cbn [denotation]. unfold CfgJ;left_step. eapply before_join;[apply d_run|do 3 left_step].
   word. rewrite <-copy_repeat. rewrite copies_push. apply before_refl.
Qed.
Definition classification o := match o with stopped=>Stop|returned _ _=>Turn end.
Lemma feed_class o w : classification (feed o w)=classification o.
Proof. destruct o;reflexivity. Qed.
Lemma resolve m s a : accepts m s a -> exists o, emit m s o /\ classification o=a.
Proof.
 induction 1; try destruct IHaccepts as [o1 [E C]];
 first [eexists;split;[constructor|reflexivity] |
   eexists;split;[solve [econstructor;eassumption]|first [rewrite feed_class;exact C|exact C]]].
Qed.
Theorem emit_total w m : exists o, emit m (w *> 0inf) o.
Proof. destruct (accepts_total w m) as [a A]. destruct (resolve _ _ _ A) as [o [H _]]. now exists o. Qed.
End LeftOutput429.
Print Assumptions LeftOutput429.emit_correct.
Print Assumptions LeftOutput429.emit_total.
