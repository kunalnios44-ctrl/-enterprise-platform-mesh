import json
import subprocess
import sys
from pathlib import Path

GUARDRAIL_SCRIPT = Path(__file__).resolve().parent / "slo_guardrail.py"


def run_guardrail(payload_text: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GUARDRAIL_SCRIPT)],
        input=payload_text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_slo_guardrail_healthy() -> None:
    payload = json.dumps(
        {
            "service": "payments-api",
            "environment": "prod",
            "availability_pct": 99.98,
            "target_slo_pct": 99.95,
            "p99_latency_ms": 140,
            "max_p99_ms": 250,
            "error_budget_burn_rate": 0.4,
        }
    )
    proc = run_guardrail(payload)
    assert proc.returncode == 0, f"Expected 0, got {proc.returncode}: {proc.stderr}"


def test_slo_guardrail_malformed_json() -> None:
    proc = run_guardrail("{broken-slo-json")
    assert proc.returncode == 2, f"Expected 2, got {proc.returncode}"


def test_slo_guardrail_exceeds_1mib() -> None:
    oversized = json.dumps({"payload": "w" * 1100000})
    proc = run_guardrail(oversized)
    assert proc.returncode == 2, f"Expected 2, got {proc.returncode}"


if __name__ == "__main__":
    test_slo_guardrail_healthy()
    test_slo_guardrail_malformed_json()
    test_slo_guardrail_exceeds_1mib()
    print("ALL_SLO_GUARDRAIL_TESTS_PASSED")
