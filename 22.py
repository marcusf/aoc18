from collections import namedtuple, defaultdict
from heapq import *

Point = namedtuple('Point', ['x','y'])
Node = namedtuple('Node', ['x','y','t'])

depth = 7740
target = Point(12,763)
start = Point(0,0)

cache = dict()

def gi(x,y):
  global target
  global cache

  if (x,y) == (0,0): v = 0
  elif (x,y) == target: v = 0
  elif y == 0: v = x * 16807
  elif x == 0: v = y * 48271
  else: v = cache[x-1,y] * cache[x,y-1]
  cache[x,y] = el(v)
  return v

def el(gi):
  global depth
  return (gi + depth) % 20183

def tt(el): return ['.','=','|'][el%3]

def t(x,y): return tt(el(gi(x,y)))
def s(x,y): return el(gi(x,y)) % 3

# Pretty
#for y in range(target[1]+6):
#  print("".join([t(x,y) for x in range(target[0]+6)]))
# Part 1
print(sum([(sum([s(x,y) for x in range(target[0]+1)])) for y in range(target[1]+1)]))

# Part 2
def neighbors(coord):
  x,y = coord
  n = {(x+1,y),(x,y+1)}
  if x>0: n.add((x-1,y))
  if y>0: n.add((x,y-1))
  return n

def permissible(x,y):
  tt = t(x,y)
  if tt == '.': return ['c','t']
  if tt == '=': return ['c','n']
  if tt == '|': return ['t','n']

def cost(x,y,t):
  c = permissible(x,y)
  return 1 if t in c else 8

def h(fr,to):
  return abs(to.x-fr.x)+abs(to.y-fr.y)

def straight_cost(fr,to,t):
  c = 0
  dx = int(to.x-fr.x/abs(to.x-fr.x))
  dy = int(to.y-fr.y/abs(to.y-fr.y))
  step = fr
  while step.x != to.x:
    step = Point(step.x+dx,step.y)
    c += cost(step.x,step.y,t)
    if not t in permissible(step.x,step.y):
      t = permissible(step.x,step.y)[0]
  while step.y != to.y:
    step = Point(step.x,step.y+dy)
    c += cost(step.x,step.y,t)
    if not t in permissible(step.x,step.y):
      t = permissible(step.x,step.y)[0]
  return c

def dijkstra(start, ends, nodes, edges):
  #q = list([(10000,n) for n in nodes if n != start])

  cost = defaultdict(lambda: 1000000)
  prev = defaultdict(lambda: None)
  seen = set()

  q = [(0,start)]
  cost[start] = 0

  while q:
    cc, u = heappop(q)
    if u in seen: 
      continue
    seen.add(u)
    for (v,c2) in edges[u]:
      alt = cost[u] + c2
      if alt < cost[v]:
        cost[v] = alt
        prev[v] = u
        heappush(q, (alt, v))

  result = []
  for end in ends:
    S, u = [], end
    if prev[u] or u == start:
      while u:
        S.append((u,cost[u]))
        u = prev[u]
    if S:
      result.append((end,S))

  return result


def find_path():
  nodes, edges = set(), defaultdict(set)
  for y in range(target.y+500):
    for x in range(target.x+100):
      types = permissible(x,y)
      for t in types:
        node = Node(x,y,t)
        if x > 0:
          for tt in permissible(x-1,y):
            if Node(x-1,y,tt) in nodes:
              n = Node(x-1,y,tt) 
              edges[node].add((n,1 if t==tt else 8))
              edges[n].add((node,1 if t==tt else 8))
        if y > 0:
          for tt in permissible(x,y-1):
            if Node(x,y-1,tt) in nodes:
              n = Node(x,y-1,tt) 
              edges[node].add((n,1 if t==tt else 8))
              edges[n].add((node,1 if t==tt else 8))
        nodes.add(node)

  ends = [Node(target.x,target.y,tt) for tt in ['n','t','c'] if node in nodes]

  res = dijkstra(Node(start.x,start.y,'t'),ends,nodes,edges)
  print(max([max([c[1] for c in r[1]]) for r in res]))

find_path()