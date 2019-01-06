from collections import namedtuple, defaultdict
import math
from math import ceil
from statistics import median, mean
from functools import reduce
import sys

Bot,Point = namedtuple('Bot', ['p','r']), namedtuple('Point', ['x','y','z'])

def d(p0,p1): return abs(p1.x-p0.x)+abs(p1.y-p0.y)+abs(p1.z-p0.z)

def in_range(p,bs): return [b for b in bs if d(p,b.p) <= b.r]

def sphere(b):
  p,r = b.p, b.r
  return set([Point(p.x+r,p.y,p.z),Point(p.x-r,p.y,p.z),Point(p.x,p.y+r,p.z),
    Point(p.x,p.y-r,p.z),Point(p.x,p.y,p.z+r),Point(p.x,p.y,p.z-r)])

def hull(b1,b2):
  out = set()
  s1 = sphere(b1)
  s2 = sphere(b2)
  for pp in sphere(b2):
    if d(b1.p,pp) <= b1.r:out.add(pp)
  for pp in sphere(b1):
    if d(b2.p,pp) <= b2.r:out.add(pp)
  return out

def mutual_hull(b1,b2):
  return len(hull(b1,b2)) > 0

def flatten(l): return [item for sublist in l for item in sublist]

lines = open('23.in').read().split('\n')
points = [Bot(Point(*map(int,l[0].split(','))),int(l[1])) 
        for l in [l[5:].split('>, r=') for l in lines]]

prime = max(points,key=lambda l:l.r)
print(sum([1 for p in points if d(p.p,prime.p) <= prime.r]))

#pts, l = find_all(points)
#print(pts,l)

#p = Point(x=14944081, y=58027080, z=27054384)
#def in_range_e(p,bs): return [(i,b) for i,b in enumerate(bs) if d(p,b.p) <= b.r]
#mins = []
#for i,b in in_range_e(p,points):
#  print(i,b)
#  bmin,bp = min((d(p,pp),pp) for pp in sphere(b))
#  mins.append((bmin,bp,b))
#
#for dist,pt,b in (sorted(mins)):
#  print(len(in_range(pt, points)))
#all_points = flatten([sphere(b) for b in points])
#dists = [(len(in_range(pt,points)),pt) for pt in all_points]
#top10 = sorted(dists,reverse=True)[0:50]
#
#bx,by,bz = top10[0][1]
#
#print(d(p,top10[0][1]))
#
#for r,p in top10:
#  print(r,Point(p.x-bx,p.y-by,p.z-bz))
#
#

# I'll be quite honest, I just brute-forced the living jesus out of this one.
p = Point(x=13839482, y=57977321, z=25999544) # 97816347

queue = [p]
visited = set(queue)
mmx = 0
times = 0
mind = 1000000000000
minp = []

while queue:
  pt = queue.pop(0)
  dists = len(in_range(pt, points))
  if dists > mmx:
    mmx = dists
    times = 1
    minp = pt
    print(mmx,times, pt,d(Point(0,0,0),minp))
  elif dists == mmx:
    dd = d(Point(0,0,0),pt)
    if dd < mind:
      mind = dd
      minp = pt
      times += 1
      print(mmx,times,mind,minp)
  INTERV = [-1,0,1]
  for x in INTERV:
    for y in INTERV:
      for z in INTERV:
        p = Point(pt.x+x,pt.y+y,pt.z+z)
        if not p in visited:
          visited.add(p)
          queue.append(p)

#dd = p.x+p.y+p.z
#dp = Point(-p.x/dd,-p.y/dd,-p.z/dd)
#print(p,len(in_range(p,points)),d(Point(0,0,0),p))
#k = 1
#while True:
#  p = Point(p.x,p.y,p.z-1)
#  print(p,len(in_range(p,points)),d(Point(0,0,0),p))

#  def _find(candidate, not_it,it,best=[]):
#    if len(candidate) > len(best): best = candidate
#    if len(bset) == len(candidate)+len(not_it): return best
#    if len(not_it) > 100: return best
#    remaining = bset - candidate - not_it
#    for bot in remaining:
#      if reduce((lambda a,b: a and b), [mutual_hull(b, bot) for b in candidate]):
#        cand = _find(candidate.union([bot]), not_it, best)
#        if len(cand) > len(best):
#          best = cand
#      else: 
#        not_it.add(bot)
#    return best
#
#  maxs = []
#  for i, bot in enumerate(bset):
#    print(i)
#    bset = set(bots[i:])
#    solution = _find(set([sphere(bot)]),set([]),set([bot]))
#    print(len(solution))
#    if len(solution) > len(maxs):
#      maxs = solution
#  return maxs
#


