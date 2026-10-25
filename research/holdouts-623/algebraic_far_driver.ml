(* Driver for the untrusted native extraction of ResearchAlgebraicFAR.v.
   A true result is a candidate: replay it with vm_compute and coqchk.
   Usage: algebraic_far INPUT MODULUS MULTIPLIER SUFFIX_BITS EVENTS SECONDS
   Each input is checked in its original and reflected orientation. *)
open Algebraic_far

let rec positive k =
  if k = 1 then XH else
  if k land 1 = 0 then XO (positive (k / 2)) else XI (positive (k / 2))
let n k = if k = 0 then N0 else Npos (positive k)
exception Timeout
let () = Sys.set_signal Sys.sigalrm (Sys.Signal_handle (fun _ -> raise Timeout))

let valid s =
  String.length s = 41 &&
  List.length (String.split_on_char '_' s) = 6 &&
  List.for_all (fun row ->
    String.length row = 6 &&
    List.for_all (fun i ->
      String.sub row i 3 = "---" ||
      ((row.[i] = '0' || row.[i] = '1') &&
       (row.[i+1] = 'L' || row.[i+1] = 'R') &&
       row.[i+2] >= 'A' && row.[i+2] <= 'F')) [0;3])
    (String.split_on_char '_' s)

let () =
  if Array.length Sys.argv <> 7 then
    failwith "Usage: algebraic_far INPUT MODULUS MULTIPLIER SUFFIX_BITS EVENTS SECONDS";
  let path = Sys.argv.(1) in
  let modulus = int_of_string Sys.argv.(2) in
  let multiplier = int_of_string Sys.argv.(3) in
  let bits = int_of_string Sys.argv.(4) in
  let events = int_of_string Sys.argv.(5) in
  let seconds = float_of_string Sys.argv.(6) in
  if modulus < 2 || multiplier < 1 || multiplier >= modulus ||
     bits < 0 || bits > 16 || events < 1 || seconds <= 0. then
    failwith "Invalid search parameters";
  let input = open_in path in
  let machines = ref [] in
  (try while true do
     let s = String.trim (input_line input) in
     if s <> "" then begin
       if not (valid s) then failwith "Invalid machine table";
       machines := s :: !machines
     end
   done with End_of_file -> close_in input);
  let found = ref 0 and unknown = ref 0 and timed_out = ref 0 in
  let start = Unix.gettimeofday () in
  List.iteri (fun index code ->
    List.iter (fun reflected ->
      let base = tM_from_str code in
      let tm = if not reflected then base else
        fun qs -> match base qs with
          | None -> None
          | Some ((s,d),q) -> Some ((s,(match d with L -> R | R -> L)),q)
      in
      let stop_timer () = ignore (Unix.setitimer Unix.ITIMER_REAL
        {Unix.it_interval = 0.; it_value = 0.}) in
      let result =
        ignore (Unix.setitimer Unix.ITIMER_REAL
          {Unix.it_interval = 0.; it_value = seconds});
        try
          let answer = AlgebraicFAR.decide tm (n modulus) (n multiplier)
            (n (1 lsl bits)) (n 8192) (n events) in
          stop_timer (); Some answer
        with Timeout -> stop_timer (); None
      in
      (match result with
       | Some true -> incr found;
           Printf.printf
             "{\"candidate\":%d,\"reflected\":%b,\"modulus\":%d,\"multiplier\":%d,\"suffix_bits\":%d,\"events\":%d}\n%!"
             (index+1) reflected modulus multiplier bits events
       | Some false -> incr unknown
       | None -> incr timed_out);
      if (index mod 32 = 0) then Gc.full_major ()
    ) [false;true]
  ) (List.rev !machines);
  Printf.printf
    "{\"modulus\":%d,\"multiplier\":%d,\"suffix_bits\":%d,\"events\":%d,\"seconds_per_case\":%.3f,\"candidates\":%d,\"unknown\":%d,\"timeouts\":%d,\"seconds\":%.3f}\n%!"
    modulus multiplier bits events seconds !found !unknown !timed_out
    (Unix.gettimeofday () -. start)
