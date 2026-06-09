# Generates realistic fake movement data into the CSV, so analysis and
# learning can be built/tested before/alongside the real radar data.
# Writes the SAME schema as data_logger.py, so analysis.py and learn.py
# can't tell simulated from real. Matched to the eight-pod layout.
# Run:  python simulator.py --minutes 240   (optionally --days-ago N)

import csv
import os
import random
import time
import argparse

import config
import pod_registry

COLUMNS = ["timestamp", "pod_id", "presence", "unusual", "sequence", "rssi"]

# Plausible adjacency for the real home: where a person tends to go next.
# Keys/values are space names from pod_registry. Repeats bias the random pick.
_TRANSITIONS = {
    "hallway":         ["kitchen_cooking", "kitchen_island", "office", "hallway"],
    "kitchen_cooking": ["kitchen_island", "hallway", "kitchen_cooking"],
    "kitchen_island":  ["kitchen_cooking", "lounge", "bedroom_doorway", "office", "hallway"],
    "office":          ["hallway", "kitchen_island", "office", "office"],
    "lounge":          ["kitchen_island", "bedroom_doorway", "lounge", "lounge"],
    "bedroom_doorway": ["bedroom", "bathroom", "kitchen_island", "lounge"],
    "bathroom":        ["bedroom_doorway", "bedroom", "bathroom"],
    "bedroom":         ["bedroom_doorway", "bathroom", "bedroom", "bedroom"],
}

# Rough dwell time (seconds) per space - how long a person lingers.
_DWELL = {
    "hallway":         (5, 30),
    "kitchen_cooking": (120, 1800),
    "kitchen_island":  (30, 600),
    "office":          (600, 7200),     # study sessions (the Time Timer pod)
    "lounge":          (300, 5400),
    "bedroom_doorway": (3, 20),
    "bathroom":        (60, 900),
    "bedroom":         (1800, 28800),   # sleep
}


def _space_to_pod():
    """Invert pod_registry: space name -> pod_id (first match wins)."""
    out = {}
    for pod_id, meta in pod_registry.POD_REGISTRY.items():
        out.setdefault(meta["space"], pod_id)
    return out


def _time_of_day_bias(hour):
    """A likely starting space given the hour, to make days realistic."""
    if 0 <= hour < 7:
        return "bedroom"
    if 7 <= hour < 9:
        return "kitchen_cooking"
    if 9 <= hour < 17:
        return "office"
    if 17 <= hour < 19:
        return "kitchen_cooking"
    if 19 <= hour < 22:
        return "lounge"
    if 22 <= hour < 24:
        return "bedroom"
    return random.choice(["lounge", "kitchen_island", "office"])


def simulate(minutes, start_time=None, log_file=None):
    """Produce rows of a person moving between spaces with realistic timing.
    Appends to the CSV (creating header if needed). Returns rows written."""
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

            step = 10  # seconds between logged broadcasts while present
            elapsed = 0
            while elapsed < dwell and t < end_time:
                writer.writerow([
                    round(t, 3),
                    pod_id,
                    1,                                  # presence
                    1 if random.random() < 0.03 else 0, # unusual: occasional
                    sequence % 256,
                    random.randint(-85, -45),           # plausible RSSI
                ])
                rows_written += 1
                sequence += 1
                t += step
                elapsed += step

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
