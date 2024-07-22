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

from sys import stderr

from scade.model.project.stdproject import get_roots as get_projects


def main(name: str):
    # there must be at least one project
    project = get_projects()[0]
    for configuration in project.configurations:
        if configuration.name == name:
            break
    else:
        # report a message on stderr, return status not reported by scade.exe -script
        print(
            "%s: no such configuration for %s" % (name, project.pathname), file=stderr
        )
        return
    # compute the macros usable to define the target directory
    tool = "GENERATOR"
    # $(NodeName)
    # retrieve the root operators for the given configuration
    prop = "ROOTNODE"
    roots = project.get_tool_prop_def(tool, prop, "", configuration)
    # convert the path of the first operator to an identifier
    # while moving the name from the last to the first position
    tokens = roots[0].rstrip("/").split("::")
    tokens = [tokens[-1]] + tokens[:-1]
    node_name = "__".join(tokens)
    # $(CG)
    # retrieve the code generator for the given configuration
    prop = "GENERATOR"
    cg = project.get_scalar_tool_prop_def(tool, prop, "", configuration)
    # convert by family: algorithm valid at least until 2024 R2
    # C QUAL661, C QUAL663, C MC66, ADA QUAL661, ADA QUAL663, ADA MC66 --> KCG66
    # C MCG --> MCG
    # C ACG --> ACG
    if cg == "C MCG":
        cg = "MCG"
    elif cg == "C MCG":
        cg = "MCG"
    else:
        cg = "KCG66"
    # retrieve the target directory for the given configuration
    prop = "TARGET_DIR"
    default = "$(NodeName)_$(CG)"
    target_dir = project.get_scalar_tool_prop_def(tool, prop, default, configuration)
    # expand the macros
    target_dir = (
        target_dir.replace("$(CG)", cg)
        .replace("$(NodeName)", node_name)
        .replace("$(Configuration)", "configuration")
    )
    # print the result
    print(target_dir)
    # report a message on stderr, return status not reported by scade.exe -script
    print("Command completed.", file=stderr)
