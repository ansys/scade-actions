@echo off

rem parameters:
rem %1: SCADE installation directory, e.g. C:\Program Files\ANSYS Inc\v242\SCADE
rem %2: project
rem %3: configuration


set LOGFILE=%~dpn0.log

:: check if there are 3 parameters
if ["%~3"]==[""] (
    @echo Usage: %0 ^<SCADE directory^> ^<SCADE Display project^> ^<SCADE Display configuration^>
    exit /B 1
)

:: check the correctness of the SCADE installation directory
if not exist "%~1\SCADE Display\bin\ScadeDisplayConsole.exe" (
    @echo Error: file ^<%~s1\SCADE Display\bin\ScadeDisplayConsole.exe^> does not exist
    exit /B 1
)
set SCADE_DISPLAY_CONSOLE_EXE=%~1\SCADE Display\bin\ScadeDisplayConsole.exe

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
"%SCADE_DISPLAY_CONSOLE_EXE%" batch report "%PROJECT%" -conf "%CONF%"
