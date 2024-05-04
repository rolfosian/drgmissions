local json = require("./mods/long_term_mission_data_collector/Scripts/dkjson")
-- local socket = require('./mods/long_term_mission_data_collector/Scripts/socket')

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
end

function Main()
    local currytime = nil

    PressStartAndWaitForLoad()

    -- Get current UTC Time
    local firstdate = os.date("!*t")
    local current_time = os.time(firstdate)
    --Set target date
    local target_date = os.time{year=2024, month=07, day=01, hour=00, min=00, sec=00}
    -- Calculate the difference in seconds between the current UTC time and the target date
    local diff_seconds = os.difftime(target_date, current_time)
    -- Calculate total amount of 30 minute increments between current time and the target date
    local total_increments = math.floor(diff_seconds / 1800)
    total_increments = total_increments + 1

    local utils = require('./mods/long_term_mission_data_collector/Scripts/bulkmissions_funcs')
    local SeasonsAndFuncs = {
        s0 = utils.S4Off,
        s4 = utils.S4On
    }

    -- Initialize Table
    local god = {}
    local count = 0
    local missionscount = 0
    local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    local GlobalSeed = nil
    local PreviousGlobalSeed = nil
    local FSDGameInstance = FindFirstOf('FSDGameInstance')
    -- Loop for the increments
    utils.CreatePollFile('firstpoll.txt')
    for i = 1, total_increments do
        while true do
            GlobalSeed = FSDGameInstance:GetGlobalMissionSeed()
            if GlobalSeed == PreviousGlobalSeed then
                print('SEEN')
            else
                break
            end
        end

        local master = {}
        local SeasonSeeds = {}
        for season, season_switch in pairs(SeasonsAndFuncs) do
            season_switch()

            -- FSDGameInstance:UpdateGlobelMissionSeed() -- No, this is not a typo (but maybe it was on gsg's end). Unneeded - I believe GetGlobalMissionSeed calls this itself or uses a similar mechanism
            while true do
                GlobalSeed = FSDGameInstance:GetGlobalMissionSeed()
                if utils.IsInTable(SeasonSeeds, GlobalSeed) then
                    print('SEEN')
                else
                    break
                end
            end
            SeasonSeeds[season] = GlobalSeed

            master[season] = {}
            master[season]['Biomes'] = {}
            -- Get GeneratedMission UObjects
            local b = nil
            local missions = utils.GetMissions()
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
                PreviousGlobalSeed = GlobalSeed
            end
            -- socket.sleep(0.1)
        end
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
        local newtime = utils.IncrementDatetime(currytime)
        newtime = utils.Split(newtime, ' ')

        -- Remove ReverseDateFormat function and just use newtime[1] if your system date format is YY-MM-DD
        local command = 'date '..utils.ReverseDateFormat(newtime[1])..' & time '..newtime[2]

        -- Set time forward 30 minutes
        print(command..'\n')
        count = count + 1
        print(tostring(count)..'\n')
        os.execute(command)

        -- socket.sleep(1.4)
        utils.CreatePollFile('poll.txt')
    end

    god = json.encode(god)
    local file = io.open('drgmissionsgod.json', 'w')
    if file then
        file:write(god)
        file:close()
    end
end
Main()