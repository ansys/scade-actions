@echo off
:: nominal check without error
call ..\..\display-check\CheckSdyModel.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "specification.sgfx" "TXT"
if errorlevel 1 (
    echo unexpected checker error
)
call ..\..\display-check\CheckSdyModel.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "specification.sgfx" "CSV"
if errorlevel 1 (
    echo unexpected checker error
)
@echo off
:: nominal check with error
call ..\..\display-check\CheckSdyModel.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "specificationNOK.sgfx" "TXT"
if errorlevel 1 (
    echo *checker errors detected*
) else (
    echo error: checker error not detected
)
call ..\..\display-check\CheckSdyModel.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "specificationNOK.sgfx" "CSV"
if errorlevel 1 (
    echo *checker errors detected*
) else (
    echo error: checker error not detected
)
:: check for errors
call ..\..\display-check\CheckSdyModel.bat "c:\Program Files\ANSYS Inc\v242\xSCADE" "Model/Model.etp" "specificationNOK.sgfx" "CSV"
if errorlevel 1 (
    echo *wrong SCADE dir detected*
) else (
    echo error: wrong SCADE dir not detected
)

call ..\..\display-check\CheckSdyModel.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/xModel.etp" "specificationNOK.sgfx" "CSV"
if errorlevel 1 (
    echo *wrong project detected*
) else (
    echo error: wrong project not detected
)

call ..\..\display-check\CheckSdyModel.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "specificationNOK.sgfx" "Unknown"
if errorlevel 1 (
    echo *checker error detected*
) else (
    echo error: checker error not detected
)
