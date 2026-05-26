# Main MODULES loop where i will import all files and libraries
# =============================================================================
# main.py  (POD)
# =============================================================================
# Independent pod behaviour: when a person enters THIS pod's space, run a blue
# arrival sweep, then hold a purple glow that fades to off over 30 seconds.
# Brightness shows how recently the person was here.
#
# This pod does NOT tell other pods to light. Each pod lights only for its own
# presence. The "trail" across rooms is the emergent pattern as a result of
# the person moving and triggering each pod in turn. But this is sent to the Hub
# which helps the Hub to learn larger patterns for data logging and application.
# also allows pods to gain crude awareness of their relationships in space.
# =============================================================================

import time
from machine import Pin
import led
import gossip
import config
from baseline import AdaptiveBaseline

# =============================================================================
# Setup
# =============================================================================

presence = Pin(config.PRESENCE_PIN, Pin.IN)
led.clear()

learner = AdaptiveBaseline(config.ALPHA)

last_seen = None       # when presence was last detected (None = faded/never)
prev_unusual = 0

# =============================================================================
# Main loop: sense -> learn -> light trail -> broadcast
# =============================================================================

while True:
    reading = presence.value()

    # learn the baseline, then judge if this reading is unusual (above normal)
    learner.update(reading)
    unusual = 1 if learner.is_unusual(reading, config.THRESHOLD) else 0

    # NEW arrival (newly unusual): play the sweep
    if unusual == 1 and prev_unusual == 0:
        print("ARRIVAL - sweep")
        led.arrival_sweep()

    # while unusual (someone here), keep the glow at full (reset the timer)
    if unusual == 1:
        last_seen = time.ticks_ms()

    prev_unusual = unusual

    # set the trail brightness from time since last seen
    if last_seen is None:
        led.set_trail(0.0)
        print("reading:", reading, " unusual:", unusual, " brightness: 0.0 (off)")
    else:
        elapsed_s = time.ticks_diff(time.ticks_ms(), last_seen) / 1000
        if elapsed_s >= config.FADE_SECONDS:
            led.set_trail(0.0)
            last_seen = None
            print("reading:", reading, " unusual:", unusual, " faded out")
        else:
            b = 1.0 - (elapsed_s / config.FADE_SECONDS)
            led.set_trail(b)
            print("reading:", reading, " unusual:", unusual, " brightness: %.2f" % b)

    # broadcast this pod's state (non-blocking, radio handles it)
    gossip.broadcast(config.POD_ID, reading, unusual)

    time.sleep_ms(100)