import json
import subprocess
import sys
from pathlib import Path

GUARDRAIL_SCRIPT = Path(__file__).resolve().parent / "rollout_guardrail.py"


def run_guardrail(payload_text: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GUARDRAIL_SCRIPT)],
        input=payload_text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_rollout_guardrail_allowed() -> None:
    payload = json.dumps(
        {
            "app": "order-service",
            "cluster": "prod-eks-01",
            "namespace": "orders",
            "strategy": "canary",
            "replicas": 3,
            "canary_percent": 15,
        }
    )
    proc = run_guardrail(payload)
    assert proc.returncode == 0, f"Expected 0, got {proc.returncode}: {proc.stderr}"


def test_rollout_guardrail_malformed_json() -> None:
    proc = run_guardrail("{broken-rollout-json")
    assert proc.returncode == 2, f"Expected 2, got {proc.returncode}"


def test_rollout_guardrail_exceeds_1mib() -> None:
    oversized = json.dumps({"payload": "v" * 1100000})
    proc = run_guardrail(oversized)
    assert proc.returncode == 2, f"Expected 2, got {proc.returncode}"


if __name__ == "__main__":
    test_rollout_guardrail_allowed()
    test_rollout_guardrail_malformed_json()
    test_rollout_guardrail_exceeds_1mib()
    print("ALL_ROLLOUT_GUARDRAIL_TESTS_PASSED")
