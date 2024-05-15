@echo off

set PYTHON_PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe

set SCRIPT_PATH="C:\Program Files (x86)\Steam\steamapps\common\Deep Rock Galactic\FSD\Binaries\Win64\DeepDives_Run.py"

cd /d %~dp0

%PYTHON_PATH% %SCRIPT_PATH%

exit