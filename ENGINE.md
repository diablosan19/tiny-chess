# Engine notes — tiny-chess-01 (v2)

`main.py`: 4,094 bytes (cap 4,096), stdlib only; env protocol, always plays an env-listed move.

Design deltas (v2 vs v1):
- Transposition table added (board-string key; exact scores + best-move ordering; cleared per move).
- Killer moves (one slot/depth); ordering fixed to true MVV-LVA — v1's capture key was sign-flipped.
- Eval: material folded into two shared file-mirrored PSTs; one 64-square pass (~3x faster than v1).
- Root seeding kept: a move replaces the incumbent only by beating its score.

Node cap: 50k worst move 5.38 s — too hot; 40k worst ≈3.8 s vs the 10 s limit. Fixed budget, no clocks: deterministic.

Perft (exact): startpos d3 8,902 / d4 197,281; Kiwipete d3 97,862; ep/pin d4 43,238; promo d3 9,467; CPW5 d3 62,379.

Matches: v2 vs v1, 20 games: 11W 7D 2L; v2 @6k nodes vs kit greedy starter: 16W 4D 0L. Kiwipete depth 4 at cap (v1: 1).

Limitations: no repetition/contempt handling in search; king shares the rook/queen PST (own table didn't fit).
