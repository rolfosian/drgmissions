local currentTime = os.date("*t")
local day = currentTime.day
function GetBASEBiomesTable()    
    local widget_trees = FindAllOf("ITM_MisSel_Biome_C")
    local biomes = {}
    if not widget_trees then
        return nil
    else
        for key, widget_tree in pairs(widget_trees) do
            local widget_tree_fullname = string.format("%s",widget_tree:GetFullName())
            if widget_tree_fullname == "ITM_MisSel_Biome_C /Game/UI/Menu_MissionSelectionMK3/_SCREEN_MissionSelectionMK3._SCREEN_MissionSelectionMK3_C:WidgetTree.ITEM_Biome_AzureWeald" then goto continue end
            if widget_tree_fullname == "ITM_MisSel_Biome_C /Game/UI/Menu_MissionSelectionMK3/_SCREEN_MissionSelectionMK3._SCREEN_MissionSelectionMK3_C:WidgetTree.ITEM_Biome_Crystal" then goto continue end
            if widget_tree_fullname == "ITM_MisSel_Biome_C /Game/UI/Menu_MissionSelectionMK3/_SCREEN_MissionSelectionMK3._SCREEN_MissionSelectionMK3_C:WidgetTree.ITEM_Biome_Dense" then goto continue end
            if widget_tree_fullname == "ITM_MisSel_Biome_C /Game/UI/Menu_MissionSelectionMK3/_SCREEN_MissionSelectionMK3._SCREEN_MissionSelectionMK3_C:WidgetTree.ITEM_Biome_Fungus" then goto continue end
            if widget_tree_fullname == "ITM_MisSel_Biome_C /Game/UI/Menu_MissionSelectionMK3/_SCREEN_MissionSelectionMK3._SCREEN_MissionSelectionMK3_C:WidgetTree.ITEM_Biome_Glacial" then goto continue end
            if widget_tree_fullname == "ITM_MisSel_Biome_C /Game/UI/Menu_MissionSelectionMK3/_SCREEN_MissionSelectionMK3._SCREEN_MissionSelectionMK3_C:WidgetTree.ITEM_Biome_HollowBough" then goto continue end
            if widget_tree_fullname == "ITM_MisSel_Biome_C /Game/UI/Menu_MissionSelectionMK3/_SCREEN_MissionSelectionMK3._SCREEN_MissionSelectionMK3_C:WidgetTree.ITEM_Biome_Magma" then goto continue end
            if widget_tree_fullname == "ITM_MisSel_Biome_C /Game/UI/Menu_MissionSelectionMK3/_SCREEN_MissionSelectionMK3._SCREEN_MissionSelectionMK3_C:WidgetTree.ITEM_Biome_Radioactive" then goto continue end
            if widget_tree_fullname == "ITM_MisSel_Biome_C /Game/UI/Menu_MissionSelectionMK3/_SCREEN_MissionSelectionMK3._SCREEN_MissionSelectionMK3_C:WidgetTree.ITEM_Biome_Salt" then goto continue end
            if widget_tree_fullname == "ITM_MisSel_Biome_C /Game/UI/Menu_MissionSelectionMK3/_SCREEN_MissionSelectionMK3._SCREEN_MissionSelectionMK3_C:WidgetTree.ITEM_Biome_Sandblasted" then goto continue end
            if string.find(widget_tree_fullname, "ITEM_Biome_AzureWeald") then biomes['Azure Weald'] = widget_tree goto continue end
            if string.find(widget_tree_fullname, "ITEM_Biome_Crystal") then biomes['Crystalline Caverns'] = widget_tree goto continue end
            if string.find(widget_tree_fullname, "ITEM_Biome_Dense") then biomes['Dense Biozone'] = widget_tree goto continue end
            if string.find(widget_tree_fullname, "ITEM_Biome_Fungus") then biomes['Fungus Bogs'] = widget_tree goto continue end
            if string.find(widget_tree_fullname, "ITEM_Biome_Glacial") then biomes['Glacial Strata'] = widget_tree goto continue end
            if string.find(widget_tree_fullname, "ITEM_Biome_HollowBough") then biomes['Hollow Bough'] = widget_tree goto continue end
            if string.find(widget_tree_fullname, "ITEM_Biome_Magma") then biomes['Magma Core'] = widget_tree goto continue end
            if string.find(widget_tree_fullname, "ITEM_Biome_Radioactive") then biomes['Radioactive Exclusion Zone'] = widget_tree goto continue end
            if string.find(widget_tree_fullname, "ITEM_Biome_Salt") then biomes['Salt Pits'] = widget_tree goto continue end
            if string.find(widget_tree_fullname, "ITEM_Biome_Sandblasted") then biomes['Sandblasted Corridors'] = widget_tree goto continue end
            ::continue::
        end
    end
    return biomes
