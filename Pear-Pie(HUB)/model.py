# load the trained model and make predictions.
#
# Thin wrapper so rules.py and any status display can ask the trained model
# questions without knowing how it was stored.

import os
import joblib

import config

_cache = {"model": None, "path": None}

def load(path=None):
    """Load the persisted model from disk (cached)."""
    path = path or config.MODEL_FILE
    if _cache["model"] is not None and _cache["path"] == path:
        return _cache["model"]
    if not os.path.exists(path):
        return None
    model = joblib.load(path)
    _cache["model"], _cache["path"] = model, path
    return model

def predict_next_space(hour, dow, from_code, path=None):
    """Predict the next space given time + current space code."""
    model = load(path)
    if model is None:
        return None
    return model.predict([[hour, dow, from_code]])[0]

def is_ready(path=None):
    """True if a trained model exists on disk."""
    return load(path) is not None
