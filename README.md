# GameMash

Eight game mechanics share one procedural city. You can switch any combination on or off live, and your momentum carries across every switch. Built with Rust and Bevy 0.19, running natively or in the browser (WebGL2).

| Key | Mode | Inspired by | What it does |
|---|---|---|---|
| F1 | SKATE | 2010 skateboarding sim | Kick pushes, charged ollies, flips, grinds, manuals, combos, bails |
| F2 | JUMP | N64 3D platformer | Triple jump, long jump, backflip, side flip, wall kick, ground pound, dive, shards to collect |
| F3 | WARFARE | 2009 military shooter | Aim down sights, recoil, bots, health regen, killstreaks (UAV, care package, airstrike) |
| F4 | STREETS | 2004 open-world crime game | Traffic, carjacking, 5-star wanted level, police that chase and shoot, minimap |
| F5 | BLOCKS | Voxel sandbox | Break and place blocks anywhere, TNT, rail blocks you can grind |
| F6 | PORTALS | 2007 portal puzzler | Linked portals that keep momentum. Bullets, cars and boards all pass through |
| F7 | SWING | Web-swinging / grapple games | Pendulum web-swing, release fling, tethers that yank cars and bots |
| F8 | BULLET-TIME | Time-moves-when-you-move shooter | The world clock follows your input |

Synergies get bonus scores. Examples: "KICKFLIP KILL" for a kill mid-trick, "AERIAL JACK" for carjacking out of a swing, "THROUGH THE PORTAL" for kills through a portal, and "SWING BOOST" for tricks after a swing release. Ground pounds smash blocks, and explosions carve the voxel layer and wreck cars.

**Clean room.** Every mechanic is an original implementation, written from observed behaviour and publicly documented values (see `docs/specs/`). No decompiled code, ROM or disc data, original assets, names or likenesses are used.

## One engine, six games
GameMash is also the engine for five clean-room tribute games. Each tribute locks one combination of modes, one world and one time of day: a `GameConfig` in `src/games.rs` and a three-line binary in `src/bin/`.

| Game | Binary | Modes · world | Tribute to |
|---|---|---|---|
| GameMash | `gamemash` | any, live · `?world=` | — |
| Blockrealm | `blockrealm` | BLOCKS · realm | SkyCraft (Minecraft in Skyrim) |
| Hollow Warden | `hollow_warden` | JUMP · arena | ER Mario (Mario in Elden Ring) |
| Night Swing | `night_swing` | STREETS + SWING · city at night | ArkWeb |
| Kickflip Ops | `kickflip_ops` | SKATE + WARFARE + BLOCKS · city | 2010 Rust Rewrite Mashup |
| Block City | `block_city` | STREETS + BLOCKS · city | Minecraft-in-GTA V mods |

All six are built by CI and published under https://andrewnakas.github.io/GameMash/<game>/ (for example `/GameMash/night-swing/`).

## Run
```sh
cargo run                      # native
cargo test                     # sim + rules unit tests
cargo run --bin night_swing    # a tribute game
trunk serve --release          # web build at http://127.0.0.1:8080 (uses the rustup toolchain: wasm32 target)
scripts/build-web.sh night_swing  # both web variants + loader into dist/night_swing/
```

Automation harness (native only): see `src/core/debug.rs`. Example:
`GAMEMASH_MODES=skate,warfare GAMEMASH_SHOTS=/tmp/s:3 GAMEMASH_SCRIPT="0.5:W+;2:Space+;2.3:Space-;2.4:J!" cargo run`

## Layout
- `src/sim/`: engine-free, unit-tested sims (skate, jump, walker, car, voxel, collision).
- `src/core/`: modes, shared player and locomotion hand-off, input latch, camera, hotbar, scoring and synergies, UI, FX.
- `src/modes/`: one plugin per game mode.
- `src/world/`: the procedural city, the realm and arena worlds, and the geometry builder.
- `src/game.rs`, `src/games.rs`, `src/bin/`: which game a build is.
- `scripts/web_html.py`: generates each game's web page from `index.html`.
- `index.html`: the web page, with ad slots (left and right rails, bottom banner).

## Play and download
- **Browser:** https://andrewnakas.github.io/GameMash/gamemash/. Start with specific modes on: `?modes=skate,warfare` (add `&panel=0` to skip the mode panel). Embedded on [aimashups.com](https://aimashups.com/play/).
- **Desktop:** Windows, macOS and Linux builds are on [Releases](https://github.com/andrewnakas/GameMash/releases), built by CI for every `v*` tag.

CI (`.github/workflows/ci.yml`) runs the tests, builds both web variants, publishes them to GitHub Pages, and on tags builds the native releases.
