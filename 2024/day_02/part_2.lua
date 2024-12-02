-- https://adventofcode.com/2024/day/2

local function read_input_file()
  local dir = debug.getinfo(1, 'S').source:sub(2):match('^(.*)/')
  local file, err
  if dir == nil then
    file, err = io.open('input.txt')
  else
    file, err = io.open(dir .. '/input.txt')
  end
  if not file then
    print('input opening failed ' .. err)
    os.exit()
  end
  return file
end

local function split(input, sep)
  if sep == nil then
    sep = '%s'
  end
  local res = {}
  for str in string.gmatch(input, '([^' .. sep .. ']+)') do
    table.insert(res, str)
  end
  return res
end

local function is_safe(list)
  local is_inc = true
  local is_dec = true
  for i = 2, #list do
    local diff = math.abs(list[i] - list[i - 1])
    is_inc = is_inc and (list[i] > list[i - 1]) and (diff >= 1) and (diff <= 3)
    is_dec = is_dec and (list[i] < list[i - 1]) and (diff >= 1) and (diff <= 3)
  end
  return is_inc or is_dec
end

local function main()
  local result = 0
  local file = read_input_file()
  for line in file:lines() do
    local t = split(line)
    for i = 1, #t do
      t[i] = tonumber(t[i])
    end

    if is_safe(t) then
      result = result + 1
    else
      for i = 1, #t do
        local v = table.remove(t, i)
        if is_safe(t) then
          result = result + 1
          break
        end
        table.insert(t, i, v)
      end
    end
  end
  file:close()

  print(result)
end

main()
