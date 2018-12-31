import re
from itertools import count
from PIL import Image, ImageColor

def parse_input(fname):
  grid = [[0 for _ in range(3000)] for _ in range(3000)]
  d = open(fname).read().split('\n')
  maxy, miny, maxx, minx = 0,1000,0,1000
  for row in d:
    # y=1612, x=314..331
    m = re.match(r"([xy])=(\d+), [xy]=(\d+)..(\d+)", row)
    x, p, t0, t1 = m.group(1)=='x', int(m.group(2)), int(m.group(3)), int(m.group(4))
    if x:
      maxx = max(maxx, p)
      for y in range(t0,t1):
        grid[y][p] = 1
        maxy = max(y, maxy)
        miny = min(y, miny)
    else:
      maxy = max(maxy, p)
      for x in range(t0, t1+1):
        grid[p][x] = 1
        maxx = max(x, maxx)
        minx = min(x, minx)
  for i, row in enumerate(grid):
    grid[i] = row[minx-1:maxx+1]
  return (grid[0:maxy+2], maxy, miny, maxx, minx)

def simulate(g):
  #grid[0] = 2
  inp = [[500-minx,0]]

  while len(inp) > 0:
    x,y = inp.pop() 
    while y < len(g) and g[y][x] == 0:
      g[y][x] = 3
      y = y + 1
  
    if y < len(g)-1 and g[y][x] == 1:
      y = y-1
      # Hit a floor
      # Find left and right
      leftmost, rightmost = x, x
      while g[y][leftmost] != 1 and leftmost > 0: leftmost -= 1
      while g[y][rightmost] != 1 and rightmost < len(g[0])-1: rightmost += 1

      while True:
        y = y - 1
        currentleft, currentright = x, x
        while g[y][currentleft] in [0,3] and currentleft > 0: currentleft -= 1
        while g[y][currentright] in [0,3] and currentright < len(g[0])-1: currentright += 1
        if currentleft >= leftmost and currentright <= rightmost:
          for xx in range(currentleft,currentright): 
            if g[y][xx] in [0,3]: g[y][xx] = 2
            i = 1
            while (g[y+i][xx] != 1):
              holes.append((xx,y+i))
              xi = 1
              while (g[y+i][xx-xi] == 0):
                holes.append((xx-xi,y+i))
                xi+=1
              i += 1
        else:
          if currentleft < leftmost:
            leftcliff = leftmost
            inp.append([leftcliff-1,y])
          else:
            leftcliff = max(currentleft,leftmost)+1

          if currentright > rightmost:
            rightcliff = rightmost+1
            inp.append([rightcliff,y])
          else:
            rightcliff = min(currentright,rightmost)

          for xx in range(leftcliff,rightcliff): g[y][xx] = 3
          break

  for x, y in holes:
    if grid[y][x] in [0,3]:
      grid[y][x] = 2

  return

grid, maxy, miny, maxx, minx = parse_input('17.in')

result, holes = [[500-minx, 0]], []

im = Image.new('RGB', (len(grid[0]), len(grid)), 'white')
images = []

frame = im.copy()
images.append(frame)
for y, row in enumerate(grid):
  for x, c in enumerate(row):
    if c == 1:
      frame.putpixel((x,y), (0,0,0))
    elif c==2:
      frame.putpixel((x,y), (100,100,255))
    elif c==3:
      frame.putpixel((x,y), (255,0,0))


simulate(grid)

ctr, ctr2 = 0,0
for y in range(0, maxy):
  for x in range(0, len(grid[0])):
    if grid[y][x] == 2:
      ctr+=1
    elif grid[y][x] == 3:
      ctr2+=1

print("Reached", ctr+ctr2,"squares, of which", ctr,"still")

frame = im.copy()
images.append(frame)
for y, row in enumerate(grid):
  for x, c in enumerate(row):
    if c == 1:
      frame.putpixel((x,y), (0,0,0))
    elif c==2:
      frame.putpixel((x,y), (100,100,255))
    elif c==3:
      frame.putpixel((x,y), (255,0,0))

print("Saving")
images[0].save('test_0.gif',
          save_all=True,
          append_images=images[1:],
          duration=100,
          loop=1)

#lenn = max(lenn, r)
#print(r, lenn)
#print("Number of threads:",len(result))
