@echo off
:: nominal check without error
call ..\..\suite-metrics\ComputeMetrics.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "MetricRule"
if errorlevel 1 (
    echo unexpected checker error
)
:: check for errors
call ..\..\suite-metrics\ComputeMetrics.bat "c:\Program Files\ANSYS Inc\v242\xSCADE" "Model/Model.etp" "MetricRule"
if errorlevel 1 (
    echo *wrong SCADE dir detected*
) else (
    echo error: wrong SCADE dir not detected
)

call ..\..\suite-metrics\ComputeMetrics.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/xModel.etp" "MetricRule"
if errorlevel 1 (
    echo *wrong project detected*
) else (
    echo error: wrong project not detected
)

call ..\..\suite-metrics\ComputeMetrics.bat "c:\Program Files\ANSYS Inc\v242\SCADE" "Model/Model.etp" "Unknown"
if errorlevel 1 (
    echo *checker error detected*
) else (
    echo error: checker error not detected
)

call ..\..\suite-metrics\ComputeMetrics.bat "c:\Program Files\ANSYS Inc\v242\xSCADE" "Model/Model.etp"
if errorlevel 1 (
    echo *missing parameter detected*
) else (
    echo error: missing parameter not detected
)
