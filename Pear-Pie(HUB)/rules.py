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
# =============================================================================
# rules.py  (HUB)  -  second-order step, now informed by the trained model
# =============================================================================
# Frequency baseline as before, THEN the trained decision tree predicts the
# user's likely next space for the current hour, and that pod is pre-warmed
# (made more sensitive) so it is ready before the user arrives. This is the
# tree actually driving a decision, not just sitting trained on disk.
# =============================================================================

import analysis
import config
import model
import pod_registry

ALPHA_MIN, ALPHA_MAX         = 0.005, 0.05
THRESHOLD_MIN, THRESHOLD_MAX = 0.3, 0.7
DEFAULT_ALPHA     = 0.01
DEFAULT_THRESHOLD = 0.5
PREWARM_DELTA     = 0.1   # how much more sensitive the predicted-next pod gets


def _clamp(x, lo, hi):
    return lo if x < lo else (hi if x > hi else x)


def compute_updates(path=None):
    """Return {pod_id: {"alpha": a, "threshold": t}} from the logged data.
    Frequency sets the baseline; the trained tree pre-warms the predicted
    next pod. Safe to call any time; returns {} if the log can't be read."""
    try:
        df = analysis.load_log(path)
    except Exception as e:
        print("rules: could not load log:", e)
        return {}

    if df.empty:
        return {}

    updates = {}
    # baseline: presence frequency per pod
    for pod_id, grp in df.groupby("pod_id"):
        present = (grp["presence"] == 1).sum()
        frac = present / len(grp) if len(grp) else 0.0
        threshold = THRESHOLD_MIN + frac * (THRESHOLD_MAX - THRESHOLD_MIN)
        alpha     = ALPHA_MIN + frac * (ALPHA_MAX - ALPHA_MIN)
        updates[int(pod_id)] = {
            "alpha":     round(_clamp(alpha, ALPHA_MIN, ALPHA_MAX), 4),
            "threshold": round(_clamp(threshold, THRESHOLD_MIN, THRESHOLD_MAX), 3),
        }

    # --- the ML step: predict the next space and pre-warm that pod ----------
    try:
        if model.is_ready():
            last = df.sort_values("timestamp").iloc[-1]
            from_space = last["space"]
            hour = int(last["hour"])
            dow = int(last["dow"])
            predicted = model.predict_next_space(hour, dow, from_space)
            if predicted:
                pid = pod_registry.get_pod_for_space(predicted)
                if pid in updates:
                    t = updates[pid]["threshold"] - PREWARM_DELTA
                    updates[pid]["threshold"] = round(
                        _clamp(t, THRESHOLD_MIN, THRESHOLD_MAX), 3)
                    print("model predicts next space:", predicted,
                          "-> pre-warming pod", pid)
    except Exception as e:
        print("rules: model step skipped:", e)

    return updates


if __name__ == "__main__":
    ups = compute_updates()
    if not ups:
        print("no updates (no/empty log). Run simulator.py first to test.")
    else:
        for pod_id, vals in sorted(ups.items()):
            print("pod %d -> alpha %.4f, threshold %.3f"
                  % (pod_id, vals["alpha"], vals["threshold"]))
                  % (pod_id, vals["alpha"], vals["threshold"]))
