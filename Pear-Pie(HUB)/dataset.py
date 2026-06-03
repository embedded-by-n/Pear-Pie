# helpers to load/clean the CSV for training, the preprocessing step.
#
# Loads pod_log.csv, attaches each row's space (via pod_registry), drops
# obviously broken rows, and sorts by time. analysis.py and learn.py both
# build on top of this so the cleaning logic lives in one place.

import pandas as pd

import config
import pod_registry

COLUMNS = ["timestamp", "pod_id", "presence", "unusual", "sequence", "rssi"]

def load_raw(path=None):
    """Read the CSV into a dataframe with correct dtypes."""
    path = path or config.LOG_FILE
    df = pd.read_csv(path)
    # be tolerant of a header-less or partial file
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("log file missing columns: %s" % missing)
    return df

def clean(df):
    """Drop broken rows, coerce types, sort by time, attach space + role."""
    df = df.copy()
    for col in ["timestamp", "pod_id", "presence", "unusual", "sequence", "rssi"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["timestamp", "pod_id"])
    df["pod_id"] = df["pod_id"].astype(int)
    df["presence"] = df["presence"].fillna(0).astype(int)
    df["unusual"] = df["unusual"].fillna(0).astype(int)
    df = df.sort_values("timestamp").reset_index(drop=True)

    df["space"] = df["pod_id"].map(pod_registry.get_space)
    df["role"] = df["pod_id"].map(pod_registry.get_role)

    # readable datetime for time-of-day features
    df["dt"] = pd.to_datetime(df["timestamp"], unit="s")
    df["hour"] = df["dt"].dt.hour
    df["dow"] = df["dt"].dt.dayofweek  # 0 = Monday
    return df

def load(path=None):
    """Convenience: load + clean in one call."""
    return clean(load_raw(path))
