(** Transfer the certificate parser's literal output through the piece-level
    finite-history factorization to a genuinely represented next tape. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36History Line36Word Line36Tiles
  Line36Left Line36LeftStep Line36LeftParse Line36Front.
Import ListNotations L36History L36Tiles L36Left L36LeftStep L36LeftParse.
Local Open Scope nat_scope.

Module L36HistoryParse.

Lemma standard_header g : physical_header g = guard36 g.
Proof. destruct g as [|[|[|[|[|g]]]]]; reflexivity. Qed.
Lemma standard_derivative b bits : derivative b bits = deriv36 b bits.
Proof. revert b. induction bits as [|c t IH]; intro b; cbn; congruence. Qed.
Definition incomplete ph cs v n := firstn n (phase_pieces ph (boundary 0 cs) v).
Definition parsed_front ph cs v n := front ph cs ++ incomplete ph cs v n.
Lemma skipn_word_suffix {T} (a b:list T) :
  skipn (length a) (a++b) = b.
Proof. rewrite skipn_app, skipn_all, Nat.sub_diag; reflexivity. Qed.

(** Decode one successful call to the finite evaluator. The returned suffix
    is precisely the unused part of its complete known output, including the
    three remembered digits and any further known digits. *)
Lemma decoded_edge s c d e out
  (Ph : phase s < 6)
  (O : observed (full c) d = (phase_guard (phase s),out))
  (E : evaluate s c d = Some e) :
  exists cs r,
    out = parsed_front (next (phase s)) cs (partial_choice (target e)) (partial_len (target e)) ++ r /\
    phase (target e) = next (phase s) /\
    kind (target e) = boundary 0 cs /\
    last_choice (target e) = last cs false /\
    halo (target e) = encode_halo r /\ encode_halo r <> 8 /\
    piece_count (kind s)-4 <= length cs /\
    dx e = (Z.of_nat (length (parsed_front (next (phase s)) cs
                               (partial_choice (target e)) (partial_len (target e))))
              - Z.of_nat (x c))%Z.
Proof.
  unfold evaluate in E. unfold observed in O.
  destruct (mark36 (full c) d) as [g bits] eqn:M.
  inversion O; subst out g. repeat rewrite Nat.eqb_refl in E. cbn [negb] in E.
  rewrite standard_header, standard_derivative, (next_mod _ Ph) in E.
  set (ph := next (phase s)) in *.
  assert (Bound : ph < 6) by (unfold ph; now apply next_bound).
  set (out := guard36 (phase_guard (phase s)) ++
              deriv36 (phase_guard (phase s) =? 1) bits) in *.
  set (lim := x c+length (guard36 (phase_guard (phase s)))) in E.
  assert (Read := read_piece_word (pre ph) (firstn lim out)).
  destruct (read_piece (pre ph) (firstn lim out)) as [np [r|]] eqn:Pr; [|discriminate].
  destruct Read as [_ [Np R]].
  destruct (reparse 24 ph 0 0 false np r) as [p|] eqn:Par; [|discriminate].
  destruct (complete p <? piece_count (kind s)-4) eqn:C; [discriminate|].
  apply Nat.ltb_ge in C.
  destruct (encode_halo (skipn (cut p) out) =? 8) eqn:EH; [discriminate|].
  apply Nat.eqb_neq in EH.
  destruct (scan (skipn (cut p) out) _ _ 0) as [cl sw] eqn:S.
  inversion E; subst e; clear E. cbn [target phase kind last_choice partial_choice partial_len halo dx].
  destruct (reparse_readback 24 ph 0 0 false np r p Bound ltac:(lia) Par)
    as [cs [t [W [K [B [N Cut]]]]]].
  pose proof (parse_bounds 24 ph 0 0 false np r p ltac:(lia) Par) as PB.
  rewrite (pre_exact ph Bound) in Np,R.
  assert (Kbound : next_kind p < 6) by lia.
  rewrite (piece_exact ph (next_kind p) (next_bit p) Bound Kbound) in W,PB.
  assert (Pw : out = parsed_front ph cs (next_bit p) (partial p) ++ (t ++ skipn lim out)).
  { pose proof (firstn_skipn lim out) as All. rewrite R, W in All.
    unfold parsed_front, front, incomplete. rewrite <- K.
    rewrite <- All at 1. now repeat rewrite <- app_assoc. }
  assert (Pl : length (parsed_front ph cs (next_bit p) (partial p)) = cut p).
  { unfold parsed_front, front, incomplete. rewrite !length_app, firstn_length, <- K, Nat.min_l by lia.
    lia. }
  assert (Tail : skipn (cut p) out = t ++ skipn lim out).
  { rewrite <- Pl, Pw at 1. apply skipn_word_suffix. }
  exists cs, (t ++ skipn lim out). rewrite <- Tail at 2 3.
  repeat split; try assumption; try reflexivity; lia.
Qed.


Lemma phase_piece_closing ph k b (Hp:ph<6) (Hk:k<6) :
  In false (phase_pieces ph k b).
Proof.
  assert (X : existsb negb (phase_pieces ph k b) = true).
  { cases_six ph; cases_six k; destruct b; reflexivity. }
  apply existsb_exists in X. destruct X as [[] [I E]]; [discriminate|exact I].
Qed.
Lemma same_last_suffix {T} (xs ys z:list T) a : z<>[] -> last (xs++z) a = last (ys++z) a.
Proof.
  intro Non. destruct z as [|x z]; [contradiction|]. revert a xs ys.
  induction z as [|b z IH]; intros a xs ys.
  - now rewrite !last_last.
  - assert (D: forall (l:list T) st1 st2 x0, last (x0::l) st1 = last (x0::l) st2).
    { induction l as [|e t HH]; intros; [reflexivity|]. cbn; apply HH. }
    assert (Ap: forall (l:list T) c r st, last (l++c::r) st=last (c::r) st).
    { induction l as [|a0 l HH]; intros c r st; [reflexivity|].
      cbn [app]. destruct (l++c::r) eqn:C; [apply app_eq_nil in C; intuition discriminate|].
      change (last (t::l0) st = last (c::r) st). rewrite <- C; apply HH. }
    now rewrite !Ap.
Qed.

Lemma fkind_boundary k cs (Hk:k<6) : boundary k cs = (k+length cs) mod 6.
Proof.
  revert k Hk. induction cs as [|c cs IH]; intros k Hk.
  - change (k=(k+0) mod 6). rewrite Nat.add_0_r, Nat.mod_small; lia.
  - cbn [boundary length]. rewrite IH by auto using next_bound.
    rewrite <- next_mod by assumption.
    rewrite Nat.add_mod_idemp_l by lia. f_equal. lia.
Qed.
Lemma fkind_start cs : boundary 0 cs = length cs mod 6.
Proof. apply fkind_boundary; lia. Qed.

Lemma encode_halo_append a b : encode_halo a <> 8 ->
  encode_halo (a++b) = encode_halo a /\ 3<=length a.
Proof. destruct a as [|x [|y [|z a]]]; cbn; intuition lia. Qed.

Record transported := Transported {
  further : list bool; common_out : list bool; unused : list bool
}.

(** The graph has retained at least one complete piece after the padding.
    The next physical cut can therefore use exactly the choices identified
    by [reparse] and its closing anchor lies in common output data. *)
Theorem transfer_edge s c d e actual padded local old_common
  (Ph : phase s<6)
  (Bk : boundary 0 actual = boundary 0 padded)
  (Cnt : length padded+5=piece_count (kind s))
  (X : x c = length (front (phase s) padded ++ old_common))
  (O : observed (full c) d =
    (phase_guard (phase s), front (next (phase s)) padded ++ local))
  (E : evaluate s c d = Some e) :
  let pn := next (phase s) in
  exists t,
    further t <> [] /\ In false (common_out t) /\
    local = common_out t ++ unused t /\
    parsed_front pn (actual ++ further t) (partial_choice (target e)) (partial_len (target e))
       = front pn actual ++ common_out t /\
    parsed_front pn (padded ++ further t) (partial_choice (target e)) (partial_len (target e))
       = front pn padded ++ common_out t /\
    phase (target e) = pn /\ kind (target e) = boundary 0 (actual ++ further t) /\
    last_choice (target e) = last (actual ++ further t) false /\
    halo (target e) = encode_halo (unused t) /\ encode_halo (unused t) <> 8 /\
    dx e = (Z.of_nat (length (front pn actual ++ common_out t))
              - Z.of_nat (length (front (phase s) actual ++ old_common)))%Z.
Proof.
  cbn zeta. destruct (decoded_edge s c d e _ Ph O E)
      as [cs [r [Out [P [K [B [Hh [Ne [Count Dx]]]]]]]]].
  set (pn:=next (phase s)) in *. assert (Hpn:pn<6) by (unfold pn;auto using next_bound).
  unfold parsed_front,front in Out. repeat rewrite <- app_assoc in Out.
  apply app_inv_head in Out.
  destruct (cancel_piece_prefix pn 0 padded cs local _ Hpn ltac:(lia) ltac:(lia) Out)
    as [more [C Loc]].
  assert (More:more<>[]) by (intro Nil;rewrite C,Nil,app_nil_r in Count;lia).
  subst cs. unfold incomplete in *.
  set (part := firstn (partial_len (target e))
                 (phase_pieces pn (boundary 0 (padded++more)) (partial_choice (target e)))) in *.
  set (common:=segments pn (boundary 0 padded) more ++ part) in *.
  assert (Sc : forall old, boundary 0 old = boundary 0 padded ->
          parsed_front pn (old++more) (partial_choice (target e)) (partial_len (target e)) =
          front pn old ++ common).
  { intros old J. unfold parsed_front,front,incomplete,common,part.
    rewrite segments_app, !boundary_app, J. now repeat rewrite <- app_assoc. }
  assert (I : In false common).
  { unfold common. apply in_or_app. left. destruct more as [|b t]; [contradiction|].
    cbn [segments]. apply in_or_app. left. apply phase_piece_closing; [exact Hpn|apply boundary_bounded;lia]. }
  exists (Transported more common r). cbn [further common_out unused].
  rewrite Sc in Dx by reflexivity.
  assert (DA : length (front pn actual)=length (front (phase s) actual))
    by apply (front_next_length _ _ Ph).
  assert (DP : length (front pn padded)=length (front (phase s) padded))
    by apply (front_next_length _ _ Ph).
  repeat split; try assumption.
  - unfold common. now rewrite <- app_assoc.
  - now apply Sc.
  - now apply Sc.
  - rewrite !boundary_app in *. now rewrite Bk.
  - rewrite B. apply same_last_suffix. exact More.
  - rewrite X, !length_app in Dx. rewrite !length_app. lia.
Qed.
End L36HistoryParse.
