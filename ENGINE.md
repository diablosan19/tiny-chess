# Engine notes — tiny-chess-01 entry

`main.py` is **4,088 bytes** (cap: 4,096), pure Python 3 stdlib, written from
scratch for this contest. It keeps the kit starter's environment protocol
exactly (`MAKEFUN_ENV_URL`, POST `/game`, POST `/move`, stop on `done`) and
replaces the starter's greedy 1-ply brain with a real search engine.

## Design

- **Board**: 0x88 mailbox — a list of 128 one-char strings in a state list
  `[board, side_to_move, castling_bitmask, ep_square]`. Square = rank*16+file,
  rank 0 = rank 1; `s & 0x88` tests off-board.
- **Moves**: packed ints `from | to<<7 | promo<<14` (promo 1–4 = q r b n).
  Full legal generation: pawns (single/double push, captures, en passant,
  all four promotions), knights, sliders, king, and castling with
  empty-square and not-attacked transit checks. Legality is by make-the-move
  then test own king with a dedicated attack function (pawn/knight/king steps,
  then bishop/rook rays; queen = both).
- **Make/unmake**: snapshot-based — `make` returns `(board[:], turn, castling,
  ep)` and `unmake` restores by slice assignment. Castling rights are updated
  through one AND-mask table keyed by from/to home squares.
- **Search**: negamax alpha-beta (fail-hard). Iterative deepening 1→9 driven
  by a **fixed node budget — CAP = 25,000 nodes, never a clock** — so a
  replayed game always produces the same moves. When the budget runs out
  mid-iteration the search aborts via exception and the best move so far is
  kept; from depth 2 on, each iteration's root window is seeded just below
  the previous iteration's best score, so a partial iteration can only
  *replace* the incumbent with a move that actually beat it.
- **Quiescence**: at depth ≤ 0, stand-pat plus captures and promotions only.
  The capture filter lives inside move generation, so quiet moves are skipped
  before their (expensive) legality test. Capture chains are limited to 4
  plies to keep the budget for the main search. Mate = −10000 (flat),
  stalemate = 0.
- **Move ordering**: captures by MVV-LVA (`victim_value<<5 − attacker_value`),
  quiet promotions next, root candidates pre-sorted by the same score.
  (A transposition table and killer moves were implemented in the readable
  version and cut during golfing — see "With more bytes".)
- **Evaluation**: material (P100 N300 B320 R500 Q950) + piece-square tables.
  Tables are stored as single-char strings, `(ord(c) − 107) * 5` per square,
  and are file-symmetric so only files a–d are stored (32 chars per table).
  Byte pressure forced sharing: pawns and both minors use the pawn table;
  rooks, queens and kings use the rook table.
- **Root safety**: the chosen move is always one of the environment's listed
  legal moves — engine candidates are intersected with the env list, and any
  disagreement falls back to the env's first listed move. Repeated calls on
  the same FEN return the same move regardless of the env list's ordering
  (verified).

## Speed (measured on this VM — 1.5 shared vCPU, CPython 3.12)

- Raw movegen (perft): ~46k–72k nodes/sec.
- Search at CAP = 25,000: Kiwipete 2.16 s, Italian-game middlegame 1.78 s,
  queenless endgame 0.49 s per move — worst observed ≈ **2.2 s vs the 10 s
  limit**, with big headroom for a faster grader machine.
- On the most tactical positions the budget completes depth 1 and spends the
  rest on depth 2 over the most promising (capture-first) root moves; quiet
  positions complete more plies. The partial-iteration rules above mean the
  extra nodes always improve, never corrupt, the choice.

## Correctness — perft (all with state-restoration asserted after each run)

| Position | Depth | Nodes | Expected |
|---|---|---|---|
| startpos | 3 | 8,902 | 8,902 ✓ |
| startpos | 4 | 197,281 | 197,281 ✓ |
| Kiwipete | 3 | 97,862 | 97,862 ✓ |
| en-passant/pin torture | 4 | 43,238 | 43,238 ✓ |
| promotion torture | 3 | 9,467 | 9,467 ✓ |
| CPW position 5 | 3 | 62,379 | 62,379 ✓ |
| rooks + castling only | 1/2/3 | 26 / 568 / 13,744 | hand-counted, colour-symmetric ✓ |

## Playing tests

The kit's harness tarball turned out to be the generic make.fun grading
platform source (simulation/pricing/grader/server/contracts) — it contains
**no local chess env server, no Sunfish baseline and no practice openings**,
so the baseline match was played against the kit starter's own greedy logic
instead, through a local arbiter (10 opening positions × both colours,
engine at a reduced 6,000-node cap for speed):

- readable pre-golf engine: **20 W – 0 D – 0 L**
- final golfed engine: **15 W – 5 D – 0 L** (undefeated; the extra draws are
  the price of the shared PSTs and the dropped TT/killers)

Tactical suite on the final file:

- mate in 1 (scholar's-mate pattern) → Qxf7#, delivered ✓
- mate in 1 (back rank) → Ra8#, delivered ✓
- certified mate in 2 (Philidor-style rook sacrifice, verified by an
  independent brute-force solver) → engine plays the key move, solver
  confirms forced mate next move ✓
- hanging queen → pawn takes queen ✓

Protocol: the real `main.py` was run as a subprocess against a mock env
server implementing the starter protocol over HTTP — full game played,
every engine move legal, clean exit when the server reported `done`.
Self-play games stay fully legal and terminate.

## Known limitations (accepted for bytes)

- Quiescence has no in-check evasion extension: if the side to move is in
  check and no capture resolves it, stand-pat can be returned.
- En-passant captures are not searched in quiescence (their target square is
  empty, so the ordering score is 0 and the capture filter drops them).
- No draw offers/resign logic — the env ends games; repetition and the
  50-move rule are the env's business, not modelled in search.

## With more bytes, in order

1. Transposition table (bounded, keyed on a Zobrist hash) — biggest strength
   per byte; it existed in the readable version and was the last cut.
2. Killer + history move ordering.
3. Dedicated bishop, queen and king PSTs (king shelter/endgame split), and
   restoring the knight table.
4. In-check quiescence extension and en-passant captures in quiescence.
5. Null-move pruning and PVS for extra depth at the same node cap.
6. Small eval terms: bishop pair, doubled/isolated pawns, mobility.
