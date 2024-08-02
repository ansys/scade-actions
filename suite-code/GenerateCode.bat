@echo off

rem parameters:
rem %1: SCADE installation directory, e.g. C:\Program Files\ANSYS Inc\v242\SCADE
rem %2: project
rem %3: configuration
rem %4: build: true or false

set LOGFILE=%~dpn0.log

:: check if there are 4 parameters
if ["%~4"]==[""] (
    @echo Usage: %0 ^<SCADE directory^> ^<SCADE project^> ^<SCADE configuration^> ^<build^>
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

if "%4" == "true" (
    @echo Building code for %PROJECT% using the configuration %CONF%
    "%SCADE_EXE%" -code "%PROJECT%" -conf "%CONF%" -sim > "%LOGFILE%" 2>&1
) else (
    @echo Generating code for %PROJECT% using the configuration %CONF%
    "%SCADE_EXE%" -code "%PROJECT%" -conf "%CONF%" > "%LOGFILE%" 2>&1
)

:: display the command output
type "%LOGFILE%"

:: check for the correct completion of the command (no error code returned by SCADE)
type "%LOGFILE%" | find "Command completed" > nul

if %errorlevel% neq 0 exit /B 1
