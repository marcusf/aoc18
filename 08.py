data = list(map(int,open("08.in").read().split(" ")))

def parse(data, t, results):
  children, mdlen, mdstart = data[t], data[t+1], t+2

  for i in range(0, children):
    if len(data)-mdstart <= 2:
      break
    mdstart, results = parse(data, mdstart, results)

  results = results + data[mdstart:(mdstart+mdlen)]
  return (mdstart+mdlen, results)

_, result = parse(data, 0, [])
print(sum(result))
