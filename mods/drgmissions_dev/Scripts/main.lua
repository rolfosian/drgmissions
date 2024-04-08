local json = require("./mods/long_term_mission_data_collector/Scripts/dkjson")
local socket = require('./mods/long_term_mission_data_collector/Scripts/socket')
local utils = require('./mods/long_term_mission_data_collector/Scripts/bulkmissions_funcs')

function Main()
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

    -- Set desired season content
    local desired_season = nil
    utils.SetSeason(desired_season)
    socket.sleep(1.4)

    -- Initialize Table
    local missionscount = 0
    local master = {}
    master['Biomes'] = {}
    master['Season'] = desired_season
    
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
        local indent = "    "
        local master_str = utils.TableToString(master, indent)
        print(master_str)
        print('\nNo. of missions: '..tostring(missionscount))
    end
end

Main()