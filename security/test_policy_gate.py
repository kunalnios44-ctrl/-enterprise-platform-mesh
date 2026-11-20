import json
import subprocess
import sys
from pathlib import Path

GATE_SCRIPT = Path(__file__).resolve().parent / "policy-gate.py"


def run_gate(payload_text: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GATE_SCRIPT)],
        input=payload_text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_policy_gate_pass() -> None:
    payload = json.dumps({"service": "checkout", "environment": "prod", "policy": "strict"})
    proc = run_gate(payload)
    assert proc.returncode == 0, f"Expected 0, got {proc.returncode}: {proc.stderr}"


def test_policy_gate_malformed_json() -> None:
    proc = run_gate("{not-valid-json")
    assert proc.returncode == 2, f"Expected 2, got {proc.returncode}"


def test_policy_gate_exceeds_1mib() -> None:
    oversized = json.dumps({"blob": "x" * 1100000})
    proc = run_gate(oversized)
    assert proc.returncode == 2, f"Expected 2, got {proc.returncode}"


if __name__ == "__main__":
    test_policy_gate_pass()
    test_policy_gate_malformed_json()
    test_policy_gate_exceeds_1mib()
    print("ALL_POLICY_GATE_TESTS_PASSED")
  
