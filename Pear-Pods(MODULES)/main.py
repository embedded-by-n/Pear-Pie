# =============================================================================
# main.py  (POD)  -  living light, debounced and calm
# =============================================================================
# Light priority each tick:
#   1. hand close (<=60cm) -> proximity heat + fire crackle (overrides all)
#   2. present            -> arrival sweep on entry, then breathing purple
#   3. just left          -> heatmap decay over FADE_SECONDS (dim+cool+twinkle)
#   4. long gone          -> off
#
# Presence is DEBOUNCED: it must read the same value a few ticks in a row before
# the state switches, so a bouncing radar reading can't make the lights thrash.
# The loop runs at a calm pace so UART + LED + BLE don't fight.
# =============================================================================

import time
import led
import gossip
import config
import sensors
import rule_listener
from baseline import AdaptiveBaseline

sensors.begin()
led.clear()

learner = AdaptiveBaseline(config.ALPHA)
rule_listener.start(learner)

# debounce: presence must be stable for N ticks to count as a state change
DEBOUNCE = 3
_raw_prev = 0
_stable_count = 0
present = 0           # the debounced, stable presence

last_seen = None
prev_present = 0
swept = False
start_ms = time.ticks_ms()

while True:
    raw = sensors.read_presence()
    dist = sensors.last_distance_cm
    now = time.ticks_ms()
    phase = time.ticks_diff(now, start_ms) / 1000.0

    # --- debounce presence ---------------------------------------------------
    if raw == _raw_prev:
        if _stable_count < DEBOUNCE:
            _stable_count += 1
    else:
        _stable_count = 0
    _raw_prev = raw
    if _stable_count >= DEBOUNCE:
        present = raw           # only adopt a value once it's been stable

    # --- light state machine (priority order) --------------------------------
    in_proximity = led.set_proximity(dist)

    if not in_proximity:
        if present == 1:
            if prev_present == 0 and not swept:
                print("ARRIVAL  (distance:", dist, "cm)")
                led.arrival_sweep()
                swept = True
            led.set_purple(phase)
            last_seen = now
        elif last_seen is not None:
            elapsed = time.ticks_diff(now, last_seen) / 1000.0
            if elapsed >= config.FADE_SECONDS:
                led.clear()
                last_seen = None
                swept = False
            else:
                led.set_decay(1.0 - (elapsed / config.FADE_SECONDS))
        else:
            led.clear()
            swept = False

    if present == 1:
        last_seen = now

    # --- background learning + broadcast -------------------------------------
    threshold = rule_listener.get_threshold()
    learner.update(present)
    unusual = 1 if learner.is_unusual(present, threshold) else 0
    prev_present = present

    gossip.broadcast(config.POD_ID, present, unusual)
    time.sleep_ms(120)          # calmer loop: less fighting between UART/LED/BLE

