@echo off
:: success
call ..\..\test-execute\ExecuteTests.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/Test.etp" "Test Success" tmp\Success\TestSuccessResults.etp
if errorlevel 1 (
    echo failed execute tests
)

:: fail
call ..\..\test-execute\ExecuteTests.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/Test.etp" "Test Failure" tmp\Failure\TestFailureResults.etp
if errorlevel 1 (
    echo test failed detected
) else (
    echo error: test failed not detected
)

:: check for errors
call ..\..\test-execute\ExecuteTests.bat "c:\Program Files\ANSYS Inc\v242\xSCADE" "Test/Test.etp" "Test Success" tmp\TestSuccessResults.etp
if errorlevel 1 (
    echo *wrong SCADE dir detected*
) else (
    echo error: wrong SCADE dir not detected
)

call ..\..\test-execute\ExecuteTests.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/xTest.etp" "Test Success" tmp\TestSuccessResults.etp
if errorlevel 1 (
    echo *wrong project detected*
) else (
    echo error: wrong project not detected
)

call ..\..\test-execute\ExecuteTests.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Test/Test.etp" "Unknown" tmp\TestSuccessResults.etp
if errorlevel 1 (
    echo *test execution error detected*
) else (
    echo error: test execution error not detected
)
