# BLE scan: listen for pod broadcasts.
# =============================================================================
# observer.py  (HUB)
# =============================================================================
# Hub-side BLE scanner: listens for pod gossip adverts, unpacks them with the
# shared packet contract, and ignores everything that isn't a Pear Pie packet.
# Scanning runs in the background; received adverts arrive via a callback.
#
# Needs BLE_packet_format.py present (the same file the pods use).
# =============================================================================

import bluetooth
from BLE_packet_format import unpack, MARKER

_IRQ_SCAN_RESULT = 5
_IRQ_SCAN_DONE   = 6

_ble = bluetooth.BLE()
_ble.active(True)


def _extract_payload(adv_data):
    """Pull our packet out of the advert's manufacturer-data structure.
    Walks the advert's [length][type][data] blocks, finds type 0xFF (mfg),
    strips the 2-byte company id, returns the rest (our packet) or None."""
    i = 0
    data = bytes(adv_data)
    while i < len(data):
        length = data[i]
        if length == 0:
            break
        ad_type = data[i + 1]
        if ad_type == 0xFF:                      # manufacturer specific data
            body = data[i + 2 : i + 1 + length]
            return body[2:]                      # drop the 2-byte company id
        i += length + 1
    return None


def _on_event(event, data):
    if event == _IRQ_SCAN_RESULT:
        addr_type, addr, adv_type, rssi, adv_data = data
        payload = _extract_payload(adv_data)
        if payload is None:
            return
        reading = unpack(payload)                # None if not a Pear Pie packet
        if reading is None:
            return
        # A real pod packet. For now, just print it.
        print("pod", reading["pod_id"],
              "presence", reading["presence"],
              "unusual", reading["unusual"],
              "seq", reading["sequence"],
              "rssi", rssi)


def start():
    """Begin scanning. Runs continuously in the background.
    interval/window in microseconds; 0 duration = scan forever."""
    _ble.irq(_on_event)
    _ble.gap_scan(0, 30000, 30000)


def stop():
    _ble.gap_scan(None)