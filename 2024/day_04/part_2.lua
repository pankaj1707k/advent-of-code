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

local function primary_diagonal_mas(grid, i, j)
  if
    (i - 1) >= 1
    and (j - 1) >= 1
    and grid[i - 1]:sub(j - 1, j - 1) == 'M'
    and (i + 1) <= #grid
    and (j + 1) <= grid[i]:len()
    and grid[i + 1]:sub(j + 1, j + 1) == 'S'
  then
    return true
  end
  return false
end

local function primary_diagonal_sam(grid, i, j)
  if
    (i - 1) >= 1
    and (j - 1) >= 1
    and grid[i - 1]:sub(j - 1, j - 1) == 'S'
    and (i + 1) <= #grid
    and (j + 1) <= grid[i]:len()
    and grid[i + 1]:sub(j + 1, j + 1) == 'M'
  then
    return true
  end
  return false
end

local function secondary_diagonal_mas(grid, i, j)
  if
    (i - 1) >= 1
    and (j + 1) <= grid[i]:len()
    and grid[i - 1]:sub(j + 1, j + 1) == 'M'
    and (i + 1) <= #grid
    and (j - 1) >= 1
    and grid[i + 1]:sub(j - 1, j - 1) == 'S'
  then
    return true
  end
  return false
end

local function secondary_diagonal_sam(grid, i, j)
  if
    (i - 1) >= 1
    and (j + 1) <= grid[i]:len()
    and grid[i - 1]:sub(j + 1, j + 1) == 'S'
    and (i + 1) <= #grid
    and (j - 1) >= 1
    and grid[i + 1]:sub(j - 1, j - 1) == 'M'
  then
    return true
  end
  return false
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
      if grid[i]:sub(j, j) == 'A' then
        if
          (primary_diagonal_mas(grid, i, j) or primary_diagonal_sam(grid, i, j))
          and (secondary_diagonal_sam(grid, i, j) or secondary_diagonal_mas(grid, i, j))
        then
          result = result + 1
        end
      end
    end
  end

  print(result)
end

main()
