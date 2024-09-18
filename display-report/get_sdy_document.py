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
from pathlib import Path

from scade.model.project.stdproject import Project
from scade.model.project.stdproject import get_roots as get_projects


def get_sdy_document(project: Project, name: str) -> int:
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
    # retrieve the format
    tool = "SDYREP"
    prop = "FORMAT"
    format = project.get_scalar_tool_prop_def(tool, prop, "HTML", configuration)
    ext = ".rtf" if format == "RTF" else ".html"
    # retrieve source
    prop = "CONFSOURCE"
    source = project.get_scalar_tool_prop_def(tool, prop, "", configuration)
    # retrieve outdir
    tool = "SDY:@SDYREP"
    prop = "OUTPUT"
    output_dir = project.get_scalar_tool_prop_def(tool, prop, "", configuration)
    # extract model name without '.sgfx' suffix
    model_name = os.path.splitext(source)[0]
    # replace %ModelName% with the model name
    output_dir = output_dir.replace("%ModelName%", model_name)
    # create final path
    file = os.path.join(output_dir, model_name + ext)
    # make the path absolute with respect to the project
    file = os.path.normpath(os.path.join(os.path.dirname(project.pathname), file))
    path = Path(file).with_suffix(ext)
    # print the results as the definition of an environment variables
    print("report=%s" % path)
    print("target-directory=%s" % path.parent)
    # report a message on stderr, return status not reported by scade.exe -script
    print("Command completed.", file=sys.stderr)
    return 0


def main(name: str):
    # entry point with scade.exe -script
    # there must be one and only one project
    projects = get_projects()
    assert len(projects) == 1
    get_sdy_document(projects[0], name)
