# load the trained model and make predictions.
import os
import joblib

import config
import pod_registry

_cache = {"model": None, "path": None, "mtime": None}

def load(path=None):
    """Load the persisted model, reloading automatically if the file changed
    (so the hub uses the freshly retrained model each cycle)."""
    path = path or config.MODEL_FILE
    if not os.path.exists(path):
        return None
    mtime = os.path.getmtime(path)
    if (_cache["model"] is not None and _cache["path"] == path
            and _cache["mtime"] == mtime):
        return _cache["model"]
    model = joblib.load(path)
    _cache.update(model=model, path=path, mtime=mtime)
    return model

def predict_next_space(hour, dow, from_space, path=None):
    """Predict the next space name given time + current space NAME.
    Encodes the space with the same stable map used in training."""
    model = load(path)
    if model is None:
        return None
    code = pod_registry.space_code(from_space)
    if code < 0:
        return None
    try:
        return model.predict([[hour, dow, code]])[0]
    except Exception:
        return None

def is_ready(path=None):
    return load(path) is not None
