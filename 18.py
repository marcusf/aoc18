from itertools import count

def parse_input(fname):
  return [[x for x in l] for l in open(fname).read().split('\n')]

g = parse_input('18.in')

def pretty(g):
  return "\n".join(["".join(row) for row in g])

def transform(g,x,y):
  minx, maxx = max(0,x-1), min(x+1,len(g[0]))+1
  row = []
  if y-1 >= 0: row += g[y-1][minx:maxx]
  if x-1 >= 0: row.append(g[y][x-1])
  if x+1 < len(g[0]): row.append(g[y][x+1])
  if y+1 < len(g): 
    row += (g[y+1][minx:maxx])
  return row

'''
An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.
'''
def next(c,lst):
  if c=='.': return '|' if sum([1 for x in lst if x=='|' ]) >= 3 else '.'
  elif c=='|': return '#' if sum([1 for x in lst if x=='#']) >= 3 else '|'
  elif c=='#': return '#' if sum([1 for x in lst if x=='#']) >= 1 and sum([1 for x in lst if x=='|']) >= 1 else '.'

def score(g): return sum([sum([1 for c in r if c == '#']) for r in g])*sum([sum([1 for c in r if c == '|']) for r in g])

def part1(g):
  for t in range(1,11):
    g = one_pass(g)
  print(score(g))

def one_pass(g):
  og = []
  for y in range(len(g)):
    row = []
    for x in range(len(g[0])):
      row.append(next(g[y][x], transform(g,x,y)))
    og.append(row)
  return og

def part2(g):
  ranges = []
  for t in range(1,900):
    g = one_pass(g)

  for t in range(900,1000):
    g = one_pass(g)
    ranges.append(g)

  end = ranges[-1]#"".join([item for sublist in ranges[-1] for item in sublist])
  cycle = 0
  for i,state in enumerate(list(reversed(ranges))[1:]):
    if end == state:#"".join([item for sublist in state for item in sublist]):
      cycle = i+1
      break
  start,lst = t+1, dict()
  for t in range(start,start+cycle):
    g = one_pass(g)
    lst[t%cycle] = score(g)

  t = 1000000000
  print(lst[t%cycle])

part1(g)
part2(g)