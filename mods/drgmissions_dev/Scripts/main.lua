local json = require("./mods/BulkMissionsScraper/Scripts/dkjson")

function IsLoaded()
    local umgsequenceplayers = FindAllOf('UMGSequencePlayer')
    if umgsequenceplayers then
        if #umgsequenceplayers > 150 then
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

function Main()
    -- -- Wait for start menu to load
    if IsLoaded() then
        goto isloaded
    else
        PressStartAndWaitForLoad()
    end
    ::isloaded::

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
            else
                break
            end
        end
        SeasonSeeds[season] = GlobalSeed

        missionscount = 0
        master[season] = {}
        master[season]['Biomes'] = {}
        -- Get GeneratedMission UObjects
        local b = nil
        local missions = utils.GetMissions()
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

--     god[timestamp] = master
--     god = json.encode(god)
--     local file = io.open('drgmissionsdev.json', 'w')
--     if file then
--         file:write(god)
--         file:close()
--     end
end

Main()
-- utils.Exit()