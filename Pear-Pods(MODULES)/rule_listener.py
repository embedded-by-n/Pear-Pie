# =============================================================================
# rule_listener.py  (POD)
# =============================================================================
# Pod scans for parameter updates from the hub and applies them (new alpha,
# threshold, target). Mirror of the hub's observer.
# Build last - pairs with pusher.py on the hub.
# =============================================================================

import bluetooth
# from update_packet_format import unpack_update   # TODO: shared contract

_IRQ_SCAN_RESULT = 5

_ble = bluetooth.BLE()
_ble.active(True)


def _on_event(event, data):
    if event == _IRQ_SCAN_RESULT:
        addr_type, addr, adv_type, rssi, adv_data = data
        # TODO: extract payload, unpack_update, check it's for THIS pod,
        # then apply the new parameters.
        pass


def start():
    _ble.irq(_on_event)
    _ble.gap_scan(0, 30000, 30000)


def stop():
    _ble.gap_scan(None)