local json = require("./mods/long_term_mission_data_collector/Scripts/dkjson")
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
  -- Initialize Table
  local DailyDeal = {}
  local fullname = nil
  local resource = nil
  local resourceamount = nil
  local dealtype = nil
  local credits = nil
  local changepercent = nil
  local dailydeals = FindAllOf('_MENU_Trading_C')
  if dailydeals then
      for index, dailydeal in pairs(dailydeals) do
          fullname = string.format("%s",dailydeal:GetFullName())
          if fullname == '_MENU_Trading_C /Game/UI/Menu_Trading/_MENU_Trading.Default___MENU_Trading_C' then goto continue end
          dailydeal = dailydeal:GetPropertyValue('WND_DailyDeal')
          dailydeal = dailydeal:GetPropertyValue('CurrDeal')

          resource = dailydeal.Resource
          DailyDeal['Resource'] = string.format("%s",resource:GetFullName())
          DailyDeal['ResourceAmount'] = dailydeal.ResourceAmount
          DailyDeal['DealType'] = dailydeal.DealType
          DailyDeal['Credits'] =  dailydeal.Credits
          DailyDeal['ChangePercent'] = dailydeal.ChangePercent
          ::continue::
      end
  end

  DailyDeal = json.encode(DailyDeal)
  local file = io.open('drgdailydeal.json', 'w')
  if file then
    file:write(DailyDeal)
    file:close()
  end

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
Main()