# =============================================================================
# neighbours.py  (POD)
# =============================================================================
# Each pod hears the broadcasts of OTHER pods in radio range. This module
# turns those into a sense of relative proximity, who is near, and when that
# relationship changes, using BLE signal strength (RSSI).
#
# HONEST LIMITS: RSSI is a coarse, noisy proximity cue. It is good for "near /
# far / which pods are close" and for detecting CHANGE (the person moved
# between two pods and the signal shifted). It is NOT reliable for precise
# distance in metres. So we track relative strength and flag significant
# shifts, we never claim exact distance.
#
# This is the relational layer: a pod builds a live picture of its neighbours
# from what it overhears, without any pod relaying messages (simplex mesh).
# =============================================================================

import time

WINDOW       = 20      # rolling RSSI samples kept per neighbour
BASELINE_MIN = 20      # samples needed before a baseline is set
SHIFT_DBM    = 6       # dBm change from baseline counted as "significant"
STALE_MS     = 30000   # forget a neighbour not heard for this long (ms)

# pod_id -> {"history": [...], "baseline": float|None, "last_seen": ms}
_neighbours = {}


def record(pod_id, rssi):
    """Log one heard advert from another pod. Updates its rolling RSSI and,
    once enough samples exist, its baseline. Returns True if this advert marks
    a significant proximity shift from that neighbour's baseline."""
    now = time.ticks_ms() if hasattr(time, "ticks_ms") else int(time.time() * 1000)

    n = _neighbours.get(pod_id)
    if n is None:
        n = {"history": [], "baseline": None, "last_seen": now}
        _neighbours[pod_id] = n

    n["history"].append(rssi)
    if len(n["history"]) > WINDOW:
        n["history"] = n["history"][-WINDOW:]
    n["last_seen"] = now

    avg = sum(n["history"]) / len(n["history"])

    # set the baseline once we have enough samples to trust it
    if n["baseline"] is None and len(n["history"]) >= BASELINE_MIN:
        n["baseline"] = avg
        return False

    # flag a significant shift (person moved, relationship changed)
    if n["baseline"] is not None and abs(avg - n["baseline"]) >= SHIFT_DBM:
        return True
    return False


def _prune(now):
    """Drop neighbours not heard from in a while."""
    dead = [pid for pid, n in _neighbours.items()
            if time.ticks_diff(now, n["last_seen"]) > STALE_MS] \
        if hasattr(time, "ticks_diff") else \
        [pid for pid, n in _neighbours.items()
         if now - n["last_seen"] > STALE_MS]
    for pid in dead:
        del _neighbours[pid]


def get_neighbours():
    """Return a snapshot: {pod_id: {"avg_rssi":..,"baseline":..,"samples":..}}.
    Stronger (less negative) avg_rssi = nearer."""
    now = time.ticks_ms() if hasattr(time, "ticks_ms") else int(time.time() * 1000)
    _prune(now)
    out = {}
    for pid, n in _neighbours.items():
        if not n["history"]:
            continue
        out[pid] = {
            "avg_rssi": sum(n["history"]) / len(n["history"]),
            "baseline": n["baseline"],
            "samples":  len(n["history"]),
        }
    return out


def nearest():
    """Return the pod_id of the currently strongest (nearest-sounding)
    neighbour, or None if none heard yet."""
    snap = get_neighbours()
    if not snap:
        return None
    return max(snap.items(), key=lambda kv: kv[1]["avg_rssi"])[0]


# --- self-test ---------------------------------------------------------------
if __name__ == "__main__":
    # simulate hearing pod 2 steadily, then it getting closer (stronger RSSI)
    for _ in range(20):
        record(2, -70)
    print("after baseline:", get_neighbours())
    shifted = False
    for _ in range(20):
        if record(2, -55):     # signal jumped ~15 dBm stronger
            shifted = True
    print("shift detected:", shifted)
    record(3, -80)
    print("nearest pod:", nearest())   # pod 2 (stronger) should win
    print("snapshot:", get_neighbours())
