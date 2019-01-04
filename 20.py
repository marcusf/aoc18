from collections import namedtuple, defaultdict
from copy import deepcopy
#from anytree import Node, RenderTree

def flatten_list(nested_list):
    """Flatten an arbitrarily nested list, without recursion (to avoid
    stack overflows). Returns a new list, the original list is unchanged.
    >> list(flatten_list([1, 2, 3, [4], [], [[[[[[[[[5]]]]]]]]]]))
    [1, 2, 3, 4, 5]
    >> list(flatten_list([[1, 2], 3]))
    [1, 2, 3]
    """
    
    while nested_list:
        sublist = nested_list.pop(0)

        if isinstance(sublist, list):
            nested_list = sublist + nested_list
        else:
            yield sublist

class Node:
  def __init__(self,froml,chars):
    self.inn = []#set()
    self.out = []#set()
    self.chars = chars
    self.rooms = []
    if froml:
      for o in froml:
        self.inn.append(o)
      #for o in froml:
      #  if not self in o.out:
      #    o.out.append(self)

  def __str__(self): 
    return "{}, in=[{}], out=[{}]".format("".join(self.chars),
      ", ".join(["".join(n.chars) for n in self.inn]), 
      ", ".join(["".join(n.chars) for n in self.out]))

  def __repr__(self):
    #return "{}".format("".join(self.chars))
    return "{}".format("".join(self.chars))

#Node = namedtuple('Node', ['inn','out','chars'])
Room = namedtuple('Room', ['x','y'])

#ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))
def parsetree(rexp):
  i = 0
  tree = []
  buf = []
  curr = tree
  stack = []

  def peek(): return rexp[i]
  def get(): 
    nonlocal i
    i+=1
    return rexp[i-1]
  def letter():      return peek() in 'ESWN'
  def startparen():  return peek() == '('
  def divider():     return peek() == '|'
  def endparen():    return peek() == ')'
  def eat(): 
    nonlocal buf
    while i < len(rexp) and letter(): 
      buf.append(get())
  def letters(): 
    nonlocal curr, buf
    curr.append(('l',buf))
    buf = []
  def node():
    nonlocal curr
    n = []
    curr.append(('n',n))
    curr = n
    buf = []
  def split():
    nonlocal curr
    curr.append(('d',[]))

  while i < len(rexp):
    if letter():
      eat()
      letters()
    elif startparen():
      get()
      stack.append(curr)
      node()
    elif endparen():
      get()
      curr = stack.pop()
      buf = []
    elif divider():
      get()
      split()

  return tree

def to_dag(tree):
  meh = None
  def _dag(tree,parents):
    nonlocal meh
    output = 0
    outs = dict()
    prev = parents
    for node in tree:
      if node[0] == 'l':
        n = Node(prev,node[1])
        for p in prev: 
          p.out.append(n)
        prev = [n]
        outs[output] = n
      elif node[0] == 'n':
        prev = _dag(node[1], prev)
      elif node[0] == 'd':
        prev = parents
        output += 1
        outs[output] = parents
    return list(flatten_list(list(outs.values())))

  root = Node(None,[])
  _dag(tree,[root])
  return root.out[0]

def build_world(root):
  def _create(parent, char):
    dx = -1 if char == 'W' else 1 if char == 'E' else 0
    dy = 1 if char == 'S' else -1 if char == 'N' else 0
    newnode = Room(parent.x+dx,parent.y+dy)
    graph.add(newnode)
    ins[newnode].add(parent)
    outs[parent].add(newnode)
    return newnode

  queue = [root]
  graph = set([Room(0,0)])
  ins = defaultdict(set)
  outs = defaultdict(set)
  visited = set(queue)

  while queue:
    node = queue.pop(0)
    parents = set()
    for parent in node.inn:
      if len(parent.rooms) > 0:
        parents.add(parent.rooms[-1])
    if len(parents) == 0:
      parents.add(Room(0,0))

    for parent in parents:
      current = parent
      for char in node.chars:
        newnode = _create(current, char)
        node.rooms.append(newnode)
        current = newnode
    for n in node.out:
      if not n in visited:
        queue.append(n)
        visited.add(n)

  return graph, ins, outs


