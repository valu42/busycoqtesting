open Engine448

let check label initial expected =
  let rec visit n state =
    match next448 state with
    | Some next when n < expected -> visit (n + 1) next
    | Some _ -> failwith (label ^ " continues past its witness")
    | None ->
        if n <> expected || not (reading_F1 state) then
          failwith (label ^ " stopped at an unexpected count or configuration");
        Printf.printf "%s: %d successful accelerated steps, then F1\n%!" label n
  in
  visit 0 (blank_start448 initial)

let () =
  check "T4 from B (published control)" B 261156;
  check "T4 from C (line 448)" C 427055
