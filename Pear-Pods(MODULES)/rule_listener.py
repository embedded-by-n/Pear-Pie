# =============================================================================
# rule_listener.py  (POD)
# =============================================================================
# The pod scans for parameter updates from the hub and APPLIES them to its
# live baseline. Mirror of the hub's observer. Pairs with pusher.py.
#
# The apply step lives here: when an update addressed to THIS pod arrives,
# the listener swaps the new alpha into the running AdaptiveBaseline and stores
# the new threshold, which main.py reads each loop via get_threshold().
#
# Needs downlink_packet.py present on the pod (byte-identical to the hub copy).
# =============================================================================

import bluetooth
from downlink_packet import unpack_update
import config

_IRQ_SCAN_RESULT = 5

_ble = bluetooth.BLE()
_ble.active(True)

# live parameters - start from config, updated when the hub pushes a change.
_state = {"alpha": config.ALPHA, "threshold": config.THRESHOLD}
_learner = None        # the AdaptiveBaseline instance, set by start()


def get_threshold():
    """main.py reads this each loop instead of config.THRESHOLD."""
    return _state["threshold"]


def get_alpha():
    return _state["alpha"]


def _extract_payload(adv_data):
    """Pull our packet out of the advert's manufacturer-data block - same walk
    as the hub's observer."""
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
    """The apply step: swap new parameters into the live baseline + state."""
    _state["alpha"] = alpha
    _state["threshold"] = threshold
    if _learner is not None:
        _learner.alpha = alpha                   # live baseline adapts immediately
    print("applied update -> alpha", alpha, "threshold", threshold)


def _on_event(event, data):
    if event == _IRQ_SCAN_RESULT:
        addr_type, addr, adv_type, rssi, adv_data = data
        payload = _extract_payload(adv_data)
        if payload is None:
            return
        update = unpack_update(payload)          # None if not an update packet
        if update is None:
            return
        if update["target_pod_id"] != config.POD_ID:
            return                               # not for this pod
        _apply(update["alpha"], update["threshold"])


def start(learner=None):
    """Begin scanning for updates. Pass the pod's AdaptiveBaseline so applied
    alpha changes take effect on the live baseline."""
    global _learner
    _learner = learner
    _ble.irq(_on_event)
    _ble.gap_scan(0, 30000, 30000)


def stop():
    _ble.gap_scan(None)
