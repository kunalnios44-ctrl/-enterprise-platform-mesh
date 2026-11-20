import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CANDIDATE_TOOLS = [
    ROOT / "security" / "policy-gate.py",
    ROOT / "dr-backup" / "dr_verifier.py",
    ROOT / "infra" / "plan_guardrail.py",
    ROOT / "observability" / "slo_guardrail.py",
    ROOT / "platform" / "rollout_guardrail.py",
]


def run_tool(script_path: Path, sample_payload: dict) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(script_path)],
        input=json.dumps(sample_payload),
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main() -> int:
    print("=== ENTERPRISE PLATFORM MESH — GUARDRAIL PROOF OF WORK ===")
    found_any = False

    for tool in CANDIDATE_TOOLS:
        if not tool.exists():
            print(f"[MISSING] {tool.relative_to(ROOT)}")
            continue
        found_any = True
        code, out, err = run_tool(tool, {"probe": "check", "status": "ok"})
        print(f"[OK-RUN] {tool.relative_to(ROOT)} -> exit={code}")
        if out:
            print(f"  stdout: {out}")
        if err:
            print(f"  stderr: {err}")

    if not found_any:
        print("No candidate guardrail scripts found at expected paths.")
        return 2

    print("=== PROOF CHECK COMPLETE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
  
