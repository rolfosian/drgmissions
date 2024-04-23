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
    
    local seasons = {'s0', 's4'}

    -- Initialize Table
    local god = {}
    utils.CreatePollFile('firstpoll.txt')
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
        for _, season in pairs(seasons) do
            master[season] = {}
            master[season]['Biomes'] = {}
            -- Get GeneratedMission UObjects
            local b = nil
            local missions = utils.GetMissions(season)
            if missions then
                timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
                master[season]['timestamp'] = timestamp
                for index, mission in pairs(missions) do
                    b = utils.GetBiome(mission)
                    if not utils.HasKey(master[season]['Biomes'], b) then
                        master[season]['Biomes'][b] = {}
                    end
                    missionscount = utils.UnpackStandardMission(mission, master, b, missionscount, season)
                end
            end
        end
        god[timestamp] = master

        utils.CreatePollFile('poll.txt')
    end

    god = json.encode(god)
    local file = io.open('redonemissions.json', 'w')
    if file then
        file:write(god)
        file:close()
    end
end
Main()