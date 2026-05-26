#static map: pod_id in space/location.
# =============================================================================
# pod_registry.py  (HUB)
# =============================================================================
# Static map of pod_id -> the space it sits in and what it does.
# The hub uses this to turn a bare pod_id from a packet into meaning
# ("pod 1 = hallway"). Edit this when you add or move a pod.
#
# v1: all pods are identical presence pods; only their location differs.
# =============================================================================

POD_REGISTRY = {
    1: {"space": "hallway",  "role": "presence"},
    2: {"space": "lounge",   "role": "presence"},
    3: {"space": "kitchen",  "role": "presence"},
    4: {"space": "bedroom",  "role": "presence"},
}


def get_space(pod_id):
    """Return the space name for a pod_id, or 'unknown' if not registered."""
    pod = POD_REGISTRY.get(pod_id)
    return pod["space"] if pod else "unknown"


def get_role(pod_id):
    pod = POD_REGISTRY.get(pod_id)
    return pod["role"] if pod else "unknown"