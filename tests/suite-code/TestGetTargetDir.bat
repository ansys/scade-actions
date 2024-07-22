@echo off
"c:\Program Files\ANSYS Inc\v242\SCADE\SCADE\bin\SCADE.exe" -script Model/Model.etp ..\..\suite-code\get_target_dir.py "main('Suite Code')" > log.txt 2> err.txt
if errorlevel 1 (type log.txt & exit /b 1)
:: check for the correct completion of the command,
:: when no error code is returned by scade.exe -script
type err.txt | find "Command completed" > nul
if errorlevel 1 (type err.txt & exit /b 1)
for /F %%t in (log.txt) do (
    echo target-dir=%%t
)
