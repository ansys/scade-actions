# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Unit tests fixtures."""

import os
import re
import sys
from inspect import getsourcefile
from pathlib import Path

# import pytest

# set sys.path from the python interpreter location (<install>/SCADE/contrib/Python3xx)
# note: these tests are executed in the context of a virtual environment
# on top of a SCADE's Python distribution

for line in (Path(sys.executable).parent.parent / "pyvenv.cfg").open("r"):
    m = re.match(r"^home\s*=\s*(.*)$", line)
    if m:
        contrib = Path(m.groups()[0]).parent
        break

assert contrib
base = contrib.parent / "SCADE"
bin = base / "bin"
assert bin.exists()
sys.path.append(str(bin))
lib = base / "APIs" / "Python" / "lib"
assert lib.exists()
sys.path.append(str(lib))


# can be imported since sys.path is updated
# isort: split
# activate the SCADE Python APIs by importing scade_env
import scade_env  # noqa: E402, F401

# must be imported after scade_env
# isort: split
import scade  # noqa: E402
import scade.model.suite as suite  # noqa: E402


def get_resources_dir() -> Path:
    """Return the directory ./resources relative to this file's directory."""
    script_path = Path(os.path.abspath(getsourcefile(lambda: 0)))
    return script_path.parent


def load_session(pathname: Path):
    """
    Load a Scade model in a separate environment.

    Note: The model can have unresolved references since the libraries
    are not loaded.
    """
    session = suite.Session()
    session.load2(str(pathname))
    assert session.model
    return session


def load_project(pathname: Path):
    """
    Load a Scade project in a separate environment.

    Note: Undocumented API.
    """
    project_ = scade.load_project(str(pathname))
    return project_
