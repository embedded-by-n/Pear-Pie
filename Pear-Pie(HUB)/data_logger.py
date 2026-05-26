# #append each received reading to the CSV over time
# =============================================================================
# data_logger.py  (HUB)
# =============================================================================
# Listens for pod gossip (via the same BLE scan as observer) and appends each
# received reading to a CSV that grows over time. The HUB applies the
# timestamp from its own clock, so all pods share one consistent time base
# (needed for dwell-time and movement-between-spaces analysis later).
#
# Runs on the hub (full Python on the Pi). Needs uplink_packet.py present.
# =============================================================================

import bluetooth
import time
import csv
import os
from uplink_packet import unpack

_IRQ_SCAN_RESULT = 5

LOG_FILE = "pod_log.csv"
COLUMNS  = ["timestamp", "pod_id", "presence", "unusual", "sequence", "rssi"]

_ble = bluetooth.BLE()
_ble.active(True)


def _ensure_header():
    """Write the column header once, if the file doesn't exist yet."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            csv.writer(f).writerow(COLUMNS)


def _log_row(reading, rssi):
    """Append one reading as a CSV row. Hub stamps the time."""
    row = [
        time.time(),            # hub's clock - single consistent timebase
        reading["pod_id"],
        reading["presence"],
        reading["unusual"],
        reading["sequence"],
        rssi,
    ]
    with open(LOG_FILE, "a", newline="") as f:
        csv.writer(f).writerow(row)
    print("logged:", row)


def _extract_payload(adv_data):
    """Pull our packet out of the advert's manufacturer-data block."""
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


def _on_event(event, data):
    if event == _IRQ_SCAN_RESULT:
        addr_type, addr, adv_type, rssi, adv_data = data
        payload = _extract_payload(adv_data)
        if payload is None:
            return
        reading = unpack(payload)
        if reading is None:
            return
        _log_row(reading, rssi)


def start():
    _ensure_header()
    _ble.irq(_on_event)
    _ble.gap_scan(0, 30000, 30000)


def stop():
    _ble.gap_scan(None)


# --- run directly to start logging ------------------------------------------
if __name__ == "__main__":
    print("logging to", LOG_FILE, "- Ctrl+C to stop")
    start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop()
        print("stopped")