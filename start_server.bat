@echo off
taskkill /IM nginx.exe /T /F
setlocal
call generate_conf.bat
cd /d %~dp0
set workspaceFolder=%CD%
for /f "delims=" %%i in ('where nginx') do set "nginxpath=%%i"
for %%A in ("%nginxpath%") do set "nginxdir=%%~dpA"
echo Starting nginx...
start %nginxpath% -c %CD%\nginx.conf -p %nginxdir%
cd museum && ^
pip install -r requirements.txt && ^
python manage.py migrate && ^
start cmd /k python manage.py runserver 0.0.0.0:9000 --noreload