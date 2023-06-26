@echo off
setlocal enableextensions disabledelayedexpansion
cd /d %~dp0
set "search=CONFIG_PATH"
set "pathSeparator=/"

for /F "delims=" %%i in ("%CD%") do set "currentPath=%%i"
set "currentPath=%currentPath:\=/%"
echo %currentPath%

set "replace=%currentPath%"


set "textFile=nginx.conf.template"
set "outputFile=nginx.conf"


if exist "%outputFile%" del "%outputFile%"

for /f "delims=" %%i in ('type "%textFile%"') do (
    set "line=%%i"
    setlocal enabledelayedexpansion
    >>"%outputFile%" echo(!line:%search%=%replace%!
    endlocal
)
