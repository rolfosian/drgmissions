local json = require("./mods/BulkMissionsScraper/Scripts/dkjson")
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
    PressStartAndWaitForLoad()
    
    local utils = require('./mods/BulkMissionsScraper/Scripts/bulkmissions_funcs')
    local total_days = 365
    local DailyDealSettings = FindFirstOf('DailyDealSettings')
    local DailyDeals = {}
    local Seed = nil
    local PreviousSeed = nil
    local currytime = nil
    local newtime = nil
    local count = 0

    local resources = {
      {pattern = 'Jadiz', result = 'Jadiz'},
      {pattern = 'Enor', result = 'Enor Pearl'},
      {pattern = 'Magnite', result = 'Magnite'},
      {pattern = 'Umanite', result = 'Umanite'},
      {pattern = 'Croppa', result = 'Croppa'},
      {pattern = 'Bismor', result = 'Bismor'},
    }
    local dealtypes = {
      [0] = 'Buy',
      [1] = 'Sell'
    }

    utils.CreatePollFile('firstpoll.txt')
    for i = 1, total_days do
    -- Initialize Table
      local DailyDeal = {}
      while true do
          Seed = DailyDealSettings:GetDailyDealSeed()
          if Seed == PreviousSeed then
              print('SEEN') -- never seen, but keeping this just in case
          else
              break
          end
      end
      PreviousSeed = Seed
    
      DailyDealSettings:GetDailyDeal(DailyDeal)

      DailyDeal.Resource = string.format("%s",DailyDeal.Resource:GetFullName())
      for _, tbl in ipairs(resources) do
        if string.find(DailyDeal.Resource, tbl.pattern) then
          DailyDeal.Resource = tbl.result
          break
        end
      end

      DailyDeal.DealType = dealtypes[DailyDeal.DealType]

      local timestamp = os.date("!%Y-%m-%dT00:00:00Z")
      DailyDeals[timestamp] = DailyDeal


      --Get 'current' time
      currytime = os.date("%Y-%m-%d %H:%M:%S")
      local year, month, day, hour, minute, second = currytime:match("(%d+)-(%d+)-(%d+) (%d+):(%d+):(%d+)")

      hour = tonumber(hour)
      hour = 0
      minute = tonumber(minute)
      minute = 0
      second = 1

      currytime = string.format("%04d-%02d-%02d %02d:%02d:%02d", year, month, day, hour, minute, second)

      newtime = utils.IncrementDatetimeOneDay(currytime)
      newtime = utils.Split(newtime, ' ')

      -- Remove ReverseDateFormat function and just use newtime[1] if your system date format is YY-MM-DD
      local command = 'date '..utils.ReverseDateFormat(newtime[1])..' & time '..newtime[2]

      -- Set time forward 30 minutes
      print(command..'\n')
      count = count + 1
      print(tostring(count)..'\n')
      os.execute(command)
      utils.CreatePollFile('poll.txt')
    end

    DailyDeals = json.encode(DailyDeals)
    local file = io.open('drgdailydeals.json', 'w')
    if file then
      file:write(DailyDeals)
      file:close()
    end
end
Main()