end
function Extract_MissionsArrays_from_BASE(biomes)
    for biome, widget_tree in pairs(biomes) do
        local missions = widget_tree:GetPropertyValue("missions")
        biomes[biome] = missions
    end
    return biomes
end
function Index(num)
    local index = {}
    for i = 1, num do
        if i == 1 then
            index[1] = 0x0
        elseif i == 2 then
            index[2] = 0x8
        elseif i == 3 then
            index[3] = 0x10
        elseif i == 4 then
            index[4] = 0x18
        elseif i == 5 then
            index[5] = 0x20
        end
    end
    return index
end
function Extract_MissionsClasses(biomes)
    for biome, missions in pairs(biomes) do
        local missions1 = {}
        local missions_num = missions:GetArrayNum()
        if missions_num == 0 then
            biomes[biome] = nil
            goto continue end
        local missions_index = Index(missions_num)
        for num, offset in pairs(missions_index) do
            local mission = missions[num]
            table.insert(missions1, mission)
            biomes[biome] = missions1
        end
        ::continue::
    end
    return biomes
end
function UnpackMissionsClasses(biomes)
    for biome, missions in pairs(biomes) do
        local missions1 = {}
        for index, mission in pairs(missions) do
            local mission1 = {}
            local missionfullname = string.format("%s",mission:GetFullName())
            local missionfullname_parts = Split(missionfullname, '_')
            local missionid_string = missionfullname_parts[#missionfullname_parts]
            missionid_string = string.sub(missionid_string, -3)
            local missionid = tonumber(missionid_string)
            mission1['id'] = missionid
            -- local MissionName = mission:GetPropertyValue("MissionName") -- Get FText object
            -- print(MissionName) -- CRASHES
            -- print(MissionName:ToString()) -- RETURNS EMPTY STRING DUE TO BUG IN RE-UE4SS LUA API
            -- MissionName = MissionName:ToString()
            -- MissionName = GetCodeName(MissionName) -- NEED TO WAIT FOR RE-UE4SS LUA API FIX BEFORE CODENAMES CAN BE FETCHED
            mission1['CodeName'] = ' '
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
                complexity = 'Either 2 or 3'
            end
            mission1['Complexity'] = complexity
            local DurationLimit = mission:GetPropertyValue("DurationLimit")
            DurationLimit =  string.format("%s",DurationLimit:GetFullName())
            local length = nil
            if DurationLimit == 'nil' then
                length = 'Either 2 or 3'
            elseif string.find(DurationLimit, 'Duration_Short') then
                length = '1'
            elseif string.find(DurationLimit, 'Duration_Normal') then
                length = '2'
            end
            mission1['Length'] = length
            local MissionDNA = mission:GetPropertyValue("MissionDNA")
            MissionDNA = string.format("%s",MissionDNA:GetFullName())
            if string.find(MissionDNA, '_Complex') and complexity == 'Either 2 or 3' then
                mission1['Complexity'] = '3'
            end
            if string.find(MissionDNA, "SalvageFractured_Complex") and complexity == 'Either 2 or 3' and length == 'Either 2 or 3' then
                mission1['Complexity'] = '3'
                mission1['Length'] = '3'
            end
            if string.find(MissionDNA, 'SalvageFractured_Medium') and complexity == 'Either 2 or 3' and length == 'Either 2 or 3' then
                mission1['Complexity'] = '2'
                mission1['Length'] = '2'
            end
            if string.find(MissionDNA, 'Motherlode_Short_C') and PrimaryObjective == 'Point Extraction' and length == 'Either 2 or 3' and complexity == 'Either 2 or 3' then
                mission1['Complexity'] = '3'
                mission1['Length'] = '2'
            end
            if string.find(MissionDNA, 'Refinery_Complex') and complexity == 'Either 2 or 3' and length == 'Either 2 or 3' then
                mission1['Complexity'] = '3'
                mission1['Length'] = '2'
            end
            if string.find(MissionDNA, 'Refinery_Medium_C') and complexity == 'Either 2 or 3' and length == 'Either 2 or 3' then
                mission1['Complexity'] = '2'
                mission1['Length'] = '2'
            end
            if string.find(MissionDNA, 'Motherlode_Long_C') and length == 'Either 2 or 3' and PrimaryObjective == 'Point Extraction' then
                mission1['Complexity'] = '3'
            end
            if string.find(MissionDNA, 'DNA_2_01_C') and complexity == 'Either 2 or 3' and length == 'Either 2 or 3' and PrimaryObjective == 'Mining Expedition' then
                mission1['Complexity'] = '1'
                mission1['Length'] = '1'
            end
            if string.find(MissionDNA, 'DNA_2_02_C') and complexity == 'Either 2 or 3' and length == 'Either 2 or 3' and PrimaryObjective == 'Mining Expedition' then
                mission1['Complexity'] = '2'
                mission1['Length'] = '2'
            end
            if string.find(MissionDNA, 'DNA_2_03_C') and complexity == 'Either 2 or 3' and length == 'Either 2 or 3' then
                mission1['Complexity'] = '1'
                mission1['Length'] = '2'
            end
            if string.find(MissionDNA, 'DNA_2_04_C') and complexity == 'Either 2 or 3' and length == 'Either 2 or 3' and PrimaryObjective == 'Mining Expedition' then
                mission1['Complexity'] = '2'
                mission1['Length'] = '3'
            end
            if string.find(MissionDNA, 'DNA_2_05_C') and complexity == 'Either 2 or 3' and length == 'Either 2 or 3' then
                mission1['Complexity'] = '3'
                mission1['Length'] = '3'
            end
            if string.find(MissionDNA, 'DNA_Fractured_Complex_C') and complexity == 'Either 2 or 3' and length == 'Either 2 or 3' and PrimaryObjective == 'Egg Hunt' then
                mission1['Length'] = '3'
                mission1['Complexity'] = '3'
            end
            if string.find(MissionDNA, 'Fractured_Medium_C') and PrimaryObjective == 'Egg Hunt' and length == 'Either 2 or 3' and complexity == 'Either 2 or 3' then
                mission1['Length'] = '2'
                mission1['Complexity'] = '2'
            end 
            if string.find(MissionDNA, 'FracturedSimple_C') and PrimaryObjective == 'Egg Hunt' then
                mission1['Complexity'] = '1'
                mission1['Length'] = '1'
            end
            if string.find(MissionDNA, 'Star_Medium_C') and PrimaryObjective == 'Elimination' then
                mission1['Complexity'] = '2'
                mission1['Length'] = '2'
            end
            if string.find(MissionDNA, 'Star_Complex_C') and PrimaryObjective == 'Elimination' then
                mission1['Complexity'] = '3'
                mission1['Length'] = '3' 
            end
            if string.find(MissionDNA, 'Motherlode_Long_C') and PrimaryObjective == 'Point Extraction' and length == 'Either 2 or 3' and complexity == 'Either 2 or 3' then
                mission1['Complexity'] = '3'
                mission1['Length'] = '3'
            end
            if string.find(MissionDNA, 'MediumComplex') and complexity == 'Either 2 or 3' then
                mission1['Length'] = '2'
                mission1['Complexity'] = '3'
            end
            if string.find(MissionDNA, 'LongAverage') and complexity == 'Either 2 or 3' then
                mission1['Length'] = '3'
                mission1['Complexity'] = '2'
            end
            if string.find(MissionDNA, 'LongComplex') and complexity == 'Either 2 or 3' then
                mission1['Length'] = '3'
                mission1['Complexity'] = '3'
            end
            if string.find(MissionDNA, 'MediumAverage') and complexity == 'Either 2 or 3' then
                mission1['Length'] = '2'
                mission1['Complexity'] = '2'
            end
            if string.find(MissionDNA, 'Simple') and complexity == 'Either 2 or 3' then
                mission1['Complexity'] = '1'
            end
            if mission1['Length'] == 'Either 2 or 3' or mission1['Complexity'] == 'Either 2 or 3' then
                mission1['id'] = missionid
            end
            table.insert(missions1, mission1)
            ::continue::
        biomes[biome] = missions1
        end
    end
    return biomes
end
function GetDailyDrink()
    local drinks = FindAllOf("UI_Bar_BackgroundMenu_ItemSpecialBig_C")
    local special = nil
    if drinks then
        for index, drink in pairs(drinks) do
            local drink_fullname = string.format("%s",drink:GetFullName())
            if drink_fullname == "UI_Bar_BackgroundMenu_ItemSpecialBig_C /Game/GameElements/Bar/UI/UI_Bar_BackgroundMenu.UI_Bar_BackgroundMenu_C:WidgetTree.UI_Bar_BackgroundMenu_ItemSpecialBig" then goto continue end
            special = drink
            ::continue::
            end
        end
        if special then
            local drink = special:GetPropertyValue("Drinkable")
            drink = string.format("%s",drink:GetFullName())
            local drinks = {
                {pattern = 'TunnelRat', result = 'Tunnel Rat'},
                {pattern = 'Backbreaker', result = 'Backbreaker Stout'},
                {pattern = 'DarkMorkite', result = 'Dark Morkite'},
                {pattern = 'PotsOGold', result = "Pots O' Gold"},
                {pattern = 'RedRockBlaster', result = 'Red Rock Blaster'},
                {pattern = 'RockyMountain', result = 'Rocky Mountain'},
                {pattern = 'SkullCrusherAle', result = 'Skull Crusher Ale'},
                {pattern = 'SlayerStout', result = 'Slayer Stout'}
            }
            for _, obj in ipairs(drinks) do
                if string.find(drink, obj.pattern) then
                    drink = obj.result
                    break
                end
            end
            return drink
            end
        end
-- function GetDeepDives()
--     local dds1 = FindAllOf("DeepDive")
--     local dds = {}
--     dds['Deep Dive Normal'] = {}
--     dds['Deep Dive Elite'] = {}
--     local biomesmatch = {
--         {pattern = 'BIOME_AzureWeald', result = 'Azure Weald'},
--         {pattern = 'BIOME_CrystalCaves', result = 'Crystalline Caverns'},
--         {pattern = 'BIOME_SaltCaves', result = 'Salt Pits'},
--         {pattern = 'BIOME_FungusBogs', result = "Fungus Bogs"},
--         {pattern = 'BIOME_MagmaCaves', result = 'Magma Core'},
--         {pattern = 'BIOME_IceCaves', result = 'Glacial Strata'},
--         {pattern = 'BIOME_HollowBough', result = 'Hollow Bough'},
--         {pattern = 'BIOME_SandblastedCorridors', result = 'Sandblasted Corridors'},
--         {pattern = 'BIOME_RadioactiveZone', result = 'Radioactive Exclusion Zone'},
--         {pattern = 'BIOME_LushDownPour', result = 'Dense Biozone'},
--     }
--     if dds1 then
--         for index, dd in pairs(dds1) do
--             local dd_fullname = string.format("%s",dd:GetFullName())
--             table.insert(dd)
--         end
--         for index, dd in pairs(dds) do
--             local ddTemplate = dd:GetPropertyValue('Template')
--             local ddTemplate = string.format("%s"ddTemplate:GetFullName())
--             if string.find(ddTemplate, 'DD_Normal') then
--                 local ddbiome = dd:GetPropertyValue('Biome')
--                 local ddbiome = string.format("%s"ddbiome:GetFullName())
--                 for _, obj in ipairs(biomesmatch) do
--                     if string.find(ddbiome, obj.pattern) then
--                         ddbiome = obj.result
--                         break
--                     end
--                 end
--                 dds['Deep Dive Normal']['Biome'] = ddbiome
--                 local ddmissions = dd:GetPropertyValue('missions')
--                 dds['Deep Dive Normal']['Missions'] = {}
--                 for index, mission in ddmissions do
                    
--                 end
                
--             end
            
--         end
--     end
-- end

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

function strip(str)
    return str:match("^%s*(.-)%s*$")
end
function sleep(seconds)
    os.execute("sleep " .. seconds)
end
function Main()
    local indent = ""
    local biomes = nil
    local dailyspecial = nil
    local file = io.open("biomes.txt", "r")
    if file then
        local contents = file:read("*all")
    while true do
        if strip(contents) ~= '' then goto continue end
        biomes = GetBASEBiomesTable()
        if biomes == nil then goto continue end
        dailyspecial = GetDailyDrink()
        for key, value in pairs(biomes) do
            print(string.format("%s\n",value:GetFullName()))
        end
        biomes = Extract_MissionsArrays_from_BASE(biomes)
        biomes = Extract_MissionsClasses(biomes)
        biomes = UnpackMissionsClasses(biomes)
        biomes['Daily Special'] = dailyspecial
        biomes = TableToString(biomes, indent)
        file = io.open("biomes.txt", "w")
        if file then
            file:write(biomes)
        end
        sleep(2)
        ::continue::
    end
end
end

local indent = "    "
local biomes = GetBASEBiomesTable()
if biomes == nil then
    print('no biomes')
else
    for key, value in pairs(biomes) do
        print(string.format("%s\n",value:GetFullName()))
    end
    biomes = Extract_MissionsArrays_from_BASE(biomes)
    biomes = Extract_MissionsClasses(biomes)
    biomes = UnpackMissionsClasses(biomes)
    local dailyspecial = GetDailyDrink()
    biomes['Daily Special'] = dailyspecial
    biomes = TableToString(biomes, indent)
    end