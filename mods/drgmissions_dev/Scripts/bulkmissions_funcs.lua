function CreatePollFile(filename)
    while true do
        local success, error = pcall(function()
            local file = io.open(filename, 'w')
            if file then
                file:close()
            end
        end
        )
        if success then
            return
        end
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
function IsTableEmpty(t)
    return next(t) == nil
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
function IncrementDatetimeOneDay(datetime)
    local year, month, day, hour, min, sec = datetime:match("(%d+)-(%d+)-(%d+) (%d+):(%d+):(%d+)")
    year, month, day, hour, min, sec = tonumber(year), tonumber(month), tonumber(day), tonumber(hour), tonumber(min), tonumber(sec)
    hour = hour + 24
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
    local updatedDatetime = string.format("%4d-%02d-%02d %02d:%02d:%02d", year, month, day, hour, min, sec)
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
function Endswith(str, ending)
    return ending == "" or str:sub(-#ending) == ending
end
function Strip(s)
    return (s:gsub("^%s*(.-)%s*$", "%1"))
end
function HasKey(table, key)
    return table[key] ~= nil
end
function TableIndexExists(table, index)
    return table[index] ~= nil
end
MissionGenerationManager = FindFirstOf('MissionGenerationManager')
MapKeys = {
    [0] = 0,
    [1] = 1,
    [2] = 1,
    [3] = 3,
    [4] = 3,
    [5] = 5
}
function GetSeedTable(Season, RandomSeed)
    local NewSeed = {
        RandomSeed = RandomSeed,
        Season = Season,
        MapKey = MapKeys[Season]
    }
    return NewSeed
end
function GetMissions_(Season, RandomSeed)
    local Missions = {}
    local Missions_ = MissionGenerationManager:GetMissions(GetSeedTable(Season, RandomSeed))
    for _, m in pairs(Missions_) do
        table.insert(Missions, m:get())
    end
    return Missions
end
PrimaryObjectives = {
 ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_1st_PointExtraction.OBJ_1st_PointExtraction_C'] = 'Point Extraction',
 ['BlueprintGeneratedClass /Game/GameElements/Objectives/Elimination/OBJ_Eliminate_Eggs.OBJ_Eliminate_Eggs_C'] = 'Elimination',
 ['BlueprintGeneratedClass /Game/GameElements/Objectives/Escort/OBJ_1st_Escort.OBJ_1st_Escort_C'] = 'Escort Duty',
 ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_1st_Extraction.OBJ_1st_Extraction_C'] = 'Mining Expedition',
 ['BlueprintGeneratedClass /Game/GameElements/Objectives/Refinery/OBJ_1st_Refinery.OBJ_1st_Refinery_C'] = 'On-Site Refining',
 ['BlueprintGeneratedClass /Game/GameElements/Objectives/Salvage/OBJ_1st_Salvage.OBJ_1st_Salvage_C'] = 'Salvage Operation',
 ['BlueprintGeneratedClass /Game/GameElements/Objectives/Facility/OBJ_1st_Facility.OBJ_1st_Facility_C'] = 'Industrial Sabotage',
 ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_1st_Gather_AlienEggs.OBJ_1st_Gather_AlienEggs_C'] = 'Egg Hunt',
 ['BlueprintGeneratedClass /Game/GameElements/Objectives/DeepScan/OBJ_1st_DeepScan.OBJ_1st_DeepScan_C'] = 'Deep Scan'
}
function GetPrimaryObj(fullname)
    return PrimaryObjectives[fullname]
end
SecondaryObjectives = {
    ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_2nd_KillFleas.OBJ_2nd_KillFleas_C'] = 'Fester Fleas',
    ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_2nd_Mine_Dystrum.OBJ_2nd_Mine_Dystrum_C'] = 'Dystrum',
    ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_2nd_Mine_Hollomite.OBJ_2nd_Mine_Hollomite_C'] = 'Hollomite',
    ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_2nd_Find_Gunkseed.OBJ_2nd_Find_Gunkseed_C'] = 'Gunk Seeds',
    ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_2nd_Find_Fossil.OBJ_2nd_Find_Fossil_C'] = 'Fossils',
    ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_2nd_Find_Ebonut.OBJ_2nd_Find_Ebonut_C'] = 'Ebonuts',
    ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_2nd_Find_BooloCap.OBJ_2nd_Find_BooloCap_C'] = 'Boolo Caps',
    ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_2nd_Find_ApocaBloom.OBJ_2nd_Find_ApocaBloom_C'] = 'ApocaBlooms',
    ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_2nd_DestroyBhaBarnacles.OBJ_2nd_DestroyBhaBarnacles_C'] = 'Exterminate Bha Barnacles',
    ['BlueprintGeneratedClass /Game/GameElements/Objectives/OBJ_2nd_DestroyEggs.OBJ_2nd_DestroyEggs_C'] = 'Exterminate Glyphid Eggs'
}
function GetSecondaryObj(fullname)
    return SecondaryObjectives[fullname]
end
MissionMutators = {
    ['MissionMutator /Game/GameElements/Missions/Warnings/ExplosiveEnemies/MMUT_ExplosiveEnemies.MMUT_ExplosiveEnemies'] = 'Volatile Guts',
    ['MissionMutator /Game/GameElements/Missions/Mutators/XXXP/MMUT_XXXP.MMUT_XXXP'] = 'Double XP',
    ['MissionMutator /Game/GameElements/Missions/Mutators/Weakspot/MMUT_Weakspot.MMUT_Weakspot'] = 'Critical Weakness',
    ['MissionMutator /Game/GameElements/Missions/Mutators/RichInMinerals/MMUT_RichInMinerals.MMUT_RichInMinerals'] = 'Mineral Mania',
    ['MissionMutator /Game/GameElements/Missions/Mutators/OxygenRich/MMUT_OxygenRich.MMUT_OxygenRich'] = 'Rich Atmosphere',
    ['MissionMutator /Game/GameElements/Missions/Mutators/LowGravity/MMUT_LowGravity.MMUT_LowGravity'] = 'Low Gravity',
    ['MissionMutator /Game/GameElements/Missions/Mutators/GoldRush/MMUT_GoldRush.MMUT_GoldRush'] = 'Gold Rush',
    ['MissionMutator /Game/GameElements/Missions/Mutators/EliminationContract/MMUT_ExterminationContract.MMUT_ExterminationContract'] = 'Golden Bugs',
    ['MissionMutator /Game/GameElements/Missions/Mutators/BloodSugar/MMUT_BloodSugar.MMUT_BloodSugar'] = 'Blood Sugar',
    ['MissionMutator /Game/GameElements/Missions/Mutators/SecretSecondary/MMUT_SecretSecondary.MMUT_SecretSecondary'] = 'Secret Secondary'
}
function GetMissionMutator(fullname)
    return MissionMutators[fullname]
end
Warnings = {
    ['MissionWarning /Game/GameElements/Missions/Warnings/ShieldDisruption/WRN_NoShields.WRN_NoShields'] = 'Shield Disruption',
    ['MissionWarning /Game/GameElements/Missions/Warnings/Swarmageddon/WRN_Swarmagedon.WRN_Swarmagedon'] = 'Swarmageddon',
    ['MissionWarning /Game/GameElements/Missions/Warnings/RivalIncursion/WRN_RivalIncursion.WRN_RivalIncursion'] = 'Rival Presence',
    ['MissionWarning /Game/GameElements/Missions/Warnings/RegenerativeEnemies/WRN_RegenerativeEnemies.WRN_RegenerativeEnemies'] = 'Regenerative Bugs',
    ['MissionWarning /Game/GameElements/Missions/Warnings/Plague/WRN_Plague.WRN_Plague'] = 'Lithophage Outbreak',
    ['MissionWarning /Game/GameElements/Missions/Warnings/NoOxygen/WRN_NoOxygen.WRN_NoOxygen'] = 'Low Oxygen',
    ['MissionWarning /Game/GameElements/Missions/Warnings/MacteraCave/WRN_MacteraCave.WRN_MacteraCave'] = 'Mactera Plague',
    ['MissionWarning /Game/GameElements/Missions/Warnings/LethalEnemies/WRN_LethalEnemies.WRN_LethalEnemies'] = 'Lethal Enemies',
    ['MissionWarning /Game/GameElements/Missions/Warnings/InfestedEnemies/WRN_InfestedEnemies.WRN_InfestedEnemies'] = 'Parasites',
    ['MissionWarning /Game/GameElements/Missions/Warnings/HeroEnemies/WRN_HeroEnemies.WRN_HeroEnemies'] = 'Elite Threat',
    ['MissionWarning /Game/GameElements/Missions/Warnings/Ghost/WRN_Ghost.WRN_Ghost'] = 'Haunted Cave',
    ['MissionWarning /Game/GameElements/Missions/Warnings/ExploderInfestation/WRN_ExploderInfestation.WRN_ExploderInfestation'] = 'Exploder Infestation',
    ['MissionWarning /Game/GameElements/Missions/Warnings/CaveLeechDen/WRN_CaveLeechDen.WRN_CaveLeechDen'] = 'Cave Leech Cluster',
    ['MissionWarning /Game/GameElements/Missions/Warnings/BulletHell/WRN_BulletHell.WRN_BulletHell'] = 'Duck and Cover',
    ['MissionWarning /Game/GameElements/Missions/Warnings/RockInfestation/WRN_RockInfestation.WRN_RockInfestation'] = 'Ebonite Outbreak',
    ['MissionWarning /Game/GameElements/Missions/Warnings/TougherEnemies/WRN_TougherEnemies.TougherEnemies'] = 'Tougher Enemies',
}
function GetMissionWarning(fullname)
    return Warnings[fullname]
end
DurationLimits = {
    ['nil'] = 'Indefinite',
    ['MissionDuration /Game/GameElements/Missions/MissionDescription/MD_Duration_Short.MD_Duration_Short'] = '1',
    ['MissionDuration /Game/GameElements/Missions/MissionDescription/MD_Duration_Normal.MD_Duration_Normal'] = '2',
    ['MissionDuration /Game/GameElements/Missions/MissionDescription/MD_Duration_Long.MD_Duration_Long'] = 'Indefinite'
}
function GetInitialLength(fullname)
    return DurationLimits[fullname]
end
ComplexityLimits = {
    ['nil'] = 'Indefinite',
    ['MissionComplexity /Game/GameElements/Missions/MissionDescription/MD_Complexity_Simple.MD_Complexity_Simple'] = '1',
    ['MissionComplexity /Game/GameElements/Missions/MissionDescription/MD_Complexity_Average.MD_Complexity_Average'] = '2',
    ['MissionComplexity /Game/GameElements/Missions/MissionDescription/MD_Complexity_Complex.MD_Complexity_Complex'] = '3'
}
function GetInitialComplexity(fullname)
    return ComplexityLimits[fullname]
end
MissionDNAs = {
    -- Salvage
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_SalvageFractured_Complex.DNA_SalvageFractured_Complex_C'] = {complexity = '3', length = '3'},
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_SalvageFractured_Medium.DNA_SalvageFractured_Medium_C'] = {complexity = '2', length = '2'},

    -- Point Extraction
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_Motherlode_Short.DNA_Motherlode_Short_C'] = {complexity = '3', length = '2'},
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_Motherlode_Long.DNA_Motherlode_Long_C'] = {complexity = '3', length = '3'},

    -- Refinery
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_Refinery_Complex.DNA_Refinery_Complex_C'] = {complexity = '3', length = '2'},
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_Refinery_Medium.DNA_Refinery_Medium_C'] = {complexity = '2', length = '2'},

    -- Mining Expedition
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_2_01.DNA_2_01_C'] = {complexity = '1', length = '1'},
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_2_02.DNA_2_02_C'] = {complexity = '2', length = '2'},
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_2_03.DNA_2_03_C'] = {complexity = '1', length = '2'},
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_2_04.DNA_2_04_C'] = {complexity = '2', length = '3'},
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_2_05.DNA_2_05_C'] = {complexity = '3', length = '3'},

    --Deep Scan
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_Web_Medium.DNA_Web_Medium_C'] = {complexity = '3', length='2'},
    ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_Web_Small.DNA_Web_Small_C'] = {complexity = '2', length='1'}
}
MissionDNAs_obscure = {
    ['Egg Hunt'] = {
        ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_Fractured_Medium.DNA_Fractured_Medium_C'] = {complexity = '2', length = '2'},
        ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_FracturedSimple.DNA_FracturedSimple_C'] = {complexity = '1', length = '1'},
    },

    ['Elimination'] = {
        ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_Star_Medium.DNA_Star_Medium_C'] = {complexity = '2', length = '2'},
        ['BlueprintGeneratedClass /Game/GameElements/Missions/DNA_Star_Complex.DNA_Star_Complex_C'] = {complexity = '3', length = '3'},
    },
}
Pe_length_condition = {pattern = 'Motherlode_Short_C', result = {complexity = '3', length = '2'}, conditions = {length = '2', complexity = 'Indefinite'}}

function FinalizeComplexityAndLength(mission1, MissionDNA, length, complexity)
    if mission1['PrimaryObjective'] == 'Point Extraction' and string.find(MissionDNA, Pe_length_condition.pattern) and complexity == Pe_length_condition.conditions.complexity and length == Pe_length_condition.conditions.length then
        mission1['Complexity'] = Pe_length_condition.result.complexity
        mission1['Length'] = Pe_length_condition.result.length

    elseif complexity == 'Indefinite' and length == 'Indefinite' then
        pcall(function()
            mission1['Complexity'] = MissionDNAs[MissionDNA].complexity
            mission1['Length'] = MissionDNAs[MissionDNA].length
        end)
    end

    if mission1['PrimaryObjective'] == 'Egg Hunt' and mission1['Complexity'] == 'Indefinite' and mission1['Length'] == 'Indefinite' then
        local complexity_gate_dna = {pattern = '_Complex', result = {complexity = '2', length = '3'}}
        if string.find(MissionDNA, complexity_gate_dna.pattern) then
            mission1['Complexity'] = complexity_gate_dna.result.complexity
            mission1['Length'] = complexity_gate_dna.result.length
            complexity = '2'
        else
            mission1['Complexity'] = MissionDNAs_obscure['Egg Hunt'][MissionDNA].complexity
            mission1['Length'] = MissionDNAs_obscure['Egg Hunt'][MissionDNA].length
        end

    elseif mission1['PrimaryObjective'] == 'Elimination' and mission1['Complexity'] == 'Indefinite' and mission1['Length'] == 'Indefinite' then
        mission1['Complexity'] = MissionDNAs_obscure['Elimination'][MissionDNA].complexity
        mission1['Length'] = MissionDNAs_obscure['Elimination'][MissionDNA].length
    end

    if complexity == 'Indefinite' then
        local MissionDNAs_generic = {
            {pattern = 'MediumComplex', result = {complexity = '3', length = '2'}},
            {pattern = 'LongAverage', result = {complexity = '2', length = '3'}},
            {pattern = 'LongComplex', result = {complexity = '3', length = '3'}},
            {pattern = 'MediumAverage', result = {complexity = '2', length = '2'}},
            {pattern = 'Simple', result =  {complexity = '1', length = mission1['Length']}},
            {pattern = '_Complex', result = {complexity = '3', length = mission1['Length']}}
        }
        for _, dna in pairs(MissionDNAs_generic) do
            if string.find(MissionDNA, dna.pattern) then
                mission1['Length'] = dna.result.length
                mission1['Complexity'] = dna.result.complexity
                break
            end
        end
    end
    return mission1
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
    
    -- print(PrimaryObjective)
    mission1['PrimaryObjective'] = GetPrimaryObj(PrimaryObjective)
    _L.PrimaryObjective = PrimaryObjective

    local SecondaryObjective = mission:GetPropertyValue("SecondaryObjectives")[1]
    SecondaryObjective = string.format("%s",SecondaryObjective:GetFullName())
    SecondaryObjective = GetSecondaryObj(SecondaryObjective)

    _L.SecondaryObjective = SecondaryObjective
    mission1['SecondaryObjective'] = SecondaryObjective

    local MissionWarnings = mission:GetPropertyValue("MissionWarnings")
    local num_MissionWarnings = MissionWarnings:GetArrayNum()
    if num_MissionWarnings == 0 then
        mission1['MissionWarnings'] = nil

    elseif num_MissionWarnings == 1 then
        local MissionWarning1 = MissionWarnings[1]:GetFullName()
        MissionWarning1 = GetMissionWarning(MissionWarning1)

        _L.MissionWarnings = {MissionWarning1}
        mission1['MissionWarnings'] = _L.MissionWarnings
    elseif num_MissionWarnings == 2 then
        local MissionWarning1 = MissionWarnings[1]:GetFullName()
        MissionWarning1 = GetMissionWarning(MissionWarning1)

        -- print(MissionWarning1)
        local MissionWarning2 = MissionWarnings[2]:GetFullName()
        MissionWarning2 = GetMissionWarning(MissionWarning2)
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
            MissionMutator = GetMissionMutator(MissionMutator)
            mission1['MissionMutator'] = MissionMutator
            -- print(MissionMutator)
            _L.MissionMutator = MissionMutator
        end
    end

    local ComplexityLimit = mission:GetPropertyValue("ComplexityLimit")
    ComplexityLimit = string.format("%s",ComplexityLimit:GetFullName())
    local complexity = GetInitialComplexity(ComplexityLimit)
    _L.complexity = complexity
    mission1['Complexity'] = complexity

    local DurationLimit = mission:GetPropertyValue("DurationLimit")
    DurationLimit =  string.format("%s",DurationLimit:GetFullName())
    local length = GetInitialLength(DurationLimit)
    _L.length = length
    mission1['Length'] = length

    if complexity == 'Indefinite' or length == 'Indefinite' then
        local MissionDNA = mission:GetPropertyValue("MissionDNA")
        MissionDNA = string.format("%s",MissionDNA:GetFullName())
        mission1 = FinalizeComplexityAndLength(mission1, MissionDNA, length, complexity)
    end

    if mission1['Length'] == 'Indefinite' or mission1['Complexity'] == 'Indefinite' then
        mission1['debug'] = {
        dna = mission:GetPropertyValue("MissionDNA"):GetFullName(),
        ComplexityLimit = ComplexityLimit,
        DurationLimit = DurationLimit
        }
    end
    
    table.insert(master[season]['Biomes'][b], mission1)
    return missionscount
end
function BiomesTable()
    return {
        ['Crystalline Caverns'] = {},
        ['Glacial Strata'] = {},
        ['Radioactive Exclusion Zone'] = {},
        ['Fungus Bogs'] = {},
        ['Dense Biozone'] = {},
        ['Salt Pits'] = {},
        ['Sandblasted Corridors'] = {},
        ['Magma Core'] = {},
        ['Azure Weald'] = {},
        ['Hollow Bough'] = {}
    }
end
Biomesmatch = {
    ['Biome /Game/Landscape/Biomes/Biomes_Ingame/AzureWeald/BIOME_AzureWeald.BIOME_AzureWeald'] = 'Azure Weald',
    ['Biome /Game/Landscape/Biomes/Biomes_Ingame/CrystalCaves/BIOME_CrystalCaves.BIOME_CrystalCaves'] = 'Crystalline Caverns',
    ['Biome /Game/Landscape/Biomes/Biomes_Ingame/SaltCaves/BIOME_SaltCaves.BIOME_SaltCaves'] = 'Salt Pits',
    ['Biome /Game/Landscape/Biomes/Biomes_Ingame/FungusBogs/BIOME_FungusBogs.BIOME_FungusBogs'] = "Fungus Bogs",
    ['Biome /Game/Landscape/Biomes/Biomes_Ingame/MagmaCaves/BIOME_MagmaCaves.BIOME_MagmaCaves'] = 'Magma Core',
    ['Biome /Game/Landscape/Biomes/Biomes_Ingame/IceCaves/BIOME_IceCaves.BIOME_IceCaves'] = 'Glacial Strata',
    ['Biome /Game/Landscape/Biomes/Biomes_Ingame/HollowBough/BIOME_HollowBough.BIOME_HollowBough'] = 'Hollow Bough',
    ['Biome /Game/Landscape/Biomes/Biomes_Ingame/SandblastedCorridors/BIOME_SandblastedCorridors.BIOME_SandblastedCorridors'] = 'Sandblasted Corridors',
    ['Biome /Game/Landscape/Biomes/Biomes_Ingame/RadioactiveZone/BIOME_RadioactiveZone.BIOME_RadioactiveZone'] = 'Radioactive Exclusion Zone',
    ['Biome /Game/Landscape/Biomes/Biomes_Ingame/LushDownpour/BIOME_LushDownpour.BIOME_LushDownpour'] = 'Dense Biozone'
}
function GetBiome(mission)
    local b = mission:GetPropertyValue('Biome')
    b = string.format("%s",b:GetFullName())
    return Biomesmatch[b]
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

function GetDNAValues(mission)
    local dna = mission:GetPropertyValue("MissionDNA"):GetFullName()
    local PrimaryObjective = GetPrimaryObj(mission:GetPropertyValue('PrimaryObjective'):GetFullName())
    return {dna, PrimaryObjective}
end

return {
    GetDNAValues = GetDNAValues,
    IsInTable = IsInTable,
    IsTableEmpty = IsTableEmpty,
    ReverseDateFormat = ReverseDateFormat,
    IncrementDatetime = IncrementDatetime,
    IncrementDatetimeOneDay = IncrementDatetimeOneDay,
    TableToString = TableToString,
    Split = Split,
    HasKey = HasKey,
    UnpackStandardMission = UnpackStandardMission,
    BiomesTable = BiomesTable,
    GetBiome = GetBiome,
    Exit = Exit,
    GetMissions = GetMissions_,
    CreatePollFile = CreatePollFile,
    Strip = Strip
}