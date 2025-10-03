@echo off
:: nominal generation
call ..\..\rapid-prototyper-generate\RPGenerate.bat "c:\Program Files\ANSYS Inc\v252\SCADE" "Model/Model.etp" "Windows"
if errorlevel 1 (
    echo failed to generate code
)
:: nominal build
call ..\..\rapid-prototyper-generate\RPGenerate.bat "c:\Program Files\ANSYS Inc\v252\SCADE" "Model/Model.etp" "ScadeOneCosimulation"
if errorlevel 1 (
    echo failed to build code
)
:: check for errors
call ..\..\rapid-prototyper-generate\RPGenerate.bat "c:\Program Files\ANSYS Inc\v252\xSCADE" "Model/Model.etp" "Code"
if errorlevel 1 (
    echo *wrong SCADE dir detected*
) else (
    echo error: wrong SCADE dir not detected
)

call ..\..\rapid-prototyper-generate\RPGenerate.bat "c:\Program Files\ANSYS Inc\v252\SCADE" "Model/xModel.etp" "Windows"
if errorlevel 1 (
    echo *wrong project detected*
) else (
    echo error: wrong project not detected
)

call ..\..\rapid-prototyper-generate\RPGenerate.bat "c:\Program Files\ANSYS Inc\v252\SCADE" "Model/Model.etp" "Unknown"
if errorlevel 1 (
    echo *code generation error detected*
) else (
    echo error: code generation error not detected
)
