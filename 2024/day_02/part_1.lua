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

local function main()
  local result = 0
  local file = read_input_file()
  for line in file:lines() do
    local t = split(line)
    for i = 1, #t do
      t[i] = tonumber(t[i])
    end

    local is_inc = true
    local is_dec = true
    for i = 2, #t do
      local diff = math.abs(t[i] - t[i - 1])
      is_inc = is_inc and (t[i] > t[i - 1]) and (diff >= 1) and (diff <= 3)
      is_dec = is_dec and (t[i] < t[i - 1]) and (diff >= 1) and (diff <= 3)
    end
    if is_inc or is_dec then
      result = result + 1
    end
  end
  file:close()

  print(result)
end

main()
