# =============================================================================
# sensors.py  (POD)
# =============================================================================
# Driver for the Waveshare HMMD mmWave radar (S3KM1110), 24GHz.
#
# This sensor's firmware outputs simple TEXT lines over UART:
#     ON\r\n            (a person is present)
#     OFF\r\n           (no person)
#     Range 65\r\n      (distance to target in cm)
#
# So we read those lines and distance-gate them: only report "present" if the
# sensor says ON *and* the range is within DISTANCE_GATE_CM. That stops a pod
# from seeing the whole room - it only reacts within its own space.
#
# Wiring (already done):
#   radar TX  -> Pico GP13 (UART0 RX)
#   radar RX  -> Pico GP12 (UART0 TX)
#   radar OT2 -> Pico GP11 (digital presence, fast fallback)
#   radar VCC -> 3V3,  GND -> GND
#
# UART: 115200 baud, 8N1.  Note: GP12/GP13 are UART **0** on the Pico.
#
# Usage from main.py:
#   import sensors
#   sensors.begin()
#   present = sensors.read_presence()   # 0 or 1, distance-gated
#   dist    = sensors.last_distance_cm  # most recent range in cm, or None
# =============================================================================

from machine import UART, Pin
import time

# --- tuning ------------------------------------------------------------------
DISTANCE_GATE_CM = 200      # only count presence within this many cm.
                            # Lower it so the pod only watches its own doorway/
                            # space and ignores movement further away.
                            # Set to 0 to disable the gate (any ON counts).

UART_ID = 0                 # GP12/GP13 are UART0 on the Pico
UART_TX = 12                # Pico GP12 -> radar RX
UART_RX = 13                # Pico GP13 <- radar TX
BAUD    = 115200
OT2_PIN = 11                # digital presence fallback

# --- module state ------------------------------------------------------------
_uart = None
_ot2 = None
last_distance_cm = None
last_on = 0
_buf = b""


def begin():
    """Open the UART and the OT2 pin. Call once at startup."""
    global _uart, _ot2
    _uart = UART(UART_ID, baudrate=BAUD, tx=Pin(UART_TX), rx=Pin(UART_RX),
                 bits=8, parity=None, stop=1, timeout=50)
    _ot2 = Pin(OT2_PIN, Pin.IN)
    time.sleep_ms(100)


def _process_lines():
    """Read whatever text the sensor has sent and update last_on /
    last_distance_cm from any complete lines. Returns True if anything fresh
    was parsed."""
    global _buf, last_on, last_distance_cm
    if _uart is None:
        return False

    n = _uart.any()
    if n:
        chunk = _uart.read(n)
        if chunk:
            _buf += chunk

    if b"\n" not in _buf:
        return False

    # split into complete lines; keep any trailing partial line in the buffer
    parts = _buf.split(b"\n")
    _buf = parts[-1]                 # last piece may be incomplete
    fresh = False

    for raw in parts[:-1]:
        line = raw.strip().upper()   # drop \r, normalise case
        if not line:
            continue
        if line == b"ON":
            last_on = 1
            fresh = True
        elif line == b"OFF":
            last_on = 0
            last_distance_cm = None
            fresh = True
        elif line.startswith(b"RANGE"):
            # "RANGE 65" -> 65
            digits = b"".join(c.to_bytes(1, "little") for c in line
                              if 48 <= c <= 57)   # keep 0-9
            if digits:
                try:
                    last_distance_cm = int(digits)
                    fresh = True
                except Exception:
                    pass

    # keep the buffer from growing without bound
    if len(_buf) > 128:
        _buf = _buf[-128:]
    return fresh


def read_presence():
    """Return 1 if a person is present WITHIN the distance gate, else 0.

    Uses the sensor's ON/OFF + Range text. Falls back to the raw OT2 pin only
    if the UART has sent nothing at all yet."""
    got = _process_lines()

    # if we've ever parsed a real line, trust the UART (distance-gated)
    if got or last_on or last_distance_cm is not None:
        if not last_on:
            return 0
        if DISTANCE_GATE_CM <= 0 or last_distance_cm is None:
            return 1
        return 1 if last_distance_cm <= DISTANCE_GATE_CM else 0

    # nothing from UART yet: fall back to the raw OT2 pin
    if _ot2 is not None:
        return _ot2.value()
    return 0


# --- standalone test ---------------------------------------------------------
if __name__ == "__main__":
    begin()
    print("HMMD radar test. Stand in front, then walk away. Ctrl+C to stop.")
    print("gate =", DISTANCE_GATE_CM, "cm")
    while True:
        p = read_presence()
        print("present:", p,
              " on:", last_on,
              " distance_cm:", last_distance_cm,
              " ot2:", _ot2.value() if _ot2 else "-")
        time.sleep_ms(300)
