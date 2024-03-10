local json = require("./mods/long_term_mission_data_collector/Scripts/dkjson")
local socket = require('./mods/long_term_mission_data_collector/Scripts/socket')
local utils = require('./mods/long_term_mission_data_collector/Scripts/bulkmissions_funcs')
function ReverseDateFormat(inputDate)
    local oldDate = Split(inputDate, "-")
    local year = oldDate[1]
    local month = oldDate[2]
    local day = oldDate[3]
    
    local reversedDate = day .. "-" .. month .. "-" .. year
    return reversedDate
  end

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
    
    local god = {}
    for _, timestamp in pairs(timestamps) do

        -- Change System Clock
        local datetime = utils.Split(timestamp, 'T')
        datetime[2] = datetime[2]:gsub('Z', '')
        local command = 'date '..ReverseDateFormat(datetime[1])..' & time '..datetime[2]
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
    -- Get the current instance of the Escape Menu (This doesn't actually really load the menu)
    local playercontrollers = FindAllOf('BP_PlayerController_SpaceRig_C')
    if playercontrollers then
        for index, playercontroller in pairs(playercontrollers) do
            local fullname = string.format("%s",playercontroller:GetFullName())
            if fullname == 'BP_PlayerController_SpaceRig_C /Game/Game/SpaceRig/BP_PlayerController_SpaceRig.Default__BP_PlayerController_SpaceRig_C' then goto continue end
            local escape_menu = playercontroller:GetEscapeMenu()
            -- Execute function to quit the game 'organically' rather than terminate externally
            escape_menu:Yes_1ADE94D8445F020C5D27B8822516025E()
            break
            ::continue::
        end
    end
end
Main()