#S = 10000000
#
#sp = [Bot(Point(ceil(b.p.x/S),ceil(b.p.y/S),ceil(b.p.z/S)), ceil(b.r/S)) for b in points]
#
#xs,ys,zs,rs = [p.p.x for p in sp],[p.p.y for p in sp],[p.p.z for p in sp],[p.r for p in sp]
#mid = Point(ceil(median(xs)),ceil(median(ys)),ceil(median(zs)))
#
#minx,maxx = min(xs)-max(rs),max(xs)+max(rs)
#miny,maxy = min(ys)-max(rs),max(ys)+max(rs)
#minz,maxz = min(zs)-max(rs),max(zs)+max(rs)
#dims = (maxx-minx)*(maxy-miny)*(maxz-minz)
##print("Search space is",dims,"points")
#
#m = 0
#pmax = []
#
#for x in range(minx,maxx):
#  for y in range(miny,maxy):
#    for z in range(minz,maxz):
#      p = Point(x,y,z)
#      mm = len(in_range(p, sp))
#      if mm > m:
#        m = mm
#        pmax = p
#        print(m, pmax)
#cur = Point(2*S,7*S,3*S)
#cur = Point(x=14944081, y=58027080, z=27054384)
#914 1428 99325545

#queue = [cur]
#visited = set(queue)
#mmx = 0
#times = 0
#mind = 1000000000000
#
#while queue:
#  pt = queue.pop(0)
#  dists = len(in_range(pt, points))
#  if dists > mmx:
#    mmx = dists
#    times = 1
#    print(mmx,times, pt)
#  elif dists == mmx:
#    times += 1
#    mind = min(mind,d(Point(0,0,0),pt))
#    print(mmx,times,mind)
#  INTERV = [-10000,0,10000]
#  for x in INTERV:
#    for y in INTERV:
#      for z in INTERV:
#        p = Point(pt.x+x,pt.y+y,pt.z+z)
#        if not p in visited:
#          visited.add(p)
#          queue.append(p)

#mmx = 0
#while True:
#  rg = set(in_range(cur, points))
#  mmx = max(mmx,len(rg))
#  out = set(points) - rg
#  i = 0
#  while i < len(out):
#    pxx = sorted([(abs(b.r-d(cur,b.p)),b) for b in out])[i]
#    px = pxx[1]
#    vec = Point((px.p.x-cur.x)/d(cur,px.p),
#      (px.p.y-cur.y)/d(cur,px.p),(px.p.z-cur.z)/d(cur,px.p))
#    
#    cur = Point(math.floor(cur.x+vec.x*pxx[0]),math.floor(cur.y+vec.y*pxx[0]),math.floor(cur.z+vec.z*pxx[0]))
#    rrg = set(in_range(cur, points))
#    if len(rrg) <= len(rg):
#      i += 1
#    else:
#      if len(rrg) > mmx:
#        mmx = len(rrg)
#        print(cur,mmx)
#      rg = rrg

#print(vec)
#print(px)


#S = 10000000
#
#sp = [Bot(Point(ceil(b.p.x/S),ceil(b.p.y/S),ceil(b.p.z/S)), ceil(b.r/S)) for b in points]
#
#xs,ys,zs,rs = [p.p.x for p in sp],[p.p.y for p in sp],[p.p.z for p in sp],[p.r for p in sp]
#mid = Point(ceil(median(xs)),ceil(median(ys)),ceil(median(zs)))
#
#minx,maxx = min(xs)-max(rs),max(xs)+max(rs)
#miny,maxy = min(ys)-max(rs),max(ys)+max(rs)
#minz,maxz = min(zs)-max(rs),max(zs)+max(rs)
#dims = (maxx-minx)*(maxy-miny)*(maxz-minz)
##print("Search space is",dims,"points")
#
#m = 0
#pmax = []
#
#for x in range(minx,maxx):
#  for y in range(miny,maxy):
#    for z in range(minz,maxz):
#      p = Point(x,y,z)
#      mm = len(in_range(p, sp))
#      if mm > m:
#        m = mm
#        pmax = p
#        print(m, pmax)
#cur = Point(2*S,7*S,3*S)
#cur = Point(x=14944081, y=58027080, z=27054384)
#914 1428 99325545

