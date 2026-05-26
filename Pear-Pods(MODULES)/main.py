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

# =============================================================================
# LED light chase behaviour of pods
# =============================================================================

PRESENCE_PIN = 11      # radar OT2
FADE_SECONDS = 30      # how long the glow takes to fade to off

presence = Pin(PRESENCE_PIN, Pin.IN)
led.clear()

last_seen = None       # when presence was last detected (None = faded/never)
prev_presence = 0

while True:
    reading = presence.value()

    # NEW arrival (presence just turned on): play the sweep
    if reading == 1 and prev_presence == 0:
        print("ARRIVAL - sweep")
        led.arrival_sweep()

    # while someone is present, keep the glow at full (reset the timer)
    if reading == 1:
        last_seen = time.ticks_ms()

    prev_presence = reading

    # set the trail brightness from time since last seen
    if last_seen is None:
        led.set_trail(0.0)
        print("presence:", reading, " brightness: 0.0 (off)")
    else:
        elapsed_s = time.ticks_diff(time.ticks_ms(), last_seen) / 1000
        if elapsed_s >= FADE_SECONDS:
            led.set_trail(0.0)
            last_seen = None
            print("presence:", reading, " faded out")
        else:
            b = 1.0 - (elapsed_s / FADE_SECONDS)
            led.set_trail(b)
            print("presence:", reading, " brightness: %.2f" % b)

    # broadcast this pod's state (non-blocking, radio handles it)
    gossip.broadcast(POD_ID, reading, 0)
    
    time.sleep_ms(100)