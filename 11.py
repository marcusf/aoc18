S, WIDTH = 4172, 300

def p(x,y,sn): return int(str(((y * (x+10)) + sn) * (x+10))[::-1][2])-5
def sq(x,y,size,grid): return sum([sum(row[x:x+size]) for row in grid[y:y+size]])

grid = [[p(x,y,S) for x in range(1,WIDTH)] for y in range(1, WIDTH)]

# Number One
def part1(grid):
  maxpow = -100000
  maxx,maxy = -100,-100

  for x in range(0,297):
    for y in range(0,297):
      power = sq(x,y,3,grid)
  
      if power > maxpow:
        maxpow = power
        maxx = x
        maxy = y

  print(str(maxx+1)+","+str(maxy+1))

# Number One
def part2(grid):
  maxpow = -100000
  maxx,maxy, maxs = -100,-100, 0

  for size in range(1,300):

    for x in range(0,300-size):
      for y in range(0,300-size):
        power = sq(x,y,size,grid)
    
        if power > maxpow:
          maxpow = power
          maxx = x
          maxy = y
          maxs = size
  
    print(str(size)+": "+str(maxx+1)+","+str(maxy+1)+","+str(maxs)+" ("+str(maxpow)+")")

part2(grid)