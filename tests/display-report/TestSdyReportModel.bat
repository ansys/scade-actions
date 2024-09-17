@echo off
:: nominal report without error
call ..\..\display-report\ReportModel.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "HTML"
if errorlevel 1 (
    echo unexpected reporter error
)
@echo off
:: check for errors
call ..\..\display-report\ReportModel.bat "c:\Program Files\ANSYS Inc\v242\xSCADE" "Model/Model.etp" "HTML"
if errorlevel 1 (
    echo *wrong SCADE dir detected*
) else (
    echo error: wrong SCADE dir not detected
)

call ..\..\display-report\ReportModel.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/xModel.etp" "HTML"
if errorlevel 1 (
    echo *wrong project detected*
) else (
    echo error: wrong project not detected
)

call ..\..\display-report\ReportModel.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "Unknown"
if errorlevel 1 (
    echo *reporter error detected*
) else (
    echo error: reporter error not detected
)
