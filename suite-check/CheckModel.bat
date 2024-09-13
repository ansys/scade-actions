@echo off

rem parameters:
rem %1: SCADE installation directory, e.g. C:\Program Files\ANSYS Inc\v242\SCADE
rem %2: project
rem %3: configuration

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

:: retrieve the configuration
set CONF=%~3

set LOGFILE=%~dpn0.log

@echo Check model for %PROJECT% using the configuration %CONF%
"%SCADE_EXE%" -check "%PROJECT%" -conf "%CONF%" > "%LOGFILE%" 2>&1

:: display the command output
type "%LOGFILE%"

:: check for errors
for /F "tokens=4,5" %%I in (%LOGFILE%) do (
    if "%%J" == "error(s)" (
        if %%I NEQ 0 exit /B 1
    )
)

exit /B 0