@echo off

set "ESC="
set "RESET=%ESC%[0m"
set "RED=%ESC%[31m"
set "GREEN=%ESC%[40;92m"
set "YELLOW=%ESC%[1;33m"
set "BLUE=%ESC%[40;94m"

cd /d %~dp0 >nul
NET SESSION >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    goto :startScript
) ELSE (
    ECHO This script is required to be run with Administrator Privileges.
    pause
    exit
)
:startScript

for /f "delims=" %%a in ('tzutil /g') do set timezone=%%a
if /i NOT "%timezone%"=="UTC" (
    echo System Timezone is not UTC, it is %timezone%
    echo Please set system Timezone to UTC
    pause
)

echo:Please ensure your environment is set up to handle abuse of the system clock.
:resetScript
echo:Select a scraper option:
echo:
echo:[%YELLOW%1%RESET%] Bulk Missions
echo:[%YELLOW%2%RESET%] Daily Deals
echo:[%YELLOW%3%RESET%] Deep Dives
echo:[%YELLOW%4%RESET%] Exit
echo:%BLUE%___________%RESET%
setlocal enabledelayedexpansion
choice /C:1234 /N >nul
set _erl=%errorlevel%

if %_erl%==4 exit /b
if %_erl%==3 goto :DeepDives
if %_erl%==2 goto :DailyDeals
if %_erl%==1 goto :BulkMissions

:BulkMissions
echo:Bulk Missions Scraper selected.
python BulkMissions_Run.py /wait
echo:Data saved at%GREEN% %cd%\drgmissionsgod.json%RESET%
echo:%BLUE%___________%RESET%
goto :resetScript

:DailyDeals
echo:Daily Deals Scraper selected.
python DailyDeals_Run.py /wait
echo:Data saved at%GREEN% %cd%\drgdailydeals.json%RESET%
echo:%BLUE%___________%RESET%
goto :resetScript

:DeepDives
echo:Deep Dives Scraper selected.
call :previousThursdayAt11UTC result
python DeepDives_Run.py manual /wait
echo:Data saved at%GREEN% %cd%\DD_%result%.json%RESET%
echo:%BLUE%___________%RESET%
goto :resetScript

:previousThursdayAt11UTC
setlocal enabledelayedexpansion
for /f %%a in ('powershell -Command "$now = Get-Date; if ($now.DayOfWeek -eq 'Thursday' -and $now.TimeOfDay.Hours -gt 11) { $targetDateTime = Get-Date -Year $now.Year -Month $now.Month -Day $now.Day -Hour 11 -Minute 0 -Second 0 } else { $daysUntilLastThursday = [int]$now.DayOfWeek - [int][DayOfWeek]::Thursday; if ($daysUntilLastThursday -lt 0) { $daysUntilLastThursday += 7 }; $lastThursday = $now.AddDays(-$daysUntilLastThursday); $targetDateTime = Get-Date -Year $lastThursday.Year -Month $lastThursday.Month -Day $lastThursday.Day -Hour 11 -Minute 0 -Second 0 }; $isoFormatWithZ = $targetDateTime.ToUniversalTime().ToString('yyyy-MM-ddTHH-mm-ssZ'); Write-Output $isoFormatWithZ"') do (
    set thursdate=%%a
)
endlocal & set "%~1=%thursdate%"
exit /b