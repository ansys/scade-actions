# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

# add the path containing get_document.py
script_dir = Path(__file__).parent
sys.path.append(str(script_dir.parent.parent / "test-execute"))

from get_results_dir import get_results_dir  # noqa: E402


@pytest.fixture(scope="session")
def test_project(request) -> Project:
    # load request.param
    assert Path(request.param).exists()
    return load_project(request.param)


@pytest.mark.parametrize(
    "test_project", ["tests/test-execute/Test/Test.etp"], indirect=True
)
@pytest.mark.parametrize(
    "configuration, expected",
    [
        ("Sibling", r"tests\test-execute\Sibling"),
        ("Test Success", r"tests\test-execute\Test\Test Success"),
        ("Test Failure", r"tests\test-execute\Test\Test Failure"),
    ],
)
def test_get_results_dir_nominal(test_project, configuration, expected, capsys):
    # clear stdout/stderr before the test
    capsys.readouterr()
    # test
    status = get_results_dir(test_project, configuration)
    assert status == 0
    std = capsys.readouterr()
    assert std.err.split("\n")[0] == "Command completed."
    outs = std.out.split("\n")
    assert outs[0] == "results-directory=" + expected


@pytest.mark.parametrize(
    "test_project", ["tests/test-execute/Test/Test.etp"], indirect=True
)
@pytest.mark.parametrize(
    "configuration, expected",
    [
        ("AVX", "<n/a>"),
    ],
)
def test_get_results_dir_robustness(test_project, configuration, expected, capsys):
    # clear stdout/stderr before the test
    capsys.readouterr()
    # test
    status = get_results_dir(test_project, configuration)
    assert status != 0
    std = capsys.readouterr()
    assert "Command completed." not in std.err.split("\n")
    assert not std.out
