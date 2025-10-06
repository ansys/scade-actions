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
if not exist "%~1\SCADE Test\Rapid Prototyper\bin\ScadeRPConsole.exe" (
    @echo Error: file ^<%~s1\SCADE Test\Rapid Prototyper\bin\ScadeRPConsole.exe^> does not exist
    exit /B 1
)
set SCADE_RP_CONSOLE_EXE=%~1\SCADE Test\Rapid Prototyper\bin\ScadeRPConsole.exe

:: check if the project exists
if not exist "%2" (
    @echo Error: file ^<%~s2^> does not exist
    exit /B 1
)

:: check if the project exists
if not exist "%2" (
    @echo Error: file ^<%~s2^> does not exist
    exit /B 1
)
set PROJECT=%~2

:: retrieve the configuration
set CONF=%~3

@echo Generate model for %PROJECT% using the configuration %CONF%
"%SCADE_RP_CONSOLE_EXE%" batch generate "%PROJECT%" -conf "%CONF%"
