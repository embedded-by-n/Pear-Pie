# =============================================================================
# rules.py  (HUB)
# =============================================================================
# The second-order step: look at what the hub has learned from the logged
# network data, and decide what parameter updates (alpha, threshold) each pod
# should run. This is the "uniselector" in Ashby terms - but informed by the
# data, not random.
#
# It does NOT command pods. It adjusts the rules they follow, then pusher.py
# broadcasts the result. Pods apply it (or not) on their own.
#
# Logic (deliberately simple and defensible):
#   - For each pod, measure how often it sees presence in the log.
#   - A busy space can afford a slightly higher threshold (less twitchy) and a
#     slightly faster alpha (adapts quicker to a changing normal).
#   - A quiet space gets a lower threshold (stay sensitive to rare events) and
#     a slower alpha (steadier baseline).
#   - All values are clamped to safe bounds so a bad log can't push a pod into
#     a useless state.
# =============================================================================

import analysis
import config

# safe bounds - the system never pushes a pod outside these
ALPHA_MIN, ALPHA_MAX         = 0.005, 0.05
THRESHOLD_MIN, THRESHOLD_MAX = 0.3, 0.7

# defaults if there isn't enough data for a pod yet
DEFAULT_ALPHA     = config_default_alpha = 0.01
DEFAULT_THRESHOLD = 0.5


def _clamp(x, lo, hi):
    return lo if x < lo else (hi if x > hi else x)


def compute_updates(path=None):
    """Return {pod_id: {"alpha": a, "threshold": t}} from the logged data.

    Uses presence frequency per pod as the signal. Pods with no data get the
    defaults. Safe to call any time; returns {} if the log can't be read."""
    try:
        df = analysis.load_log(path)
    except Exception as e:
        print("rules: could not load log:", e)
        return {}

    if df.empty:
        return {}

    updates = {}
    total = len(df)

    # presence fraction per pod (how active is this space, 0..1)
    for pod_id, grp in df.groupby("pod_id"):
        present = (grp["presence"] == 1).sum()
        frac = present / len(grp) if len(grp) else 0.0

        # busy space -> higher threshold + faster alpha; quiet -> the reverse
        threshold = THRESHOLD_MIN + frac * (THRESHOLD_MAX - THRESHOLD_MIN)
        alpha     = ALPHA_MIN + frac * (ALPHA_MAX - ALPHA_MIN)

        updates[int(pod_id)] = {
            "alpha":     round(_clamp(alpha, ALPHA_MIN, ALPHA_MAX), 4),
            "threshold": round(_clamp(threshold, THRESHOLD_MIN, THRESHOLD_MAX), 3),
        }

    return updates


if __name__ == "__main__":
    ups = compute_updates()
    if not ups:
        print("no updates (no/empty log). Run simulator.py first to test.")
    else:
        for pod_id, vals in sorted(ups.items()):
            print("pod %d -> alpha %.4f, threshold %.3f"
                  % (pod_id, vals["alpha"], vals["threshold"]))
