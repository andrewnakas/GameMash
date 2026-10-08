#!/usr/bin/env python3
"""Writes the Trunk page for one game and renderer, using index.html (GameMash, WebGL2) as the template.

usage: web_html.py <bin> <gl|gpu>   ->  prints the path it wrote (.web-<bin>-<variant>.html)

Titles and taglines mirror src/games.rs; the footers credit the original each tribute honours.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GAMES = {
    "gamemash": None,  # the template as-is
    "blockrealm": ("Blockrealm", "A block-builder in an open-world RPG: mine, build and fight raiders across a voxel countryside.",
                   "SkyCraft (Minecraft in Skyrim) by chasmlol"),
    "hollow_warden": ("Hollow Warden", "A 3D platformer hero against a soulslike boss: jump its sweeps, break its posture, spin-throw it.",
                      "ER Mario (Mario in Elden Ring) by deltarooo"),
    "night_swing": ("Night Swing", "Web-swing through a moonlit city, steal cars out of the air and lose the police in the dark.",
                    "ArkWeb by luki-1"),
    "kickflip_ops": ("Kickflip Ops", "A military shooter where you can drop onto a skateboard any time, in a city with a block quarry you can dig and build.",
                     "the 2010 Rust Rewrite Mashup by chasmlol"),
    "block_city": ("Block City", "An open-world crime city with a block-sandbox layer: steal cars, dig, build and blow up the streets.",
                   "the Minecraft-in-GTA V mods made with universal-modder by Rehan Sheikh"),
}


def sub(s: str, pattern: str, new: str) -> str:
    out, n = re.subn(pattern, lambda _: new, s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"index.html: pattern not found: {pattern!r}")
    return out


def main(bin_name: str, variant: str) -> None:
    if bin_name not in GAMES or variant not in ("gl", "gpu"):
        raise SystemExit(__doc__)
    s = (ROOT / "index.html").read_text()
    if variant == "gpu":
        s = sub(s, r'data-cargo-profile="wasm-release" />', 'data-cargo-profile="wasm-release" data-cargo-features="webgpu" />')
    meta = GAMES[bin_name]
    if meta:
        title, tagline, tribute = meta
        slug = bin_name.replace("_", "-")
        s = sub(s, r'data-bin="gamemash"', f'data-bin="{bin_name}"')
        s = sub(s, r"<title>.*?</title>", f"<title>{title}</title>")
        s = sub(s, r'<meta name="description" content=".*?" />', f'<meta name="description" content="{tagline}" />')
        s = sub(s, r"<h1>GAME<span>MASH</span></h1>", f"<h1>{title.upper()}</h1>")
        s = sub(s, r"<p>8 mechanics, one city\..*?</p>", f"<p>{tagline}  Tab: controls.</p>")
        s = sub(s, r"Loading the city…", f"Loading {title}…")
        s = sub(s, r"<footer>All mechanics are original clean-room recreations.*?<br>",
                f'<footer>A clean-room tribute to {tribute}: original code, no game files, names or likenesses. '
                f'Not affiliated with any publisher or with the original project. <a href="https://aimashups.com/play/{slug}/">aimashups.com</a><br>')
    out = ROOT / f".web-{bin_name}-{variant}.html"
    out.write_text(s)
    print(out.name)


if __name__ == "__main__":
    main(*sys.argv[1:3])
