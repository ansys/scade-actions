@echo off
SETLOCAL EnableDelayedExpansion
rem parameters:
rem %1: SCADE installation directory, e.g. C:\Program Files\ANSYS Inc\v242\SCADE
rem %2: project
rem %3: specification
rem %4: format

:: check if there are 4 parameters
if ["%~4"]==[""] (
    @echo Usage: %0 ^<SCADE directory^> ^<SCADE project^> ^<SCADE specification^> ^<format^>
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

:: retrieve the specification and format
set SPECIFICATION=%~3
set FORMAT=%~4

:: set extension
@echo Check%FORMAT% model for %PROJECT% using the specification %SPECIFICATION%
if /I "%FORMAT%"=="TXT" (
    set EXTENSION=.txt
) else if /I "%FORMAT%"=="CSV" (
    set EXTENSION=.csv
) else (
    echo Unknown format: %FORMAT%
    exit /b 1
)


:: Remove the .sgfx extension from SPECIFICATION
for %%i in (%SPECIFICATION%) do set NAME_ONLY=%%~ni

:: Create DESIGN_CHECKER_REPORT by appending the EXTENSION
set DESIGN_CHECKER_REPORT=design-checker-report-%NAME_ONLY%%EXTENSION%

"%SCADE_DISPLAY_CONSOLE_EXE%" batch check"%FORMAT%" "%PROJECT%" -source "%SPECIFICATION%" -out %DESIGN_CHECKER_REPORT%

if /I "%FORMAT%"=="TXT" (
    :: check for the correct completion of the command
    type %DESIGN_CHECKER_REPORT% | find "No problems found" > nul

) else if /I "%FORMAT%"=="CSV" (
    :: count nb of lines
    for /f %%a in ('type %DESIGN_CHECKER_REPORT% ^| find /c /v ""') do set lines=%%a
    :: check if nb of lines superior to 1
    if !lines! gtr 1 (
        exit /b 1
    )
)


if %errorlevel% neq 0 exit /B 1