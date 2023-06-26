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
  local startmenus = nil
  local currytime = nil

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

function Main()
    -- Get current UTC Time
    local firstdate = os.date("!*t")
    local current_time = os.time(firstdate)
    --Set target date
    local target_date = os.time{year=2023, month=6, day=14, hour=0, min=0, sec=0}
    -- Calculate the difference in seconds between the current UTC time and the target date
    local diff_seconds = os.difftime(target_date, current_time)



    
    local fullname = nil
    local dailydeals = FindAllOf('_MENU_Trading_C')
    if dailydeals then
        for index, dailydeal in pairs(dailydeals) do
            fullname = string.format("%s",dailydeal:GetFullName())
            if fullname == '_MENU_Trading_C /Game/UI/Menu_Trading/_MENU_Trading.Default___MENU_Trading_C' then goto continue end
            dailydeal = dailydeal:GetPropertyValue('WND_DailyDeal')
            dailydeal = dailydeal:GetPropertyValue('CurrDeal')
            local dtype = dailydeal:type()
            print(dtype) -- UScriptStruct
            -- dailydeal = dailydeal:__index('Resource') -- Crashes
            -- dailydeal = dailydeal:__index('GemResourceData') -- Crashes
            -- dailydeal = dailydeal:__index('DealType') -- Crashes
            -- dailydeal = dailydeal:__index('Credits') -- Crashes
            -- dailydeal = dailydeal:__index('ChangePercent') -- Crashes

            -- I'm sure these ones aren't anywhere near supposed to be working but I tried anyway to exhaust options
            -- dailydeal = dailydeal:__index('CurrDeal') -- Crashes
            -- dailydeal = dailydeal:__index('WND_Trading_DailyDeal_C:CurrDeal') -- Crashes
            -- dailydeal = dailydeal:__index('StructProperty /Game/UI/Menu_Trading/WND_Trading_DailyDeal.WND_Trading_DailyDeal_C:CurrDeal') -- Crashes
            ::continue::
        end
    end
end