# =============================================================================
# BLE_packet_format.py
# =============================================================================
# Defines the Pear Pie BLE packet: the agreed byte layout that pods use to
# broadcast their state and the hub uses to read it.
#
# Contains: the marker/signature, the field layout, and pack()/unpack().
# pack() and unpack() are mirror images and MUST stay in sync.
#
# -----------------------------------------------------------------------------
# !!! REPLICATED FILE - lives on BOTH the pods and the hub !!!
# This file is copied onto every pod AND the hub. All copies MUST be identical.
# If you change the packet format here, update EVERY copy (all pods + hub) at
# the same time. If the copies drift apart, pods and hub will silently
# misread each other's data with no error. The repo version is the master.
# =============================================================================
#----------------------------------------------------------------------
# DEFINE THE FORMAT (fixed on both sides)
#----------------------------------------------------------------------

MARKER  = b"PP"     # identifies a Pear Pie packet; hub ignores anything else
VERSION = 1         # version of THIS packet layout (bump when format changes)

# struct layout for the fields after the marker:
#   B = version   (1 byte)
#   B = pod_id    (1 byte, 1-255)
#   B = presence  (1 byte, 0 or 1)
#   B = unusual   (1 byte, 0 or 1)
#   B = sequence  (1 byte, 0-255, wraps)
# "<" = little-endian, fixed so both sides agree on byte order.

_LAYOUT = "<BBBBB"

PACKET_SIZE = len(MARKER) + struct.calcsize(_LAYOUT)   # = 7 bytes


#----------------------------------------------------------------------
#PACK  (used by the POD: turn its state into bytes to broadcast)
#----------------------------------------------------------------------

def pack(pod_id, presence, unusual, sequence):
    """Build the bytes a pod broadcasts. Used by gossip.py on the pod."""
    return MARKER + struct.pack(_LAYOUT, VERSION, pod_id, presence, unusual, sequence)

#----------------------------------------------------------------------
#UNPACK  (used by the HUB: turn received bytes back into values)
#----------------------------------------------------------------------

def unpack(data):
    """Read received bytes back into values. Used by observer.py on the hub.
    Returns None for anything that isn't a readable Pear Pie packet, so the
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
        return None     # a packet format this code doesn't understand

    return {
        "version":  version,
        "pod_id":   pod_id,
        "presence": presence,
        "unusual":  unusual,
        "sequence": sequence,
    }

#----------------------------------------------------------------------
#SELF-TEST  (runs only if this file is run on its own; needs no BLE)
#----------------------------------------------------------------------

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