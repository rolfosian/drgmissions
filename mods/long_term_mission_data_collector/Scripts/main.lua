local json = require("./mods/long_term_mission_data_collector/Scripts/dkjson")
local socket = require('./mods/long_term_mission_data_collector/Scripts/socket')
local utils = require('./mods/long_term_mission_data_collector/Scripts/bulkmissions_funcs')

function Main()
    local startmenus = nil
    local currytime = nil

    -- Wait for start menu to load
    while true do
        startmenus = FindAllOf('Bp_StartMenu_PlayerController_C')
        if startmenus then
            break
        end
    end
    -- Execute the function that 'press any key' invokes
    for index, startmenu in pairs(startmenus) do
        startmenu:PressStart()
    end
    local waiting_for_load = true
    -- Wait for Space Rig to load
    while waiting_for_load do
        local count = 0
        local umgsequenceplayers = FindAllOf('UMGSequencePlayer')
        if umgsequenceplayers then
            for index, sequenceplayer in ipairs(umgsequenceplayers) do
                local fullname = string.format("%s",sequenceplayer:GetFullName())
                if string.match(fullname, 'UMGSequencePlayer /Engine/Transient%.GameEngine_.*:BP_GameInstance_C_.*%.ConsoleScreen_Crafting_C_.*%.UMGSequencePlayer_.*') then
                    count = count + 1
                    if count > 11 then
                        waiting_for_load = false
                    end
                end
            end
        end
    end

    -- Get current UTC Time
    local firstdate = os.date("!*t")
    local current_time = os.time(firstdate)
    --Set target date
    local target_date = os.time{year=2023, month=10, day=25, hour=00, min=00, sec=00}
    -- Calculate the difference in seconds between the current UTC time and the target date
    local diff_seconds = os.difftime(target_date, current_time)
    -- Calculate total amount of 30 minute increments between current time and the target date
    local total_increments = math.floor(diff_seconds / 1800)
    total_increments = total_increments + 1

    -- Set desired season content
    local desired_season = nil
    utils.SetSeason(desired_season)
    socket.sleep(1.4)

    -- Initialize Table
    local god = {}
    local count = 0
    local missionscount = 0
    -- Loop for the increments
    for i = 1, total_increments do
        local master = {}
        master['Biomes'] = {}
        -- Get GeneratedMission UObjects
        local b = nil
        local missions = {}
        local MissionGenerationManagers = FindAllOf('MissionGenerationManager')
        if MissionGenerationManagers then
            for index, manager in pairs(MissionGenerationManagers) do
                local fullname = string.format("%s",manager:GetFullName())
                if fullname == 'MissionGenerationManager /Script/FSD.Default__MissionGenerationManager' then goto continue end
                local remotemissions = manager:GetAvailableMissions()
                for index, remotemission in pairs(remotemissions) do
                    local mission = remotemission:get()
                    table.insert(missions, mission)
                end
                break
                ::continue::
            end
        end
        if missions then
            local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
            master['timestamp'] = timestamp
            for index, mission in pairs(missions) do
                b = utils.GetBiome(mission)
                if not utils.HasKey(master['Biomes'], b) then
                    master['Biomes'][b] = {}
                end
                missionscount = utils.UnpackStandardMission(mission, master, b, missionscount)
            end
            
            god[timestamp] = master

            --Get 'current' time
            local currytime = os.date("%Y-%m-%d %H:%M:%S")
            local year, month, day, hour, minute, second = currytime:match("(%d+)-(%d+)-(%d+) (%d+):(%d+):(%d+)")
            minute = tonumber(minute)
            -- Round down to the nearest half-hour
            if minute >= 30 then
                minute = 30
            else
                minute = 0
            end
            -- Set the second to 1
            second = 1
            currytime = string.format("%04d-%02d-%02d %02d:%02d:%02d", year, month, day, hour, minute, second)
            -- Increment currytime forward by 30 minutes
            local newtime = utils.IncrementDatetime(currytime)
            newtime = utils.Split(newtime, ' ')
            -- Remove ReverseDateFormat function and just use newtime[1] if your system date format is YY-MM-DD
            local command = 'date '..utils.ReverseDateFormat(newtime[1])..' & time '..newtime[2]
            -- Set time forward 30 minutes
            print(command..'\n')
            count = count + 1
            print(tostring(count)..'\n')
            os.execute(command)

            socket.sleep(1.3)
        end
    end

    god = json.encode(god)
    local file = io.open('drgmissionsgod.json', 'w')
    if file then
        file:write(god)
        file:close()
    end
end
Main()
