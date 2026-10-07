# SKATE feel spec (clean room)

Source: observing gameplay of the 2010 skateboarding game, plus black-box measurement of the owner's live build. No code or disc data is used. Sim: `src/sim/skate.rs` (`SkateTuning`).

| Behaviour | Value | Status |
|---|---|---|
| Pushes | Discrete kicks of +1.7 m/s every 0.62 s while W is held | observed |
| Push speed cap | 8 m/s (faster downhill) | observed |
| Ollie | Crouch while Space is held, pop on release. 4.3–5.9 m/s (apex 0.47–0.89 m) scaled by crouch time (0.32 s to full) | observed, to measure |
| Flip durations | Shove-it 0.36 s, kickflip/heelflip 0.42 s, hardflip 0.48 s, 360 flip 0.55 s | observed, to measure |
| Landing | ≤24° off travel is clean, ≤62° is sketchy (lose 40% speed), worse is a bail. Landing with the flip <82% done is a bail | observed |
| Grinds | Latch within 0.42 m while descending. Type comes from board angle to the rail (50-50, crooked, boardslide, 5-0 if falling fast) | observed |
| Wall bail | Hitting a wall at more than 6.5 m/s | observed |
| Combo | Each trick raises the multiplier. Banked after 1 s of clean rolling | observed |

Unit tests cover: discrete pushes reach the cap; a charged ollie goes higher than a tap; a kickflip with enough air lands clean; a late 360 flip bails; rails are grindable; hitting a wall hard bails.
