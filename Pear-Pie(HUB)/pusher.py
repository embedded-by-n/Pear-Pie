# =============================================================================
# pusher.py  (HUB)
# =============================================================================
# The DOWN path: broadcasts parameter updates (alpha, threshold, target) from
# the hub so pods can hear them and adjust the rules they follow.
# Mirror of the pods' gossip - hub advertises, pods scan.
#
# Needs a shared update-packet format (like BLE_packet_format, but for updates).
# Build last - depends on rules.py producing real updates to send.
# =============================================================================

import bluetooth
# from update_packet_format import pack_update   # TODO: shared update contract

_ble = bluetooth.BLE()
_ble.active(True)


def broadcast_update(pod_id, alpha, threshold):
    """Advertise a parameter update aimed at a given pod.
    TODO: pack (pod_id, alpha, threshold) into bytes and gap_advertise them,
    same wrapper style as gossip.py."""
    pass  # TODO


def stop():
    _ble.gap_advertise(None)