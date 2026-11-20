import json
import sys
from typing import Any, Dict, List


def validate_payload(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object")
    required_keys = ["oidc_enabled", "iam_least_privilege", "semgrep_critical", "trivy_high_or_critical", "image_ref", "cosign_verified"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required field: {key}")
    if not isinstance(data["oidc_enabled"], bool) or not isinstance(data["iam_least_privilege"], bool) or not isinstance(data["cosign_verified"], bool):
        raise ValueError("Boolean fields must be strictly true/false")
    if not isinstance(data["semgrep_critical"], int) or isinstance(data["semgrep_critical"], bool):
        raise ValueError("semgrep_critical must be an integer")
    if not isinstance(data["trivy_high_or_critical"], int) or isinstance(data["trivy_high_or_critical"], bool):
        raise ValueError("trivy_high_or_critical must be an integer")
    if not isinstance(data["image_ref"], str) or not data["image_ref"].strip():
        raise ValueError("image_ref must be a non-empty string")
    return data


def evaluate_policy(cfg: Dict[str, Any]) -> List[str]:
    violations: List[str] = []
    if not cfg["oidc_enabled"]:
        violations.append("OIDC keyless authentication is disabled")
    if not cfg["iam_least_privilege"]:
        violations.append("IAM/RBAC is not enforced as least-privilege")
    if cfg["semgrep_critical"] > 0:
        violations.append(f"Semgrep critical findings detected: {cfg['semgrep_critical']}")
    if cfg["trivy_high_or_critical"] > 0:
        violations.append(f"Trivy high/critical vulnerabilities detected: {cfg['trivy_high_or_critical']}")
    if not cfg["cosign_verified"]:
        violations.append("Container image is not verified with Cosign")
    if "@sha256:" not in cfg["image_ref"]:
        violations.append("Image reference must be pinned by immutable digest (@sha256:...)")
    return violations


def main() -> int:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            raise ValueError("Empty input on stdin")
        if len(raw.encode("utf-8")) > 1048576:
            raise ValueError("Input exceeds 1 MiB limit")
        parsed = json.loads(raw)
        cfg = validate_payload(parsed)
    except Exception as exc:
        print(f"[RUNTIME_ERROR] {exc}", file=sys.stderr)
        return 2

    violations = evaluate_policy(cfg)
    if violations:
        for v in violations:
            print(f"[POLICY_VIOLATION] {v}", file=sys.stderr)
        return 1

    print(f"[PASS] Zero-trust gate passed for {cfg['image_ref']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
      
