def d(p0,p1): return sum([abs(p-q) for p,q in zip(p0,p1)])

data = [tuple([int(v) for v in line.split(',')]) for line in open('25.in').read().split('\n')]

def generate(data):
  constellations = []
  while data:
    item = data[0]
    c = set([item])
    while True:
      l = len(c)
      for dd in data:
        if reduce((lambda a,b: a or b), [d(dd,ll) <= 3 for ll in c]):
          c.add(dd)
      if l == len(c): 
        break
    data = [dd for dd in data if dd not in c]
    constellations.append(c)
  return constellations

constellations = generate(data)
print("{} constellations".format(len(constellations)))
for c in constellations: print(c)