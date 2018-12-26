import itertools
from operator import attrgetter, itemgetter

def window(seq, n=2):
    it = iter(seq)
    result = tuple(itertools.islice(it, n))
    if len(result) == n:
        yield result    
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def flatten(l): return [item for sublist in l for item in sublist]

def dijkstra(start, end, game):
  Q = []
  [[Q.append(node) for node in y if not node.wall] for y in game.mapp]

  for node in Q: 
    node.distance = 10000
    node.prev = None

  start.distance = 0
  sst = []

  while len(Q) > 0:
    Q.sort(key=attrgetter('distance'), reverse=True)
    u = Q.pop()
    for v in u.adjacent():
      alt = u.distance + (1000 if v.character else 1)
      if alt < v.distance:
        v.distance = alt
        v.prev = u

  S, u = [], end
  if u.prev or u == start:
    while u:
      S.append(u)
      u = u.prev

  print(S)
  return S

# =======================================================================================
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
    if self.top: perim    = perim + 'T'
    if self.right: perim  = perim + 'R'
    if self.bottom: perim = perim + 'B'
    if self.left: perim   = perim + 'L'
    return cname + ' (' + perim + ')'

  def __repr__(self): 
    pos = self.character.ctype if self.character else "#" if self.wall else "."
    return "{} ({}x{})".format(pos, self.x, self.y)

  def adjacent(self):
    return [c for c in [self.top, self.left, self.right, self.bottom] if c]

  def adjacent_empty(self):
    return [c for c in [self.top, self.left, self.right, self.bottom] if c and c.empty()]


  def empty(self):
    return not self.wall and not self.character

# =======================================================================================
class Character:
  ELF = 'E'
  GOBLIN = 'G'
  ctype = None
  hit_points = 200
  attack_power = 3
  x, y = 0, 0
  node = None

  def __init__(self, ctype, x, y):
    self.ctype = ctype
    self.x = x
    self.y = y

  def __str__(self): return "{} ({}x{})".format(self.ctype, self.x, self.y)
  def __repr__(self): return "{} ({}x{})".format(self.ctype, self.x, self.y)

  def move(self, new):
    self.node.character = None
    new.character = self
    self.x = new.x
    self.y = new.y
    self.node = new

  def die(self):
    self.x = -1
    self.y = -1
    self.node.character = None
    self.node = None

# =======================================================================================
class GameMap:
  mapp = None
  characters = None

  def __init__(self, fname):
    mapp, chars = self.parse_input(fname)
    self.mapp = mapp
    self.characters = chars

  def parse_char(self, c,x,y):
    char = Character('E',x,y) if c == 'E' else Character('G',x,y) if c == 'G' else None
    val = Node(c == '#', x, y, char)
    if char: char.node = val
    return val, char

  def parse_row(self, row, y):
    parsed = [self.parse_char(c, x, y) for x, c in enumerate(row)]
    row, chars = [list(t) for t in zip(*parsed)]
    return row, [c for c in chars if c]
  
  def parse_input(self, fname):
    d = open(fname).read().split('\n')
    chars = [self.parse_row(row, y) for y, row in enumerate(d)]
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

  def remove(self, character):
    print("Removing", character)
    self.characters = [c for c in self.characters if c != character]
    character.die()


# =======================================================================================
def by_read_order(items): return sorted(sorted(items, key=attrgetter('x')), key=attrgetter('y'))
def by_hitpoint(items): return sorted(items, key=attrgetter('hit_points'))
def find_targets(character, game): return [c for c in game.characters if c.ctype != character.ctype]
def adjacent_targets(character, targets): return [t for t in targets if t.node in character.node.adjacent()]

def attack(character, target, game):
  target.hit_points -= character.attack_power
  if target.hit_points <= 0:
    game.remove(target)
  print(character,'hit',target,'with',target.hit_points,'remaining')

def squares_in_range(character, game):
  return flatten([[n for n in c.node.adjacent() if n.empty()] 
   for c in game.characters if c != character and c.ctype != character.ctype])

def reachable_squares(character, squares, game):
  discovered, result = set(), []
  def _r(node, distance):
    discovered.add(node)
    if node in squares:
      result.append(node)
    for v in node.adjacent():
      if not v in discovered and v.empty():
        _r(v, distance+1)
  _r(character.node, 0)
  return result

def try_attack(character, targets):
  adjacent = by_hitpoint(by_read_order(adjacent_targets(character, targets)))
  if len(adjacent) > 0:
    attack(character, adjacent[0], game)
    return True
  return False

def smallest_square_distances(c, lst):
  r = sorted([(v, abs(c.x-v.x)+abs(c.y-v.y)) for v in lst], key=itemgetter(1))
  print(r)
  return by_read_order([v[0] for v in r if v[1] == r[0][1]]) if len(r) > 0 else []

def nearest_node(character, squares, game):
  square = squares[0]
  paths = sorted([(node, len(dijkstra(node, square, game))) 
    for node in character.node.adjacent() if node.empty()], key=itemgetter(1))
  print(character, square, paths)
  sorted_paths = by_read_order([p[0] for p in paths if p[1] == paths[0][1]])
  return sorted_paths[0]

def get_nearest_squares(character, game):
  squares = squares_in_range(character, game)
  reachable = reachable_squares(character, squares, game)
  return smallest_square_distances(character, reachable)

def game_one_pass(character, game):
  targets = find_targets(character, game)

  if len(targets) == 0:
    return False

  if not try_attack(character, targets):
    nearest_squares = get_nearest_squares(character, game)
    if len(nearest_squares) > 0:
      node = nearest_node(character, nearest_squares, game)
      character.move(node)
      try_attack(character, targets)

  return True

def pretty(mapp):
  def p(row):
    return "".join([c.character.ctype if c.character else '#' if c.wall else '.' for c in row])
  for row in mapp: print(p(row))

def hp_left(characters): return sum([c.hit_points for c in characters])

def run_game(game):
  pretty(game.mapp)
  for tick in itertools.count():
    print("-----------------------------")
    print("Round " + str(tick))

    ordering = by_read_order(game.characters)

    for c in ordering:
      if c in game.characters: # In case they die mid for-loop
        cont = game_one_pass(c, game)
      pretty(game.mapp)
    if not cont:
      print(tick, hp_left(game.characters), tick * hp_left(game.characters))
      print([(c, c.hit_points) for c in game.characters])
      return


game = GameMap('15_8.example')

run_game(game)
