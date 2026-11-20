(* Native search on the verified step function. Optional checkpoint is local to this build. *)
open Bell429z
module B = Bell429

(* Original state F is reflected state E. Its next two scanned symbols are
   read toward the left on the reflected tape. *)
let sibling_guard s = match B.fs_mode s with
  | B.RAW (E, d) ->
    let l = B.fs_L s in
    let a, rest = match d with
      | L -> B.runs_pop l
      | R -> fst (B.popBitRTape (B.fs_R s)), l in
    a = S1 && fst (B.runs_pop rest) = S1
  | _ -> false

let () =
  let limit = int_of_string Sys.argv.(1) in
  let path = if Array.length Sys.argv > 2 then Some Sys.argv.(2) else None in
  let initial = match path with
    | Some f when Sys.file_exists f ->
      let chan = open_in_bin f in
      let data : B.coq_FastState * int * int = Marshal.from_channel chan in
      close_in chan; data
    | _ -> B.initFastB, 0, 0 in
  let st, idx, hits = initial in
  if limit < idx then invalid_arg "limit precedes the starting checkpoint";
  let s = ref st and i = ref idx and h = ref hits in
  let power n = n > 0 && (n land (n-1))=0 in
  let report label = let n = Score429.config_count !s in
    Printf.printf "%s steps=%d F11_checkpoints=%d ones_bits=%d ones=%s\n%!"
      label !i !h (Z.numbits n) (Z.to_string n) in
  let save () = match path with None -> () | Some f ->
    let chan = open_out_bin (f ^ ".tmp") in
    Marshal.to_channel chan (!s,!i,!h) []; close_out chan; Sys.rename (f ^ ".tmp") f in
  while !i < limit do
    match B.stepFast !s with
    | None -> report "HALT"; save (); exit 0
    | Some t ->
      s := t; incr i;
      if sibling_guard t then begin
        incr h; if !h <= 12 || power !h then report "F11"
      end;
      if power !i || !i mod 1000000=0 then report "checkpoint";
      if !i mod 1000000=0 then save ()
  done;
  report "limit"; save ()
