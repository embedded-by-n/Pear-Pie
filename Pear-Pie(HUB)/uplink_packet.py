# =============================================================================
# uplink_packet.py
# =============================================================================
# The Pear Pie UP-path packet: how pods broadcast their state and the hub
# reads it. Contains the marker, the field layout, and pack()/unpack().
# pack() and unpack() are mirror images and MUST stay in sync.
#
# -----------------------------------------------------------------------------
# !!! REPLICATED FILE - lives on BOTH the pods and the hub !!!
# Copied onto every pod AND the hub. All copies MUST be byte-identical.
# If you change the format here, update EVERY copy at the same time.
# The repo version is the master.
# =============================================================================

import struct

MARKER  = b"PP"     # identifies a Pear Pie state packet; hub ignores anything else
VERSION = 1         # bump when the layout changes

# fields after the marker:
#   B = version   (1 byte)
#   B = pod_id    (1 byte, 1-255)
#   B = presence  (1 byte, 0 or 1)
#   B = unusual   (1 byte, 0 or 1)
#   B = sequence  (1 byte, 0-255, wraps)
_LAYOUT = "<BBBBB"

PACKET_SIZE = len(MARKER) + struct.calcsize(_LAYOUT)   # = 7 bytes


def pack(pod_id, presence, unusual, sequence):
    """Build the bytes a pod broadcasts. Used by gossip.py on the pod."""
    return MARKER + struct.pack(_LAYOUT, VERSION, pod_id, presence, unusual, sequence)


def unpack(data):
    """Read received bytes back into values. Used by observer.py/data_logger.py
    on the hub. Returns None for anything that isn't a Pear Pie packet, so the
    hub can ignore all the other BLE devices in range."""
    if not data:
        return None
    if len(data) != PACKET_SIZE:
        return None
    if data[:len(MARKER)] != MARKER:
        return None

    version, pod_id, presence, unusual, sequence = struct.unpack(
        _LAYOUT, data[len(MARKER):])

    if version != VERSION:
        return None

    return {
        "version":  version,
        "pod_id":   pod_id,
        "presence": presence,
        "unusual":  unusual,
        "sequence": sequence,
    }


# --- self-test (runs only if this file is run directly; needs no BLE) --------
if __name__ == "__main__":
    packet = pack(pod_id=3, presence=1, unusual=0, sequence=5)
    print("packed bytes:", packet)
    print("packet size :", PACKET_SIZE)

    result = unpack(packet)
    print("unpacked    :", result)

    assert result == {"version": 1, "pod_id": 3, "presence": 1,
                      "unusual": 0, "sequence": 5}, "round-trip failed!"
    print("rubbish data:", unpack(b"\x00\x01\x02"))   # should print None
    print("self-test passed")
