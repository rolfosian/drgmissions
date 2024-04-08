local json = require("./mods/long_term_mission_data_collector/Scripts/dkjson")
local socket = require('./mods/long_term_mission_data_collector/Scripts/socket')
local utils = require('./mods/long_term_mission_data_collector/Scripts/bulkmissions_funcs')

function Main()
    local startmenus = nil
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

    local invalid_keys = io.open("invalid_keys.txt", "r")
    local timestamps = {}
    if invalid_keys then
        for line in invalid_keys:lines() do
            line = line:gsub("\n", "")
            if line == "" then goto continue end
            table.insert(timestamps, line)
            ::continue::
        end
        invalid_keys:close()
    end
    
    -- Set desired season content
    local desired_season = nil
    utils.SetSeason(desired_season)
    socket.sleep(1.4)

    -- Initialize Table
    local god = {}
    for _, timestamp in pairs(timestamps) do

        -- Change System Clock
        local datetime = utils.Split(timestamp, 'T')
        datetime[2] = datetime[2]:gsub('Z', '')
        local command = 'date '..utils.ReverseDateFormat(datetime[1])..' & time '..datetime[2]
        os.execute(command)
        socket.sleep(2.5)

        -- Initialize Table
        local master = {}
        local missionscount = 0
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
            master['timestamp'] = timestamp
            for index, mission in pairs(missions) do
                b = utils.GetBiome(mission)
                if not utils.HasKey(master['Biomes'], b) then
                    master['Biomes'][b] = {}
                end
                missionscount = utils.UnpackStandardMission(mission, master, b, missionscount)
            end
            god[timestamp] = master
        end
    end

    god = json.encode(god)
    local file = io.open('redonemissions.json', 'w')
    if file then
        file:write(god)
        file:close()
    end

    utils.Exit()
end
Main()