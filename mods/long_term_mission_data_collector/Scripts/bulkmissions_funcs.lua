function CreatePollFile(filename)
    local file = io.open(filename, 'w')
    if file then
        file:close()
    end
end
function IsInTable(tbl, val)
    for key, value in pairs(tbl) do
        if value == val then
            return true
        end
    end
    return false
end
function ReverseDateFormat(inputDate)
    local oldDate = Split(inputDate, "-")
    local year = oldDate[1]
    local month = oldDate[2]
    local day = oldDate[3]
    
    local reversedDate = day .. "-" .. month .. "-" .. year
    return reversedDate
  end
function IncrementDatetime(datetime)
    local year, month, day, hour, min, sec = datetime:match("(%d+)-(%d+)-(%d+) (%d+):(%d+):(%d+)")
    year, month, day, hour, min, sec = tonumber(year), tonumber(month), tonumber(day), tonumber(hour), tonumber(min), tonumber(sec)
    min = min + 30
    if min > 59 then
      min = min - 60
      hour = hour + 1
    end
    if hour > 23 then
      hour = hour - 24
      day = day + 1
    end
    local daysInMonth = {31,28,31,30,31,30,31,31,30,31,30,31}
    
    if month == 2 and year % 4 == 0 and (year % 100 ~= 0 or year % 400 == 0) then
      daysInMonth[2] = 29
    end
    if day > daysInMonth[month] then
      day = day - daysInMonth[month]
      month = month + 1
    end
    if month > 12 then
      month = month - 12
      year = year + 1
    end
    local updatedDatetime = string.format("%02d-%02d-%02d %02d:%02d:%02d", year % 100, month, day, hour, min, sec)
    return updatedDatetime
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
function HasOptedOutSeasonContent()
    local subsystems = FindAllOf('SeasonsSubsystem')
    local bool = nil
    if subsystems then
        for i, subsystem in pairs(subsystems) do
            local fullname = string.format("%s",subsystem:GetFullName())
            if fullname == 'SeasonsSubsystem /Script/FSD.Default__SeasonsSubsystem' then goto continue end
            bool = subsystem:HasOptedOutOfSeasonContent()
            break
            ::continue::
        end
    end
    return bool
end
function S4Off()
    local subsystems = FindAllOf('SeasonsSubsystem')
    if subsystems then
        for i, subsystem in pairs(subsystems) do
            local fullname = string.format("%s",subsystem:GetFullName())
            if fullname == 'SeasonsSubsystem /Script/FSD.Default__SeasonsSubsystem' then goto continue end
            subsystem:SetHasOptedOutOfSeasonContent(true)
            break
            ::continue::
        end
    end
end
function S4On()
    local subsystems = FindAllOf('SeasonsSubsystem')
    if subsystems then
        for i, subsystem in pairs(subsystems) do
            local fullname = string.format("%s",subsystem:GetFullName())
            if fullname == 'SeasonsSubsystem /Script/FSD.Default__SeasonsSubsystem' then goto continue end
            subsystem:SetHasOptedOutOfSeasonContent(false)
            break
            ::continue::
        end
    end
end
function GetMissions()
    local remotemissions = nil
    local missions = {}

    local MissionGenerationManagers = FindAllOf('MissionGenerationManager')
    if MissionGenerationManagers then
        for index, manager in pairs(MissionGenerationManagers) do
            local fullname = string.format("%s",manager:GetFullName())
            if fullname == 'MissionGenerationManager /Script/FSD.Default__MissionGenerationManager' then goto continue end

            remotemissions = manager:GetAvailableMissions()
            if remotemissions then
                for _, remotemission in pairs(remotemissions) do
                    local mission = remotemission:get()
                    table.insert(missions, mission)
                end
            end
            break
            ::continue::
        end
    end
    return missions
