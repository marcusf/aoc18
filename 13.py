from operator import itemgetter
from collections import deque
import itertools

# Constants. 
up,down,left,right,hp,vp,tl,tr,x='^','v','<','>','-','|','/','\\','+'
ctrl = [up,down,left,right]
UP, DOWN, LEFT, RIGHT=(0,-1), (0,1), (-1,0), (1,0)

def parse_input(fname):
  "Reads a file and gets a clean map (no carts) and a list of carts"
  d = open(fname).read().split('\n')
  mapp = [list(s) for s in d]
  positions = []
  for y, line in enumerate(mapp):
    for x, char in enumerate(line):
      if char in ctrl:
        positions.append(((x,y), char, left, str(x)+','+str(y)))
        line[x] = '|' if char == up or char == down else '-'
  return mapp, positions

def charf(dx, dy):
  "Given a direction, returns the right character"
  if dx==1: return right
  if dx==-1: return left
  if dy==1: return down
  if dy==-1: return up

def progress(cur, car, turn, x, y):
  "Figures out the next state of a cart"
  if cur=='|':
    if car==up:
      return UP
    elif car==down:
      return DOWN
    else:
      print('Unexpected car on vertical pipe', car, cur, x, y)
  elif cur=='-':
    if car==left:
      return LEFT
    elif car==right:
      return RIGHT
    else:
      print('Unexpected car on horizontal pipe', car, cur, x, y)
  elif cur=='/':
    if car==up:
      return RIGHT
    elif car==down:
      return LEFT
    elif car==right:
      return UP
    elif car==left:
      return DOWN
    else:
      print('Unexpected car on turning pipe forward-slash')
  elif cur=='\\':
    if car==up:
      return LEFT
    elif car==down:
      return RIGHT
    elif car==right:
      return DOWN
    elif car==left:
      return UP
    else:
      print('Unexpected car on turning pipe back-slash', car, cur, x, y)
  elif cur=='+':
    if turn==left:
      if car==up: return LEFT
      elif car==down: return RIGHT
      elif car==left: return DOWN
      elif car==right: return UP
    elif turn==right:
      if car==up: return RIGHT
      elif car==down: return LEFT
      elif car==left: return UP
      elif car==right: return DOWN
    else:
      if car==up: return UP
      elif car==down: return DOWN
      elif car==left: return LEFT
      elif car==right: return RIGHT
  elif cur==' ':
    print('Out of bounds', x, y)
  else:
    print('Unknown parsing error', cur)

def collided(target, comparables):
  lst = []
  x1, y1 = target[0]
  for p in comparables:
    x2, y2 = p[0]
    if x1==x2 and y1==y2:
      lst.append(target[3]) # Label
      lst.append(p[3]) # label
  return lst

def get_next(mapp, item):
  "Takes the map and and a cart and iterates it one time"
  position, direction, turn, label = item
  x, y = position
  cur = mapp[y][x]
  dx, dy = progress(cur, direction, turn, x, y)
  next_pos = (x+dx, y+dy)
  next_direction = charf(dx, dy)
  if cur=='+':
    next_turn = vp if turn == left else right if turn == vp else left
  else:
    next_turn = turn
  return (next_pos, next_direction, next_turn, label)

def sort_by_y(lst):
  return sorted(sorted(lst, key=lambda x: x[0][0]), key=lambda x: x[0][1])

def part1(mapp, positions):
  "Find the location of the first collision"
  workset = positions
  for tick in itertools.count():
    workset = deque(sort_by_y(workset))

    for _ in range(len(workset)):
      position = workset.popleft()
      attempt = get_next(mapp, position)
      collisions = collided(attempt, workset)
      if len(collisions) > 0:
        print('Part 1: Collisions at',
          str(attempt[0][0])+','+str(attempt[0][1]))
        return
      workset.append(attempt)


def part2(mapp, positions):
  "Find the last cart standing after all other have collided"
  should_terminate = False

  for tick in itertools.count():

    # Don't break immediately if terminated, since last item
    # not collided is supposed to run free for one.
    if len(positions) <= 1:
      print('Part 2: Last remaining is',
        str(positions[0][0][0])+','+str(positions[0][0][1]))
      return

    workset, did_collide = deque(sort_by_y(positions)), set()

    # Take an item from the front of the queue, update it and
    # put it at the end of the queue, until the entire queue
    # has been updated and checked for collisions.
    for _ in range(len(workset)):
      position = workset.popleft()
      attempt = get_next(mapp, position)
      did_collide.update(collided(attempt, workset))
      workset.append(attempt)

    # Now go through and create a new set of positions from those 
    # not collided during the iteration.
    positions = []
    for position in workset:
      if not position[3] in did_collide:
        positions.append(position)


mapp, positions = parse_input('13.in')

part1(mapp, positions)
part2(mapp, positions)
