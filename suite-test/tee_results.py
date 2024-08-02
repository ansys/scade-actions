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

import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from scade.model.project.stdproject import get_roots as get_projects
from scade.model.testenv import get_roots as get_test_applications


class JUnitElement:
    def __init__(self) -> None:
        # total number of tests
        self.tests = 0
        # total number of failed tests
        self.failures = 0
        # total number of skipped tests
        self.skipped = 0
        # total number of assertions for all tests
        self.assertions = 0
        # total number of errored tests
        self.errors = 0


class TestFailure:
    def __init__(self, step: int, path: str, actual: str, expected: str) -> None:
        self.message = "(%d) %s: %s (expected %s)" % (step, path, actual, expected)


class TestRecord:
    def __init__(self, record, name: str = "") -> None:
        self.record = record
        self.name = name if name else record.name
        self.result = None
        self.assertions = 0
        self.failures = []


class TestProcedure(JUnitElement):
    def __init__(self, procedure, name: str = "") -> None:
        super().__init__()
        self.procedure = procedure
        if procedure:
            self.name = procedure.name
            self.records = {_.name: TestRecord(_) for _ in procedure.records}
        else:
            # some results are not bound to a procedure
            self.name = name
            self.records = {}


class TeeResults(JUnitElement):
    ERR_PASSED = 0
    ERR_FAILED = 1
    ERR_ERROR = 2
    ERR_NOT_TEST = 3
    ERR_RE_RUN = 4
    ERR_INTERNAL_ERROR = 5

    def __init__(self, output: str):
        super().__init__()
        # output file
        self.output = output

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
                self.re_run(str(test_path), projects[0].pathname, __file__, self.output)
                return self.ERR_RE_RUN

        # dictionary of procedures using wrapping classes
        self.procedures = {}
        for application in test_applications:
            self.procedures.update(
                {
                    Path(_.pathname).stem: TestProcedure(_)
                    for _ in application.procedures
                }
            )
        # bind records using wrapping classes
        for application in test_applications:
            for file in application.result_files:
                name = Path(file.pathname).stem
                procedure = self.procedures.setdefault(name, TestProcedure(None, name))
                for result in file.raw_file.result_records:
                    record = procedure.records.setdefault(
                        result.name, TestRecord(None, result.name)
                    )
                    record.result = result

        self.gather_results()
        self.dump()
        return self.status

    def re_run(self, test: str, results: str, script: str, output: str):
        # script run with scade.exe -script
        exe = Path(sys.executable).parent / "scade.exe"
        cmd = [str(exe), "-script", test, results, script, "main(r'%s')" % output]
        print("calling", " ".join(cmd))
        sys.stdout.flush()
        subprocess.run(cmd)

    def gather_results(self):
        # compute the status pass/failed of each procedure/record
        self.status = self.ERR_PASSED
        for procedure in self.procedures.values():
            if not procedure.procedure:
                procedure.errors = 1
                self.errors += 1
            for record in procedure.records.values():
                if not record.result:
                    # not executed
                    procedure.skipped += 1
                else:
                    for result in record.result.results:
                        if not result.status:
                            failure = TestFailure(
                                result.step,
                                result.item_path,
                                result.actual_value,
                                result.expected_value,
                            )
                            record.failures.append(failure)
                        record.assertions += 1
                    if record.failures:
                        procedure.failures += 1
                procedure.tests += 1
                procedure.assertions += record.assertions
            self.tests += procedure.tests
            self.failures += procedure.failures
            self.skipped += procedure.skipped
            self.assertions += procedure.assertions

        if self.errors:
            self.status = self.ERR_ERROR
        else:
            self.status = self.ERR_FAILED if self.failures else self.ERR_PASSED

    def dump(self):
        root = ET.fromstring("<testsuites/>")
        root.set("tests", str(self.tests))
        root.set("skipped", str(self.skipped))
        root.set("failures", str(self.failures))
        root.set("errors", str(self.errors))
        root.set("assertions", str(self.assertions))
        for name in sorted(self.procedures.keys()):
            procedure = self.procedures[name]

            ts = ET.SubElement(root, "testsuite")
            ts.set("name", procedure.name)
            ts.set("tests", str(procedure.tests))
            ts.set("skipped", str(procedure.skipped))
            ts.set("failures", str(procedure.failures))
            ts.set("errors", str(procedure.errors))
            ts.set("assertions", str(procedure.assertions))
            # TODO "file" attribute
            for name in sorted(procedure.records.keys()):
                record = procedure.records[name]
                tc = ET.SubElement(ts, "testcase")
                tc.set("name", "%s/%s" % (procedure.name, record.name))
                operator = (
                    procedure.procedure.operator if procedure.procedure else "Unknown"
                )
                tc.set("classname", operator)
                tc.set("assertions", str(record.assertions))
                if not record.result:
                    tr = ET.SubElement(tc, "skipped")
                    tr.set("message", "test not executed")
                else:
                    for failure in record.failures:
                        tr = ET.SubElement(tc, "failure")
                        tr.set("message", failure.message)
                        tr.set("type", "AssertionError")

        # 3.9+ only
        try:
            ET.indent(root)
        except AttributeError:
            pass
        Path(self.output).parent.mkdir(exist_ok=True)
        ET.ElementTree(root).write(self.output)


def main(output: str):
    cls = TeeResults(output)
    status = cls.main(get_projects(), get_test_applications())
    if status != cls.ERR_RE_RUN:
        # print on stdout the overall status
        passed = cls.tests - cls.failures - cls.skipped
        print(passed, "passed -", cls.failures, "failed -", cls.skipped, "skipped")
