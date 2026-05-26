# =============================================================================
# config.py  (POD)
# =============================================================================
# Per-pod settings. This is the ONE file that differs between pods.
# Everything else (main.py, led.py, gossip.py) is identical on every pod.
# To set up a new pod: copy all the files, then edit POD_ID here.
# =============================================================================

POD_ID       = 1       # UNIQUE per pod. Change this on each physical pod.

PRESENCE_PIN = 11      # GPIO for the radar OT2 (or PIR signal)
LED_PIN      = 0       # GPIO for the lorikeet data line
NUM_LEDS     = 5

FADE_SECONDS = 30      # how long the light trail takes to fade to off

# --- learning parameters: Adaptive Baseline (Exponentially Weighted Moving Average) ---
ALPHA     = 0.01       # learning rate: smaller = slower, steadier adaptation
THRESHOLD = 0.5        # how far above normal counts as "unusual"