import json
import subprocess
import sys
from pathlib import Path

GUARDRAIL_SCRIPT = Path(__file__).resolve().parent / "plan_guardrail.py"


def run_guardrail(payload_text: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GUARDRAIL_SCRIPT)],
        input=payload_text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_safe_plan_passes() -> None:
    payload = json.dumps(
        {
            "max_deletes": 2,
            "resource_changes": [
                {
                    "address": "aws_s3_bucket.logs",
                    "actions": ["create"],
                    "after": {"public_access": False, "encrypted": True},
                }
            ],
        }
    )
    proc = run_guardrail(payload)
    assert proc.returncode == 0, f"Expected 0, got {proc.returncode}: {proc.stderr}"


def test_violation_blocks_with_exit_1() -> None:
    payload = json.dumps(
        {
            "max_deletes": 0,
            "resource_changes": [
                {
                    "address": "aws_security_group.ssh",
                    "actions": ["update"],
                    "after": {"cidr_block": "0.0.0.0/0", "from_port": 22},
                }
            ],
        }
    )
    proc = run_guardrail(payload)
    assert proc.returncode == 1, f"Expected 1, got {proc.returncode}"


def test_malformed_input_exits_2() -> None:
    proc = run_guardrail("{bad-json")
    assert proc.returncode == 2, f"Expected 2, got {proc.returncode}"


if __name__ == "__main__":
    test_safe_plan_passes()
    test_violation_blocks_with_exit_1()
    test_malformed_input_exits_2()
    print("ALL_PLAN_GUARDRAIL_TESTS_PASSED")
  
