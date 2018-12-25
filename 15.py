from itertools import islice

def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result    
    for elem in it:
        result = result[1:] + (elem,)
        yield result

class Node:
  wall = False
  character = None
  top, bottom, left, right = None, None, None, None

  def __init__(self, wall, x, y, character):
    self.wall = wall 
    self.character = character
    self.x = x
    self.y = y

  def __str__(self): 
    cname = self.character.ctype if self.character else "#" if self.wall else "."
    perim = ""
    if self.top: perim = perim + "T"
    if self.right: perim = perim + "R"
    if self.bottom: perim = perim + "B"
    if self.left: perim = perim + "L"
    return cname + " (" + perim + ")"

  def __repr__(self): 
    return self.character.ctype if self.character else "#" if self.wall else "."


class Character:
  ctype = None
  hit_point = 200
  attack_power = 3
  x, y = 0, 0
  node = None

  def __init__(self, ctype, x, y):
    self.ctype = ctype
    self.x = x
    self.y = y

  def __str__(self): return "{} ({}x{})".format(self.ctype, self.x, self.y)
  def __repr__(self): return "{} ({}x{})".format(self.ctype, self.x, self.y)

def parse_char(c,x,y):
  char = Character('E',x,y) if c == 'E' else Character('G',x,y) if c == 'G' else None
  val = Node(c == '#', x, y, char)
  if char: char.node = val

  return val, char

def parse_row(row, y):
  parsed = [parse_char(c, x, y) for x, c in enumerate(row)]
  row, chars = [list(t) for t in zip(*parsed)]
  return row, [c for c in chars if c]

def parse_input(fname):
  d = open(fname).read().split('\n')
  chars = [parse_row(row, y) for y, row in enumerate(d)]
  mapp, characters = [list(t) for t in zip(*chars)]
  characters = [item for sublist in characters for item in sublist]

  for (pr,row,nr) in window(mapp, 3):
    for (pc, col, nc) in window(row, 3):
      if not col.wall:
        if not nc.wall: col.right = nc 
        if not pc.wall: col.left = pc 
        if not pr[col.x].wall: col.top = pr[col.x] 
        if not nr[col.x].wall: col.bottom = nr[col.x] 

  return mapp, characters


mapp, characters = parse_input('15.in')
print(mapp[15][5])
print(characters)
