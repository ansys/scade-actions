@echo off
:: nominal
call ..\..\suite-coverage\AcquireCoverage.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/Test.etp" "Test" tmp\Test\TestResults.etp tmp\summary.md tmp\status.json
if errorlevel 1 (
    echo failed to acquire coverage
)

:: check for errors
call ..\..\suite-coverage\AcquireCoverage.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/Test.etp" "Test" tmp\TestResults.etp
if errorlevel 1 (
    echo *missing parameter detected*
) else (
    echo error: missing parameter not detected
)

call ..\..\suite-coverage\AcquireCoverage.bat "c:\Program Files\ANSYS Inc\v242\xSCADE" "Test/Test.etp" "Test" tmp\TestResults.etp tmp\summary.md
if errorlevel 1 (
    echo *wrong SCADE dir detected*
) else (
    echo error: wrong SCADE dir not detected
)

call ..\..\suite-coverage\AcquireCoverage.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/xTest.etp" "Test" tmp\TestResults.etp tmp\summary.md
if errorlevel 1 (
    echo *wrong project detected*
) else (
    echo error: wrong project not detected
)

call ..\..\suite-coverage\AcquireCoverage.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/Test.etp" "Unknown" tmp\TestResults.etp tmp\summary.md
if errorlevel 1 (
    echo *test execution error detected*
) else (
    echo error: test execution error not detected
)
