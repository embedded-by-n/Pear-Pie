# =============================================================================
# main.py  (HUB)
# =============================================================================
# The hub is a pod-AND-coordinator:
#   1. Senses its OWN room via 60GHz radar (another logged space).
#   2. Scans for all the pods' BLE broadcasts and logs them.
#   3. (later) Runs the learning over the logged data.
#
# All events share ONE timebase: the hub stamps every event with its own
# clock as it arrives (no per-pod clocks). An RTC on the hub gives real
# wall-clock time when off-grid (no internet).
# =============================================================================

import time
import data_logger
# import hub_sensor          # TODO: 60GHz own-room radar read (needs module ID)

def main():
    print("Pear Pie hub starting...")

    # start logging pod broadcasts to the CSV (uses the hub's clock)
    data_logger.start()
    print("logging pods ->", data_logger.LOG_FILE)

    # TODO: start the hub's own 60GHz radar sensing here, logged as pod 0 /
    # "hub", once the 60GHz module is identified and its read code written.

    # keep running; the BLE scan + logging happen in the background
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        data_logger.stop()
        print("hub stopped")

if __name__ == "__main__":
    main()