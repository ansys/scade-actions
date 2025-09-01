@echo off
:: nominal check without error
call ..\..\suite-rules\CheckRules.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "RuleSuccess"
if errorlevel 1 (
    echo unexpected checker error
)
@echo off
:: nominal check with error
call ..\..\suite-rules\CheckRules.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "RuleFailure"
if errorlevel 1 (
    echo *checker errors detected*
) else (
    echo error: checker error not detected
)
:: check for errors
call ..\..\suite-rules\CheckRules.bat "c:\Program Files\ANSYS Inc\v242\xSCADE" "Model/Model.etp" "RuleSuccess"
if errorlevel 1 (
    echo *wrong SCADE dir detected*
) else (
    echo error: wrong SCADE dir not detected
)

call ..\..\suite-rules\CheckRules.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/xModel.etp" "RuleSuccess"
if errorlevel 1 (
    echo *wrong project detected*
) else (
    echo error: wrong project not detected
)

call ..\..\suite-rules\CheckRules.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "Unknown"
if errorlevel 1 (
    echo *checker error detected*
) else (
    echo error: checker error not detected
)
