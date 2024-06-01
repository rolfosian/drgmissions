@echo off
NET SESSION >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    goto :startScript
) ELSE (
    ECHO Please run this script with Administrator Privileges.
    pause
    exit
)
:startScript

:: Disable UAC
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 0 /f >nul
echo UAC Disabled.

:: Change timezone to UTC
tzutil /s "UTC"

:: Change date format to DD-MM-YYYY
reg add "HKCU\Control Panel\International" /v sShortDate /t REG_SZ /d "d/MM/yyyy" /f >nul
reg add "HKCU\Control Panel\International" /v sTimeFormat /t REG_SZ /d "h:mm:ss tt" /f >nul

echo System timezone has been changed to UTC and date format to DD-MM-YYYY.
echo -----------------------------------------------

echo Adjust Windows GUI options for best performance if you would like.
C:\Windows\System32\SystemPropertiesPerformance.exe
echo -----------------------------------------------

echo Be aware this script will store the windows user account username and password as plaintext in the windows registry
echo Make sure time sync is disabled on the host machine if using vm software that has such a feature enabled by default
echo -----------------------------------------------
setlocal enabledelayedexpansion

:: Disable Automatic Windows Updates
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoUpdate /t REG_DWORD /d 1 /f >nul
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows" /v NoAutoUpdate /t REG_DWORD /d 1 /f >nul
PowerShell.exe -Command "Set-ItemProperty -Path 'HKLM:\Software\Policies\Microsoft\Windows\WindowsUpdate\AU' -Name AUOptions -Value 0" >nul
ver >nul
echo Automatic Windows Updates disabled.

:: Disable Game DVR
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\GameDVR" /v GameDVR_Enabled /t REG_DWORD /d 0 /f

:: Disable Game Bar
reg add "HKEY_CURRENT_USER\Software\Microsoft\GameBar" /v AllowAutoGameMode /t REG_DWORD /d 0 /f
reg add "HKEY_CURRENT_USER\Software\Microsoft\GameBar" /v AutoGameModeEnabled /t REG_DWORD /d 0 /f
reg add "HKEY_CURRENT_USER\Software\Microsoft\GameBar" /v UseNexusForGameBarEnabled /t REG_DWORD /d 0 /f
echo Game Bar has been disabled.

:PromptPassword
set CURRENT_USERNAME=%USERNAME%

set /p PASSWORD="Enter Password for %CURRENT_USERNAME%: "
set /p CONFIRM_PASSWORD="Confirm Password for %CURRENT_USERNAME%: "

if "%PASSWORD%"=="%CONFIRM_PASSWORD%" (
    goto :ConfirmedPassword
) else (
    echo Passwords do not match. Please try again.
    goto :PromptPassword
)
:ConfirmedPassword

:: Verify password
net use \\localhost\IPC$ /user:%CURRENT_USERNAME% %PASSWORD% >nul 2>&1
if %errorlevel% neq 0 (
    echo Invalid password.
    goto :PromptPassword
) else (
    net use \\localhost\IPC$ /delete >nul 2>&1
)
ver >nul

reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName /t REG_SZ /d "%CURRENT_USERNAME%" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /t REG_SZ /d "%PASSWORD%" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d "1" /f >nul

echo Automatic logon enabled.
echo -------------------------------------------

setlocal enabledelayedexpansion
set DESKTOP=%USERPROFILE%\Desktop
::Check if Python is installed
python --version 2 >nul
if errorlevel 1 (
    echo Python is not installed. Please wait...
    set PYTHON_VERSION=3.11.0
    set PYTHON_INSTALLER=python-!PYTHON_VERSION!-amd64.exe
    set PYTHON_URL="https://www.python.org/ftp/python/!PYTHON_VERSION!/!PYTHON_INSTALLER!"

    echo Downloading Python installer...
    curl -o %DESKTOP%\!PYTHON_INSTALLER! !PYTHON_URL!

    echo Installing Python...
    start /wait "" "%DESKTOP%\!PYTHON_INSTALLER!" /quiet InstallAllUsers=1 PrependPath=1 Include_launcher=0
    echo:
    echo Python installation complete.
    del "%DESKTOP%\!PYTHON_INSTALLER!"
)
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| find "Path"') do set "NewPath=%%b"
set "PATH=%NewPath%"


echo Installing python requests and psutil modules...
python -m pip install --upgrade pip >nul
pip install requests >nul
pip install psutil >nul
echo -------------------------------------------

::Check if Steam is installed
set "STEAM_PATH=C:\Program Files (x86)\Steam"
set "SteamKey=HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Steam"

