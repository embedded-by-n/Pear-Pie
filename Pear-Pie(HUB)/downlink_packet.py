# =============================================================================
# downlink_packet.py
# =============================================================================
# The Pear Pie DOWN-path packet: how the hub broadcasts parameter updates
# (alpha, threshold) and pods read them. Mirror of uplink_packet, but for
# updates instead of state.
#
# -----------------------------------------------------------------------------
# !!! REPLICATED FILE - lives on BOTH the pods and the hub !!!
# Copied onto every pod AND the hub. All copies MUST be byte-identical.
# The repo version is the master.
# =============================================================================

import struct

MARKER  = b"PU"     # "Pear Update" - distinguishes updates from "PP" state packets
VERSION = 1

# alpha and threshold are fractional, so we scale them to integers to send as
# bytes, then divide back on receipt.
ALPHA_SCALE     = 1000     # alpha 0.01  -> 10
THRESHOLD_SCALE = 100      # threshold 0.5 -> 50

# fields after the marker:
#   B = version        (1 byte)
#   B = target_pod_id  (1 byte) - which pod this update is for
#   H = alpha * 1000   (2 bytes, unsigned short)
#   B = threshold * 100 (1 byte)
_LAYOUT = "<BBHB"

PACKET_SIZE = len(MARKER) + struct.calcsize(_LAYOUT)   # = 7 bytes


def pack_update(target_pod_id, alpha, threshold):
    """Build the bytes the hub broadcasts. Used by pusher.py."""
    a = int(round(alpha * ALPHA_SCALE))
    t = int(round(threshold * THRESHOLD_SCALE))
    a = 0 if a < 0 else (65535 if a > 65535 else a)
    t = 0 if t < 0 else (255 if t > 255 else t)
    return MARKER + struct.pack(_LAYOUT, VERSION, target_pod_id, a, t)


def unpack_update(data):
    """Read received bytes back into (target_pod_id, alpha, threshold).
    Used by rule_listener.py on the pod. Returns None if not a valid update."""
    if not data or len(data) != PACKET_SIZE:
        return None
    if data[:len(MARKER)] != MARKER:
        return None
    version, target_pod_id, a, t = struct.unpack(_LAYOUT, data[len(MARKER):])
    if version != VERSION:
        return None
    return {
        "version":       version,
        "target_pod_id": target_pod_id,
        "alpha":         a / ALPHA_SCALE,
        "threshold":     t / THRESHOLD_SCALE,
    }


# --- self-test ---------------------------------------------------------------
if __name__ == "__main__":
    pkt = pack_update(target_pod_id=2, alpha=0.01, threshold=0.5)
    print("packed bytes:", pkt, "size:", PACKET_SIZE)
    got = unpack_update(pkt)
    print("unpacked:", got)
    assert got["target_pod_id"] == 2
    assert abs(got["alpha"] - 0.01) < 1e-6
    assert abs(got["threshold"] - 0.5) < 1e-6
    assert unpack_update(b"\x00\x01") is None
    print("self-test passed")
