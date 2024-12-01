-- https://adventofcode.com/2024/day/1

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
  local list_1 = {}
  local list_2 = {}

  local file = read_input_file()
  for line in file:lines() do
    local t = split(line)
    table.insert(list_1, t[1])
    table.insert(list_2, t[2])
  end
  file:close()

  table.sort(list_1)
  table.sort(list_2)

  local result = 0
  for i = 1, #list_1 do
    local freq = 0
    for j = 1, #list_2 do
      if list_2[j] == list_1[i] then
        freq = freq + 1
      end
    end
    result = result + list_1[i] * freq
  end

  print(result)
end

main()
