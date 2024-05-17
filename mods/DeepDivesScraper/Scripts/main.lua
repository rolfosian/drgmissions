local json = require("./mods/BulkMissionsScraper/Scripts/dkjson")
function Split(str, separator)
    local result = {}
    local pattern = string.format("([^%s]+)", separator)
    for match in string.gmatch(str, pattern) do
        table.insert(result, match)
    end
    return result
end
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
function UnpackDeepDiveMission(mission, master, t)
    _L = {
        MissionName = nil,
        PrimaryObjective = nil,
        SecondaryObjective = nil,
        MissionWarnings = nil,
        MissionMutator = nil,
        complexity = nil,
        length = nil
    }
    
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
        {pattern = "Gather_AlienEggs", result = "Egg Hunt"},
        -- {pattern = "DeepScan", result = "Deep Scan"}
    }
    for _, obj in ipairs(primary_objectives) do
        if string.find(PrimaryObjective, obj.pattern) then
            PrimaryObjective = obj.result
            break
        end
    end
    -- print(PrimaryObjective)
    mission1['PrimaryObjective'] = PrimaryObjective
    _L.PrimaryObjective = PrimaryObjective

    local SecondaryObjective = mission:GetPropertyValue("SecondaryObjectives")[1]
    SecondaryObjective = string.format("%s",SecondaryObjective:GetFullName())
    local secondary_objectives = {
        {pattern = "RepairMinimules", result = "Repair Minimules"},
        {pattern = "Elimination_Eggs", result = "Eliminate Dreadnought"},
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
    _L.SecondaryObjective = SecondaryObjective

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
        {pattern = 'InfestedEnemies', result = 'Parasites'},
        -- {pattern = 'DuckAndCover', result = "Duck and Cover"},
        -- {pattern = 'EboniteOutbreak', result = 'Ebonite Outbreak'}
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
        _L.MissionWarnings = {MissionWarning1}
        mission1['MissionWarnings'] = _L.MissionWarnings
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
        _L.MissionWarnings = {MissionWarning1, MissionWarning2}
        mission1['MissionWarnings'] = _L.MissionWarnings
    end

    local MissionMutator = mission:GetPropertyValue("MissionMutator")
    if MissionMutator then 
        MissionMutator = string.format("%s",MissionMutator:GetFullName())
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
                {pattern = 'ExplosiveEnemies', result = 'Volatile Guts'},
                -- {pattern = 'BloodSugar', result = 'Blood Sugar'},
                -- {pattern = 'SecretSecondary', result = 'Secret Secondary'}
            }
            for _, obj in ipairs(mutators) do
                if string.find(MissionMutator, obj.pattern) then
                    MissionMutator = obj.result
                    mission1['MissionMutator'] = MissionMutator
                    break
                end
            end
            _L.MissionMutator = MissionMutator
            -- print(MissionMutator)
        end
    end

    local ComplexityLimit = mission:GetPropertyValue("ComplexityLimit")
    ComplexityLimit = string.format("%s",ComplexityLimit:GetFullName())
    local complexity = nil

    if string.find(ComplexityLimit,'Complexity_Simple') then
        complexity = '1'
    elseif string.find(ComplexityLimit, 'Complexity_Average') then
        complexity = '2'
    elseif string.find(ComplexityLimit, 'Complexity_Complex') then
        complexity = '3'
    elseif string.find(ComplexityLimit, 'nil') then
        complexity = 'Indefinite'
    end

    mission1['Complexity'] = complexity
    _L.complexity = complexity

    local DurationLimit = mission:GetPropertyValue("DurationLimit")
    DurationLimit =  string.format("%s",DurationLimit:GetFullName())
    local length = nil

    if DurationLimit == 'nil' then
        length = 'Indefinite'
    elseif string.find(DurationLimit, 'Duration_Short') then
        length = '1'
    elseif string.find(DurationLimit, 'Duration_Normal') then
        length = '2'
    end

    mission1['Length'] = length
    _L.length = length

    local MissionDNA = mission:GetPropertyValue("MissionDNA")
    MissionDNA = string.format("%s",MissionDNA:GetFullName())

    -- Complexity and Length finalization
    local MissionDNAs = {
        -- Salvage
        {pattern = 'SalvageFractured_Complex', result = {complexity = '3', length = '3'}},
        {pattern = 'SalvageFractured_Medium', result = {complexity = '2', length = '2'}},
        -- Point Extraction
        {pattern = 'Motherlode_Short_C', result = {complexity = '3', length = '3'}},
        {pattern = 'Motherlode_Long_C', result = {complexity = '3', length = '3'}},
        -- Refinery
        {pattern = 'Refinery_Complex', result = {complexity = '3', length = '2'}},
        {pattern = 'Refinery_Medium_C', result = {complexity = '2', length = '2'}},
        -- Mining Expedition
        {pattern = 'DNA_2_01_C', result = {complexity = '1', length = '1'}},
        {pattern = 'DNA_2_02_C', result = {complexity = '2', length = '2'}},
        {pattern = 'DNA_2_03_C', result = {complexity = '1', length = '2'}},
        {pattern = 'DNA_2_04_C', result = {complexity = '2', length = '3'}},
        {pattern = 'DNA_2_05_C', result = {complexity = '3', length = '3'}},
    }
    if complexity == 'Indefinite' and length == 'Indefinite' then
        for _, dna in pairs(MissionDNAs) do
            if string.find(MissionDNA, dna.pattern) then
                mission1['Complexity'] = dna.result.complexity
                mission1['Length'] = dna.result.length
                break
            end
        end
    end
    if PrimaryObjective == "On-Site Refining" and mission1['Complexity'] == 'Indefinite' then
        mission1['Complexity'] = '2'
        mission1['Length'] = '2'
    end

    -- Industrial Sabotage DNA
    if string.find(MissionDNA, 'Facility_Simple_C') and complexity == 'Indefinite' then
        mission1['Complexity'] = '2'
    end
    if string.find(MissionDNA, 'Facility_Simple_C') and length == 'Indefinite' then
        mission1['Length'] = '2'
    end

    if length == 'Indefinite' then
        local twolength_objs = {
            "On-Site Refining",
            "Industrial Sabotage",
        }
        for _, obj in pairs(twolength_objs) do
            if obj == PrimaryObjective then
                length = '2'
                mission1['Length'] = length
                _L.length = length
                break
            end
        end
    end

    -- Mining Expedition finalization
    if PrimaryObjective == 'Mining Expedition' then
        local MissionDNAs_Mining_Expedition = {
            {pattern = 'DNA_2_01_C', result = {complexity = '1', length = '1'}, conditions = {complexity = 'Indefinite', length = '1'}},
            {pattern = 'DNA_2_01_C', result = {complexity = '1', length = '1'}, conditions = {complexity = 'Indefinite', length = 'Indefinite'}},
            {pattern = 'DNA_2_02_C', result = {complexity = '2', length = mission1['Length']}, conditions = {complexity = 'Indefinite', length = '2'}},
            {pattern = 'DNA_2_02_C', result = {complexity = mission1['Complexity'], length = '2'}, conditions = {complexity = '2', length = 'Indefinite'}},
            {pattern = 'DNA_2_02_C', result = {complexity = '2', length = '2'}, conditions = {complexity = 'Indefinite', length = 'Indefinite'}},
            {pattern = 'DNA_2_03_C', result = {complexity = '1', length = '2'}, conditions = {complexity = 'Indefinite', length = 'Indefinite'}},
            {pattern = 'DNA_2_03_C', result = {complexity = '1', length = '2'}, conditions = {complexity = 'Indefinite', length = '2'}},
            {pattern = 'DNA_2_04_C', result = {complexity = '2', length = '3'}, conditions = {complexity = 'Indefinite', length = 'Indefinite'}},
            {pattern = 'DNA_2_05_C', result = {complexity = '3', length = '3'}, conditions = {complexity = 'Indefinite', length = 'Indefinite'}},
        }
        for _, dna in pairs(MissionDNAs_Mining_Expedition) do
            if string.find(MissionDNA, dna.pattern) then
                if dna.conditions.complexity == complexity and dna.conditions.length == length then
                    mission1['Complexity'] = dna.result.complexity
                    mission1['Length'] = dna.result.length
                    break
                end
            end
        end
    end
    -- Egg Hunt
    if PrimaryObjective == 'Egg Hunt' then
        local MissionDNAs_Egg_Hunt = {
            {pattern = '_Complex', result = {complexity = '2', length = '3', load = {variable = 'complexity', value = '2'}}, conditions = {complexity = 'Indefinite', length = 'Indefinite'}},
            {pattern = 'Fractured_Medium_C', result = {complexity = '2', length = '2', load = {variable = 'nil' , value = 'nil'}}, conditions = {complexity = 'Indefinite', length = 'Indefinite'}},
            {pattern = 'Fractured_Medium_C', result = {complexity = '2', length = length, load = {variable = 'nil' , value = 'nil'}}, conditions = {complexity = 'Indefinite', length = '2'}},
        }
        if string.find(MissionDNA, 'FracturedSimple_C') then
            mission1['Complexity'] = '1'
            mission1['Length'] = '1'
            goto skip
        end
        for _, dna in pairs(MissionDNAs_Egg_Hunt) do
            if string.find(MissionDNA, dna.pattern) and dna.conditions.complexity == complexity and dna.conditions.length == length then
                mission1['Complexity'] = dna.result.complexity
                mission1['Length'] = dna.result.length
                _L[dna.result.load.variable] = dna.result.load.value
                break
            end
        end
        ::skip::
        complexity = _L['complexity']
    end

    -- Elimination
    if PrimaryObjective == 'Elimination' then
        local MissionDNAs_Elimination = {
            {pattern = 'Star_Medium_C', result = {complexity = '2', length = '2'}},
            {pattern = 'Star_Complex_C', result = {complexity = '3', length = '3'}},
        }
        for _, dna in pairs(MissionDNAs_Elimination) do
            if string.find(MissionDNA, dna.pattern) then
                mission1['Complexity'] = dna.result.complexity
                mission1['Length'] = dna.result.length
                break
            end
        end
    end
    -- Point Extraction
    if PrimaryObjective == 'Point Extraction' then
        local MissionDNAs_Point_Extraction = {
            {pattern = 'Motherlode_Short_C', result = {complexity = '2', length = '2'}, conditions = {length = 'Indefinite', complexity = 'Indefinite'}},
            {pattern = 'Motherlode_Short_C', result = {complexity = '3', length = '2'}, conditions = {length = '2', complexity = 'Indefinite'}},
            {pattern = 'Motherlode_Long_C', result = {complexity = '3', length = '3'}, conditions = {length = 'Indefinite', complexity = 'Indefinite'}},
        }
        for _, dna in pairs(MissionDNAs_Point_Extraction) do
            if string.find(MissionDNA, dna.pattern) and dna.conditions.length == length and dna.conditions.complexity == complexity then
                mission1['Complexity'] = dna.result.complexity
                mission1['Length'] = dna.result.length
                break
            end
        end
    end
    -- General
    local MissionDNAs_generic = {
        {pattern = 'MediumComplex', result = {complexity = '3', length = '2'}},
        {pattern = 'LongAverage', result = {complexity = '2', length = '3'}},
        {pattern = 'LongComplex', result = {complexity = '3', length = '3'}},
        {pattern = 'MediumAverage', result = {complexity = '2', length = '2'}},
    }
    if complexity == 'Indefinite' then
        for _, dna in pairs(MissionDNAs_generic) do
            if string.find(MissionDNA, dna.pattern) then
                mission1['Length'] = dna.result.length
                mission1['Complexity'] = dna.result.complexity
                break
            end
        end
    end
    local MissionDNAs_generic_complexity_nolength = {
        {pattern = 'Simple', result = '1'},
        {pattern = '_Complex', result = '3'},
    }
    if complexity == 'Indefinite' then
        for _, dna in pairs(MissionDNAs_generic_complexity_nolength) do
            if string.find(MissionDNA, dna.pattern) then
                mission1['Complexity'] = dna.result
            end
        end
    end
    -- if mission1['Length'] == 'Indefinite' or mission1['Complexity'] == 'Indefinite' then
    --     print(missionfullname)
    --     print(TableToString(mission1, "  "))
    -- end
    table.insert(master['Deep Dives'][t]['Stages'], mission1)
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
function GetDeepDiveCodename(t) -- Get DD Codename terminal label widget assets
    local fsdlabelwidgets = FindAllOf('FSDLabelWidget')
    local text = nil
    local name
    if fsdlabelwidgets then
        for index, fsdlabelwidget in pairs(fsdlabelwidgets) do
            local fullname = string.format("%s",fsdlabelwidget:GetFullName())
            if string.find(fullname, 'Data_CodeName') and string.find(fullname, 'Normal') and t == 'Deep Dive Normal' then
                text = fsdlabelwidget:GetPropertyValue('text')
                name = text:ToString()
                break
            elseif string.find(fullname, 'Data_CodeName') and string.find(fullname, 'Hard') and t == 'Deep Dive Elite' then
                text = fsdlabelwidget:GetPropertyValue('text')
                name = text:ToString()
                break
            end
        end
        return name
    end
