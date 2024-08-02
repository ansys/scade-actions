@echo off

rem parameters:
rem %1: SCADE installation directory, e.g. C:\Program Files\ANSYS Inc\v242\SCADE
rem %2: project
rem %3: configuration
rem %4: results project
rem %5: coverage file or empty

set LOGFILE=%~dpn0.log

:: check if there are 4 parameters
if ["%~4"]==[""] (
    @echo Usage: %0 ^<SCADE directory^> ^<SCADE Test project^> ^<SCADE configuration^> ^<SCADE Test results project^> ^<coverage file^>
    exit /B 1
)

:: check the correctness of the SCADE installation directory
if not exist "%~1\SCADE\bin\scade.exe" (
    @echo Error: file ^<%~s1\SCADE\bin\scade.exe^> does not exist
    exit /B 1
)
set SCADE_EXE=%~1\SCADE\bin\scade.exe

:: check if the project exists
if not exist "%2" (
    @echo Error: file ^<%~s2^> does not exist
    exit /B 1
)
set PROJECT=%~2

:: retrieve the configuration
set CONF=%~3

:: results project
set RESULT=%~4

@echo Acquiring coverage for %PROJECT% using the configuration %CONF%
"%SCADE_EXE%" -test -mc "%PROJECT%" -conf "%CONF%" -result_project "%RESULT%"
if errorlevel 1 exit /B 1

if "%~5" == "" (
    rem predefined file name in the results project's directory
    set TESTS_RESULT=%~dpn4_mc.json
) else (
    set TESTS_RESULT=%~5
)
set SCRIPT=%~dp0mc_results.py
:: gather coverage results
@echo "gather coverage results for %RESULT% using %SCRIPT% to %TESTS_RESULT%
"%SCADE_EXE%" -script "%RESULT%" "%SCRIPT%" "main(r'%TESTS_RESULT%')"
