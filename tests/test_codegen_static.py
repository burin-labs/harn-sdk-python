"""Static refusal must name the intended type rule and exact source line."""

import json
import subprocess
import sys
from pathlib import Path

from harn._codegen.api import render
from harn._codegen.request import CodegenIr, CodegenRole

FIXTURE = Path(__file__).parent / "fixtures/codegen"


def test_strict_positive_and_nine_exact_static_refusals(tmp_path):
    ir = CodegenIr.model_validate_json((FIXTURE / "pathological/ir.json").read_bytes())
    (tmp_path / "bindings.py").write_text(render(ir, CodegenRole.BOTH).content)
    configuration = {
        "typeCheckingMode": "strict",
        "pythonVersion": "3.11",
        "extraPaths": [str(Path(__file__).parents[1] / "src")],
        "include": ["bindings.py", "case.py"],
    }
    config = tmp_path / "pyrightconfig.json"
    config.write_text(json.dumps(configuration))
    case = tmp_path / "case.py"
    for positive in (True, False):
        source = (
            FIXTURE / ("static_positive.py" if positive else "static_negative.py")
        ).read_text()
        case.write_text(source)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pyright",
                "--pythonpath",
                sys.executable,
                "--project",
                str(config),
                "--outputjson",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        report = json.loads(result.stdout)
        assert report["summary"]["filesAnalyzed"] >= 2
        if positive:
            assert result.returncode == 0, report
            assert report["generalDiagnostics"] == []
        else:
            expected = [
                (line_number - 1, line.split("# EXPECT ")[1])
                for line_number, line in enumerate(source.splitlines(), 1)
                if "# EXPECT " in line
            ]
            observed = [
                (diagnostic["range"]["start"]["line"], diagnostic["rule"])
                for diagnostic in report["generalDiagnostics"]
                if diagnostic["file"] == str(case)
            ]
            assert result.returncode == 1 and len(expected) == 9
            assert observed == expected, report
            assert len(report["generalDiagnostics"]) == len(expected), report


def test_duplicate_literal_is_refused_by_ruff_before_serve(tmp_path):
    path = tmp_path / "duplicate.py"
    for duplicate in (False, True):
        path.write_text(
            'handlers = {"echo": 1' + (', "echo": 2' if duplicate else "") + "}\n"
        )
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--isolated",
                "--select",
                "F601",
                "--output-format",
                "json",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        diagnostics = json.loads(result.stdout)
        if duplicate:
            assert result.returncode == 1 and len(diagnostics) == 1
            assert (
                diagnostics[0]["code"] == "F601"
                and diagnostics[0]["location"]["row"] == 1
            )
            assert diagnostics[0]["filename"] == str(path)
        else:
            assert result.returncode == 0 and diagnostics == []
