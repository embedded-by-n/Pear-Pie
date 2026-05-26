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
#DEFINE THE FORMAT (the fixed facts both sides agree on)
#----------------------------------------------------------------------

MARKER        = the two bytes "PP"        // identifies a Pear Pie packet
VERSION       = 1                         // this packet format is version 1
LAYOUT        = order and size of fields after the marker:
                  pod_id    (1 byte)
                  version   (1 byte)
                  presence  (1 byte)
                  unusual   (1 byte)
                  sequence  (1 byte)
PACKET_SIZE   = size of marker + size of all fields   // = 7 bytes total


#----------------------------------------------------------------------
#PACK  (used by the POD: turn its state into bytes to broadcast)
#----------------------------------------------------------------------

FUNCTION pack(pod_id, presence, unusual, sequence):
    take the MARKER
    append pod_id
    append VERSION
    append presence
    append unusual
    append sequence
    return the combined bytes


#----------------------------------------------------------------------
#UNPACK  (used by the HUB: turn received bytes back into values)
#----------------------------------------------------------------------

FUNCTION unpack(data):

    IF data is empty:
        return nothing            // ignore, not a pod

    IF length of data is not PACKET_SIZE:
        return nothing            // wrong size, not our packet

    IF the first bytes are not the MARKER:
        return nothing            // not a Pear Pie packet, ignore it

    read the fields after the marker:
        pod_id, version, presence, unusual, sequence

    IF version is not one we understand:
        return nothing            // a future packet format we can't read

    return (pod_id, version, presence, unusual, sequence)


#----------------------------------------------------------------------
#SELF-TEST  (runs only if this file is run on its own; needs no BLE)
#----------------------------------------------------------------------

IF this file is run directly:
    packet = pack(pod_id=3, presence=1, unusual=0, sequence=5)
    print the packed bytes and the packet size
    result = unpack(packet)
    print the unpacked values
    check result matches what went in    // proves round-trip works
    check unpack(random rubbish) returns nothing   // proves the filter works
    print "self-test passed"