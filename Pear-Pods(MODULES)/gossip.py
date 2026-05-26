# =============================================================================
# gossip.py  (POD)
# =============================================================================
# The pod's BLE "gossip": broadcasts this pod's current state so other pods
# and the hub can hear it. Advertising runs in the BLE hardware in the
# background, so calling start_advertising() does NOT block the main loop.
#
# Uses the shared packet contract in BLE_packet_format.py (must be on the Pico).
# =============================================================================

import bluetooth
import struct
from BLE_packet_format import pack, MARKER   # the shared packet format

# Bluetooth SIG "manufacturer specific data" advert type.
_ADV_TYPE_MFG = 0xFF

# A placeholder company ID (0xFFFF is reserved for testing/no-company).
# Our MARKER inside the payload is what actually identifies a Pear Pie packet.
_COMPANY_ID = b"\xff\xff"

_ble = bluetooth.BLE()
_ble.active(True)

_sequence = 0     # ticks up each broadcast so the hub can spot missed/dupes


def _build_advert(payload):
    """Wrap our packet bytes in the BLE manufacturer-data structure.
    Structure = [length][type 0xFF][company id][our payload]."""
    body = _COMPANY_ID + payload
    return bytes((len(body) + 1, _ADV_TYPE_MFG)) + body


def broadcast(pod_id, presence, unusual, interval_ms=200):
    """Update what this pod is broadcasting. Call this whenever state changes
    (or every loop - it's cheap). Non-blocking: the radio handles the rest.
    The sequence number is managed here and ticks up each call."""
    global _sequence
    payload = pack(pod_id, presence, unusual, _sequence)
    adv = _build_advert(payload)
    _ble.gap_advertise(interval_ms * 1000, adv_data=adv, connectable=False)
    _sequence = (_sequence + 1) % 256       # wrap at 255 -> 0


def stop():
    """Stop advertising."""
    _ble.gap_advertise(None)