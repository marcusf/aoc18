import itertools
import sys
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

def prettyd(mapp):
  def nn(c):
    return hex(c.distance)[2:] if c.distance < 16 else '*'
  def p(row):
    return "".join([nn(c) if not c.wall else '#' for c in row])
  for row in mapp: print(p(row))

def dijkstra(start, ends, game):
  Q = flatten([[node for node in y if node.empty()] for y in game.mapp])

  Q.extend(ends)
  Q.append(start)

  for node in Q: 
    node.distance = 10000
    node.prev = None

  start.distance = 0

  while len(Q) > 0:
    Q.sort(key=attrgetter('distance'), reverse=True)
    u = Q.pop()
    for v in u.adjacent_empty():
    #for v in u.adjacent():
      alt = u.distance + 1
      if alt < v.distance:
        v.distance = alt
        v.prev = u

  result = []
  for end in ends:
    S, u = [], end
    if u.prev or u == start:
      while u:
        S.append(u)
        u = u.prev
    if len(S) > 0:
      result.append((end,S))

  return result

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
    #pos = self.character.ctype if self.character else "#" if self.wall else "."
    return "{}x{}".format(self.x, self.y) #"{} ({}x{})".format(pos, self.x, self.y)

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

  def __init__(self, ctype, x, y, hp=3):
    self.ctype = ctype
    self.x = x
    self.y = y
    self.attack_power = hp

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
  elf_hp = None

  def __init__(self, fname, elf_hp=3):
    self.elf_hp = elf_hp    
    mapp, chars = self.parse_input(fname)
    self.mapp = mapp
    self.characters = chars

  def parse_char(self, c,x,y):
    char = Character(c,x,y, self.elf_hp) if c == 'E' else Character(c,x,y) if c == 'G' else None
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

def squares_in_range(character, game):
  return flatten([[n for n in c.node.adjacent() if n.empty()] 
   for c in game.characters if c != character and c.ctype != character.ctype])

def try_attack(character, targets, game):
  adjacent = by_hitpoint(by_read_order(adjacent_targets(character, targets)))
  if len(adjacent) > 0:
    attack(character, adjacent[0], game)
    return True
  return False

def nearest_node(character, squares, game):
  min_dist, paths, debug = 100000, [], []
  squares = sorted(dijkstra(character.node, squares, game), key=lambda x: len(x[1]))

  if len(squares) == 0:
    return None

  dists = dijkstra(squares[0][0], character.node.adjacent_empty(), game)
  
  for (node, path) in dists:
    dist = len(path)
    if dist < min_dist:
      paths = [node]
      debug = [path]
      min_dist = dist
    elif dist == min_dist:
      paths.append(node)
      debug.append(path)

  sorted_paths = by_read_order(paths)
  return sorted_paths[0]

def squares_for_character(character, game):
  squares = squares_in_range(character, game)
  return squares

def game_one_pass(character, game):
  targets = find_targets(character, game)

  if len(targets) == 0:
    return False

  if not try_attack(character, targets, game):
    squares = squares_for_character(character, game)
    #print("Reachable", character, squares)
    node = nearest_node(character, squares, game)
    if node:
      character.move(node)
      try_attack(character, targets, game)

  return True

def pretty(mapp):
  def p(row):
    return "".join([c.character.ctype if c.character else '#' if c.wall else '.' for c in row])
  for row in mapp: print(p(row))

def hp_left(characters): return sum([c.hit_points for c in characters])

def run_game(game, break_if_elf_dies=False):
  pretty(game.mapp)
  total_elves = len([c for c in game.characters if c.ctype == Character.ELF])
  for tick in itertools.count():
    print("-----------------------------")
    print("Round " + str(tick))

    no_elves = len([c for c in game.characters if c.ctype == Character.ELF])
    no_goblins = len(game.characters) - no_elves

    if break_if_elf_dies and no_elves < total_elves:
      return (tick * hp_left(game.characters), total_elves, no_elves, game.characters)

    if no_elves == 0 or no_goblins == 0:
      cont = False
    else:
      ordering = by_read_order(game.characters)
      for c in ordering:
        if c in game.characters: # In case they die mid for-loop
          #print(c)
          cont = game_one_pass(c, game)
      pretty(game.mapp)
    if not cont:
      print(tick, hp_left(game.characters), tick * hp_left(game.characters))
      score = tick * hp_left(game.characters)
      return (score, total_elves, no_elves, game.characters)

def part1():
  game = GameMap(sys.argv[1])
  run_game(game)

def part2():
  for attack_power in itertools.count(23):
    print("=============================================")
    print("Attack Power:", attack_power)
    game = GameMap(sys.argv[1], attack_power)
    score, total, count, chars = run_game(game, True)
    if total - count == 0:
      print("Attack power from elves is", attack_power)
      print([(c,c.hit_points) for c in chars])
      print("Score is ", score)
      return

part2()

# 209440 too high