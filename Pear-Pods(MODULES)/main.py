# =============================================================================
# main.py  (POD)
# =============================================================================
# Independent pod behaviour: when a person enters THIS pod's space, run a blue
# arrival sweep, then hold a purple glow that fades to off over FADE_SECONDS.
#
# Now also closes the second-order loop on the pod side: rule_listener scans
# for parameter updates from the hub and applies new alpha/threshold to this
# pod's live baseline. The loop reads the live threshold each pass, so a hub
# push changes behaviour without a restart. If the hub never speaks, the pod
# simply keeps its config defaults (graceful degradation).
# =============================================================================

import time
from machine import Pin
import led
import gossip
import config
import rule_listener
from baseline import AdaptiveBaseline

# --- setup -------------------------------------------------------------------
presence = Pin(config.PRESENCE_PIN, Pin.IN)
led.clear()

learner = AdaptiveBaseline(config.ALPHA)

# start listening for hub updates; pass the learner so applied alpha is live
rule_listener.start(learner)

last_seen = None
prev_unusual = 0

# --- main loop: sense -> learn -> light -> broadcast -------------------------
while True:
    reading = presence.value()

    # live threshold (hub may have updated it; falls back to config default)
    threshold = rule_listener.get_threshold()

    learner.update(reading)
    unusual = 1 if learner.is_unusual(reading, threshold) else 0

    if unusual == 1 and prev_unusual == 0:
        print("ARRIVAL - sweep")
        led.arrival_sweep()

    if unusual == 1:
        last_seen = time.ticks_ms()

    prev_unusual = unusual

    if last_seen is None:
        led.set_trail(0.0)
    else:
        elapsed_s = time.ticks_diff(time.ticks_ms(), last_seen) / 1000
        if elapsed_s >= config.FADE_SECONDS:
            led.set_trail(0.0)
            last_seen = None
        else:
            led.set_trail(1.0 - (elapsed_s / config.FADE_SECONDS))

    gossip.broadcast(config.POD_ID, reading, unusual)
    time.sleep_ms(100)
