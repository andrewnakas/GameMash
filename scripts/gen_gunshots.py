#!/usr/bin/env python3
"""Synthesises the rifle and pistol shots from noise and sine sweeps, so they're original
(no recordings involved). Deterministic: the same seed always writes the same files.

usage: scripts/gen_gunshots.py   ->  assets/sounds/rifle_shot.wav, assets/sounds/pistol_shot.wav
"""
import math
import random
import struct
import wave
from pathlib import Path

RATE = 44100
OUT = Path(__file__).resolve().parent.parent / "assets" / "sounds"


def lowpass(xs, cutoff):
    a = 1 - math.exp(-2 * math.pi * cutoff / RATE)
    y, out = 0.0, []
    for x in xs:
        y += a * (x - y)
        out.append(y)
    return out


def highpass(xs, cutoff):
    lp = lowpass(xs, cutoff)
    return [x - l for x, l in zip(xs, lp)]


def shot(seed, length, crack_hz, body_hz, body_decay, thump_from, thump_to, thump_decay, tail_decay, tail_gain):
    rng = random.Random(seed)
    n = int(length * RATE)
    noise = [rng.uniform(-1, 1) for _ in range(n)]
    t = [i / RATE for i in range(n)]
    # Muzzle crack: a few milliseconds of bright noise.
    crack = [x * math.exp(-ti / 0.0025) for x, ti in zip(highpass(noise, crack_hz), t)]
    # Body: the blast itself, mid-band noise with a quick decay.
    body = [x * math.exp(-ti / body_decay) for x, ti in zip(lowpass(highpass(noise, 180), body_hz), t)]
    # Thump: a falling sine for the low-end punch.
    phase, thump = 0.0, []
    for ti in t:
        f = thump_to + (thump_from - thump_to) * math.exp(-ti / 0.03)
        phase += 2 * math.pi * f / RATE
        thump.append(math.sin(phase) * math.exp(-ti / thump_decay))
    # Tail: dark, slowly decaying noise standing in for the room / outdoor echo.
    tail_src = lowpass([rng.uniform(-1, 1) for _ in range(n)], 900)
    tail = [x * tail_gain * (1 - math.exp(-ti / 0.012)) * math.exp(-ti / tail_decay) for x, ti in zip(tail_src, t)]
    mix = [0.9 * c + 1.4 * b + 0.8 * th + 2.2 * tl for c, b, th, tl in zip(crack, body, thump, tail)]
    peak = max(abs(x) for x in mix)
    # Soft clip, normalise to -1 dBFS, and fade the last 20 ms to avoid a click.
    mix = [math.tanh(1.6 * x / peak) for x in mix]
    peak = max(abs(x) for x in mix)
    fade = int(0.02 * RATE)
    return [x / peak * 0.89 * (min(1.0, (n - i) / fade)) for i, x in enumerate(mix)]


def write(name, samples):
    with wave.open(str(OUT / name), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 32767)) for s in samples))
    print(f"wrote {OUT / name} ({len(samples) / RATE:.2f} s)")


if __name__ == "__main__":
    write("rifle_shot.wav", shot(seed=7, length=0.9, crack_hz=2500, body_hz=3200, body_decay=0.035,
                                 thump_from=160, thump_to=48, thump_decay=0.09, tail_decay=0.28, tail_gain=0.22))
    write("pistol_shot.wav", shot(seed=11, length=0.6, crack_hz=3200, body_hz=4200, body_decay=0.022,
                                  thump_from=210, thump_to=70, thump_decay=0.05, tail_decay=0.17, tail_gain=0.16))
