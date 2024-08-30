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

import json
import subprocess
import sys
from pathlib import Path

# add methods to testenv.TestApplication
import mcr  # noqa: F401
from scade.model.project.stdproject import get_roots as get_projects
from scade.model.testenv import get_roots as get_test_applications
from scade.test.suite.mcoverage.utils import Status as MCStatus


class TestProcedure:
    def __init__(self, procedure, name: str = "") -> None:
        super().__init__()
        self.procedure = procedure
        if procedure:
            self.name = procedure.name
            # self.records = {_.name: TestRecord(_) for _ in procedure.records}
        else:
            # some results are not bound to a procedure
            self.name = name
            # self.records = {}


class McResults:
    ERR_OK = 0
    ERR_ERROR = 2
    ERR_NOT_TEST = 3
    ERR_RE_RUN = 4
    ERR_INTERNAL_ERROR = 5

    MCMETRICS = {
        MCStatus.OBSERVED: "Observed",
        MCStatus.OBSERVED_JUSTIFIED: "Observed justified",
        MCStatus.JUSTIFIED: "Justified",
        MCStatus.NOT_OBSERVED: "Not observed",
        MCStatus.NOT_COVERABLE: "Not coverable",
    }

    def __init__(self, output: str, summary: str):
        super().__init__()
        # output file
        self.output = output
        # job summary file
        self.summary = summary
        # results
        self.metadatas = {}
        # dictionary of procedures for fast access
        self.procedures = {}
        # status not computed yet
        self.status = self.ERR_INTERNAL_ERROR

    def main(self, projects, test_applications) -> int:
        # four possible use cases:
        # 1 one test project including test results: OK
        # 2 one test project and one results project: OK
        # 3 one results project: re-run by adding the test project
        # 4 no test project nor results projects: NOK
        projects = [
            _
            for _ in projects
            if "QTE" in _.get_tool_prop_def("STUDIO", "PRODUCT", None, None)
        ]
        if not projects:
            self.status = self.ERR_NOT_TEST
            return self.status
        if len(projects) == 1:
            test_path = projects[0].get_scalar_tool_prop_def(
                "QTE", "TEST_PROJECT", None, None
            )
            if test_path:
                # only a results project
                # --> rerun with both test and results projects
                test_path = (Path(projects[0].pathname).parent / test_path).resolve()
                self.re_run(
                    str(test_path),
                    projects[0].pathname,
                    __file__,
                    self.output,
                    self.summary,
                )
                return self.ERR_RE_RUN
        # get the name of the model for reporting
        model = projects[0].get_scalar_tool_prop_def("QTE", "SOURCE_MODEL", "", None)
        self.model = Path(model).stem

        # dictionary of procedures using wrapping classes
        self.procedures = {}
        for application in test_applications:
            self.procedures.update(
                {
                    Path(_.pathname).stem: TestProcedure(_)
                    for _ in application.procedures
                }
            )
        # coverage results: last project/application of the lists
        coverage_project = projects[-1]
        coverage_application = test_applications[-1]

        # extension: load the coverage files
        coverage_application.load_coverage_data(coverage_project)

        if coverage_application.coverage_merge_dir:
            report = coverage_application.coverage_merge_dir.report_file.report
            coverage_points = report.get_coverage_points()
            for status, metric in self.MCMETRICS.items():
                self.metadatas[metric] = coverage_points.filter_status(status).count()

            not_observed = self.metadatas[self.MCMETRICS[MCStatus.NOT_OBSERVED]]
            # self.status = self.ERR_PASSED if not_observed == 0 else self.ERR_FAILED
            # error on partial coverage disabled
            self.status = self.ERR_OK

            # add coverage ratios
            total = coverage_points.count()
            # round value to 2 digits
            self.metadatas["Count"] = total
            self.metadatas["Coverage %"] = (
                int(10000 * (total - not_observed) / total + 0.5) / 100
            )

        self.dump_status()
        self.dump_summary()

        return self.status

    def re_run(self, test: str, results: str, script: str, output: str, summary: str):
        # script run with scade.exe -script
        exe = Path(sys.executable).parent / "scade.exe"
        cmd = [
            str(exe),
            "-script",
            test,
            results,
            script,
            "main(r'%s', r'%s')" % (output, summary),
        ]
        print("calling", " ".join(cmd))
        sys.stdout.flush()
        subprocess.run(cmd)

    def dump_status(self):
        """
        custom format example from https://docs.codecov.com/docs/codecov-custom-coverage-format
        {
          "coverage": {
            "filename": {
              "1": 0,      # line 1 missed
              "2": 1,      # line 2 hit once
              "3": "1/2",  # line 3 partial hit, one missing branch
              "4": "1/3",  # line 4 partial hit, two missing branches
                                                         # skip line 5
              "6": null,   # skip line 6
              "7": 5       # line 7 hit 5 times
            }
          }
        }
        """
        not_observed = self.metadatas[self.MCMETRICS[MCStatus.NOT_OBSERVED]]
        count = self.metadatas["Count"]
        d = {"coverage": {self.model: {"1": "%d/%d" % (not_observed, count)}}}
        Path(self.output).parent.mkdir(exist_ok=True)
        with open(self.output, "w") as f:
            json.dump(d, f, indent=4)

    def dump_summary(self):
        Path(self.summary).parent.mkdir(exist_ok=True)
        with open(self.summary, "w") as f:
            f.write("### Model coverage\n")
            f.write("\n")
            f.write("|Metric|Value\n")
            f.write("|--|--\n")
            for metric in ["Count", "Coverage %"]:
                f.write("|{0}|{1}\n".format(metric, self.metadatas[metric]))
            for metric in self.MCMETRICS.values():
                f.write("|{0}|{1}\n".format(metric, self.metadatas[metric]))
            f.write("\n")


def main(output: str, summary: str):
    cls = McResults(output, summary)
    status = cls.main(get_projects(), get_test_applications())
    if status != cls.ERR_RE_RUN:
        for data, value in cls.metadatas.items():
            print("{0} = {1}".format(data, value))
