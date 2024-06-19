local json = require("./mods/shared/dkjson")

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
        startmenu:OpenGameLevel()
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
    local utils = require('./mods/shared/shared_drgmissions_lua_funcs')
    
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

    local SeasonsValues = {
        ['s0'] = 0,
        ['s1'] = 1,
        ['s2'] = 2,
        ['s3'] = 3,
        ['s4'] = 4,
        ['s5'] = 5
    }
    local port = 12345
    local PollingClient = utils.ConnectPollClient(port)

    -- Initialize Table
    local god = {}
    local FSDGameInstance = FindFirstOf('FSDGameInstance')
    local RandomSeed = nil
    local PreviousRandomSeed = nil
    local missionscount = 0
    for _, timestamp in pairs(timestamps) do
        PollingClient:send('pol\n')
        PollingClient:receive("*l")

        -- Change System Clock
        local datetime = utils.Split(timestamp, 'T')
        datetime[2] = datetime[2]:gsub('Z', '')
        local command = 'date '..utils.ReverseDateFormat(datetime[1])..' & time '..datetime[2]
        os.execute(command)

        while true do
            FSDGameInstance:UpdateGlobelMissionSeed() -- No, this is not a typo (but maybe it was on gsg's end).
            RandomSeed = FSDGameInstance:GetGlobalMissionSeedNew().RandomSeed
            if RandomSeed == PreviousRandomSeed then
                print('SEEN') -- has never seen as far as i can tell, prob ditch the stall when i trust this enough
            else
                break
            end
        end

        -- Initialize Table
        local master = {}
        for SeasonKey, SeasonValue in pairs(SeasonsValues) do
            missionscount = 0

            master[SeasonKey] = {}
            master[SeasonKey]['Biomes'] = utils.BiomesTable()

            -- Get GeneratedMission UObjects
            local b = nil
            local missions = utils.GetMissions(SeasonValue, RandomSeed)
            if missions then
                master[SeasonKey]['timestamp'] = timestamp
                for index, mission in pairs(missions) do
                    b = utils.GetBiome(mission)
                    missionscount = utils.UnpackStandardMission(mission, master, b, missionscount, SeasonKey)
                end
            end
            for biome, ms  in pairs(master[SeasonKey]['Biomes']) do
                if utils.IsTableEmpty(ms) then
                    master[SeasonKey]['Biomes'][biome] = nil
                end
            end
        end
        PreviousRandomSeed = tonumber(tostring(RandomSeed))
        god[timestamp] = master
    end
    PollingClient:send('enc\n')
    PollingClient:receive('*l')
    PollingClient:close()

    print('Encoding JSON...\n')
    god = json.encode(god) .. 'END'
    print('Completed encoding JSON...\n')
    -- local file = io.open('redonemissions.json', 'w')
    -- if file then
    --     file:write(string.sub(god, 1, -4))
    --     file:close()
    -- end
    utils.Send_data(port, god)
end
Main()