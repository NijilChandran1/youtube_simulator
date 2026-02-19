class ProximityComparator:
    PERFECT_TOLERANCE_MS = 1000      # ≤1 second
    ACCEPTABLE_TOLERANCE_MS = 2000   # ≤2 seconds
    MISS_TOLERANCE_MS = 5000         # ≤5 seconds
    
    def evaluate_attempt(
        self, 
        user_timestamp: float, 
        ground_truth_timestamp: float
    ) -> tuple[str, float]:
        """
        Evaluate how close the user's attempt was to the ground truth.
        Returns: (accuracy_level, difference_in_ms)
        
        Accuracy levels:
        - perfect: ≤1 second
        - acceptable: 1-2 seconds
        - miss: 2-5 seconds
        - false_positive: >5 seconds (wrong timing)
        """
        diff_ms = abs(user_timestamp - ground_truth_timestamp) * 1000
        
        if diff_ms <= self.PERFECT_TOLERANCE_MS:
            return "perfect", diff_ms
        elif diff_ms <= self.ACCEPTABLE_TOLERANCE_MS:
            return "acceptable", diff_ms
        elif diff_ms <= self.MISS_TOLERANCE_MS:
            return "miss", diff_ms
        else:
            return "false_positive", diff_ms
