# =============================================================================
# pusher.py  (HUB)
# =============================================================================
# The DOWN path: broadcasts parameter updates (alpha, threshold) from the hub
# so pods can hear them and adjust the rules they follow. Mirror of the pods'
# gossip.py - the hub advertises, the pods scan.
#
# Uses the shared downlink_packet contract (must be byte-identical to the pod
# copy). Each update is aimed at one pod by target_pod_id.
# =============================================================================

import bluetooth
import time
from downlink_packet import pack_update

_ADV_TYPE_MFG = 0xFF
_COMPANY_ID   = b"\xff\xff"          # same wrapper the pods use

_ble = bluetooth.BLE()
_ble.active(True)


def _build_advert(payload):
    """Wrap update bytes in the BLE manufacturer-data structure, same shape as
    gossip.py: [length][type 0xFF][company id][payload]."""
    body = _COMPANY_ID + payload
    return bytes((len(body) + 1, _ADV_TYPE_MFG)) + body


def broadcast_update(target_pod_id, alpha, threshold, hold_ms=1500, interval_ms=200):
    """Advertise one parameter update aimed at a given pod, for hold_ms.
    Pods scanning will pick it up; after hold_ms we stop so the next update
    (or another pod's) can go out cleanly."""
    payload = pack_update(target_pod_id, alpha, threshold)
    adv = _build_advert(payload)
    _ble.gap_advertise(interval_ms * 1000, adv_data=adv, connectable=False)
    time.sleep_ms(hold_ms) if hasattr(time, "sleep_ms") else time.sleep(hold_ms / 1000)
    _ble.gap_advertise(None)


def push_all(updates):
    """Broadcast a whole dict of {pod_id: {"alpha":..,"threshold":..}} in turn.
    Used by the hub main loop after rules.compute_updates()."""
    for pod_id, vals in updates.items():
        print("pushing -> pod", pod_id, "alpha", vals["alpha"], "threshold", vals["threshold"])
        broadcast_update(pod_id, vals["alpha"], vals["threshold"])


def stop():
    _ble.gap_advertise(None)