#===============================================================
# Pretty printers for the various stages of the pipeline
def pretty_tree(tree,d=0):
  prefix = '-' * d
  for node in tree:
    if node[0] == 'l':
      print(prefix+"".join(node[1]))
    elif node[0] == 'd':
      print(prefix+"|")
    elif node[0] == 'n':
      pretty_tree(node[1],d+1)

def pretty_dag(node):
  queue = [node]
  visited = set(queue)

  while queue:
    node = queue.pop(0)
    print(node)
    for n in node.out:
      if not n in visited:
        queue.append(n)
        visited.add(n)

def pretty_grid(rooms, ins, outs):
  minx,miny,maxx,maxy = 100,100,-100,-100
  for room in rooms:
    maxx, maxy = max(maxx, room.x), max(maxy,room.y)
    minx, miny = min(minx, room.x), min(miny,room.y)

  edges = defaultdict(set) 
  for r in rooms: edges[r] = ins[r] | outs[r]

  array = [['.' for _ in range(1+2*(maxx-minx))] for y in range(2*(maxy-miny)+1)]

  for y in range(len(array)):
    for x in range(len(array[0])):
      if y % 2 == 1 and array[y][x] == '.' or x % 2 == 1 and array[y][x] == '.':
        array[y][x] = '#'
      if y % 2 == 0 and x % 2 == 0:
        xx = round(x / 2 + minx)
        yy = round(y / 2 + miny)
        if Room(xx+1,yy) in edges[Room(xx,yy)]: array[y][x+1] = '|'
        if Room(xx-1,yy) in edges[Room(xx,yy)]: array[y][x-1] = '|'
        if Room(xx,yy+1) in edges[Room(xx,yy)]: array[y+1][x] = '-'
        if Room(xx,yy-1) in edges[Room(xx,yy)]: array[y-1][x] = '-'
        if yy == 0 and xx == 0: array[y][x] = 'X'
  out = [['#']*(len(array[0])+2)]
  out.extend([['#']+row+['#'] for row in array])
  out.append(['#']*len(out[0]))
  print("\n".join(["".join(row) for row in out]))


def max_distance(ins, outs):
  root = Room(0,0)
  distances = defaultdict(int)
  maxd = 0

  queue = [root]
  visited = set(queue)

  while queue:
    room = queue.pop(0)
    if len(ins[room]) == 0:
      distance = 0
    else:
      distance = 1 + max([distances[n] for n in ins[room]])
      distances[room] = distance
      maxd = max(distance, maxd)
    for n in outs[room]:
      if not n in visited:
        queue.append(n)
        visited.add(n)

  return maxd

def above_1000(ins, outs):
  root = Room(0,0)
  distances = defaultdict(int)
  counter = 0

  queue = [root]
  visited = set(queue)

  while queue:
    room = queue.pop(0)
    if len(ins[room]) == 0:
      distance = 0
    else:
      distance = 1 + max([distances[n] for n in ins[room]])
      distances[room] = distance
      if distance >= 1000:
        counter += 1
      #maxd = max(distance, maxd)
    for n in outs[room]:
      if not n in visited:
        queue.append(n)
        visited.add(n)

  return counter

rexp = open('20.in').read()[1:-1]
print(rexp)

# Sequence is: 
# 1. Build a parse tree
# 2. Transform to a DAG matching the regexp
# 3. Generate a complete world from that DAG
# 4. To a DFS scan through the world, calculating
#    maximum distances for each node.
tree = parsetree(rexp)
graph = to_dag(tree)

rooms, ins, outs = build_world(graph)

pretty_grid(rooms, ins, outs)
print(max_distance(ins, outs))
print(above_1000(ins, outs))