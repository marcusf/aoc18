from collections import namedtuple, defaultdict
import math
import random
from math import ceil
from statistics import median, mean
from functools import reduce
import sys
import numpy as np

Bot,Point = namedtuple('Bot', ['p','r']), namedtuple('Point', ['x','y','z'])

def d(p0,p1): return abs(p1.x-p0.x)+abs(p1.y-p0.y)+abs(p1.z-p0.z)

def in_range(p,bs): return len([1 for b in bs if d(p,b.p) <= b.r])

lines = open('23.in').read().split('\n')
points = [Bot(Point(*map(int,l[0].split(','))),int(l[1])) 
        for l in [l[5:].split('>, r=') for l in lines]]

prime = max(points,key=lambda l:l.r)
print(sum([1 for p in points if d(p.p,prime.p) <= prime.r]))

xs,ys,zs,rs = [p.p.x for p in points],[p.p.y for p in points],[p.p.z for p in points],[p.r for p in points]
p = Point(ceil(median(xs)),ceil(median(ys)),ceil(median(zs)))

def generate(p,n,order):
  ps = [p]
  for _ in range(n):
    ps.append(Point(p.x+np.random.randint(-order,order), p.y+random.randint(-order,order), p.z+random.randint(-order,order)))
  return ps

queue = [(i,100000000) for i in generate(Point(0,0,0),4,100000000)]
#visited = set(queue)
mmx = 0
times = 0
mind = 1000000000000
minp = []
attempts = 1
i = 0
iv = 100000
top100 = []
while queue:
  point,dev = queue.pop(0)
  print(point,dev)
  delta = 100000000#np.std([b[1].x for b in top100]) if top100 else 100000000
  pts = generate(point,3000,dev)
  otp = sorted([(in_range(pt, points),pt) for pt in pts], reverse=True)
  output = otp[0]

  dev = max(3000,ceil(np.std([b[1].x for b in otp[:30]])))
  queue.append((output[1],dev))

  top100.append(output)
  top100 = sorted(top100, reverse=True)[0:4]

  for score, point in top100[:4]:
    print(score, point)
  print("-----------------------------------------------------")

