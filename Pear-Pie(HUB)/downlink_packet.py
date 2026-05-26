# =============================================================================
# downlink_packet.py
# =============================================================================
# Shared contract for the DOWN-path packets: the hub broadcasts parameter
# updates (alpha, threshold, target) and pods read them. Mirror of
# BLE_packet_format.py, but for updates instead of presence.
#
# -----------------------------------------------------------------------------
# !!! REPLICATED FILE - lives on BOTH the pods and the hub !!!
# Copied onto every pod AND the hub. All copies MUST be identical. If you
# change it, update EVERY copy at the same time. The repo version is master.
# =============================================================================

import struct

# --- Fixed format facts ------------------------------------------------------
MARKER  = b"PU"     # "Pear Update" - distinguishes updates from "PP" state packets
VERSION = 1

# struct layout for the fields after the marker:
#   B = version       (1 byte)
#   B = target_pod_id (1 byte) - which pod this update is for
#   ? = alpha         (TODO: how to encode - it's a float 0..1)
#   ? = threshold     (TODO: how to encode)
# _LAYOUT = "<..."   # TODO: decide encoding once fields are settled

# Note: alpha and threshold are fractional (e.g. 0.01). BLE packets are bytes,
# so a float needs encoding - either scale to an int (e.g. alpha*1000 -> 10)
# and send as a byte/short, or pack a real float. Decide when filling this in.


# --- Pack (HUB side: update -> bytes) ---------------------------------------
def pack_update(target_pod_id, alpha, threshold):
    """Build the bytes the hub broadcasts. Used by pusher.py.
    TODO: encode alpha/threshold (scale-to-int or struct float) and pack."""
    pass  # TODO


# --- Unpack (POD side: bytes -> update) -------------------------------------
def unpack_update(data):
    """Read received bytes back into (target_pod_id, alpha, threshold).
    Used by rule_listener.py. Returns None if not a valid update packet
    or not addressed to a recognised pod.
    TODO: check MARKER, check VERSION, unpack, decode alpha/threshold."""
    pass  # TODO


# --- Self-test (fill in once pack/unpack are written) -----------------------
if __name__ == "__main__":
    # TODO: pack an update, unpack it, assert round-trip, like
    # BLE_packet_format's self-test.
    pass