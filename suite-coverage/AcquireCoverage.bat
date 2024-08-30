@echo off

rem parameters:
rem %1: SCADE installation directory, e.g. C:\Program Files\ANSYS Inc\v242\SCADE
rem %2: project
rem %3: configuration
rem %4: results project
rem optional parameters:
rem -summary file
rem -status file

set LOGFILE=%~dpn0.log

:: check there are at least 4 parameters
if ["%~4"]==[""] (
    @echo Usage: %0 ^<SCADE directory^> ^<SCADE Test project^> ^<SCADE configuration^> ^<SCADE Test results project^> [-summary ^<coverage file^>] [-status ^<coverage file^>]
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

set SCRIPT_ARGS=
set SCRIPT_SEPARATOR=(
if "%~5" == "-summary" (
    set SCRIPT_ARGS=%SCRIPT_SEPARATOR%summary=r'%~6'
    set SCRIPT_SEPARATOR=,
    shift /5
    shift /5
)

if "%~5" == "-status" (
    set SCRIPT_ARGS=%SCRIPT_ARGS%%SCRIPT_SEPARATOR%output=r'%~6'
    set SCRIPT_SEPARATOR=,
    shift /5
    shift /5
)
set SCRIPT=%~dp0mc_results.py
:: gather coverage results and summary
@echo "gather coverage status and summary for %RESULT% using %SCRIPT%%SCRIPT_ARGS%)
"%SCADE_EXE%" -script "%RESULT%" "%SCRIPT%" "main%SCRIPT_ARGS%)"
