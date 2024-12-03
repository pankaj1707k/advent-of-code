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

-- split string using either regex or plain text
local function split(input, sep, plain)
  local result = {}
  local from = 1
  local sep_from, sep_to = string.find(input, sep, from, plain)
  while sep_from do
    if sep_from ~= 1 then
      table.insert(result, string.sub(input, from, sep_from - 1))
    end
    from = sep_to + 1
    sep_from, sep_to = string.find(input, sep, from, plain)
  end
  if from <= #input then
    table.insert(result, string.sub(input, from))
  end
  return result
end

local function eval(exp)
  local one, two = string.match(exp, '%((%d+),(%d+)%)')
  return tonumber(one) * tonumber(two)
end

local function main()
  local result = 0
  local file = read_input_file('input.txt')
  local text = file:read('*a')
  for _, section in pairs(split(text, 'do()', true)) do
    local s, _ = string.find(section, "don't()", 0, true)
    if s == nil then
      s = section:len()
    end
    for mul in section:sub(1, s):gmatch('mul%(%d+,%d+%)') do
      result = result + eval(mul)
    end
  end
  file:close()

  print(result)
end

main()
