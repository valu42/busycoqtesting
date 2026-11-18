open Engine448
open H155900

let number n = "0x" ^ Z.format "%x" n
let list show xs = "[" ^ String.concat ";" (List.map show xs) ^ "]"
let digits = list (fun (n, k) -> "(" ^ number n ^ "," ^ number k ^ ")")
let symbols = list (function S0 -> "S0" | S1 -> "S1")

let word = function
  | SW_raw bits -> "SW_raw " ^ symbols bits
  | SW_D n -> "SW_D " ^ number n
  | SW_S n -> "SW_S " ^ number n
  | SW_PL n -> "SW_PL " ^ number n
  | SW_DEF (a, k) -> "SW_DEF " ^ number a ^ " " ^ number k
  | SW_DF ds -> "SW_DF " ^ digits ds
  | SW_DB ds -> "SW_DB " ^ digits ds

let runs = list (fun (w, k) -> "(" ^ word w ^ ", " ^ number k ^ ")")
let state_name = function A -> "A" | B -> "B" | C -> "C" | D -> "D" | E -> "E" | F -> "F"
let mode = function
  | MR -> "MR" | ML -> "ML" | MJ -> "MJ"
  | RAW (q, d) -> "(RAW " ^ state_name q ^ " " ^ (if d = L then "L" else "R") ^ ")"

let checkpoint s =
  let r = s.fs_R in
  String.concat " " ["MkFastState"; runs s.fs_L; "(MkRTape"; runs r.r_raw;
    digits r.d_front; digits r.d_back; runs r.r_tail ^ ")"; mode s.fs_mode]

let () =
  let points = List.map int_of_string (List.tl (Array.to_list Sys.argv)) in
  let rec visit i s points =
    let remaining = match points with
      | next :: rest when i = next ->
        let oc = open_out_bin (Printf.sprintf "state-%d.txt" i) in
        output_string oc (checkpoint s); close_out oc; rest
      | _ -> points in
    match remaining with
    | [] -> ()
    | _ -> match next448 s with
      | Some t -> visit (i + 1) t remaining
      | None -> failwith "halted before the requested checkpoint"
  in visit 0 (blank_start448 C) points
