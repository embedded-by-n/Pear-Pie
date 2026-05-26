# derive dwell-time and movement-between-spaces from the logs. (AKA "how long, which spaces" etc etc)
import pandas as pd
import pod_registry

def load_log(path):
    """Read the CSV into a dataframe, map pod_id -> space."""
    # TODO

def dwell_times(df):
    """How long presence stayed in each space."""
    # TODO

def movements(df):
    """Sequence of space-to-space transitions, with timing."""
    # TODO