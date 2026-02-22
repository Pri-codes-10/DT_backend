"""Graph-related routes and helpers for health trajectory visualization."""

from typing import Dict, Any, List


class GraphRoutes:
    """Helpers for computing health score and trajectory between two vitals sets.

    The module provides a lightweight health scoring heuristic (0-100) built from
    common vital signs and a helper to produce a minimal payload suitable for
    plotting a previous -> current trajectory.
    """

    # Metric configuration: (ideal_value, tolerance_for_100_to_0)
    _METRIC_CONFIG = {
        "heart_rate": (150.0, 20.0),
        "bp_systolic": (110.0, 60.0),
        "bp_diastolic": (75.0, 40.0),
        "oxygen_saturation": (98.0, 10.0),
        "respiratory_rate": (16.0, 8.0),
    }

    @staticmethod
    def compute_health_score(vitals: Dict[str, float]) -> float:
        """Compute a 0-100 health score from vital sign measurements.

        Args:
            vitals: Mapping of vital name to numeric value.

        Returns:
            A float health score in range [0.0, 100.0]. Higher is better.
        """
        scores: List[float] = []

        for metric, (ideal, tol) in GraphRoutes._METRIC_CONFIG.items():
            value = float(vitals.get(metric, ideal))
            deviation = abs(value - ideal)
            # Linear decay: 0 deviation -> 100, deviation >= tol -> 0
            metric_score = max(0.0, 100.0 - (deviation / tol) * 100.0)
            scores.append(metric_score)

        if not scores:
            return 0.0

        # Average across metrics and clamp
        avg = sum(scores) / len(scores)
        return float(max(0.0, min(100.0, avg)))

    @staticmethod
    def compute_health_trajectory(prev_vitals: Dict[str, float], curr_vitals: Dict[str, float]) -> Dict[str, Any]:
        """Produce a payload with previous/current health scores and trajectory info.

        Args:
            prev_vitals: Vital signs at previous timepoint.
            curr_vitals: Vital signs at current timepoint.

        Returns:
            Dict containing `previous_score`, `current_score`, `delta`, `trend`, and
            `series` appropriate for plotting (list of two points).
        """
        prev_score = GraphRoutes.compute_health_score(prev_vitals)
        curr_score = GraphRoutes.compute_health_score(curr_vitals)

        delta = curr_score - prev_score

        if delta > 2.0:
            trend = "improving"
        elif delta < -2.0:
            trend = "declining"
        else:
            trend = "stable"

        series = [
            {"label": "previous", "score": round(prev_score, 2), "vitals": prev_vitals},
            {"label": "current", "score": round(curr_score, 2), "vitals": curr_vitals},
        ]

        return {
            "previous_score": round(prev_score, 2),
            "current_score": round(curr_score, 2),
            "delta": round(delta, 2),
            "trend": trend,
            "series": series,
        }


__all__ = ["GraphRoutes"]
