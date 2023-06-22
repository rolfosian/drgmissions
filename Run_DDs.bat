@echo off

set PYTHON_PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe

set SCRIPT_PATH="C:\Program Files (x86)\Steam\steamapps\common\Deep Rock Galactic\FSD\Binaries\Win64\DDs_RUN.py"

cd /d %~dp0

%PYTHON_PATH% %SCRIPT_PATH%

exit