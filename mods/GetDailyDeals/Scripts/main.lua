local json = require("./mods/long_term_mission_data_collector/Scripts/dkjson")
local socket = require('./mods/long_term_mission_data_collector/Scripts/x64/socket')

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
function ReverseDateFormat(inputDate)
    local year = inputDate:sub(1, 2)
    local month = inputDate:sub(4, 5)
    local day = inputDate:sub(7, 8)
    
    local reversedDate = day .. "-" .. month .. "-" .. year
    
    return reversedDate
end
function IncrementDatetime(datetime)
    local year, month, day, hour, min, sec = datetime:match("(%d+)-(%d+)-(%d+) (%d+):(%d+):(%d+)")
    year, month, day, hour, min, sec = tonumber(year), tonumber(month), tonumber(day), tonumber(hour), tonumber(min), tonumber(sec)
    day = day + 1
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
  -- Get current UTC Time
  local firstdate = os.date("!*t")
  local timestamp = nil
  local current_time = os.time(firstdate)
  --Set target date
  local target_date = os.time{year=2023, month=6, day=14, hour=0, min=0, sec=0}
  -- Calculate the difference in seconds between the current UTC time and the target date
  local diff_seconds = os.difftime(target_date, current_time)
  -- Calculate total amount of 24 hour increments between current time and the target date
  local total_increments = math.floor(diff_seconds / 86400)
  -- Initialize Table
  local AllTheDeals = {}
  local fullname = nil
  local resource = nil
  local resources = nil
  local resourceamount = nil
  local dealtype = nil
  local credits = nil
  local changepercent = nil
  local DAILYDEAL = nil
  local dailydeal = nil
  local TRADING_DAILYDEALS = nil
  --Get playercontroller
  local playercontroller = nil
  local playercontrollers = FindAllOf('BP_PlayerController_SpaceRig_C')
  if playercontrollers then
      for index, playercontroller1 in pairs(playercontrollers) do
          ---@type ABP_PlayerController_SpaceRig_C
          playercontroller1 = playercontroller1
          fullname = string.format("%s",playercontroller1:GetFullName())
          if fullname == 'BP_PlayerController_SpaceRig_C /Game/Game/SpaceRig/BP_PlayerController_SpaceRig.Default__BP_PlayerController_SpaceRig_C' then goto continue end
          playercontroller = playercontroller1
          break
          ::continue::
      end
  end
  -- Get Trading Window
  local menu = nil
  local menus = FindAllOf('_MENU_Trading_C')
  if menus then
    for index, menu1 in pairs(menus) do
      ---@type U_MENU_Trading_C
      menu1 = menu1
      fullname = string.format("%s",menu1:GetFullName())
      if fullname == '_MENU_Trading_C /Game/UI/Menu_Trading/_MENU_Trading.Default___MENU_Trading_C' then goto continue end
      menu = menu1
      ::continue::
    end
  end
  -- Loop for the increments
  local count = 0
  for i = 1, total_increments do
    timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    --Open Trading Window
    playercontroller:ShowTrading()
    TRADING_DAILYDEALS = FindAllOf('ITM_Trading_DailyDeal_C')
    DAILYDEAL = TRADING_DAILYDEALS[#TRADING_DAILYDEALS]
    dailydeal = {}
    
    -- resource = DAILYDEAL:GetPropertyValue('TextBlock_ResourceName')
    -- resource = resource:GetPropertyValue('Text')
    -- resource = resource:ToString()
    resource = 'NSLOCTEXT("", "69326EE443907E50A01CB2BE667771D3", "Jadiz")' -- PLACEHOLDER
    resource = Split(resource, ',')
    resource = Split(resource[3], '"')
    resource = resource[2]
    --print(resource)
    dailydeal['Resource'] = resource
    
    -- resourceamount = DAILYDEAL:GetPropertyValue('TextBlock_Amount')
    -- resourceamount = resourceamount:GetPropertyValue('Text')
    -- resourceamount = resourceamount:ToString()
    resourceamount = 'LOCGEN_NUMBER_UNGROUPED(167, "")' -- PLACEHOLDER
    resourceamount = Split(resourceamount, '(')
    resourceamount = resourceamount[2]
    resourceamount = string.gsub(resourceamount, ', ""%)', '')
    --print(resourceamount)
    dailydeal['ResourceAmount'] = resourceamount
    
    -- credits = DAILYDEAL:GetPropertyValue('TextBlock_Credits')
    -- credits = credits:GetPropertyValue('Text')
    -- credits = credits:ToString()
    credits = 'LOCGEN_NUMBER_UNGROUPED(13041, "")' -- PLACEHOLDER
    credits = Split(credits, '(')
    credits = credits[2]
    credits = string.gsub(credits, ', ""%)', '')
    -- print(credits)
    dailydeal['Credits'] = credits
    
    -- changepercent = DAILYDEAL:GetPropertyValue('TextBlock_Percent')
    -- changepercent = changepercent:GetPropertyValue('Text')
    -- changepercent = changepercent:ToString()
    changepercent = 'LOCGEN_FORMAT_NAMED(INVTEXT("{Percent}%"), "Percent", LOCGEN_NUMBER_CUSTOM(47.939156f, SetUseGrouping(false).SetMaximumFractionalDigits(0), ""))' -- PLACEHOLDER
    changepercent = Split(changepercent, '(')
    changepercent = changepercent[4]
    changepercent = string.gsub(changepercent, 'f, SetUseGrouping', '')
    -- print(changepercent)
    dailydeal['ChangePercent'] = changepercent
    
    -- dealtype = DAILYDEAL:GetPropertyValue('TexBlock_Sell')
    -- dealtype = dealtype:GetPropertyValue('Text')
    -- dealtype = dealtype:ToString()
    dealtype = 'NSLOCTEXT("", "04A839C2412E77F780A2EC8FC785D617", "Buy")' -- PLACEHOLDER
    dealtype = Split(dealtype, ',')
    dealtype = dealtype[3]
    dealtype = Split(dealtype, '"')
    dealtype = dealtype[2]
    -- print(dealtype)
    dailydeal['DealType'] = dealtype
    socket.sleep(1)
    -- Close Trading Window
    menu:CloseThisWindow()

    AllTheDeals[timestamp] = dailydeal

    --Get 'current' time
    local currytime = os.date("%Y-%m-%d %H:%M:%S")
    local year, month, day, hour, minute, second = currytime:match("(%d+)-(%d+)-(%d+) (%d+):(%d+):(%d+)")
    minute = tonumber(minute)
    -- Set minute to 0
    minute = 0
    -- Set the second to 1
    second = 1
    currytime = string.format("%04d-%02d-%02d %02d:%02d:%02d", year, month, day, hour, minute, second)
    -- Increment currytime forward by 24 hours
    local newtime = IncrementDatetime(currytime)
    newtime = Split(newtime, ' ')
    -- Remove ReverseDateFormat function and just use newtime[1] if your system date format is YY-MM-DD
    local command = 'date '..ReverseDateFormat(newtime[1])..' & time '..newtime[2]
    -- Set time forward 24 hours
    print(command..'\n')
    count = count + 1
    print(tostring(count)..'\n')
    os.execute(command)
    socket.sleep(1.3)
  end
AllTheDeals = json.encode(AllTheDeals)
local file = io.open('drgdailydeals.json', 'w')
if file then
  file:write(AllTheDeals)
  file:close()
end
end
-- Main()





-- local fullname = nil
-- local DailyDealSettings = nil
-- local Classes = FindAllOf('DailyDealSettings')
-- if Classes then
--   for index, settings in pairs(Classes) do
--     ---@type UDailyDealSettings
--     settings = settings
--     local outdeal = settings:GetDailyDealSeed()
--     fullname = string.format("%s",settings:GetFullName())
--     -- DailyDealSettings = class
--     -- local sneed = class:GetCDO()
--     -- fullname = string.format("%s",sneed:GetFullName())
--     -- if fullname == 'Class /Script/FSD.DailyDealSettings' then
--     --   DailyDealSettings = class:GetCDO()
--     --   break
--     -- end
--   end
-- end

-- print(type(DailyDealSettings))

-- local dailydealsettings = 

-- local fullname = nil
-- local resource = nil
-- local resourceamount = nil
-- local dealtype = nil
-- local credits = nil
-- local changepercent = nil
-- local profit = nil
-- -- local playercontrollers = FindAllOf('BP_PlayerController_SpaceRig_C')
-- -- if playercontrollers then
-- --     for index, playercontroller in pairs(playercontrollers) do
-- --         ---@type ABP_PlayerController_SpaceRig_C
-- --         playercontroller = playercontroller
-- --         fullname = string.format("%s",playercontroller:GetFullName())
-- --         if fullname == 'BP_PlayerController_SpaceRig_C /Game/Game/SpaceRig/BP_PlayerController_SpaceRig.Default__BP_PlayerController_SpaceRig_C' then goto continue end
-- --         playercontroller:ShowTrading()
-- --         break
-- --         ::continue::
-- --     end
-- -- end

-- local TRADING_DAILYDEALS = FindAllOf('ITM_Trading_DailyDeal_C')
-- local DAILYDEAL = TRADING_DAILYDEALS[#TRADING_DAILYDEALS]
-- local dailydeal = {}

-- -- resource = DAILYDEAL:GetPropertyValue('TextBlock_ResourceName')
-- -- resource = resource:GetPropertyValue('Text')
-- -- resource = resource:ToString()
-- resource = 'NSLOCTEXT("", "69326EE443907E50A01CB2BE667771D3", "Jadiz")' -- PLACEHOLDER
-- resource = Split(resource, ',')
-- resource = Split(resource[3], '"')
-- resource = resource[2]
-- --print(resource)
-- dailydeal['Resource'] = resource

-- -- resourceamount = DAILYDEAL:GetPropertyValue('TextBlock_Amount')
-- -- resourceamount = resourceamount:GetPropertyValue('Text')
-- -- resourceamount = resourceamount:ToString()
-- resourceamount = 'LOCGEN_NUMBER_UNGROUPED(167, "")' -- PLACEHOLDER
-- resourceamount = Split(resourceamount, '(')
-- resourceamount = resourceamount[2]
-- resourceamount = string.gsub(resourceamount, ', ""%)', '')
-- --print(resourceamount)
-- dailydeal['ResourceAmount'] = resourceamount

-- -- credits = DAILYDEAL:GetPropertyValue('TextBlock_Credits')
-- -- credits = credits:GetPropertyValue('Text')
-- -- credits = credits:ToString()
-- credits = 'LOCGEN_NUMBER_UNGROUPED(13041, "")' -- PLACEHOLDER
-- credits = Split(credits, '(')
-- credits = credits[2]
-- credits = string.gsub(credits, ', ""%)', '')
-- -- print(credits)
-- dailydeal['Credits'] = credits

-- -- changepercent = DAILYDEAL:GetPropertyValue('TextBlock_Percent')
-- -- changepercent = changepercent:GetPropertyValue('Text')
-- -- changepercent = changepercent:ToString()
-- changepercent = 'LOCGEN_FORMAT_NAMED(INVTEXT("{Percent}%"), "Percent", LOCGEN_NUMBER_CUSTOM(47.939156f, SetUseGrouping(false).SetMaximumFractionalDigits(0), ""))' -- PLACEHOLDER
-- changepercent = Split(changepercent, '(')
-- changepercent = changepercent[4]
-- changepercent = string.gsub(changepercent, 'f, SetUseGrouping', '')
-- print(changepercent)
-- dailydeal['ChangePercent'] = changepercent

-- -- dealtype = DAILYDEAL:GetPropertyValue('TexBlock_Sell')
-- -- dealtype = dealtype:GetPropertyValue('Text')
-- -- dealtype = dealtype:ToString()
-- dealtype = 'NSLOCTEXT("", "04A839C2412E77F780A2EC8FC785D617", "Buy")' -- PLACEHOLDER
-- dealtype = Split(dealtype, ',')
-- dealtype = dealtype[3]
-- dealtype = Split(dealtype, '"')
-- dealtype = dealtype[2]
-- -- print(dealtype)
-- dailydeal['DealType'] = dealtype

-- -- local tablestring = TableToString(dailydeal, '  ')
-- -- print(tablestring)

-- -- local options = {
-- --     indent = "  ",
-- -- }
-- -- dailydeal = json.encode(dailydeal, options)
-- -- print(dailydeal)
-- -- local menus = FindAllOf('_MENU_Trading_C')
-- -- if menus then
-- --   for index, menu in pairs(menus) do
-- --     ---@type U_MENU_Trading_C
-- --     menu = menu
-- --     fullname = string.format("%s",menu:GetFullName())
-- --     if fullname == '_MENU_Trading_C /Game/UI/Menu_Trading/_MENU_Trading.Default___MENU_Trading_C' then goto continue end
-- --     menu:CloseThisWindow()
-- --     ::continue::
-- --   end
-- -- end