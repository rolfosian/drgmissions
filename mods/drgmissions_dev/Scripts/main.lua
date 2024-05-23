local json = require("./mods/BulkMissionsScraper/Scripts/dkjson")
function IsLoaded()
    local GeneratedMissions = FindAllOf('GeneratedMission')
    if GeneratedMissions then
        if #GeneratedMissions > 6 then
            return true
        else
            return false
        end
    else
        return false
    end
end
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

function TestSeasonSeeds()
    local utils = require('./mods/BulkMissionsScraper/Scripts/bulkmissions_funcs')
    local SeasonsAndFuncs = {
        s0 = utils.S4Off,
        s4 = utils.S4On
    }

    -- Initialize Table
    local god = {}
    local missionscount = 0
    local master = {}
    local SeasonSeeds = {}
    local GlobalSeed = nil
    local PreviousGlobalSeed = nil
    local FSDGameInstance = FindFirstOf('FSDGameInstance')
    local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    for season, season_switch in pairs(SeasonsAndFuncs) do
        season_switch()

        -- FSDGameInstance:UpdateGlobelMissionSeed() -- No, this is not a typo (but maybe it was on gsg's end). Unneeded - I believe GetGlobalMissionSeed calls this itself or uses a similar mechanism
        while true do
            GlobalSeed = FSDGameInstance:GetGlobalMissionSeed()
            if utils.IsInTable(SeasonSeeds, GlobalSeed) then
                print('SEED DUPLICATES FOUND: ')
                for s, seed in pairs(SeasonSeeds) do
                    if seed == GlobalSeed then
                        print(s)
                        print(season)
                    end
                end
                break
            else
                break
            end
        end
        SeasonSeeds[season] = GlobalSeed
    end
end
function TestTwoWeeks()
    local currytime = nil
    -- Get current UTC Time
    local firstdate = os.date("!*t")
    local current_time = os.time(firstdate)
    --Set target date
    local target_date = current_time + 1209600
    -- Calculate the difference in seconds between the current UTC time and the target date
    local diff_seconds = os.difftime(target_date, current_time)
    -- Calculate total amount of 30 minute increments between current time and the target date
    local total_increments = math.floor(diff_seconds / 1800)
    total_increments = total_increments + 1

    local utils = require('./mods/BulkMissionsScraper/Scripts/bulkmissions_funcs')
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
    for i = 1, total_increments do
        while true do
            GlobalSeed = FSDGameInstance:GetGlobalMissionSeed()
            if GlobalSeed == PreviousGlobalSeed then
                print('SEEN') -- has never seen as far as i can tell, prob ditch the stall when GetGlobalMissionSeed is trusted enough
                break
            else
                break
            end
        end

        local master = {}
        local SeasonSeeds = {}
        for season, season_switch in pairs(SeasonsAndFuncs) do
            missionscount = 0
            season_switch()

            while true do
                GlobalSeed = FSDGameInstance:GetGlobalMissionSeed()
                if utils.IsInTable(SeasonSeeds, GlobalSeed) then
                    print('SEED DUPLICATES FOUND: ')
                    for s, seed in pairs(SeasonSeeds) do
                        if seed == GlobalSeed then
                            print(season)
                            print(s)
                        end
                    break
                    end
                else
                    break
                end
            end
            SeasonSeeds[season] = GlobalSeed

            master[season] = {}
            master[season]['Biomes'] = utils.BiomesTable()

            -- Get GeneratedMission UObjects
            local b = nil
            local missions = utils.GetMissions()
            if missions then
                timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
                master[season]['timestamp'] = timestamp
                for index, mission in pairs(missions) do
                    b = utils.GetBiome(mission)
                    missionscount = utils.UnpackStandardMission(mission, master, b, missionscount, season)
                end
                PreviousGlobalSeed = GlobalSeed
            end
            print('\nNo. of missions in '..season..': '..tostring(missionscount))
            for biome, ms  in pairs(master[season]['Biomes']) do
                if utils.IsTableEmpty(ms) then
                    master[season]['Biomes'][biome] = nil
                end
            end
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
    end

    god = json.encode(god)
    local file = io.open('drgmissionsdev.json', 'w')
    if file then
        file:write(god)
        file:close()
    end
end
function TestCurrentTimeOnly()
    local utils = require('./mods/BulkMissionsScraper/Scripts/bulkmissions_funcs')
    local SeasonsAndFuncs = {
        s0 = utils.S4Off,
        s4 = utils.S4On
    }

    -- Initialize Table
    local god = {}
    local missionscount = 0
    local master = {}
    local SeasonSeeds = {}
    local GlobalSeed = nil
    local PreviousGlobalSeed = nil
    local FSDGameInstance = FindFirstOf('FSDGameInstance')
    local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    for season, season_switch in pairs(SeasonsAndFuncs) do
        season_switch()

        -- FSDGameInstance:UpdateGlobelMissionSeed() -- No, this is not a typo (but maybe it was on gsg's end). Unneeded - I believe GetGlobalMissionSeed calls this itself or uses a similar mechanism
        while true do
            GlobalSeed = FSDGameInstance:GetGlobalMissionSeed()
            if utils.IsInTable(SeasonSeeds, GlobalSeed) then
                print('SEEN')
                print(season)
                print(GlobalSeed)
            else
                break
            end
        end
        SeasonSeeds[season] = GlobalSeed

        missionscount = 0
        master[season] = {}
        master[season]['Biomes'] = utils.BiomesTable()

        -- Get GeneratedMission UObjects
        local b = nil
        local missions = utils.GetMissions()
        if missions then
            local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
            master[season]['timestamp'] = timestamp
            for index, mission in pairs(missions) do
                b = utils.GetBiome(mission)
                missionscount = utils.UnpackStandardMission(mission, master, b, missionscount, season)
            end
            print('\nNo. of missions in '..season..': '..tostring(missionscount))
        end

        for biome, ms  in pairs(master[season]['Biomes']) do
            if utils.IsTableEmpty(ms) then
                master[season]['Biomes'][biome] = nil
            end
        end
    end
    local indent = "    "
    local master_str = utils.TableToString(master, indent)
    print(master_str)

    -- god[timestamp] = master
    -- god = json.encode(god, {indent=true})
    -- print(god)

--     local file = io.open('drgmissionsdev.json', 'w')
--     if file then
--         file:write(god)
--         file:close()
--     end
end

if IsLoaded() then
    goto isloaded
else
    PressStartAndWaitForLoad()
end
::isloaded::

TestSeasonSeeds()
-- TestCurrentTimeOnly()
-- TestTwoWeeks()