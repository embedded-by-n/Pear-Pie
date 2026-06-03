# =============================================================================
# sensors.py  (POD)
# =============================================================================
# Driver for the Waveshare HMMD mmWave radar (S3KM1110 chip), 24GHz.
#
# This sensor is VERY sensitive at factory defaults: it detects micro-motion
# (breathing) and stationary people up to ~8.5m, so the bare OT2 pin reads
# "present" almost constantly in a normal room. This driver fixes that by
# reading DISTANCE over UART and only reporting presence within a distance you
# choose (DISTANCE_GATE_CM), so a pod only "sees" its own doorway/space.
#
# Wiring (already done):
#   radar TX  -> Pico GP13 (UART1 RX)
#   radar RX  -> Pico GP12 (UART1 TX)
#   radar OT2 -> Pico GP11 (digital presence, fast fallback)
#   radar VCC -> 3V3,  GND -> GND
#
# UART: 115200 baud, 8 data bits, 1 stop bit, no parity (S3KM1110 default).
#
# Usage from main.py:
#   import sensors
#   sensors.begin()
#   present = sensors.read_presence()   # 0 or 1, distance-gated
#   dist    = sensors.last_distance_cm  # most recent distance, or None
# =============================================================================

from machine import UART, Pin
import time

# --- tuning ------------------------------------------------------------------
DISTANCE_GATE_CM = 200      # only count presence within this many cm.
                            # Set to the size of the space the pod watches.
                            # 200 = ~2m. Lower it to ignore the rest of the room.

UART_ID   = 1
UART_TX   = 12              # Pico GP12 -> radar RX
UART_RX   = 13              # Pico GP13 <- radar TX
BAUD      = 115200
OT2_PIN   = 11             # digital presence fallback

# --- S3KM1110 / HMMD report frame markers ------------------------------------
# Report frames are wrapped: header F4 F3 F2 F1 ... footer F8 F7 F6 F5.
# (This is the Hi-Link-style framing the S3KM1110/HMMD uses for its data.)
_HEADER = b"\xf4\xf3\xf2\xf1"
_FOOTER = b"\xf8\xf7\xf6\xf5"

# --- module state ------------------------------------------------------------
_uart = None
_ot2 = None
last_distance_cm = None
last_state = 0
_buf = bytearray()


def begin():
    """Open the UART and the OT2 pin. Call once at startup."""
    global _uart, _ot2
    _uart = UART(UART_ID, baudrate=BAUD, tx=Pin(UART_TX), rx=Pin(UART_RX),
                 bits=8, parity=None, stop=1, timeout=50)
    _ot2 = Pin(OT2_PIN, Pin.IN)
    # small settle
    time.sleep_ms(100)


def _parse_frame(frame):
    """Pull (state, distance_cm) out of a report frame body.

    The S3KM1110 report frame body (between header and footer) carries a
    target state byte and a 16-bit distance. Layout used here:
      body[0]      = data length low (ignored)
      body[1]      = data length high (ignored)
      body[2]      = report type (ignored)
      body[3]      = head 0xAA (ignored if present)
      body[4]      = target state: 0=none, 1=moving, 2=still, 3=both
      body[5:7]    = distance in cm, little-endian
    Different firmwares vary slightly, so we read defensively and fall back to
    the OT2 pin if the frame doesn't parse.
    """
    try:
        if len(frame) < 7:
            return None
        # find the target-state + distance pair defensively:
        # state is the first byte that is 0..3 followed by a plausible distance.
        for i in range(2, len(frame) - 2):
            state = frame[i]
            if state in (0, 1, 2, 3):
                dist = frame[i + 1] | (frame[i + 2] << 8)
                if 0 <= dist <= 1200:          # plausible cm (sensor max ~850)
                    return state, dist
        return None
    except Exception:
        return None


def _read_uart_once():
    """Read available UART bytes, extract the newest complete frame, update
    last_state / last_distance_cm. Returns True if a frame was parsed."""
    global _buf, last_state, last_distance_cm
    if _uart is None:
        return False
    n = _uart.any()
    if n:
        _buf.extend(_uart.read(n))
    # keep the buffer from growing without bound
    if len(_buf) > 256:
        _buf = _buf[-256:]
    # find the last complete header...footer frame in the buffer
    start = _buf.rfind(_HEADER)
    if start < 0:
        return False
    end = _buf.find(_FOOTER, start)
    if end < 0:
        return False
    body = bytes(_buf[start + len(_HEADER):end])
    _buf = _buf[end + len(_FOOTER):]
    parsed = _parse_frame(body)
    if parsed is None:
        return False
    state, dist = parsed
    last_state = state
    last_distance_cm = dist
    return True


def read_presence():
    """Return 1 if a person is present WITHIN the distance gate, else 0.

    Tries the UART (distance-gated) first; if no fresh UART frame is available,
    falls back to the raw OT2 pin so the pod still works even if UART is quiet.
    """
    got = _read_uart_once()
    if got:
        if last_state == 0:
            return 0
        if last_distance_cm is None:
            return 1
        return 1 if last_distance_cm <= DISTANCE_GATE_CM else 0
    # fallback: raw OT2 pin (not distance-gated)
    if _ot2 is not None:
        return _ot2.value()
    return 0


# --- standalone test: run this file directly on the Pico to see live output --
if __name__ == "__main__":
    begin()
    print("HMMD radar test. Stand in front, then walk away. Ctrl+C to stop.")
    print("gate =", DISTANCE_GATE_CM, "cm")
    while True:
        p = read_presence()
        print("present:", p,
              " state:", last_state,
              " distance_cm:", last_distance_cm,
              " ot2:", _ot2.value() if _ot2 else "-")
        time.sleep_ms(300)
