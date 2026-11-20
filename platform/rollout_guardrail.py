import json
import sys
from typing import Any, Dict, List


def validate_rollout_spec(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("Rollout spec must be a JSON object")

    for field in ["app", "cluster", "namespace", "strategy"]:
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"{field} must be a non-empty string")

    replicas = data.get("replicas")
    if not isinstance(replicas, int) or isinstance(replicas, bool) or replicas < 1:
        raise ValueError("replicas must be an integer >= 1")

    canary = data.get("canary_percent")
    if not isinstance(canary, int) or isinstance(canary, bool) or not (0 <= canary <= 100):
        raise ValueError("canary_percent must be an integer between 0 and 100")

    return data


def evaluate_rollout(spec: Dict[str, Any]) -> List[str]:
    violations: List[str] = []

    if spec["namespace"].strip().lower() == "default":
        violations.append("Production-style rollout is not allowed in 'default' namespace")

    if spec["strategy"].strip().lower() == "canary" and spec["canary_percent"] > 50:
        violations.append(f"Canary traffic too high ({spec['canary_percent']}% > 50% safe cap)")

    if spec["replicas"] < 2:
        violations.append("High-availability check failed: replicas must be at least 2")

    return violations


def main() -> int:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            raise ValueError("Empty input on stdin")
        if len(raw.encode("utf-8")) > 1048576:
            raise ValueError("Input exceeds 1 MiB limit")
        parsed = json.loads(raw)
        spec = validate_rollout_spec(parsed)
    except Exception as exc:
        print(f"[ROLLOUT_RUNTIME_ERROR] {exc}", file=sys.stderr)
        return 2

    violations = evaluate_rollout(spec)
    if violations:
        for v in violations:
            print(f"[ROLLOUT_VIOLATION] {v}", file=sys.stderr)
        return 1

    print(f"[ROLLOUT_ALLOWED] {spec['app']} -> {spec['cluster']} ({spec['namespace']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
      
