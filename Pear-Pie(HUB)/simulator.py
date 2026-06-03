# Generates realistic fake movement data into the CSV,
# so analysis and learning can be built/tested before the radar works.
#
# Writes rows in the SAME schema data_logger.py uses, so analysis.py and
# learn.py can't tell simulated data from real pod data.
# Run directly:  python simulator.py --minutes 240

import csv
import os
import random
import time
import argparse

import config
import pod_registry

COLUMNS = ["timestamp", "pod_id", "presence", "unusual", "sequence", "rssi"]

# Plausible adjacency: which space a person tends to move to next.
# Keyed by space name (from pod_registry), values are likely next spaces.
_TRANSITIONS = {
    "hallway":  ["lounge", "kitchen", "bedroom", "hallway"],
    "lounge":   ["hallway", "kitchen", "lounge", "lounge"],
    "kitchen":  ["hallway", "lounge", "kitchen"],
    "bedroom":  ["hallway", "bedroom", "bedroom"],
}

# Rough dwell time (seconds) ranges per space - how long a person lingers.
_DWELL = {
    "hallway":  (5, 30),
    "lounge":   (300, 5400),
    "kitchen":  (120, 1800),
    "bedroom":  (1800, 28800),
}

def _space_to_pod():
    """Invert pod_registry: space name -> pod_id (first match wins)."""
    out = {}
    for pod_id, meta in pod_registry.POD_REGISTRY.items():
        out.setdefault(meta["space"], pod_id)
    return out

def _time_of_day_bias(hour):
    """Return a likely starting space given the hour, to make days realistic."""
    if 0 <= hour < 7:
        return "bedroom"
    if 7 <= hour < 9:
        return "kitchen"
    if 22 <= hour < 24:
        return "bedroom"
    return random.choice(["lounge", "kitchen", "hallway"])

def simulate(minutes, start_time=None, log_file=None):
    """Produce rows of a person moving between spaces with realistic timing.

    Appends to the CSV (creating header if needed). Returns the number of
    rows written. Timestamps are real epoch seconds so the off-grid clock
    assumptions downstream still hold.
    """
    log_file = log_file or config.LOG_FILE
    space_to_pod = _space_to_pod()
    spaces = list(space_to_pod.keys())
    if not spaces:
        raise RuntimeError("pod_registry is empty - nothing to simulate")

    start_time = start_time if start_time is not None else time.time()
    end_time = start_time + minutes * 60

    new_file = not os.path.exists(log_file)
    rows_written = 0
    sequence = 0

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(COLUMNS)

        t = start_time
        hour = time.localtime(int(t)).tm_hour
        current = _time_of_day_bias(hour)
        if current not in space_to_pod:
            current = random.choice(spaces)

        while t < end_time:
            pod_id = space_to_pod[current]
            low, high = _DWELL.get(current, (60, 600))
            dwell = random.randint(low, high)

            # While present in this space, emit periodic "unusual" readings
            # (mirrors a pod broadcasting every ~loop while someone's there).
            step = 10  # seconds between logged broadcasts while present
            elapsed = 0
            while elapsed < dwell and t < end_time:
                # presence reading: 1 while here. unusual: 1 (above baseline).
                writer.writerow([
                    round(t, 3),
                    pod_id,
                    1,          # presence
                    1,          # unusual (person is here, above normal)
                    sequence % 256,
                    random.randint(-85, -45),  # plausible RSSI
                ])
                rows_written += 1
                sequence += 1
                t += step
                elapsed += step

            # transition to next space
            nxt = random.choice(_TRANSITIONS.get(current, spaces))
            current = nxt if nxt in space_to_pod else random.choice(spaces)

    return rows_written

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Simulate pod movement data.")
    ap.add_argument("--minutes", type=int, default=240,
                    help="how many minutes of activity to generate")
    ap.add_argument("--days-ago", type=int, default=0,
                    help="shift the start back this many days (for history)")
    args = ap.parse_args()

    start = time.time() - args.days_ago * 86400
    n = simulate(args.minutes, start_time=start)
    print("wrote", n, "rows to", config.LOG_FILE)
