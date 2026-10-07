# JUMP feel spec (clean room)

Source: publicly documented movement values used by the speedrun/TAS community, plus black-box observation of a running build. No decompiled code or game data is consulted.
Units: 1 u = 1 cm. The game runs on a 30 Hz frame clock (`src/sim/jump.rs`, `JumpTuning`).

| Behaviour | Value | Status |
|---|---|---|
| Gravity (normal jumps) | 4 u/f² | documented |
| Terminal fall speed | 75 u/f | documented |
| Run speed cap | 32 u/f (9.6 m/s) | documented |
| Single jump launch | 42 + 0.25·speed u/f | documented |
| Double jump launch | 52 + 0.25·speed u/f | documented |
| Triple jump launch | 69 u/f, needs speed > 20 u/f | documented |
| Jump-chain window after landing | 5 frames | documented |
| Backflip | 62 u/f up, −16 u/f back | documented |
| Side flip | 62 u/f up, 8 u/f forward | documented |
| Long jump | 30 u/f up, speed ×1.5 capped at 48, low gravity | documented |
| Wall kick | 52 u/f up, 24 u/f away, 5-frame window | approximate, to measure |
| Ground pound | 10-frame hover, then 50 u/f down | approximate, to measure |
| Releasing jump early | vertical speed above 20 cut to ¼ | approximate, to measure |
| Turn rate on ground | 11.25°/frame | approximate, to measure |

Unit tests in `src/sim/jump.rs` lock these in (single-jump apex is 242 u, the triple jump goes higher than the double, and a jump after the window does not chain).

## Measurement still to do
Drive the owner's live build in the browser with scripted inputs, log Mario's position every frame, and fill in the "to measure" rows. Only behaviour gets recorded, never code.
