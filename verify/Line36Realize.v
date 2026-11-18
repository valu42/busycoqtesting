(** Realize a successful local reparse as an actual checkpoint with a
    canonical front and the same finite-state label as the checker. *)
From Coq Require Import List Bool Arith Lia.
From BusyCoq Require Import Line36History Line36HistoryParse Line36Front
  Line36Left Line36LeftStep Line36LeftCheck Line36Word Line36Tiles.
Import ListNotations L36Tiles L36Left L36LeftStep L36LeftGroups L36History L36HistoryParse.
Local Open Scope nat_scope.

Lemma image_derivative_length p bits : length (deriv36 p bits)=length bits.
Proof. revert p; induction bits; intros; simpl; auto. Qed.

Lemma realized_observed known ext w g out :
  step36 (known++ext)=Some w ->
  observed known (fst(mark36 ext 0))=(g,out) ->
  exists rem, w=out++rem /\
   length (guard36 g)+length known+length ext<=length w.
Proof.
  unfold observed,step36. rewrite mark36_app.
  pose proof (mark36_length ext 0) as LE.
  destruct (mark36 ext 0) as [d b]. cbn [fst snd] in *.
  pose proof (mark36_length known d) as LK.
  destruct (mark36 known d) as [g' a]. cbn [snd] in LK.
  destruct (g' <? 6); [|discriminate]. intros [= <-] [= <- <-].
  unfold output36. rewrite deriv36_app. eexists; split.
  - now repeat rewrite <-app_assoc.
  - rewrite !length_app,!image_derivative_length. lia.
Qed.

Theorem realize_front36 f dest cs halo exterior w' guard exposed :
  fvalid f -> ftail f=halo++exterior -> step36 (fword f)=Some w' ->
  let wp := parsed_front (phase dest) cs (partial_choice dest) (partial_len dest) in
  observed (fprefix f++halo) (fst(mark36 exterior 0))=(guard,wp++exposed) ->
  well_formed dest -> kind dest=boundary 0 cs ->
  last_choice dest=last cs false -> L36Left.halo dest=encode_halo exposed ->
  encode_halo exposed<>8 ->
  length wp<=length (fprefix f)+length (guard36 guard) ->
  exists f' rest, fvalid f' /\ fstate f'=dest /\ fprefix f'=wp /\
    ftail f'=exposed++rest /\ fword f'=w' /\ fchoices f'=cs /\ fphase f'=phase dest.
Proof.
  intros [_ [_ Ht]] E Step wp O W K A H Hsize Bound.
  assert (S : step36 ((fprefix f++halo)++exterior)=Some w').
  { rewrite <-app_assoc,<-E; exact Step. }
  destruct (realized_observed _ _ _ _ _ S O) as [rest [Out Size]].
  set (f' := Front36 (phase dest) cs (partial_choice dest) (partial_len dest) (exposed++rest)).
  assert (Prefix : fprefix f'=wp).
  { unfold wp,parsed_front,front,incomplete,fprefix,fdata,fpart,fkind,f'.
    cbn [fphase fchoices foption flen]; rewrite fkind_start. apply app_assoc. }
  assert (Tail : ftail f'=exposed++rest) by reflexivity.
  assert (Word : fword f'=w') by (unfold fword; rewrite Prefix,Tail,Out,<-app_assoc; reflexivity).
  assert (V : fvalid f').
  { destruct W as [Hp [Hk [Hlen Hhalo]]]. split; [exact Hp|]. split.
    - unfold fkind,f',flen,fphase,fchoices,foption.
      rewrite <-fkind_start,<-K,<-piece_exact by assumption. exact Hlen.
    - rewrite Tail. rewrite E,length_app in Ht. rewrite Out,!length_app in Size.
      rewrite length_app. lia. }
  assert (State : fstate f'=dest).
  { unfold fstate,fkind,f'. cbn [fphase fchoices flen foption ftail].
    rewrite <-fkind_start,<-K,<-A,(proj1 (encode_halo_append _ _ Hsize)),<-H.
    now destruct dest. }
  exists f',rest. repeat split; try assumption; try reflexivity. all: apply V.
Qed.
