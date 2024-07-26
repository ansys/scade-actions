@echo off
:: nominal generation
call ..\..\suite-code\GenerateCode.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "Suite Code" false
if errorlevel 1 (
    echo failed to generate code
)
:: nominal build
call ..\..\suite-code\GenerateCode.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "Simulation" true
if errorlevel 1 (
    echo failed to build code
)
:: check for errors
call ..\..\suite-code\GenerateCode.bat "c:\Program Files\ANSYS Inc\v242\xSCADE" "Model/Model.etp" "Suite Code" false
if errorlevel 1 (
    echo *wrong SCADE dir detected*
) else (
    echo error: wrong SCADE dir not detected
)

call ..\..\suite-code\GenerateCode.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/xModel.etp" "Suite Code" false
if errorlevel 1 (
    echo *wrong project detected*
) else (
    echo error: wrong project not detected
)

call ..\..\suite-code\GenerateCode.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "Unknown" false
if errorlevel 1 (
    echo *code generation error detected*
) else (
    echo error: code generation error not detected
)
