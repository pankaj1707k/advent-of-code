-- https://adventofcode.com/2024/day/4

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

local function left(grid, i, j)
  if
    (j - 1) >= 1
    and grid[i]:sub(j - 1, j - 1) == 'M'
    and (j - 2) >= 1
    and grid[i]:sub(j - 2, j - 2) == 'A'
    and (j - 3) >= 1
    and grid[i]:sub(j - 3, j - 3) == 'S'
  then
    return 1
  end
  return 0
end

local function right(grid, i, j)
  if
    (j + 1) <= grid[i]:len()
    and grid[i]:sub(j + 1, j + 1) == 'M'
    and (j + 2) <= grid[i]:len()
    and grid[i]:sub(j + 2, j + 2) == 'A'
    and (j + 3) <= grid[i]:len()
    and grid[i]:sub(j + 3, j + 3) == 'S'
  then
    return 1
  end
  return 0
end

local function up(grid, i, j)
  if
    (i - 1) >= 1
    and grid[i - 1]:sub(j, j) == 'M'
    and (i - 2) >= 1
    and grid[i - 2]:sub(j, j) == 'A'
    and (i - 3) >= 1
    and grid[i - 3]:sub(j, j) == 'S'
  then
    return 1
  end
  return 0
end

local function down(grid, i, j)
  if
    (i + 1) <= #grid
    and grid[i + 1]:sub(j, j) == 'M'
    and (i + 2) <= #grid
    and grid[i + 2]:sub(j, j) == 'A'
    and (i + 3) <= #grid
    and grid[i + 3]:sub(j, j) == 'S'
  then
    return 1
  end
  return 0
end

local function up_left(grid, i, j)
  if
    (i - 1) >= 1
    and (j - 1) >= 1
    and grid[i - 1]:sub(j - 1, j - 1) == 'M'
    and (i - 2) >= 1
    and (j - 2) >= 1
    and grid[i - 2]:sub(j - 2, j - 2) == 'A'
    and (i - 3) >= 1
    and (j - 3) >= 1
    and grid[i - 3]:sub(j - 3, j - 3) == 'S'
  then
    return 1
  end
  return 0
end

local function up_right(grid, i, j)
  if
    (i - 1) >= 1
    and (j + 1) <= grid[i]:len()
    and grid[i - 1]:sub(j + 1, j + 1) == 'M'
    and (i - 2) >= 1
    and (j + 2) <= grid[i]:len()
    and grid[i - 2]:sub(j + 2, j + 2) == 'A'
    and (i - 3) >= 1
    and (j + 3) <= grid[i]:len()
    and grid[i - 3]:sub(j + 3, j + 3) == 'S'
  then
    return 1
  end
  return 0
end

local function down_right(grid, i, j)
  if
    (i + 1) <= #grid
    and (j + 1) <= grid[i]:len()
    and grid[i + 1]:sub(j + 1, j + 1) == 'M'
    and (i + 2) <= #grid
    and (j + 2) <= grid[i]:len()
    and grid[i + 2]:sub(j + 2, j + 2) == 'A'
    and (i + 3) <= #grid
    and (j + 3) <= grid[i]:len()
    and grid[i + 3]:sub(j + 3, j + 3) == 'S'
  then
    return 1
  end
  return 0
end

local function down_left(grid, i, j)
  if
    (i + 1) <= #grid
    and (j - 1) >= 1
    and grid[i + 1]:sub(j - 1, j - 1) == 'M'
    and (i + 2) <= #grid
    and (j - 2) >= 1
    and grid[i + 2]:sub(j - 2, j - 2) == 'A'
    and (i + 3) <= #grid
    and (j - 3) >= 1
    and grid[i + 3]:sub(j - 3, j - 3) == 'S'
  then
    return 1
  end
  return 0
end

local function main()
  local result = 0
  local grid = {}
  local file = read_input_file('input.txt')
  for line in file:lines() do
    table.insert(grid, line)
  end
  file:close()

  for i = 1, #grid do
    for j = 1, grid[i]:len() do
      if grid[i]:sub(j, j) == 'X' then
        result = result
          + left(grid, i, j)
          + right(grid, i, j)
          + up(grid, i, j)
          + down(grid, i, j)
          + up_left(grid, i, j)
          + up_right(grid, i, j)
          + down_right(grid, i, j)
          + down_left(grid, i, j)
      end
    end
  end

  print(result)
end

main()
