# Engine notes — tiny-chess-01 (v4h)

`main.py` (3,731 B, cap 4,096): packed with `makefun compress` from
`v4h_src.py` (readable source, kept beside the repo for the bundle) —
lzma payload + one-line unpacker, expressly allowed by the rules.
Stdlib only; fixed 120,000-node budget, no clocks, no unseeded
randomness: a trial replays byte for byte.

Design: 0x88 board, precomputed knight/king targets and slider rays;
incremental Zobrist keys; transposition table (exact/lower/upper,
mate-distance adjusted) kept across moves; incremental eval (material +
piece-square tables, king blends middlegame/endgame by phase). PVS
alpha-beta with check extensions; quiescence over captures/promotions
(+ all evasions in check) with delta pruning. Ordering: TT move,
killers, MVV-LVA. Repetition scores 0. Lazy legality. Lone legal move
played without searching.

v4h (new): null-move pruning (depth >=3, not in check, non-pawn material
present, never twice in a row; R=2, null window); late move reductions
(quiet moves past the 4th at depth >=3, -1 ply, null window, re-search on
fail-high); passed-pawn bonus by rank (5/10/18/30/48/70, +50% supported).

Perft (exact): startpos d4 197,281; Kiwipete d3 97,862; ep/pin d4 43,238;
promotion d3 9,467; CPW5 d3 62,379.

Local practice (6 games each): v4 trial-0 Elo 1,279, trial-1 1,279
(v3: 1,191 / 1,279). v4h trial-0 Elo 1,451 (4W/0D/2L), target >=1,271
cleared. Think ~4 s/move, inside the 10 s limit.