end
function UnpackStandardMission(mission, master, b, missionscount, season)
    _L = {
        MissionName = nil,
        PrimaryObjective = nil,
        SecondaryObjective = nil,
        MissionWarnings = nil,
        MissionMutator = nil,
        complexity = nil,
        length = nil
    }
    missionscount = missionscount + 1
    local mission1 = {}
    mission1['id'] = missionscount

    local MissionName = mission:GetPropertyValue("MissionName")
    _L.MissionName = MissionName:ToString()
    mission1['CodeName'] = _L.MissionName

    local PrimaryObjective = mission:GetPropertyValue("PrimaryObjective")
    PrimaryObjective = string.format("%s",PrimaryObjective:GetFullName())
    _L.PrimaryObjective = PrimaryObjective
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

    local SecondaryObjective = mission:GetPropertyValue("SecondaryObjectives")[1]
    SecondaryObjective = string.format("%s",SecondaryObjective:GetFullName())
    _L.SecondaryObjective = SecondaryObjective
    local secondary_objectives = {
        {pattern = "Gunkseed", result = "Gunk Seeds"},
        {pattern = "Ebonut", result = "Ebonuts"},
        {pattern = "ApocaBloom", result = "ApocaBlooms"},
        {pattern = "BooloCap", result = "Boolo Caps"},
        {pattern = "Fossil", result = "Fossils"},
        {pattern = "Hollomite", result = "Hollomite"},
        {pattern = "KillFleas", result = "Fester Fleas"},
        {pattern = "Dystrum", result = "Dystrum"}
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
        -- print(MissionWarning2)
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
                {pattern = 'ExplosiveEnemies', result = 'Volatile Guts'}
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
            -- print(MissionMutator)
            _L.MissionMutator = MissionMutator
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

    _L.complexity = complexity
    mission1['Complexity'] = complexity

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
    
    _L.length = length
    mission1['Length'] = length

    -- COMPLEXITY AND LENGTH FINALIZATION FOR INDEFINITE VALUES
    local MissionDNA = mission:GetPropertyValue("MissionDNA")
    MissionDNA = string.format("%s",MissionDNA:GetFullName())

    local MissionDNAs = {
        -- Salvage
        {pattern = 'SalvageFractured_Complex', result = {complexity = '3', length = '3'}},
        {pattern = 'SalvageFractured_Medium', result = {complexity = '2', length = '2'}},
        -- Point Extraction
        {pattern = 'Motherlode_Short_C', result = {complexity = '3', length = '2'}},
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

    local pe_length_condition = {pattern = 'Motherlode_Short_C', result = {complexity = '3', length = '2'}, conditions = {length = '2', complexity = 'Indefinite'}}
    if PrimaryObjective == 'Point Extraction' and string.find(MissionDNA, pe_length_condition.pattern) and complexity == pe_length_condition.conditions.complexity and length == pe_length_condition.conditions.length then
        mission1['Complexity'] = pe_length_condition.result.complexity
        mission1['Length'] = pe_length_condition.result.length

    elseif complexity == 'Indefinite' and length == 'Indefinite' then
        for _, dna in pairs(MissionDNAs) do
            if string.find(MissionDNA, dna.pattern) then
                mission1['Complexity'] = dna.result.complexity
                mission1['Length'] = dna.result.length
                break
            end
        end
    end

    local MissionDNAs_obscure = {}
    MissionDNAs_obscure['Egg Hunt'] = {
        {pattern = 'Fractured_Medium_C', result = {complexity = '2', length = '2'}},
        {pattern = 'FracturedSimple_C', result = {complexity = '1', length = '1'}},
        {pattern = 'FracturedSimple_C', result = {complexity = '1', length = '1'}},
    }

    MissionDNAs_obscure['Elimination'] = {
        {pattern = 'Star_Medium_C', result = {complexity = '2', length = '2'}},
        {pattern = 'Star_Complex_C', result = {complexity = '3', length = '3'}},
    }

    if PrimaryObjective == 'Egg Hunt' and mission1['Complexity'] == 'Indefinite' and mission1['Length'] == 'Indefinite' then
        local complexity_gate_dna = {pattern = '_Complex', result = {complexity = '2', length = '3'}}
        if string.find(MissionDNA, complexity_gate_dna.pattern) then
            mission1['Complexity'] = complexity_gate_dna.result.complexity
            mission1['Length'] = complexity_gate_dna.result.length
            complexity = '2'
        else
            for _, dna in pairs(MissionDNAs_obscure[PrimaryObjective]) do
                if string.find(MissionDNA, dna.pattern) then
                    mission1['Complexity'] = dna.result.complexity
                    mission1['Length'] = dna.result.length
                    break
                end
            end
        end

    elseif PrimaryObjective == 'Elimination' and mission1['Complexity'] == 'Indefinite' and mission1['Length'] == 'Indefinite' then
        for _, dna in pairs(MissionDNAs_obscure[PrimaryObjective]) do
            if string.find(MissionDNA, dna.pattern) then
                mission1['Complexity'] = dna.result.complexity
                mission1['Length'] = dna.result.length
                break
            end
        end
    end
    local MissionDNAs_generic = {
        {pattern = 'MediumComplex', result = {complexity = '3', length = '2'}},
        {pattern = 'LongAverage', result = {complexity = '2', length = '3'}},
        {pattern = 'LongComplex', result = {complexity = '3', length = '3'}},
        {pattern = 'MediumAverage', result = {complexity = '2', length = '2'}},
        {pattern = 'Simple', result =  {complexity = '1', length = mission1['Length']}},
        {pattern = '_Complex', result = {complexity = '3', length = mission1['Length']}},
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
    -- if mission1['Length'] == 'Indefinite' or mission1['Complexity'] == 'Indefinite' then
    --     print(missionfullname)
    -- end
    table.insert(master[season]['Biomes'][b], mission1)
    return missionscount
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
function Exit()
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

return {
    IsInTable = IsInTable,
    ReverseDateFormat = ReverseDateFormat,
    IncrementDatetime = IncrementDatetime,
    TableToString = TableToString,
    Split = Split,
    HasKey = HasKey,
    S4Off = S4Off,
    S4On = S4On,
    UnpackStandardMission = UnpackStandardMission,
    GetBiome = GetBiome,
    Exit = Exit,
    GetMissions = GetMissions,
    CreatePollFile = CreatePollFile
}