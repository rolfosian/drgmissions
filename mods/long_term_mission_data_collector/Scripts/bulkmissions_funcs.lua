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
function GetMissions()--(desired_season)
    local remotemissions = nil
    local missions = {}

    local MissionGenerationManagers = FindAllOf('MissionGenerationManager')
    if MissionGenerationManagers then
        for index, manager in pairs(MissionGenerationManagers) do
            local fullname = string.format("%s",manager:GetFullName())
            if fullname == 'MissionGenerationManager /Script/FSD.Default__MissionGenerationManager' then goto continue end
            -- if desired_season == 's0' then
            --     S4Off()
                remotemissions = manager:GetAvailableMissions()
            -- elseif desired_season == 's4' then
            --     S4On()
                -- remotemissions = manager:GetAvailableMissions()
                -- if HasOptedOutSeasonContent() then
                --     remotemissions = manager:GetAvailableMissionsWithSeasonContentCheck(false)
                -- else
                --     remotemissions = manager:GetAvailableMissionsWithSeasonContentCheck(true)
                -- end
            -- end
            if remotemissions then
                for index, remotemission in pairs(remotemissions) do
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
    missionscount = missionscount + 1
    local mission1 = {}
    mission1['id'] = missionscount
    local MissionName = mission:GetPropertyValue("MissionName")
    MissionName = MissionName:ToString()
    mission1['CodeName'] = MissionName
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
        mission1['MissionWarnings'] = {MissionWarning1, MissionWarning2}
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

    -- COMPLEXITY AND LENGTH FINALIZATION FOR INDEFINITE VALUES
    local MissionDNA = mission:GetPropertyValue("MissionDNA")
    MissionDNA = string.format("%s",MissionDNA:GetFullName())
    -- Salvage DNA
    if string.find(MissionDNA, "SalvageFractured_Complex") and complexity == 'Indefinite' and length == 'Indefinite' then
        mission1['Complexity'] = '3'
        mission1['Length'] = '3'
    end
    if string.find(MissionDNA, 'SalvageFractured_Medium') and complexity == 'Indefinite' and length == 'Indefinite' then
        mission1['Complexity'] = '2'
        mission1['Length'] = '2'
    end
    -- Point Extraction DNA
    if string.find(MissionDNA, 'Motherlode_Short_C') and PrimaryObjective == 'Point Extraction' and length == 'Indefinite' and complexity == 'Indefinite' then
        mission1['Complexity'] = '3'
        mission1['Length'] = '2'
    end
    if string.find(MissionDNA, 'Motherlode_Long_C') and PrimaryObjective == 'Point Extraction' and length == 'Indefinite' and complexity == 'Indefinite' then
        mission1['Complexity'] = '3'
        mission1['Length'] = '3'
    end
    -- Refinery DNA
    if string.find(MissionDNA, 'Refinery_Complex') and complexity == 'Indefinite' and length == 'Indefinite' then
        mission1['Complexity'] = '3'
        mission1['Length'] = '2'
    end
    if string.find(MissionDNA, 'Refinery_Medium_C') and complexity == 'Indefinite' and length == 'Indefinite' then
        mission1['Complexity'] = '2'
        mission1['Length'] = '2'
    end
    -- Mining Expedition DNA
    if string.find(MissionDNA, 'DNA_2_01_C') and complexity == 'Indefinite' and length == 'Indefinite' and PrimaryObjective == 'Mining Expedition' then
        mission1['Complexity'] = '1'
        mission1['Length'] = '1'
    end
    if string.find(MissionDNA, 'DNA_2_02_C') and complexity == 'Indefinite' and length == 'Indefinite' and PrimaryObjective == 'Mining Expedition' then
        mission1['Complexity'] = '2'
        mission1['Length'] = '2'
    end
    if string.find(MissionDNA, 'DNA_2_03_C') and complexity == 'Indefinite' and length == 'Indefinite' then
        mission1['Complexity'] = '1'
        mission1['Length'] = '2'
    end
    if string.find(MissionDNA, 'DNA_2_04_C') and complexity == 'Indefinite' and length == 'Indefinite' and PrimaryObjective == 'Mining Expedition' then
        mission1['Complexity'] = '2'
        mission1['Length'] = '3'
    end
    if string.find(MissionDNA, 'DNA_2_05_C') and complexity == 'Indefinite' and length == 'Indefinite' then
        mission1['Complexity'] = '3'
        mission1['Length'] = '3'
    end
    -- Egg Hunt DNA
    if string.find(MissionDNA, '_Complex') and complexity == 'Indefinite' and length == 'Indefinite' and PrimaryObjective == 'Egg Hunt' then
        mission1['Length'] = '3'
        mission1['Complexity'] = '2'
        complexity = '2'
    end
    if string.find(MissionDNA, 'Fractured_Medium_C') and PrimaryObjective == 'Egg Hunt' and length == 'Indefinite' and complexity == 'Indefinite' then
        mission1['Length'] = '2'
        mission1['Complexity'] = '2'
    end 
    if string.find(MissionDNA, 'FracturedSimple_C') and PrimaryObjective == 'Egg Hunt' then
        mission1['Complexity'] = '1'
        mission1['Length'] = '1'
    end
    -- Elimination DNA
    if string.find(MissionDNA, 'Star_Medium_C') and PrimaryObjective == 'Elimination' then
        mission1['Complexity'] = '2'
        mission1['Length'] = '2'
    end
    if string.find(MissionDNA, 'Star_Complex_C') and PrimaryObjective == 'Elimination' then
        mission1['Complexity'] = '3'
        mission1['Length'] = '3' 
    end
    -- Generic finalization
    if string.find(MissionDNA, 'MediumComplex') and complexity == 'Indefinite' then
        mission1['Length'] = '2'
        mission1['Complexity'] = '3'
    end
    if string.find(MissionDNA, 'LongAverage') and complexity == 'Indefinite' then
        mission1['Length'] = '3'
        mission1['Complexity'] = '2'
    end
    if string.find(MissionDNA, 'LongComplex') and complexity == 'Indefinite' then
        mission1['Length'] = '3'
        mission1['Complexity'] = '3'
    end
    if string.find(MissionDNA, 'MediumAverage') and complexity == 'Indefinite' then
        mission1['Length'] = '2'
        mission1['Complexity'] = '2'
    end
    if string.find(MissionDNA, 'Simple') and complexity == 'Indefinite' then
        mission1['Complexity'] = '1'
    end
    if string.find(MissionDNA, '_Complex') and complexity == 'Indefinite' then
        mission1['Complexity'] = '3'
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
    ReverseDateFormat = ReverseDateFormat,
    IncrementDatetime = IncrementDatetime, 
    TableToString = TableToString, 
    Split = Split, 
    HasKey = HasKey, 
    UnpackStandardMission = UnpackStandardMission,
    GetBiome = GetBiome,
    Exit = Exit,
    GetMissions = GetMissions
}