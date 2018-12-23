from anytree import Node, PreOrderIter

d = list(map(int,open('08.in').read().split(' ')))

def deserialize(d, t, parent):
  children, entries, start, lst = d[t], d[t+1], t+2, list()
  node = Node(lst, parent=parent)
  for i in range(0, children):
    if len(d) - start <= 2: break
    start, node = deserialize(d, start, node)
  lst.extend(d[start:(start+entries)])
  return (start+entries, parent)

def value(node):
  val = 0
  if node.is_leaf:
    val = sum(node.name)
  else:
    for idx in node.name:
      if idx-1 < len(node.children):
        val = val + value(node.children[idx-1])
  return val

tree = deserialize(d, 0, Node([]))[1].children[0]

print(sum([sum(node.name) for node in PreOrderIter(tree)]))
print(value(tree))