ver >nul
reg query "%SteamKey%" >nul 2>&1
if not %ERRORLEVEL% equ 0 (
    echo Steam is not installed. Please wait...
    set STEAM_INSTALLER=SteamSetup.exe
    set STEAM_URL=https://steamcdn-a.akamaihd.net/client/installer/SteamSetup.exe

    echo Downloading Steam installer...
    curl -o %DESKTOP%\!STEAM_INSTALLER! !STEAM_URL!

    echo Installing Steam...
    start /wait "" %DESKTOP%\!STEAM_INSTALLER! /S

    echo Steam installation complete.
    del %DESKTOP%\!STEAM_INSTALLER!
) else (
    for /f "delims=" %%a in ('reg query HKCU\Software\Valve\Steam\ActiveProcess /v SteamClientDll') do set steampath=%%a
    set STEAM_PATH=!steampath:~32,-16!
)
ver >nul
if not exist "!STEAM_PATH!\steamapps" (
    mkdir "!STEAM_PATH!\steamapps"
)
if not exist "!STEAM_PATH!\steamapps\common" (
    mkdir "!STEAM_PATH!\steamapps\common"
)
if not exist "!STEAM_PATH!\steamapps\common\Deep Rock Galactic" (
    mkdir "!STEAM_PATH!\steamapps\common\Deep Rock Galactic"
    mkdir "!STEAM_PATH!\steamapps\common\Deep Rock Galactic\FSD\Binaries
    mkdir "!STEAM_PATH!\steamapps\common\Deep Rock Galactic\FSD\Binaries\Win64"
)

::Specify the name of the python process
set processName=python.exe

::Set the registry path for the compatibility settings
set "regPath=HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"

::Get the full path to the python executable from the PATH environment variable
for /f "delims=" %%i in ('where %processName%') do set "pythonPath=%%i"

::Set the registry key to run the python process as administrator
reg add "%regPath%" /v "%pythonPath%" /t REG_SZ /d "~ RUNASADMIN" /f >nul
echo Compatibility setting applied for %processName% to run as administrator.

::Set the registry key to run the Steam process as administrator
reg add "HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers" /v "!STEAM_PATH!\steam.exe" /t REG_SZ /d "~ RUNASADMIN" /f >nul
reg add "HKCU\SOFTWARE\Valve\Steam" /v IgnoreCompatMode#Steam_WindowsCompat_Description_2 /t REG_DWORD /d 1 /f >nul
for /f "tokens=*" %%i in ('reg query HKU') do (
    set "userKey=%%i"
    reg query "!userKey!\SOFTWARE" >nul 2>&1
    if !errorlevel! equ 0 (
        ver >nul
        reg query "!userKey!\SOFTWARE\Valve" >nul 2>&1
        if !errorlevel! equ 0 (
            ver >nul
            reg query "!userKey!\SOFTWARE\Valve\Steam" >nul 2>&1
            if !errorlevel! equ 0 (
                ver >nul
                reg add "!userKey!\SOFTWARE\Valve\Steam" /v IgnoreCompatMode#Steam_WindowsCompat_Description_2 /t REG_DWORD /d 1 /f >nul
            )
        )
    )
)
echo Compatibility setting applied for steam.exe to run as administrator.

::Set the registry keys to run the DRG processes as administrator
reg add "HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers" /v "!STEAM_PATH!\steamapps\common\Deep Rock Galactic\FSD.exe" /t REG_SZ /d "~ RUNASADMIN" /f >nul
reg add "HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers" /v "!STEAM_PATH!\steamapps\common\Deep Rock Galactic\FSD\Binaries\Win64\FSD-Win64-Shipping.exe" /t REG_SZ /d "~ RUNASADMIN" /f >nul
echo Compatibility setting applied for DRG processes FSD.exe and FSD-Win64-Shipping.exe to run as administrator. 
echo Be sure to install to "!STEAM_PATH!\steamapps\common\Deep Rock Galactic\"

::Set auxiliary steam start script to run steam on startup in case the native steam auto run on startup doesn't work for whatever reason like it didnt for me on one particular install
set STARTUPFOLDER="%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
echo start "" "%STEAM_PATH%\steam.exe" > "%DESKTOP%\StartSteam.bat"
set SOURCE="%DESKTOP%\StartSteam.bat"
set TARGET="%STARTUPFOLDER%\StartSteam.lnk"
mklink "%TARGET%" "%SOURCE%" >nul

::Set Run_DeepDives.bat to run on startup
(
    echo @echo off
    echo set PYTHON_PATH="%pythonPath%"
    echo set SCRIPT_PATH="%STEAM_PATH%\steamapps\common\Deep Rock Galactic\FSD\Binaries\Win64\DeepDives_Run.py"
    echo cd "%STEAM_PATH%\steamapps\common\Deep Rock Galactic\FSD\Binaries\Win64\"
    echo %%PYTHON_PATH%% %%SCRIPT_PATH%%
    echo exit
) > "%DESKTOP%\Run_DeepDives.bat"
set SOURCE="%DESKTOP%\Run_DeepDives.bat"
set TARGET="%STARTUPFOLDER%\Run_DeepDives.lnk"
mklink "%TARGET%" "%SOURCE%" >nul

echo Starting Steam.... This window will close automatically after Steam is closed, or just go ahead and close it manually
"!STEAM_PATH!\steam.exe"

endlocal