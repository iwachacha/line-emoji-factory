from __future__ import annotations

import subprocess

from conftest import PYTHON, ROOT, run_cmd_args


def test_soeshirushi_example_is_not_stale():
    result = subprocess.run(
        run_cmd_args(PYTHON, ROOT / "tools" / "check-example-drift.py", ROOT / "examples" / "soeshirushi"),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
