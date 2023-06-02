-- DEEP ROCK GALACTIC LUA SCRIPT FOR USE IN CONJUNCTION WITH RE-UE4SS LUA API (https://github.com/UE4SS-RE/RE-UE4SS/releases) TO FETCH CURRENT DEEP DIVE DATA

-- TO RUN DRG HEADLESS, USE COMMAND LINE ARG -nullrhi WHEN RUNNING THE GAME
-- CONSIDER STEAMCMD FOR EVEN LESS OVERHEAD AND EASIER AUTOMATION FOR UPDATES ETC
-- MAKE SURE TO SKIP INTRO VIDEOS AND USE -nosplash COMMAND LINE ARG
-- main.lua of course goes in Deep Rock Galactic\FSD\Binaries\Win64\Mods\missiondatafetcher\Scripts
-- RE-UE4SS goes in Deep Rock Galactic\FSD\Binaries\Win64 - this is also the CWD of the script.

-- TODO
-- Mission icon rendering PIL functions in main.py probably can be easily retooled to be used with a flask or similar app
-- Contingencies for if the game doesn't terminate gracefully on 'organic' exit
-- Contingencies for if the game crashes
-- Main loop script to actually launch the game and then run the rendering script after the json is generated in the first place (Personally waiting for sale to pick up another copy of the game for this)

local json = require("./mods/dds_fetcher/Scripts/dkjson")
function TableToString(table, indent)
    indent = indent or ""
    local str = "{\n"
    for key, value in pairs(table) do
      if type(value) == "table" then
        str = str .. indent .. "[" .. tostring(key) .. "] = " .. TableToString(value, indent .. "  ") .. ",\n"
      else
        str = str .. indent .. "[" .. tostring(key) .. "] = " .. tostring(value) .. ",\n"
      end
    end
    str = str .. indent:sub(1, -3) .. "}"
    return str
end
function Split(str, separator)
    local result = {}
    local pattern = string.format("([^%s]+)", separator)
    for match in string.gmatch(str, pattern) do
        table.insert(result, match)
    end
    return result
end
function HasKey(table, key)
    return table[key] ~= nil
end
function UnpackDeepDiveMission(mission, master, currentDateTime, t) -- Considering adding logic here to show complexity and length for dd stages, but it would remove a whole lot more from the DD mystique imo...
    local mission1 = {}
    local missionfullname = string.format("%s",mission:GetFullName())
    local missionfullname_parts = Split(missionfullname, '_')
    local missionid_string = missionfullname_parts[#missionfullname_parts]
    missionid_string = string.sub(missionid_string, -3)
    local missionid = tonumber(missionid_string)
    mission1['id'] = missionid
    local PrimaryObjective = mission:GetPropertyValue("PrimaryObjective")
    PrimaryObjective = string.format("%s",PrimaryObjective:GetFullName())
    local primary_objectives = {
        {pattern = "PointExtraction", result = "Point Extraction"},
        {pattern = "Eliminate_Eggs", result = "Elimination"},
        {pattern = "Escort", result = "Escort Duty"},
        {pattern = "1st_Extraction", result = "Mining Expedition"},
        {pattern = "Refinery", result = "On-Site Refining"},
        {pattern = "1st_Salvage", result = "Salvage Operation"},
        {pattern = "1st_Facility", result = "Industrial Sabotage"},
        {pattern = "Gather_AlienEggs", result = "Egg Hunt"}
    }
    for _, obj in ipairs(primary_objectives) do
        if string.find(PrimaryObjective, obj.pattern) then
            PrimaryObjective = obj.result
            break
        end
    end
    -- print(PrimaryObjective)
    mission1['PrimaryObjective'] = PrimaryObjective
    local SecondaryObjective = mission:GetPropertyValue("SecondaryObjectives")[1]
    SecondaryObjective = string.format("%s",SecondaryObjective:GetFullName())
    local secondary_objectives = {
        {pattern = "RepairMinimules", result = "Repair Minimules"},
        {pattern = "Elimination_Eggs", result = "Kill Dreadnought(s)"},
        {pattern = "DD_Morkite", result = "Mine Morkite"},
        {pattern = "AlienEggs", result = "Get Alien Eggs"},
        {pattern = "DD_Defense", result = "Black Box"},
    }
    for _, obj in ipairs(secondary_objectives) do
        if string.find(SecondaryObjective, obj.pattern) then
            SecondaryObjective = obj.result
            break
        end
    end
    -- print(SecondaryObjective)
    mission1['SecondaryObjective'] = SecondaryObjective
    local warnings = {
        {pattern = 'RegenerativeEnemies', result = 'Regenerative Bugs'},
        {pattern = 'ExploderInfestation', result = 'Exploder Infestation'},
        {pattern = 'ShieldDisruption', result = 'Shield Disruption'},
        {pattern = 'HeroEnemies', result = 'Elite Threat'},
        {pattern = 'WRN_Plague', result = 'Lithophage Outbreak'},
        {pattern = 'LethalEnemies', result = 'Lethal Enemies'},
        {pattern = 'Swarmagedon', result = 'Swarmageddon'},
        {pattern = 'MacteraCave', result = 'Mactera Plague'},
        {pattern = 'NoOxygen', result = 'Low Oxygen'},
        {pattern = 'CaveLeechDen', result = 'Cave Leech Cluster'},
        {pattern = 'RivalIncursion', result = 'Rival Presence'},
        {pattern = 'Ghost', result = 'Haunted Cave'},
        {pattern = 'InfestedEnemies', result = 'Parasites'}
    }
    local MissionWarnings = mission:GetPropertyValue("MissionWarnings")
    local num_MissionWarnings = MissionWarnings:GetArrayNum()
    if num_MissionWarnings == 0 then
        mission1['MissionWarnings'] = nil
    elseif num_MissionWarnings == 1 then
        local MissionWarning1 = MissionWarnings[1]:GetFullName()
        for _, obj in ipairs(warnings) do
            if string.find(MissionWarning1, obj.pattern) then
                MissionWarning1 = obj.result
                break
            end
        end
        -- print(MissionWarning1)
        mission1['MissionWarnings'] = {MissionWarning1}
    elseif num_MissionWarnings == 2 then
        local MissionWarning1 = MissionWarnings[1]:GetFullName()
        for _, obj in ipairs(warnings) do
            if string.find(MissionWarning1, obj.pattern) then
                MissionWarning1 = obj.result
                break
            end
        end
        -- print(MissionWarning1)
        local MissionWarning2 = MissionWarnings[2]:GetFullName()
        for _, obj in ipairs(warnings) do
            if string.find(MissionWarning2, obj.pattern) then
                MissionWarning2 = obj.result
                break
            end
        end
        --print(MissionWarning2)
        mission1['MissionWarnings'] = {MissionWarning1, MissionWarning2}
    end
    local MissionMutator = mission:GetPropertyValue("MissionMutator")
    if MissionMutator then 
        local MissionMutator = string.format("%s",MissionMutator:GetFullName())
        if MissionMutator == 'nil' then
            mission1['MissionMutator'] = nil
        else
            local mutators = {
                {pattern = 'GoldRush', result = 'Gold Rush'},
                {pattern = 'RichInMinerals', result = 'Mineral Mania'},
                {pattern = 'Weakspot', result = 'Critical Weakness'},
                {pattern = 'LowGravity', result = 'Low Gravity'},
                {pattern = 'XXXP', result = 'Double XP'},
                {pattern = 'OxygenRich', result = 'Rich Atmosphere'},
                {pattern = 'ExterminationContract', result = 'Golden Bugs'},
                {pattern = 'ExplosiveEnemies', result = 'Volatile Guts'}
            }
            for _, obj in ipairs(mutators) do
                if string.find(MissionMutator, obj.pattern) then
                    MissionMutator = obj.result
                    mission1['MissionMutator'] = MissionMutator
                    break
                end
            end
            -- print(MissionMutator)
        end
    end
    table.insert(master[currentDateTime][t]['Stages'], mission1)
end
function GetMissions()
    local missions = FindAllOf("GeneratedMission")
    if missions then
        return missions
    else
        return nil
    end
end
function GetBiome(mission)
    local b = mission:GetPropertyValue('Biome')
    b = string.format("%s",b:GetFullName())
    local biomesmatch = {
    {pattern = 'BIOME_AzureWeald', result = 'Azure Weald'},
    {pattern = 'BIOME_CrystalCaves', result = 'Crystalline Caverns'},
    {pattern = 'BIOME_SaltCaves', result = 'Salt Pits'},
    {pattern = 'BIOME_FungusBogs', result = "Fungus Bogs"},
    {pattern = 'BIOME_MagmaCaves', result = 'Magma Core'},
    {pattern = 'BIOME_IceCaves', result = 'Glacial Strata'},
    {pattern = 'BIOME_HollowBough', result = 'Hollow Bough'},
    {pattern = 'BIOME_SandblastedCorridors', result = 'Sandblasted Corridors'},
    {pattern = 'BIOME_RadioactiveZone', result = 'Radioactive Exclusion Zone'},
    {pattern = 'BIOME_LushDownpour', result = 'Dense Biozone'}
    }
    for _, obj in ipairs(biomesmatch) do
        if string.find(b, obj.pattern) then
            b = obj.result
            break
        end
    end
    return b
end
function GetCodeName(str) -- Extract CodeName from string of FText value
    local str_parts = Split(str, ',')
    local variables = {} 
    for i = 1, #str_parts do
        local var = string.match(str_parts[i], '"([^"]+)"')
        if var then
            table.insert(variables, var)
        end
    end
    local firstname = variables[6]
    local lastname = variables[9]
    local name = firstname .. " " .. lastname
    return name
end
function GetDeepDiveCodename(t) -- Get DD Codename terminal label widget assets
    local fsdlabelwidgets = FindAllOf('FSDLabelWidget')
    local text = nil
    local name
    if fsdlabelwidgets then
        for index, fsdlabelwidget in pairs(fsdlabelwidgets) do
            local fullname = string.format("%s",fsdlabelwidget:GetFullName())
            if string.find(fullname, 'Data_CodeName') and string.find(fullname, 'Normal') and t == 'Deep Dive Normal' then
                text = fsdlabelwidget:GetPropertyValue('text')
                text = text:ToString()
                name = GetCodeName(text)
                break
            elseif string.find(fullname, 'Data_CodeName') and string.find(fullname, 'Hard') and t == 'Deep Dive Elite' then
                text = fsdlabelwidget:GetPropertyValue('text')
                text = text:ToString()
                name = GetCodeName(text)
                break
            end
        end
        return name
    end
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
    -- Execute the function that 'press any key' evokes
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
    local currentDateTime = os.date("!%Y-%m-%dT%H:%M:%SZ")
    currentDateTime = 'DD_'..currentDateTime
    -- Initialize Table
    local master = {}
    master[currentDateTime] = {}
    master[currentDateTime]['Deep Dive Normal'] = {}
    master[currentDateTime]['Deep Dive Elite'] = {}
    master[currentDateTime]['Deep Dive Normal']['Stages'] = {}
    master[currentDateTime]['Deep Dive Elite']['Stages'] = {}
    -- Get GeneratedMission UObjects
    local missions = GetMissions()
    local MissionStructure = nil
    local t = nil
    local b = nil
    if missions then
        for index, mission in pairs(missions) do
            -- Check if Mission is a DD Stage or not
            MissionStructure = mission:GetPropertyValue("MissionStructure")
            if MissionStructure == 1 then
                t = 'Deep Dive Normal'
                if not HasKey(master[currentDateTime][t], 'Biome') then
                    b = GetBiome(mission)
                    master[currentDateTime][t]['Biome'] = b
                end
                if not HasKey(master[currentDateTime][t], 'CodeName') then
                    -- local codename = GetDeepDiveCodename(t) -- NEED TO WAIT FOR RE-UE4SS LUA API FIX BEFORE CODENAMES CAN BE FETCHED
                    local codename = ' '
                    master[currentDateTime][t]['CodeName'] = codename
                end
                UnpackDeepDiveMission(mission, master, currentDateTime, t)
            elseif MissionStructure == 2 then
                t = 'Deep Dive Elite'
                if not HasKey(master[currentDateTime][t], 'Biome') then
                    b = GetBiome(mission)
                    master[currentDateTime][t]['Biome'] = b
                end
                if not HasKey(master[currentDateTime][t], 'CodeName') then
                    -- local codename = GetDeepDiveCodename(t) -- NEED TO WAIT FOR RE-UE4SS LUA API FIX BEFORE CODENAMES CAN BE FETCHED
                    local codename = ' ' 
                    master[currentDateTime][t]['CodeName'] = codename
                end
                UnpackDeepDiveMission(mission, master, currentDateTime, t)
            end
        end
        -- local indent = "    "
        -- local master_str = TableToString(master, indent)
        -- print(master_str)

        -- Press X to json
        local options = {
            indent = "  ",
          }
        master = json.encode(master, options)        
        local file = io.open('drgmissions.json', 'w')
        if file then
            file:write(master)
            file:close()
        end
        -- Get the current instance of the Escape Menu (This doesn't actually really load the menu)
        local playercontrollers = FindAllOf('BP_PlayerController_SpaceRig_C')
        if playercontrollers then
            for index, playercontroller in pairs(playercontrollers) do
                playercontroller = playercontroller
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
end
Main()