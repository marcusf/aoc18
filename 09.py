class Node:

  def __init__(self, value):
    self.value = value
    self.cw = self.ccw = self

  def insert(self, node):
    cw = self.cw
    self.cw = node
    node.ccw = self
    cw.ccw = node
    node.cw = cw

  def killcw(self):
    self.cw = self.cw.cw
    self.cw.ccw = self
    return self

def p(player, nodes):
  lst = []
  mx = 0
  while not nodes.value in lst:
    mx = max(mx, nodes.value)
    lst.append(nodes.value)
    nodes = nodes.cw
  print(player+1, lst)

def simulate(players, rounds):
  start = Node(0)
  game = start
  current = 0
  scores = [0 for _ in range(0, players)]
  
  for i in range(1,rounds):
    if i % 23 == 0:
      game = game.ccw.ccw.ccw.ccw.ccw.ccw.ccw
      scores[current] = scores[current] + i + game.value
      game = game.ccw.killcw().cw
    else:
      node = Node(i)
      game.cw.insert(node)
      game = node
  
    current = (current + 1) % players
  
  return max(scores)

PLAYERS, ROUNDS = 463, 71787

print(simulate(PLAYERS, ROUNDS))
print(simulate(PLAYERS, ROUNDS*100))