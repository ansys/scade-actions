@echo off
echo configuration RTF
"c:\Program Files\ANSYS Inc\v242\SCADE\SCADE\bin\SCADE.exe" -script Model/Model.etp ..\..\display-report\get_sdy_document.py "main('RTF')" > log.txt 2> err.txt
if errorlevel 1 (type log.txt & exit /b 1)
:: check for the correct completion of the command
:: when no error code is returned by scade.exe -script
type err.txt | find "Command completed" > nul
if errorlevel 1 (type err.txt & exit /b 1)
type log.txt >> env.txt
type env.txt

echo configuration HTML
"c:\Program Files\ANSYS Inc\v242\SCADE\SCADE\bin\SCADE.exe" -script Model/Model.etp ..\..\display-report\get_sdy_document.py "main('HTML')" > log.txt 2> err.txt
if errorlevel 1 (type log.txt & exit /b 1)
:: check for the correct completion of the command
:: when no error code is returned by scade.exe -script
type err.txt | find "Command completed" > nul
if errorlevel 1 (type err.txt & exit /b 1)
type log.txt >> env.txt
type env.txt

