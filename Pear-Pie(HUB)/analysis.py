# derive dwell-time and movement-between-spaces from the logs.
# (AKA "how long, which spaces" etc etc)
import pandas as pd

import dataset
import pod_registry

def load_log(path=None):
    """Read the CSV into a dataframe, map pod_id -> space."""
    return dataset.load(path)

def _presence_runs(df):
    """Collapse the per-broadcast rows into continuous presence 'runs' per
    space: (space, start_ts, end_ts). A run breaks when the space changes."""
    runs = []
    active = df[df["unusual"] == 1].sort_values("timestamp")
    if active.empty:
        return pd.DataFrame(columns=["space", "start", "end", "duration_s"])

    cur_space = None
    start = end = None
    GAP = 60  # seconds; a gap longer than this ends the run

    for _, row in active.iterrows():
        s, ts = row["space"], row["timestamp"]
        if cur_space is None:
            cur_space, start, end = s, ts, ts
        elif s == cur_space and (ts - end) <= GAP:
            end = ts
        else:
            runs.append((cur_space, start, end))
            cur_space, start, end = s, ts, ts
    runs.append((cur_space, start, end))

    out = pd.DataFrame(runs, columns=["space", "start", "end"])
    out["duration_s"] = out["end"] - out["start"]
    return out

def dwell_times(df):
    """How long presence stayed in each space (total + per-visit stats)."""
    runs = _presence_runs(df)
    if runs.empty:
        return pd.DataFrame(columns=["space", "visits", "total_s", "mean_s"])
    g = runs.groupby("space")["duration_s"]
    return pd.DataFrame({
        "visits": g.count(),
        "total_s": g.sum(),
        "mean_s": g.mean(),
    }).reset_index()

def movements(df):
    """Sequence of space-to-space transitions, with timing."""
    runs = _presence_runs(df).sort_values("start").reset_index(drop=True)
    moves = []
    for i in range(1, len(runs)):
        prev, cur = runs.iloc[i - 1], runs.iloc[i]
        moves.append({
            "from": prev["space"],
            "to": cur["space"],
            "at": cur["start"],
            "gap_s": cur["start"] - prev["end"],
        })
    return pd.DataFrame(moves)
