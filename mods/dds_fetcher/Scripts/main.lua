local json = require("./mods/long_term_mission_data_collector/Scripts/dkjson")
local utils = require('./mods/long_term_mission_data_collector/Scripts/bulkmissions_funcs')
function UnpackDeepDiveMission(mission, master, t)
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
    local MissionDNA = mission:GetPropertyValue("MissionDNA")
    MissionDNA = string.format("%s",MissionDNA:GetFullName())

    -- Complexity and Length finalization
    if length == 'Indefinite' then
        local twolength_objs = {
            "On-Site Refining",
            "Industrial Sabotage",
        }
        for _, obj in pairs(twolength_objs) do
            if obj == PrimaryObjective then
                length = '2'
                break
            end
        end
    end
    mission1['Length'] = length
    -- Salvage DNA
    -- local SalvageDNAs = {
    --     {pattern = 'SalvageFractured_Complex', result = {length = '3', complexity = '3'}},
    --     {pattern = 'SalvageFractured_Medium', result = {length = '2', complexity = '2'}},
    -- }
    -- for _, pattern in pairs(SalvageDNAs) do
    --     if string.find(MissionDNA, pattern.pattern) and complexity == 'Indefinite' and length == 'Indefinite' then
    --         mission1['Length'] = pattern.result.length
    --         mission1['Complexity'] = pattern.result.complexity
    --         break
    --     end
    -- end
    if string.find(MissionDNA, "SalvageFractured_Complex") and complexity == 'Indefinite' and length == 'Indefinite' then
        mission1['Complexity'] = '3'
        mission1['Length'] = '3'
    end
    if string.find(MissionDNA, 'SalvageFractured_Medium') and complexity == 'Indefinite' and length == 'Indefinite' then
        mission1['Complexity'] = '2'
        mission1['Length'] = '2'
    end

    -- Refinery DNA
    -- local RefineryDNAs = {
    --     {pattern = 'Refinery_Complex', result = {length = '2', complexity = '3'}},
    --     {pattern = 'Refinery_Medium_C', result = {length = '2', complexity = '2'}},
    -- }
    -- for _, pattern in pairs(RefineryDNAs) do
    --     if string.find(MissionDNA, pattern.pattern) and complexity == 'Indefinite' and length == 'Indefinite' then
    --         mission1['Length'] = pattern.result.length
    --         mission1['Complexity'] = pattern.result.complexity
    --         break
    --     end
    -- end
    if string.find(MissionDNA, 'Refinery_Complex') and complexity == 'Indefinite' and length == 'Indefinite' then
        mission1['Complexity'] = '3'
        mission1['Length'] = '2'
    end
    if string.find(MissionDNA, 'Refinery_Medium_C') and complexity == 'Indefinite' and length == 'Indefinite' then
        mission1['Complexity'] = '2'
        mission1['Length'] = '2'
    end
    if string.find(MissionDNA, 'Refinery_Medium_C') and mission1['Complexity'] == 'Indefinite' then
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
    -- Mining Expedition DNA
    -- local MiningExpeditionDNAs = {
    --     {pattern = 'DNA_2_01_C', result = {length = '1', complexity = '1'}},
    --     {pattern = 'DNA_2_02_C', result = {length = '2', complexity = '2'}},
    --     {pattern = 'DNA_2_03_C', result = {length = '2', complexity = '1'}},
    --     {pattern = 'DNA_2_04_C', result = {length = '3', complexity = '2'}},
    --     {pattern = 'DNA_2_05_C', result = {length = '3', complexity = '3'}},
    -- }
    -- for _, pattern in pairs(MiningExpeditionDNAs) do
    --     if string.find(MissionDNA, pattern.pattern) and complexity == 'Indefinite' and length == 'Indefinite' then
    --         mission1['Length'] = pattern.result.length
    --         mission1['Complexity'] = pattern.result.complexity
    --         break
    --     end
    -- end
    if string.find(MissionDNA, 'DNA_2_01_C') and complexity == 'Indefinite' and length == '1' and PrimaryObjective == 'Mining Expedition' then
        mission1['Complexity'] = '1'
        mission1['Length'] = '1'
    end
    if string.find(MissionDNA, 'DNA_2_02_C') and complexity == 'Indefinite' and length == '2' then
        mission1['Complexity'] = '2'
    end
    if string.find(MissionDNA, 'DNA_2_02_C') and complexity == '2' and length == 'Indefinite' then
        mission1['Length'] = '2'
    end
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
    if string.find(MissionDNA, 'DNA_2_03_C') and complexity == 'Indefinite' and length == '2' then
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
    if string.find(MissionDNA, 'Fractured_Medium_C') and PrimaryObjective == 'Egg Hunt' and length == '2' and complexity == 'Indefinite' then
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
    -- Point Extraction DNA
    if string.find(MissionDNA, 'Motherlode_Short_C') and PrimaryObjective == 'Point Extraction' and length == 'Indefinite' and complexity == 'Indefinite' then
        mission1['Complexity'] = '3'
        mission1['Length'] = '2'
    end
    if string.find(MissionDNA, 'Motherlode_Short_C') and PrimaryObjective == 'Point Extraction' and length == '2' and complexity == 'Indefinite' then
        mission1['Complexity'] = '3'
        mission1['Length'] = '2'
    end
    if string.find(MissionDNA, 'Motherlode_Long_C') and PrimaryObjective == 'Point Extraction' and length == 'Indefinite' and complexity == 'Indefinite' then
        mission1['Complexity'] = '3'
        mission1['Length'] = '3'
    end
    -- Generic DNA
    -- local GenericDNAs = {
    --     {pattern = 'MediumComplex', result = {length = '2', complexity = '3'}},
    --     {pattern = 'LongAverage', result = {length = '3', complexity = '2'}},
    --     {pattern = 'LongComplex', result = {length = '3', complexity = '3'}},
    --     {pattern = 'MediumAverage', result = {length = '2', complexity = '2'}},
    -- }
    -- for _, pattern in pairs(GenericDNAs) do
    --     if string.find(MissionDNA, pattern.pattern) and complexity == 'Indefinite' then
    --         mission1['Length'] = pattern.result.length
    --         mission1['Complexity'] = pattern.result.complexity
    --         break
    --     end
    -- end
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
    if startmenus then
        for index, startmenu in pairs(startmenus) do
            startmenu:PressStart()
        end
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
    local currentDateTime = os.date("!%Y-%m-%dT%H-%M-%SZ")
    currentDateTime = 'DD_'..currentDateTime
    -- Initialize Table
    local master = {}
    master['Deep Dives'] = {}
    master['Deep Dives']['Deep Dive Normal'] = {}
    master['Deep Dives']['Deep Dive Elite'] = {}
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
                if not utils.HasKey(master['Deep Dives'][t], 'Biome') then
                    b = utils.GetBiome(mission)
                    master['Deep Dives'][t]['Biome'] = b
                end
                if not utils.HasKey(master['Deep Dives'][t], 'CodeName') then
                    local codename = GetDeepDiveCodename(t)
                    master['Deep Dives'][t]['CodeName'] = codename
                end
                UnpackDeepDiveMission(mission, master, t)

            elseif MissionStructure == 2 then
                t = 'Deep Dive Elite'
                if not utils.HasKey(master['Deep Dives'][t], 'Biome') then
                    b = utils.GetBiome(mission)
                    master['Deep Dives'][t]['Biome'] = b
                end
                if not utils.HasKey(master['Deep Dives'][t], 'CodeName') then
                    local codename = GetDeepDiveCodename(t)
                    master['Deep Dives'][t]['CodeName'] = codename
                end
                UnpackDeepDiveMission(mission, master, t)

            end
        end

        -- Press X to json
        master = json.encode(master)
        local file = io.open(currentDateTime..'.json', 'w')
        if file then
            file:write(master)
            file:close()
        end
        
        utils.Exit()
    end
end
Main()