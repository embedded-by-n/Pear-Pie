# =============================================================================
# rule_listener.py  (POD)  -  the pod's single BLE scanner
# =============================================================================
# The pod has ONE BLE radio and ONE scan callback, so this one listener handles
# everything the pod overhears and sorts it by packet type:
#
#   "PU" (downlink) -> a parameter update from the hub. If it's for THIS pod,
#                      apply the new alpha/threshold to the live baseline.
#   "PP" (uplink)   -> another POD's state broadcast. Log its RSSI into the
#                      neighbour table (neighbours.py) so this pod builds a
#                      sense of relative proximity to its neighbours. The pod
#                      ignores its own broadcasts.
#
# This is the relational layer of the simplex mesh: each pod hears the others
# directly (no relaying) and learns who is near from signal strength, while
# still receiving the hub's second-order updates, all on one shared scan.
#
# Needs downlink_packet.py and uplink_packet.py present on the pod.
# =============================================================================

import bluetooth
from downlink_packet import unpack_update
from uplink_packet import unpack as unpack_state, MARKER as STATE_MARKER
import neighbours
import config

_IRQ_SCAN_RESULT = 5

_ble = bluetooth.BLE()
_ble.active(True)

# live parameters - start from config, updated when the hub pushes a change.
_state = {"alpha": config.ALPHA, "threshold": config.THRESHOLD}
_learner = None        # the AdaptiveBaseline instance, set by start()


def get_threshold():
    return _state["threshold"]


def get_alpha():
    return _state["alpha"]


def _extract_payload(adv_data):
    """Pull our packet out of the advert's manufacturer-data block."""
    i = 0
    data = bytes(adv_data)
    while i < len(data):
        length = data[i]
        if length == 0:
            break
        if data[i + 1] == 0xFF:                  # manufacturer specific data
            body = data[i + 2 : i + 1 + length]
            return body[2:]                      # drop 2-byte company id
        i += length + 1
    return None


def _apply(alpha, threshold):
    """Apply hub parameters to the live baseline + state."""
    _state["alpha"] = alpha
    _state["threshold"] = threshold
    if _learner is not None:
        _learner.alpha = alpha
    print("applied update -> alpha", alpha, "threshold", threshold)


def _on_event(event, data):
    if event != _IRQ_SCAN_RESULT:
        return
    addr_type, addr, adv_type, rssi, adv_data = data
    payload = _extract_payload(adv_data)
    if payload is None:
        return

    # ---- is it a hub UPDATE? (downlink "PU") ----
    update = unpack_update(payload)
    if update is not None:
        if update["target_pod_id"] == config.POD_ID:
            _apply(update["alpha"], update["threshold"])
        return

    # ---- is it another POD's STATE? (uplink "PP") ----
    if payload[:len(STATE_MARKER)] == STATE_MARKER:
        reading = unpack_state(payload)
        if reading is None:
            return
        other_id = reading["pod_id"]
        if other_id == config.POD_ID:
            return                               # ignore our own broadcast
        # log this neighbour's RSSI -> relative proximity
        shifted = neighbours.record(other_id, rssi)
        if shifted:
            print("neighbour", other_id, "proximity shift  rssi", rssi)


def start(learner=None):
    """Begin the single shared scan. Pass the pod's AdaptiveBaseline so applied
    alpha changes take effect on the live baseline."""
    global _learner
    _learner = learner
    _ble.irq(_on_event)
    _ble.gap_scan(0, 30000, 30000)


def stop():
    _ble.gap_scan(None)
