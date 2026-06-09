# static map: pod_id -> space/location, plus stable space encoding for ML.
POD_REGISTRY = {
    1: {"space": "hallway",  "role": "presence"},
    2: {"space": "lounge",   "role": "presence"},
    3: {"space": "kitchen",  "role": "presence"},
    4: {"space": "bedroom",  "role": "presence"},
}


def get_space(pod_id):
    pod = POD_REGISTRY.get(pod_id)
    return pod["space"] if pod else "unknown"


def get_role(pod_id):
    pod = POD_REGISTRY.get(pod_id)
    return pod["role"] if pod else "unknown"


def _spaces_sorted():
    """Deterministic, alphabetical list of known spaces. Stable as long as
    POD_REGISTRY is fixed, so train-time and predict-time codes always match."""
    return sorted({m["space"] for m in POD_REGISTRY.values()})


def space_code(space):
    """Stable integer code for a space name (or -1 if unknown)."""
    s = _spaces_sorted()
    return s.index(space) if space in s else -1


def get_pod_for_space(space):
    """First pod_id sitting in a given space, or None."""
    for pid, meta in POD_REGISTRY.items():
        if meta["space"] == space:
            return pid
    return None
