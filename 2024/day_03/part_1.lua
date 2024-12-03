-- https://adventofcode.com/2024/day/3

local function read_input_file(filename)
  local dir = debug.getinfo(1, 'S').source:sub(2):match('^(.*)/')
  local file, err
  if dir == nil then
    file, err = io.open(filename)
  else
    file, err = io.open(dir .. '/' .. filename)
  end
  if not file then
    print('input opening failed ' .. err)
    os.exit()
  end
  return file
end

local function eval(exp)
  local one, two = string.match(exp, '%((%d+),(%d+)%)')
  return tonumber(one) * tonumber(two)
end

local function main()
  local result = 0
  local file = read_input_file('input.txt')
  for line in file:lines() do
    for seq in string.gmatch(line, 'mul%(%d+,%d+%)') do
      result = result + eval(seq)
    end
  end
  file:close()

  print(result)
end

main()
