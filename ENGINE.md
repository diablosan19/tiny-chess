# Engine notes — tiny-chess-01 entry (v2)

`main.py` is 4,094 bytes (cap 4,096), stdlib only. It speaks the env
protocol (`MAKEFUN_ENV_URL`, POST `/game`, POST `/move`, UCI moves) and
always answers with a move from the env's legal list.

## Design

- 0x88 mailbox board (128 cells), pieces as chars, moves packed into ints
  (`from | to<<7 | promo<<14 | double<<17`), state = board + side +
  castling mask + ep square; snapshot make/unmake (copy of 4 fields).
- Full legal movegen: pseudo-legal generation, then make each move and
  test the mover's king against a dedicated attack function `A`. Castling
  checks origin/transit squares and rook presence explicitly.
- Search: negamax alpha-beta + iterative deepening at the root under a
  fixed node budget (40,000; no clocks anywhere, so moves are
  deterministic). Root seeding: each iteration starts from the previous
  iteration's score, so the played move is only replaced by one that
  actually beat it inside the current iteration.
- Transposition table: dict keyed by board string + side (castling/ep not
  in the key — collisions can only add ordering/score noise, never an
  illegal move, since the root only plays env-listed moves). Entries hold
  (depth, score, best move, exact flag); exact scores are returned on
  probe, best moves give an ordering bonus. Cleared at every root call,
  which bounds memory and makes each move history-independent.
- Killer moves: one slot per depth, quiet cutoff moves get a sort bonus.
- Ordering: TT move, then true MVV-LVA for captures (v1's ordering key
  was sign-flipped — captures sorted *after* quiet moves; fixed in v2),
  killers, then everything else.
- Quiescence: captures + promotions, stand-pat, delta pruning, chain cap
  4 plies. In-check nodes (main search and qsearch) search all legal
  replies and score mate as -99999 + ply, so mates are preferred fast.
- Eval: material + piece-square tables. Two tables are shared
  (pawns/minors; rooks/queens/king), file-mirrored, encoded as char
  strings (`(ord-107)*5`); material is folded into the tables, so eval is
  a single pass over the 64 real squares (~3x faster than v1's 128-cell
  pass — the speed is what funds the higher node cap).

## Measurements (this VM: slow shared CPU, CPython 3.12)

Perft, all exact, state restored after every run: startpos d3 8,902 /
d4 197,281; Kiwipete d3 97,862; ep/pin torture d4 43,238; promotion
torture d3 9,467; CPW position 5 d3 62,379. Movegen fuzz: 3,600 random
positions, v2's legal sets identical to v1's. Determinism: identical
moves across processes with PYTHONHASHSEED 0/1/42.

Tactics: scholar's mate in 1 (Qxf7#), back-rank mate in 1 (Ra8#),
hanging queen (Nxh4), and a mate in 2 whose key move was verified by
brute force (every legal reply allows mate in 1).

Node-cap choice: worst move at 50k nodes took 5.38 s (startpos) — too
hot. At 40k: startpos 3.75 s, Kiwipete 2.80 s, Sicilian 2.56 s, sharp
tactical 2.71 s, pawn endgame 1.86 s; a constructed promotion-torture
outlier takes 6.26 s, still under the 10 s limit. Shipped cap: 40,000.

Depth on Kiwipete at shipped caps: v2 completes depth 4 (v1: depth 1).

Matches (10 openings x both colours, mate/stalemate/material/50-move/
threefold adjudication):

- v2 (40k) vs v1 (25k), 20 games: **11W 7D 2L** (72.5%). Both v2 losses
  came as Black by mate; most draws were threefold repetitions.
- v2 at a reduced 6,000-node cap vs the kit starter's greedy player,
  20 games: **16W 4D 0L** (v1 at the same cap: 15W 5D 0L).

## Known limitations

- No repetition or contempt handling inside the search: drawn-by-
  repetition finishes happen in near-equal positions.
- The king still shares the rook/queen PST (a separate king table and
  an endgame switch did not fit the byte budget after the TT/killers).
- TT key omits castling rights and ep square; accepted as noise, see
  above.
