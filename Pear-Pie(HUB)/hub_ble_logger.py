#!/usr/bin/env python3
# =============================================================================
# hub_ble_logger.py  (HUB)  -  Pi-native BLE receiver using bleak
# =============================================================================
# The pods broadcast their state as BLE manufacturer-data adverts. On the Pico
# that uses MicroPython's bluetooth.BLE(); the Pi can't run that API, so on the
# Pi we listen with `bleak` instead. The radio adverts are identical; only the
# listening library differs.
#
# This script:
#   1. Scans continuously for BLE adverts.
#   2. Picks out Pear Pie packets (manufacturer company id 0xFFFF, marker "PP").
#   3. Unpacks them with the SHARED uplink_packet contract (same file the pods
#      use), stamps the hub's clock + RSSI, and appends to pod_log.csv.
#   4. Prints each logged row so you can SEE it working.
#
# That CSV is exactly what dataset.py / analysis.py / learn.py already read, so
# once this is logging real pod data, the whole learning pipeline runs on it.
#
# SETUP (on the Pi, in your venv):
#   pip install bleak
#   (Bluetooth must be on:  sudo systemctl status bluetooth )
#
# RUN (from the hub folder, so it can import uplink_packet):
#   python hub_ble_logger.py
#
# Then walk in front of your pod and watch lines appear. Ctrl+C to stop.
# =============================================================================

import asyncio
import csv
import os
import time

from bleak import BleakScanner

from uplink_packet import unpack, MARKER   # shared contract, same as the pods

LOG_FILE = "pod_log.csv"
COLUMNS = ["timestamp", "pod_id", "presence", "unusual", "sequence", "rssi"]

COMPANY_ID = 0xFFFF        # the pods wrap their payload under company id 0xFFFF

_seen_count = 0


def _ensure_header():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            csv.writer(f).writerow(COLUMNS)


def _log_row(reading, rssi):
    row = [
        time.time(),              # hub's clock - one consistent timebase
        reading["pod_id"],
        reading["presence"],
        reading["unusual"],
        reading["sequence"],
        rssi,
    ]
    with open(LOG_FILE, "a", newline="") as f:
        csv.writer(f).writerow(row)
    print("logged:", row)


def _payload_from_advert(advertisement_data):
    """Find the Pear Pie payload in an advert's manufacturer data.
    bleak gives manufacturer_data as {company_id: value_bytes}. The pods use
    company id 0xFFFF and the value is the payload (marker 'PP' + fields)."""
    mfg = advertisement_data.manufacturer_data or {}
    # primary path: our company id
    payload = mfg.get(COMPANY_ID)
    if payload and payload[:len(MARKER)] == MARKER:
        return bytes(payload)
    # defensive fallback: any manufacturer entry whose value looks like ours
    for value in mfg.values():
        if value and bytes(value)[:len(MARKER)] == MARKER:
            return bytes(value)
    return None


def _on_detect(device, advertisement_data):
    global _seen_count
    payload = _payload_from_advert(advertisement_data)
    if payload is None:
        return
    reading = unpack(payload)         # None if not a valid Pear Pie packet
    if reading is None:
        return
    _seen_count += 1
    _log_row(reading, advertisement_data.rssi)


async def main():
    _ensure_header()
    print("Pear Pie hub BLE logger starting (bleak).")
    print("logging to", LOG_FILE, "- walk in front of a pod. Ctrl+C to stop.")
    scanner = BleakScanner(detection_callback=_on_detect)
    await scanner.start()
    try:
        while True:
            await asyncio.sleep(5)
            print("  ...listening (packets logged so far: %d)" % _seen_count)
    except asyncio.CancelledError:
        pass
    finally:
        await scanner.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nstopped")
