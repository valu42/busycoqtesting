(* Audit the raw entries to D from its reflected left-moving predecessor.
   Large proved sweeps can contain many additional, already certified visits. *)
open Bell429z
module B = Bell429
let () =
  let limit = int_of_string Sys.argv.(1) in
  let state = ref B.initFastB and indx = ref 0 in
  let entries = ref 0 and nonblank = ref 0 and last = ref (-1) in
  while !indx < limit do
    (match B.fs_mode !state with
     | B.RAW (D, L) ->
       let bit, outside = B.runs_pop (B.fs_L !state) in
       if bit = S0 then begin
         incr entries; last := !indx;
         if not (B.runs_zeros outside) then incr nonblank
       end
     | _ -> ());
    match B.stepFast !state with
    | None -> Printf.printf "halt after %d successful calls\n%!" !indx; exit 0
    | Some s -> state := s; incr indx
  done;
  Printf.printf "calls=%d entries=%d nonblank_outside=%d last_entry=%d\n" !indx !entries !nonblank !last
