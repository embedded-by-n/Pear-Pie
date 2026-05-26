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