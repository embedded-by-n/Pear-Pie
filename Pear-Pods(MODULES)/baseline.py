# =============================================================================
# baseline.py  (POD)
# =============================================================================
# Adaptive Baseline (Exponentially Weighted Moving Average).
# Keeps a running sense of "what's normal for this sensor", leaning on recent
# readings so old ones fade. Lets the pod judge when a reading is unusually
# high (presence) without needing a clock - it learns from the readings alone.
# =============================================================================

class AdaptiveBaseline:
    def __init__(self, alpha):
        self.alpha = alpha      # learning rate (small = slow, steady)
        self.mean = None        # the running "normal" level (None until first reading)

    def update(self, x):
        """Fold a new reading into the running normal."""
        if self.mean is None:
            self.mean = x
        else:
            self.mean = (self.alpha * x) + ((1 - self.alpha) * self.mean)
        return self.mean

    def is_unusual(self, x, threshold):
        """True if this reading sits more than `threshold` above the normal."""
        if self.mean is None:
            return False
        return (x - self.mean) > threshold