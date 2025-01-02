# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
from pathlib import Path

import ansys.scade.apitools  # noqa: F401
import pytest

# apitools import adds SCADE directories to sys.path
# --> must be done before importing other scade modules
# isort: split

from scade import load_project
from scade.model.project.stdproject import Project
from scade.model.testenv import TestApplication

# add the path containing tee_results.py
script_dir = Path(__file__).parent
sys.path.append(str(script_dir.parent.parent / "test-coverage"))

from mc_results import McResults  # noqa: E402


@pytest.fixture(scope="session")
def test_project_applications(request) -> list[tuple[Project, TestApplication]]:
    # load the projects listed in request.param
    result = []
    for path in request.param:
        assert Path(path).exists()
        project = load_project(path)
        # no independent loader for TestApplication
        # -> load manually all files referenced in the project
        application = TestApplication()
        application.project = project
        for file_ref in project.file_refs:
            suffix = Path(file_ref.pathname).suffix
            if suffix.lower() == ".stp":
                # procedure
                application.load_procedure_tcl(file_ref.pathname)
        result.append((project, application))
    return result


# derive a class to redefine "run"
class TestMcResults(McResults):
    def re_run(self, test: str, results: str, script: str, output: str, summary: str):
        # can not run another instance, store the parameters for verification
        self.test = test
        self.results = results
        self.output = output
        self.summary = summary


@pytest.mark.parametrize(
    "test_project_applications",
    [
        [
            "tests/test-coverage/Test/Test.etp",
            "tests/test-coverage/Results/Results.etp",
        ],
        ["tests/test-coverage/TestResults/TestResults.etp"],
    ],
    indirect=True,
)
def test_mc_results_nominal(test_project_applications, tmp_path):
    projects = [_[0] for _ in test_project_applications]
    applications = [_[1] for _ in test_project_applications]

    output = tmp_path / "output.json"
    summary = tmp_path / "summary.md"
    cls = TestMcResults(str(output), str(summary))
    status = cls.main(projects, applications)
    assert status == cls.ERR_OK
    assert output.exists()


@pytest.mark.parametrize(
    "test_project_applications",
    [["tests/test-coverage/Model/Model.etp"]],
    indirect=True,
)
def test_mc_results_robustness(test_project_applications, tmp_path):
    projects = [_[0] for _ in test_project_applications]
    applications = [_[1] for _ in test_project_applications]

    output = tmp_path / "no_test.json"
    summary = tmp_path / "summary.md"
    cls = TestMcResults(str(output), str(summary))
    status = cls.main(projects, applications)
    assert status == cls.ERR_NOT_TEST
    assert not output.exists()


@pytest.mark.parametrize(
    "test_project_applications",
    [["tests/test-coverage/Results/Results.etp"]],
    indirect=True,
)
def test_mc_results_re_run(test_project_applications, tmp_path):
    projects = [_[0] for _ in test_project_applications]
    applications = [_[1] for _ in test_project_applications]

    output = tmp_path / "re_run.json"
    summary = tmp_path / "summary.md"
    cls = TestMcResults(str(output), str(summary))
    status = cls.main(projects, applications)
    assert status == cls.ERR_RE_RUN
    assert not output.exists()
    assert (
        Path(cls.test).resolve() == Path("tests/test-coverage/Test/Test.etp").resolve()
    )
    assert cls.results == projects[0].pathname
    assert cls.output == str(output)
    assert cls.summary == str(summary)
