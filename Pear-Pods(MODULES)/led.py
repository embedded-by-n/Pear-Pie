# =============================================================================
# led.py  (POD)  -  the Pear Pie "living light"
# =============================================================================
# Five behaviours from brightness + colour + gentle randomness:
#   1. arrival_sweep()      slow blue chain up then down (a beat per LED)
#   2. set_purple(phase)    settled purple with a soft breathing fluctuation
#   3. set_decay(frac)      heatmap fade: warm+bright -> deep blue+dim, twinkly
#   4. set_proximity(cm)    hand 60->5cm climbs hotter to red, fire crackle
#   5. clear()              off
#
# The flicker/twinkle/breath are time-smoothed so they shimmer, not strobe.
# Brightness 0..1, colours (r,g,b) 0..255.
# =============================================================================

import time
import random
import math
from machine import Pin
import neopixel
import config

NUM = config.NUM_LEDS
_np = neopixel.NeoPixel(Pin(config.LED_PIN), NUM)

BLUE_COOL  = (0, 30, 120)
PURPLE     = (120, 0, 160)
RED_HOT    = (255, 0, 0)
SWEEP_BLUE = (0, 40, 90)

# per-LED smoothed flicker values, so crackle/twinkle ease instead of jumping
_flick = [1.0] * NUM


def _scale(rgb, b):
    return (int(rgb[0] * b), int(rgb[1] * b), int(rgb[2] * b))

def _fill(rgb):
    for i in range(NUM):
        _np[i] = rgb
    _np.write()

def clear():
    _fill((0, 0, 0))


# --- 1. slow arrival sweep ---------------------------------------------------
def arrival_sweep(step_ms=140):
    for i in range(NUM):
        for j in range(NUM):
            _np[j] = SWEEP_BLUE if j <= i else (0, 0, 0)
        _np.write()
        time.sleep_ms(step_ms)
    for i in range(NUM - 1, -1, -1):
        for j in range(NUM):
            _np[j] = SWEEP_BLUE if j <= i else (0, 0, 0)
        _np.write()
        time.sleep_ms(step_ms)
    clear()


# --- 2. breathing purple -----------------------------------------------------
def set_purple(phase):
    wave = 0.7 + 0.15 * math.sin(phase * 1.0)      # slow, gentle
    _fill(_scale(PURPLE, wave))


# --- 3. heatmap decay (eased twinkle) ----------------------------------------
def set_decay(frac):
    frac = 0.0 if frac < 0 else (1.0 if frac > 1 else frac)
    r = int(PURPLE[0] * frac + BLUE_COOL[0] * (1 - frac))
    g = int(PURPLE[1] * frac + BLUE_COOL[1] * (1 - frac))
    b = int(PURPLE[2] * frac + BLUE_COOL[2] * (1 - frac))
    base_b = 0.15 + 0.75 * frac
    twinkle = (1.0 - frac) * 0.5                    # more twinkle as it cools
    for i in range(NUM):
        # ease each LED toward a gently wandering target (no hard strobe)
        target = 1.0 - random.random() * twinkle
        _flick[i] += (target - _flick[i]) * 0.25
        bri = base_b * _flick[i]
        _np[i] = (int(r * bri), int(g * bri), int(b * bri))
    _np.write()


# --- 4. proximity heat + eased fire crackle ----------------------------------
def set_proximity(distance_cm):
    NEAR, FAR = 5, 60
    if distance_cm is None or distance_cm > FAR:
        return False
    d = NEAR if distance_cm < NEAR else distance_cm
    heat = 1.0 - (d - NEAR) / (FAR - NEAR)
    r = int(PURPLE[0] + (RED_HOT[0] - PURPLE[0]) * heat)
    g = int(PURPLE[1] + (RED_HOT[1] - PURPLE[1]) * heat)
    b = int(PURPLE[2] + (RED_HOT[2] - PURPLE[2]) * heat)
    base_b = 0.5 + 0.5 * heat
    crackle = heat * 0.85                            # stronger flicker, more fire
    for i in range(NUM):
        target = 1.0 - random.random() * crackle
        _flick[i] += (target - _flick[i]) * 0.7      # snappier = vivid crackle
        f = _flick[i]
        _np[i] = (int(r * base_b * f),
                  int(g * base_b * f),
                  int(b * base_b * f))
    _np.write()
    return True


def set_trail(b):
    _fill(_scale(PURPLE, b))
