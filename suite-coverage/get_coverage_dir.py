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

import os
import sys

from scade.model.project.stdproject import Project
from scade.model.project.stdproject import get_roots as get_projects


def get_coverage_dir(project: Project, name: str) -> int:
    for configuration in project.configurations:
        if configuration.name == name:
            break
    else:
        # report a message on stderr, return status not reported by scade.exe -script
        print(
            "%s: no such configuration for %s" % (name, project.pathname),
            file=sys.stderr,
        )
        return 1
    # retrieve the target directory for the given configuration
    tool = "QTE"
    prop = "MC_TARGET_DIR"
    default = "$(Configuration)_MC"
    target_dir = project.get_scalar_tool_prop_def(tool, prop, default, configuration)
    # expand the macros
    target_dir = target_dir.replace("$(Configuration)", name)
    # make the directory absolute with respect to the project
    target_dir = os.path.normpath(
        os.path.join(os.path.dirname(project.pathname), target_dir)
    )
    # print the result as the definition of an environment variable
    print("coverage-directory=%s" % target_dir)
    # report a message on stderr, return status not reported by scade.exe -script
    print("Command completed.", file=sys.stderr)
    return 0


def main(name: str):
    # entry point with scade.exe -script
    # there must be one and only one project
    projects = get_projects()
    assert len(projects) == 1
    get_coverage_dir(projects[0], name)
