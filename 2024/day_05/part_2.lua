-- https://adventofcode.com/2024/day/5

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

local function find_in_table(tab, target)
  for i = 1, #tab do
    if tab[i] == target then
      return i
    end
  end
  return 0
end

local function get_ordered_update(input, ordering)
  for i = 1, #input do
    if ordering[input[i]] == nil then
      goto continue
    end
    for _, val in pairs(ordering[input[i]]) do
      local k = find_in_table(input, val)
      if k ~= 0 and i > k then
        local ival = table.remove(input, k)
        table.insert(input, ival)
        return get_ordered_update(input, ordering)
      end
    end
    ::continue::
  end
  return input
end

local function main()
  local result = 0
  local ordering = {} -- { key -> { all values that should come after key } }
  local updates = {} -- list of updates

  local file = read_input_file('input.txt')
  local change = false
  for line in file:lines() do
    if change then
      table.insert(updates, split(line, ',', true))
    elseif line == '' then
      change = true
    else
      local t = split(line, '|', true)
      if ordering[t[1]] == nil then
        ordering[t[1]] = { t[2] }
      else
        table.insert(ordering[t[1]], t[2])
      end
    end
  end
  file:close()

  local incorrect = {}

  for _, update in pairs(updates) do
    local is_valid = true
    for i = 1, #update do
      if ordering[update[i]] == nil then
        goto continue
      end
      for _, val in pairs(ordering[update[i]]) do
        local k = find_in_table(update, val)
        if k ~= 0 and i > k then
          is_valid = false
          break
        end
      end
      ::continue::
    end
    if not is_valid then
      table.insert(incorrect, update)
    end
  end

  for i = 1, #incorrect do
    local correct = get_ordered_update(incorrect[i], ordering)
    result = result + correct[math.ceil(#correct / 2)]
  end

  print(result)
end

main()
