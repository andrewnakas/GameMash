//! Which game this build is: GameMash's live mode mixer, or a tribute locked to
//! one set of modes, one world and one time of day. Every game shares the engine;
//! a tribute is just a `GameConfig` (see `games.rs`) and a three-line binary.

use crate::core::modes::Mode;
use crate::core::scene::World;
use std::sync::OnceLock;

pub struct GameConfig {
    pub title: &'static str,
    pub tagline: &'static str,
    /// Fixed modes. `None` is GameMash: any combination, toggled live with F1–F8 or Tab.
    pub modes: Option<&'static [Mode]>,
    /// Fixed world. `None` reads `?world=` / `GAMEMASH_WORLD` at launch.
    pub world: Option<World>,
    /// Fixed time of day. `None` reads `?time=night` / `GAMEMASH_TIME` at launch.
    pub night: Option<bool>,
    /// Shown on the controls screen (Tab), after the movement basics and each mode's controls.
    pub help: &'static [&'static str],
}

impl GameConfig {
    /// The locked mode mask, if this game fixes its modes.
    pub fn locked(&self) -> Option<u8> {
        self.modes.map(|ms| ms.iter().fold(0, |m, x| m | x.bit()))
    }
}

static GAME: OnceLock<&'static GameConfig> = OnceLock::new();

/// The running game. Defaults to GameMash (tests, tools) until `run` sets it.
pub fn game() -> &'static GameConfig {
    GAME.get().copied().unwrap_or(&crate::games::GAMEMASH)
}

pub(crate) fn set(g: &'static GameConfig) {
    let _ = GAME.set(g);
}