#queue = [cur]
#visited = set(queue)
#mmx = 0
#times = 0
#mind = 1000000000000
#
#while queue:
#  pt = queue.pop(0)
#  dists = len(in_range(pt, points))
#  if dists > mmx:
#    mmx = dists
#    times = 1
#    print(mmx,times, pt)
#  elif dists == mmx:
#    times += 1
#    mind = min(mind,d(Point(0,0,0),pt))
#    print(mmx,times,mind)
#  INTERV = [-10000,0,10000]
#  for x in INTERV:
#    for y in INTERV:
#      for z in INTERV:
#        p = Point(pt.x+x,pt.y+y,pt.z+z)
#        if not p in visited:
#          visited.add(p)
#          queue.append(p)

#mmx = 0
#while True:
#  rg = set(in_range(cur, points))
#  mmx = max(mmx,len(rg))
#  out = set(points) - rg
#  i = 0
#  while i < len(out):
#    pxx = sorted([(abs(b.r-d(cur,b.p)),b) for b in out])[i]
#    px = pxx[1]
#    vec = Point((px.p.x-cur.x)/d(cur,px.p),
#      (px.p.y-cur.y)/d(cur,px.p),(px.p.z-cur.z)/d(cur,px.p))
#    
#    cur = Point(math.floor(cur.x+vec.x*pxx[0]),math.floor(cur.y+vec.y*pxx[0]),math.floor(cur.z+vec.z*pxx[0]))
#    rrg = set(in_range(cur, points))
#    if len(rrg) <= len(rg):
#      i += 1
#    else:
#      if len(rrg) > mmx:
#        mmx = len(rrg)
#        print(cur,mmx)
#      rg = rrg

#print(vec)
#print(px)
#
#
#def find_all(bots):
#
#  def _find(candidate, visited,best=[]):
#    if len(candidate) > len(best): best = candidate
#    if len(bots) == len(visited): return best
#    for bot in bots:
#      if not bot in visited:
#        visited.add(bot)
#        #if reduce((lambda a,b: a and b), 
#        #  [overlaps(bot,c) for c in candidate]):
#        #o = True
#        #for c in candidate:
#        #  o = o and overlaps(bot,c)
#        
#        #pts = max([len(in_range(p,candidate)) for p in sphere(bot)])
#
#        #if pts >= len(candidate):
#        if len(in_range(bot.p,candidate)) == len(candidate):
#        #if max([len(in_range(p,candidate)) for p in sphere(bot)]) == len(candidate):
#        #if o:
#        #  print(len(in_range(bot.p,candidate)), 
#        #    max([len(in_range(p,candidate)) for p in sphere(bot)]))
#
#          cand = _find(candidate+[bot], visited, best)
#          if len(cand) > len(best):
#            best = cand
#    return best
#
#  maxs = []
#
#  for bot in bots:
#    solution = _find([bot],set(bot))
#    if len(solution) == 111: #>= len(maxs):
#      #print(len(solution))
#      maxs = solution
#      return maxs
#  return maxs
#
#for point in points:
#  print(math.ceil(0.471*math.pow(point.r/2,3)))
#
##cluster = find_all(points)
##m = 0
##pmax = []
##sp = points#list(set(cluster))
##for i in range(len(sp)):
##  for j in range(i+1,len(sp)):
##    pts = set(hull(sp[i],sp[j]))
##    for p in pts:
##      mm = len(in_range(p, points))
##      if mm > m:
##        m = mm
##        pmax = p
##        print(p,m)
#
#print(d(Point(0,0,0),pmax))
#pts = set(hull(sp[0],sp[1]))
#
#for b in sp:
#  pts = pts.intersection(set([p for p in pts if d(p,b.p) <= b.r]))
#
#for p in pts:
#  print(d(Point(0,0,0),p), len(in_range(p, points)))
 

#152802563
#152071431
#106949501