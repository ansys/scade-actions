@echo off
:: nominal
call ..\..\test-coverage\AcquireCoverage.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/Test.etp" "Test" tmp\Test\TestResults.etp -summary tmp\summary.md -status tmp\status.json
if errorlevel 1 (
    echo failed to acquire coverage
)

:: check for errors
call ..\..\test-coverage\AcquireCoverage.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/Test.etp" "Test"
if errorlevel 1 (
    echo *missing parameter detected*
) else (
    echo error: missing parameter not detected
)

call ..\..\test-coverage\AcquireCoverage.bat "c:\Program Files\ANSYS Inc\v242\xSCADE" "Test/Test.etp" "Test" tmp\TestResults.etp
if errorlevel 1 (
    echo *wrong SCADE dir detected*
) else (
    echo error: wrong SCADE dir not detected
)

call ..\..\test-coverage\AcquireCoverage.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/xTest.etp" "Test" tmp\TestResults.etp
if errorlevel 1 (
    echo *wrong project detected*
) else (
    echo error: wrong project not detected
)

call ..\..\test-coverage\AcquireCoverage.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/Test.etp" "Unknown" tmp\TestResults.etp
if errorlevel 1 (
    echo *test execution error detected*
) else (
    echo error: test execution error not detected
)