end
function HasKey(table, key)
    return table[key] ~= nil
end
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
function Main()
    if IsLoaded() then
        goto isloaded
    else
        PressStartAndWaitForLoad()
    end
    ::isloaded::
    -- local utils = require('./mods/BulkMissionsScraper/Scripts/old/bulkmissions_funcs')

    local currentDateTime = os.date("!%Y-%m-%dT%H-%M-%SZ")
    currentDateTime = 'DD_'..currentDateTime
    -- Initialize Table
    local master = {}
    master['Deep Dives'] = {}
    master['Deep Dives']['Deep Dive Normal'] = {}
    master['Deep Dives']['Deep Dive Normal']['CodeName'] = GetDeepDiveCodename('Deep Dive Normal')
    master['Deep Dives']['Deep Dive Elite'] = {}
    master['Deep Dives']['Deep Dive Elite']['CodeName'] = GetDeepDiveCodename('Deep Dive Elite')
    master['Deep Dives']['Deep Dive Normal']['Stages'] = {}
    master['Deep Dives']['Deep Dive Elite']['Stages'] = {}
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
                if not HasKey(master['Deep Dives'][t], 'Biome') then
                    b = GetBiome(mission)
                    master['Deep Dives'][t]['Biome'] = b
                end
                UnpackDeepDiveMission(mission, master, t)

            elseif MissionStructure == 2 then
                t = 'Deep Dive Elite'
                if not HasKey(master['Deep Dives'][t], 'Biome') then
                    b = GetBiome(mission)
                    master['Deep Dives'][t]['Biome'] = b
                end
                UnpackDeepDiveMission(mission, master, t)

            end
        end
        -- Press X to json
        -- master = TableToString(master)
        -- print(master)
        master = json.encode(master, {indent=true})
        local file = io.open(currentDateTime..'.json', 'w')
        if file then
            file:write(master)
            file:close()
        end
        -- utils.Exit()
    end
end
Main()