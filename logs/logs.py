import json
from collections import Counter, defaultdict
from datetime import datetime

class ExcessiveLoggingDetector:

    def __init__(
        self,
        logs,
        max_logs_per_second=50,
        max_debug_ratio=0.40,
        repetition_threshold=5,
    ):
        self.logs = logs
        self.max_logs_per_second = max_logs_per_second
        self.max_debug_ratio = max_debug_ratio
        self.repetition_threshold = repetition_threshold

    # ---------------------
    # Helpers
    # ---------------------

    def parse_timestamp(self, ts):
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))

    def group_by_second(self):
        grouped = defaultdict(list)
        for log in self.logs:
            ts = self.parse_timestamp(log["timestamp"])
            grouped[ts.replace(microsecond=0)].append(log)
        return grouped

    # ---------------------
    # Detection Functions
    # ---------------------

    def detect_volume_spikes(self):
        """Check if any second has more logs than allowed."""
        spikes = []
        grouped = self.group_by_second()

        for second, logs in grouped.items():
            if len(logs) > self.max_logs_per_second:
                spikes.append({
                    "timestamp": second.isoformat(),
                    "count": len(logs)
                })

        return spikes

    def detect_debug_ratio(self):
        """Detect excessive DEBUG/TRACE logs."""
        total = len(self.logs)
        debug_or_trace = sum(1 for l in self.logs if l["level"] in ("DEBUG", "TRACE"))
        ratio = debug_or_trace / total if total > 0 else 0

        return {
            "debug_or_trace_count": debug_or_trace,
            "total_logs": total,
            "ratio": ratio,
            "excessive": ratio > self.max_debug_ratio
        }

    def detect_repetitive_messages(self):
        """Detect repeated messages beyond threshold."""
        messages = [log["message"] for log in self.logs]
        counter = Counter(messages)

        repetitive = {msg: count for msg, count in counter.items() if count >= self.repetition_threshold}
        return repetitive

    # ---------------------
    # Global evaluation
    # ---------------------

    def evaluate(self):
        result = {}

        # 1. Volume spikes (logs per second)
        spikes = self.detect_volume_spikes()
        result["volume_spikes"] = spikes
        result["has_volume_spikes"] = len(spikes) > 0

        # 2. Debug ratio
        debug_info = self.detect_debug_ratio()
        result["debug_ratio"] = debug_info

        # 3. Repetitive messages
        repetitive = self.detect_repetitive_messages()
        result["repetitive_messages"] = repetitive
        result["has_repetitive"] = len(repetitive) > 0

        # Final classification
        result["excessive_logging_detected"] = (
            result["has_volume_spikes"]
            or result["debug_ratio"]["excessive"]
            or result["has_repetitive"]
        )

        return result


# -----------------------------
# Example usage
# -----------------------------

if __name__ == "__main__":
    with open("logs.json", "r") as f:
        logs = json.load(f)

    detector = ExcessiveLoggingDetector(logs, max_logs_per_second=5)
    report = detector.evaluate()

    print(json.dumps(report, indent=2))
