# REALM feel spec (clean room)

The realm world is a tribute to "block-sandbox player inside an open-world fantasy RPG" mashups (for example SkyCraft). Values come from observing block-sandbox combat and movement. No code, assets, names or likenesses are used. Code: `src/world/realm.rs`, `src/modes/raiders.rs` (`MELEE`).

| Behaviour | Value | Status |
|---|---|---|
| Melee reach | 3.2 m from the eye (plus camera distance in third person) | observed |
| Attack cooldown | 0.6 s between swings | observed |
| Damage | 7 (player has 100) | design |
| Critical hit | ×1.5 when falling (airborne, descending) | observed |
| Knock-back | 5.5 m/s away, +4 m/s when sprinting, 4 m/s up | observed |
| Hurt invulnerability | 0.5 s after a hit | observed |
| Raider health | 20 (three normal hits) | design |
| Raider attack | 0.5 s wind-up, lands if you're within 2.5 m and in front; 15 damage | design |
| Raider movement | walks 1.6 m/s, chases 3.9 m/s, steps up one block, can't climb two | observed |
| Regeneration | +2.5 health/s after 4 s without damage | design |
| World | 128 × 128 blocks: hills, a river, three villages, a stone keep | design |
