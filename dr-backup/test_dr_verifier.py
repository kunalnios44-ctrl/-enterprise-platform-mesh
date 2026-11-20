import json
import subprocess
import sys
from pathlib import Path

VERIFIER_SCRIPT = Path(__file__).resolve().parent / "dr_verifier.py"


def run_verifier(payload_text: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VERIFIER_SCRIPT)],
        input=payload_text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_dr_verifier_pass() -> None:
    payload = json.dumps(
        {
            "cluster": "prod-eks-01",
            "rpo_age_minutes": 10,
            "max_rpo_minutes": 30,
            "restore_verified": True,
        }
    )
    proc = run_verifier(payload)
    assert proc.returncode == 0, f"Expected 0, got {proc.returncode}: {proc.stderr}"


def test_dr_verifier_malformed_json() -> None:
    proc = run_verifier("{broken-json")
    assert proc.returncode == 2, f"Expected 2, got {proc.returncode}"


def test_dr_verifier_exceeds_1mib() -> None:
    oversized = json.dumps({"payload": "y" * 1100000})
    proc = run_verifier(oversized)
    assert proc.returncode == 2, f"Expected 2, got {proc.returncode}"


if __name__ == "__main__":
    test_dr_verifier_pass()
    test_dr_verifier_malformed_json()
    test_dr_verifier_exceeds_1mib()
    print("ALL_DR_VERIFIER_TESTS_PASSED")
  
