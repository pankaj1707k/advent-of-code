-- https://adventofcode.com/2024/day/6

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

local function find_in_table(tab, target)
  if tab == nil then
    return 0
  end
  for i = 1, #tab do
    if tab[i] == target then
      return i
    end
  end
  return 0
end

local function is_edge(map, row, col)
  return row == 1 or row == #map or col == 1 or col == string.len(map[1])
end

local function main()
  local result = 0
  local map = {}

  local file = read_input_file('input.txt')
  local row, col = nil, nil
  local line_num = 1
  for line in file:lines() do
    table.insert(map, line)
    if row == nil then
      local spos, _ = string.find(line, '^', 1, true)
      if spos ~= nil then
        row = line_num
        col = spos
      end
    end
    line_num = line_num + 1
  end
  file:close()

  local dr, dc = -1, 0
  local visited = {}
  while not is_edge(map, row, col) do
    if find_in_table(visited[row], col) == 0 then
      result = result + 1
      if visited[row] == nil then
        visited[row] = { col }
      else
        table.insert(visited[row], col)
      end
    end
    if map[row + dr]:sub(col + dc, col + dc) == '#' then
      dr, dc = dc, -dr
    end
    row = row + dr
    col = col + dc
  end

  print(result + 1)
end

main()
