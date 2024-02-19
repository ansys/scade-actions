# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""
Test suite for script.py.

Test strategy:

* Verify the returned values for a simple Scade model.
"""

import pytest
import scade.model.suite as suite

# shall modify sys.path to access SCACE APIs
from conftest import get_resources_dir, load_project, load_session
from test_package import script


@pytest.fixture(scope='session')
def roots():
    """Unique instance of the test model Model."""
    path = get_resources_dir() / 'resources' / 'Model.etp'
    project = load_project(path)
    session = load_session(path)
    return project, session


def test_get_project_names(roots):
    project, _ = roots
    names = script.get_project_names([project])
    assert names == ['Model.etp']


def test_get_operator_paths(roots):
    _, session = roots
    paths = script.get_operator_paths(session.model)
    assert paths == ['P::Root/']
