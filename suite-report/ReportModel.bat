@echo off

rem parameters:
rem %1: SCADE installation directory, e.g. C:\Program Files\ANSYS Inc\v242\SCADE
rem %2: project
rem %3: configuration
rem %4: build: true or false

set LOGFILE=%~dpn0.log

:: check if there are 3 parameters
if ["%~3"]==[""] (
    @echo Usage: %0 ^<SCADE directory^> ^<SCADE project^> ^<SCADE configuration^>
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
rem TODO set PROJECT_PATH=%~d2
rem TODO set PROJECT_NAME=%~n2

:: retrieve the configuration
set CONF=%~3

@echo Report model for %PROJECT% using the configuration %CONF%
"%SCADE_EXE%" -report "%PROJECT%" -conf "%CONF%" > "%LOGFILE%" 2>&1

:: display the command output
type "%LOGFILE%"

:: check for the correct completion of the command (no error code returned by SCADE)
type "%LOGFILE%" | find "report generated in:" > nul

if %errorlevel% neq 0 exit /B 1
