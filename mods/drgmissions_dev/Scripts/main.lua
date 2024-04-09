local json = require("./mods/long_term_mission_data_collector/Scripts/dkjson")
local socket = require('./mods/long_term_mission_data_collector/Scripts/socket')
local utils = require('./mods/long_term_mission_data_collector/Scripts/bulkmissions_funcs')

-- function ToggleS4()
--     local subsystems = FindAllOf('SeasonsSubsystem')
--     if subsystems then
--         for i, subsystem in pairs(subsystems) do
--             local fullname = string.format("%s",subsystem:GetFullName())
--             if fullname == 'SeasonsSubsystem /Script/FSD.Default__SeasonsSubsystem' then goto continue end
--             subsystem:SetHasOptedOutOfSeasonContent(true)
--             break
--             ::continue::
--         end
--     end
-- end
-- function S4Off()
--     local subsystems = FindAllOf('SeasonsSubsystem')
--     if subsystems then
--         for i, subsystem in pairs(subsystems) do
--             local fullname = string.format("%s",subsystem:GetFullName())
--             if fullname == 'SeasonsSubsystem /Script/FSD.Default__SeasonsSubsystem' then goto continue end
--             subsystem:SetHasOptedOutOfSeasonContent(true)
--             break
--             ::continue::
--         end
--     end
-- end
-- function S4On()
--     local subsystems = FindAllOf('SeasonsSubsystem')
--     if subsystems then
--         for i, subsystem in pairs(subsystems) do
--             local fullname = string.format("%s",subsystem:GetFullName())
--             if fullname == 'SeasonsSubsystem /Script/FSD.Default__SeasonsSubsystem' then goto continue end
--             subsystem:SetHasOptedOutOfSeasonContent(false)
--             break
--             ::continue::
--         end
--     end
-- end

function Main()
    -- Wait for start menu to load
    local startmenus = nil
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

    -- Initialize Table
    local missionscount = 0
    local seasons = {'s0', 's4'}
    local master = {}
    for i, season in pairs(seasons) do
        missionscount = 0
        master[season] = {}
        master[season]['Biomes'] = {}
        -- Get GeneratedMission UObjects
        local b = nil
        local missions = utils.GetMissions(season)
        if missions then
            local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
            master[season]['timestamp'] = timestamp
            for index, mission in pairs(missions) do
                b = utils.GetBiome(mission)
                if not utils.HasKey(master[season]['Biomes'], b) then
                    master[season]['Biomes'][b] = {}
                end
                missionscount = utils.UnpackStandardMission(mission, master, b, missionscount, season)
            end
            print('\nNo. of missions in '..season..': '..tostring(missionscount))
        end
    end
    local indent = "    "
    local master_str = utils.TableToString(master, indent)
    print(master_str)
    -- print('\n\n\n')

    -- local master = {}
    -- master['Biomes'] = {}
    -- master['Season'] = desired_season
    -- missionscount = 0
    -- missions = utils.GetMissions('season4')
    -- if missions then
    --     local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    --     master['timestamp'] = timestamp
    --     for index, mission in pairs(missions) do
    --         b = utils.GetBiome(mission)
    --         if not utils.HasKey(master['Biomes'], b) then
    --             master['Biomes'][b] = {}
    --         end
    --         missionscount = utils.UnpackStandardMission(mission, master, b, missionscount)
    --     end
    --     local indent = "    "
    --     local master_str = utils.TableToString(master, indent)
    --     print(master_str)
    --     print('\nNo. of missions: '..tostring(missionscount))
    -- end
end

-- ToggleSeason()
Main()
-- utils.Exit()