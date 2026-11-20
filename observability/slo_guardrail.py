import json
import sys
from typing import Any, Dict, List


def validate_slo_payload(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("SLO payload must be a JSON object")

    for field in ["service", "environment"]:
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"{field} must be a non-empty string")

    for num_field in ["availability_pct", "target_slo_pct", "p99_latency_ms", "max_p99_ms", "error_budget_burn_rate"]:
        val = data.get(num_field)
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            raise ValueError(f"{num_field} must be a number")

    if not (0.0 <= float(data["availability_pct"]) <= 100.0):
        raise ValueError("availability_pct must be between 0 and 100")
    if not (0.0 <= float(data["target_slo_pct"]) <= 100.0):
        raise ValueError("target_slo_pct must be between 0 and 100")
    if float(data["p99_latency_ms"]) < 0 or float(data["max_p99_ms"]) <= 0:
        raise ValueError("Latency thresholds must be non-negative (and max_p99_ms > 0)")
    if float(data["error_budget_burn_rate"]) < 0:
        raise ValueError("error_budget_burn_rate must be non-negative")

    return data


def evaluate_slo_health(slo: Dict[str, Any]) -> List[str]:
    alerts: List[str] = []
    avail = float(slo["availability_pct"])
    target = float(slo["target_slo_pct"])
    p99 = float(slo["p99_latency_ms"])
    max_p99 = float(slo["max_p99_ms"])
    burn = float(slo["error_budget_burn_rate"])

    if avail < target:
        alerts.append(f"Availability SLO breached: {avail:.3f}% < target {target:.3f}%")
    if p99 > max_p99:
        alerts.append(f"P99 latency exceeded: {p99:.1f}ms > limit {max_p99:.1f}ms")
    if burn >= 2.0:
        alerts.append(f"High error budget burn rate detected: {burn:.2f}x (freeze risky rollouts)")

    return alerts


def main() -> int:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            raise ValueError("Empty input on stdin")
        if len(raw.encode("utf-8")) > 1048576:
            raise ValueError("Input exceeds 1 MiB limit")
        parsed = json.loads(raw)
        slo = validate_slo_payload(parsed)
    except Exception as exc:
        print(f"[SLO_RUNTIME_ERROR] {exc}", file=sys.stderr)
        return 2

    alerts = evaluate_slo_health(slo)
    if alerts:
        for item in alerts:
            print(f"[SLO_ALERT] {item}", file=sys.stderr)
        return 1

    print(f"[SLO_HEALTHY] {slo['service']} ({slo['environment']}) within SLO")
    return 0


if __name__ == "__main__":
    sys.exit(main())
      
