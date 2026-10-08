# ARENA duel spec (clean room)

The arena world is a tribute to "3D platformer hero against a soulslike boss" mashups (for example ER Mario). The player uses GameMash's JUMP moveset unchanged (`docs/specs/jump.md`). The boss is original. Code: `src/world/arena.rs`, `src/modes/boss.rs`.

| Behaviour | Value | Status |
|---|---|---|
| Boss health / posture | 600 / 100; posture decays 4/s | design |
| Sweep | 0.9 s wind-up, 7.5 m reach, 25 damage, can be jumped | design |
| Leap slam | 0.6 s crouch, 1 s leap to where you stood; 30 damage within 3.5 m; shockwave ring grows 16 m/s, 18 damage if you're grounded | design |
| Charge | 10 m/s for up to 1.6 s, 20 damage | design |
| Phase 2 | below 50% health: everything 1.35× faster, sweeps come in pairs | design |
| Your hits | punch 16, dive 14, ground pound 34, head stomp 22 (+bounce) | design |
| Posture break | 4.5 s kneel; hits do 1.5× damage; press E within 3.8 m to grab | design |
| Spin throw | spin accelerates 3→14 rad/s; release with E (or after 2 s); 40 + 7×spin damage, +40 and an explosion if thrown into the outer wall | design |
| Health | eight wedges of 12.5; each coin refills one wedge (coins respawn after 25 s) | observed |
