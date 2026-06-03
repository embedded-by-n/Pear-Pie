# =============================================================================
# main.py  (POD)
# =============================================================================
# When a person enters THIS pod's space (within the radar's distance gate),
# run a blue arrival sweep, then hold a purple glow that fades over
# FADE_SECONDS. Presence comes from the Waveshare HMMD radar via sensors.py
# (distance-gated, so the pod only reacts within its own space).
#
# Two things happen each loop:
#   1. LIGHTS: triggered directly by presence (rising edge), so they fire
#      reliably the moment someone arrives. This is what the user sees.
#   2. LEARNING: the AdaptiveBaseline still runs in the background, learning how
#      often this space is usually occupied. Its "unusual" flag is what the pod
#      broadcasts to the hub for the second-order learning. The radar gives a
#      clean 1/0, so the baseline learns occupancy *rate*, and "unusual" means
#      presence at a time this space is normally empty.
#
# rule_listener still applies any hub parameter updates to the live baseline.
# =============================================================================

import time
import led
import gossip
import config
import sensors
import rule_listener
from baseline import AdaptiveBaseline

# --- setup -------------------------------------------------------------------
sensors.begin()
led.clear()

learner = AdaptiveBaseline(config.ALPHA)

rule_listener.start(learner)

last_seen = None
prev_present = 0

# --- main loop ---------------------------------------------------------------
while True:
    # clean presence from the radar: 1 if a person is within the distance gate
    present = sensors.read_presence()

    # --- LIGHTS: fire on the rising edge of presence (reliable, immediate) ---
    if present == 1 and prev_present == 0:
        print("ARRIVAL - sweep  (distance:", sensors.last_distance_cm, "cm)")
        led.arrival_sweep()

    if present == 1:
        last_seen = time.ticks_ms()

    # --- LEARNING: baseline runs in the background for the hub ---------------
    # baseline learns the occupancy RATE of this space; "unusual" = present
    # when this space is normally empty. Broadcast that to the hub.
    threshold = rule_listener.get_threshold()
    learner.update(present)
    unusual = 1 if learner.is_unusual(present, threshold) else 0

    prev_present = present

    # --- trail fade ----------------------------------------------------------
    if last_seen is None:
        led.set_trail(0.0)
    else:
        elapsed_s = time.ticks_diff(time.ticks_ms(), last_seen) / 1000
        if elapsed_s >= config.FADE_SECONDS:
            led.set_trail(0.0)
            last_seen = None
        else:
            led.set_trail(1.0 - (elapsed_s / config.FADE_SECONDS))

    # --- broadcast state to the hub ------------------------------------------
    gossip.broadcast(config.POD_ID, present, unusual)
    time.sleep_ms(100)
