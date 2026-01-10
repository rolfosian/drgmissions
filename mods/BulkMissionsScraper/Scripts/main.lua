local json = require("./mods/shared/dkjson")

function PressStartAndWaitForLoad()
    local startmenus = nil
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
end

function Main()
    local currytime = nil

    PressStartAndWaitForLoad()

    -- Get current UTC Time
    local firstdate = os.date("!*t")
    local current_time = os.time(firstdate)
    --Set target date
    local target_date = os.time{year=2024, month=08, day=30, hour=00, min=00, sec=00}
    -- Calculate the difference in seconds between the current UTC time and the target date
    local diff_seconds = os.difftime(target_date, current_time)
    -- Calculate total amount of 30 minute increments between current time and the target date
    local total_increments = math.floor(diff_seconds / 1800)
    total_increments = total_increments + 1

    local utils = require('./mods/shared/shared_drgmissions_lua_funcs')
    local SeasonsValues = {
        ['s0'] = 0,
        ['s1'] = 1,
        ['s2'] = 2,
        ['s3'] = 3,
        ['s4'] = 4,
        ['s5'] = 5,
        ['s6'] = 6
    }
    local port = 53578
    local PollingClient = utils.ConnectPollClient(port)

    -- Initialize Table
    local god = {}
    -- local count = 0
    local missionscount = 0
    local RandomSeed = nil
    local PreviousRandomSeed = nil
    local FSDGameInstance = FindFirstOf('FSDGameInstance')
    -- Loop for the increments
    for i = 1, total_increments do
        PollingClient:send('pol\n')
        PollingClient:receive("*l")

        local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
        while true do
            FSDGameInstance:UpdateGlobelMissionSeed() -- No, this is not a typo (but maybe it was on gsg's end).
            RandomSeed = FSDGameInstance:GetGlobalMissionSeedNew().RandomSeed
            if RandomSeed == PreviousRandomSeed then
                print('SEEN') -- has never seen as far as i can tell, prob ditch the stall when i trust this enough
            else
                break
            end
        end

        local master = {}
        for SeasonKey, SeasonValue in pairs(SeasonsValues) do
            missionscount = 0
            master[SeasonKey] = {}
            master[SeasonKey]['Biomes'] = utils.BiomesTable()
            master[SeasonKey]['timestamp'] = timestamp
            master[SeasonKey]['RandomSeed'] = RandomSeed

            -- Get GeneratedMission UObjects
            local b = nil
            local missions = utils.GetMissions(SeasonValue, RandomSeed)

            for index, mission in pairs(missions) do
                b = utils.GetBiome(mission)
                missionscount = utils.UnpackStandardMission(mission, master, b, missionscount, SeasonKey)
            end

            for biome, ms  in pairs(master[SeasonKey]['Biomes']) do
                if utils.IsTableEmpty(ms) then
                    master[SeasonKey]['Biomes'][biome] = nil
                end
            end
        end
        PreviousRandomSeed = tonumber(tostring(RandomSeed))

        god[timestamp] = master

        --Get 'current' time
        currytime = os.date("%Y-%m-%d %H:%M:%S")
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
        utils.IncrementDatetime(currytime)
    end

    PollingClient:send('enc\n')
    PollingClient:receive('*l')

    print('Encoding JSON...\n')
    god = json.encode(god) .. 'END'
    print('Completed encoding JSON...\n')
    PollingClient:send('encc\n')
    PollingClient:receive('*l')
    PollingClient:close()
    -- local file = io.open('drgmissionsgod.json', 'w')
    -- if file then
    --     file:write(string.sub(god, 1, -4))
    --     file:close()
    -- end
    utils.Send_data(port, god)
end
Main()