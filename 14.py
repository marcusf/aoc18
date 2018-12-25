import math

def digitize(x):
  if x == 0: return [0]
  if x < 10: return [x]
  if x == 10: return [1,0]
  if x == 11: return [1,1]
  if x == 12: return [1,2]
  if x == 13: return [1,3]
  if x == 14: return [1,4]
  if x == 15: return [1,5]
  if x == 16: return [1,6]
  if x == 17: return [1,7]
  if x == 18: return [1,8]
  if x == 19: return [1,9]
  if x == 20: return [2,0]
  lst = []
  n = int(math.log10(x))
  for i in range(n, -1, -1):
      factor = 10**i
      k = x // factor
      lst.append(k)
      x -= k * factor
  return lst


def part1():
  e1,e2,lst=0,1,[3,7]
  MAX = 509671
  while len(lst) < MAX+10:
    n = lst[e1]+lst[e2]
    new = digitize(n)
    #new = [int(l) for l in list(str(n))]
    #print(new)
    lst.extend(new)
    e1, e2 = (e1+1+lst[e1]) % len(lst), (e2+1+lst[e2]) % len(lst)
  
  print(''.join([str(s) for s in lst[MAX:(MAX+10)]])) 

def part2():
  e1,e2,lst=0,1,[3,7]
  i = 0
  VAL = [int(l) for l in list('509671')]
  while not lst[-len(VAL):] == VAL:
    i = i + 1
    if i % 1000000 == 0: print("{:,}".format(i), "{:,}".format(len(lst)))
    n = lst[e1]+lst[e2]
    new = digitize(n)
    lst.extend(new)
    e1, e2 = (e1+1+lst[e1]) % len(lst), (e2+1+lst[e2]) % len(lst)
  print(len(lst[0:-len(VAL)]))

#part1()
part2() # 583 607 528 # 5 982 162