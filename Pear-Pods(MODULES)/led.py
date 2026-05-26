# Drives the Lorikeet LED baord.
# =============================================================================
# led.py  (POD)
# =============================================================================
# Drives the pod's 5-LED lorikeet strip: the arrival sweep and the fading
# trail.
#
# -----------------------------------------------------------------------------
# !!! REPLICATED BEHAVIOUR - must match on every pod !!!
# The colours and timing here are the user's visual language (blue = just
# arrived, purple = you were here, brightness = how recently). For the trail
# to be readable across the home, every pod must use the SAME colours and
# fade. If you change them, change them on all pods.
# =============================================================================

import machine
import neopixel
import time

NUM = 5
_np = neopixel.NeoPixel(machine.Pin(0), NUM)   # lorikeet data on GP0

# Colours kept dim to limit current draw over USB. (r, g, b), 0-255.
BLUE   = (0, 0, 60)      # arrival sweep
PURPLE = (60, 0, 60)     # presence trail at full strength


def clear():
    """All LEDs off."""
    for i in range(NUM):
        _np[i] = (0, 0, 0)
    _np.write()


def arrival_sweep():
    """Quick blue sweep up the chain then off. Briefly blocks (~0.4s),
    which is fine for a one-off arrival flourish."""
    for i in range(NUM):
        _np[i] = BLUE
        _np.write()
        time.sleep_ms(40)
    for i in range(NUM - 1, -1, -1):
        _np[i] = (0, 0, 0)
        _np.write()
        time.sleep_ms(40)


def set_trail(brightness):
    """Hold the purple trail at a given brightness (0.0 = off, 1.0 = full).
    All 5 LEDs. Called every loop with a decreasing value to make the fade."""
    if brightness < 0:
        brightness = 0
    r = int(PURPLE[0] * brightness)
    g = int(PURPLE[1] * brightness)
    b = int(PURPLE[2] * brightness)
    for i in range(NUM):
        _np[i] = (r, g, b)
    _np.write()