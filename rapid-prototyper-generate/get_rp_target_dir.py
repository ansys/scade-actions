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


def get_rp_target_dir(project: Project, name: str) -> int:
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
    # compute the macros usable to define the target directory
    tool = "RAPIDPROTO"
    # retrieve source
    prop = "CONFSOURCE"
    source = project.get_scalar_tool_prop_def(tool, prop, "", configuration)
    # retrieve outdir
    prop = "CONFOUTPUT"
    target_dir = project.get_scalar_tool_prop_def(tool, prop, "", configuration)
    # extract model name without '.rgfx' suffix
    model_name = os.path.splitext(source)[0]
    # replace %ModelName% with the model name
    target_dir = target_dir.replace("%ModelName%", model_name)
    # replace %Target% with the type of the  name
    target_dir = target_dir.replace("%Target%", name)
    # make the directory absolute with respect to the project
    target_dir = os.path.normpath(
        os.path.join(os.path.dirname(project.pathname), target_dir)
    )
    # print the results as the definition of an environment variables
    print("target-directory=%s" % target_dir)
    # report a message on stderr, return status not reported by scade.exe -script
    print("Command completed.", file=sys.stderr)
    return 0


def main(name: str):
    # entry point with scade.exe -script
    # there must be one and only one project
    projects = get_projects()
    assert len(projects) == 1
    get_rp_target_dir(projects[0], name)
