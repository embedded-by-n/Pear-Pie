# =============================================================================
# main.py  (HUB)
# =============================================================================
# The hub:
#   1. Logs every pod broadcast to the CSV (one shared timebase, hub's clock).
#   2. On a slow cycle, learns from the log, works out per-pod parameter
#      updates, and pushes them back down to the pods.
#
# This closes the second-order loop: the hub observes the network over time
# and adjusts the rules the pods follow. The cycle is deliberately slow
# (LEARN_EVERY_S) - second-order adaptation happens over hours, not seconds.
#
# Graceful degradation: if learning has too little data yet, it just keeps
# logging and tries again next cycle. Pods keep running on last-known params.
# =============================================================================

import time
import data_logger
import learn
import rules
import pusher

LEARN_EVERY_S = 3600          # how often to retrain + push (seconds). 1 hour.
# import hub_sensor           # TODO: 60GHz own-room radar (needs module ID)


def main():
    print("Pear Pie hub starting...")

    # start logging pod broadcasts to the CSV (background BLE scan)
    data_logger.start()
    print("logging pods ->", data_logger.LOG_FILE)

    # TODO: start the hub's own 60GHz radar sensing here, logged as a pod,
    # once the 60GHz module is identified and its read code written.

    last_learn = time.time()

    try:
        while True:
            time.sleep(1)

            # periodic second-order cycle: learn -> decide -> push
            if time.time() - last_learn >= LEARN_EVERY_S:
                last_learn = time.time()
                print("--- second-order cycle: learning from log ---")

                model = learn.run()              # trains + saves if enough data
                updates = rules.compute_updates()  # per-pod alpha/threshold

                if updates:
                    # pause scanning while we advertise updates, then resume
                    data_logger.stop()
                    pusher.push_all(updates)
                    data_logger.start()
                    print("--- pushed", len(updates), "updates, back to logging ---")
                else:
                    print("--- not enough data to push yet ---")

    except KeyboardInterrupt:
        data_logger.stop()
        pusher.stop()
        print("hub stopped")


if __name__ == "__main__":
    main()
