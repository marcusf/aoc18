from collections import namedtuple, defaultdict
import math
from math import ceil

def d(p0,p1): return abs(p1.x-p0.x)+abs(p1.y-p0.y)+abs(p1.z-p0.z)
def in_range(p,bs): return len([1 for b in bs if d(p,b.p) <= b.r])
Bot,Point = namedtuple('Bot', ['p','r']), namedtuple('Point', ['x','y','z'])
Quad = namedtuple('Quad',['x0','x1','y0','y1','z0','z1'])

class Node:
  def __init__(self,quad,children,parent,covers):
    self.quad = quad
    self.children = children
    self.parent = parent
    self.covers = covers

  def __str__(self): return str(self.covers)
  def __repr__(self): return str(self.covers)

def center(quad):
  return Point(ceil((quad.x1+quad.x0)/2),ceil((quad.y1+quad.y0)/2),ceil((quad.z1+quad.z0)/2))

def plane_distance(p, f):
  return (p.x-f[0].x)*f[1].x + (p.y-f[0].y)*f[1].y + (p.z-f[0].z)*f[1].z

def bot_inside_plane(bot, f): return -plane_distance(bot.p,f) > bot.r
def bot_outside_plane(bot, f): return plane_distance(bot.p,f) > bot.r
def bot_intersects_plane(bot, f): return abs(plane_distance(bot.p,f)) <= bot.r

def faces(q):
  faces = [[Point(q.x0,0,0), Point(-1,0,0)],
    [Point(q.x1,0,0), Point(1,0,0)],
    [Point(0,q.y0,0), Point(0,-1,0)],
    [Point(0,q.y1,0), Point(0,1,0)],
    [Point(0,0,q.z0), Point(0,0,-1)], 
    [Point(0,0,q.z1), Point(0,0,1)]]
  return faces

def b_in_range(ps,b): return len([1 for p in ps if d(p,b.p) <= b.r])

def qb_overlap(q,b): return b_in_range(points(q), b)>0

def qbs_overlap(q,bs): return [b for b in bs if qb_overlap(q,b)]

def split(quad):
  mx = ceil((quad.x1+quad.x0)/2)
  my = ceil((quad.y1+quad.y0)/2)
  mz = ceil((quad.z1+quad.z0)/2)

  c1 = Quad(mx-1, quad.x1+1, my-1, quad.y1+1, mz-1, quad.z1+1)
  c2 = Quad(quad.x0-1, mx+1, my-1, quad.y1, mz-1, quad.z1+1)

  c3 = Quad(mx-1, quad.x1+1, quad.y0-1, my+1, mz-1, quad.z1+1)
  c4 = Quad(quad.x0-1, mx+1, quad.y0-1, my+1, mz-1, quad.z1+1)
  c5 = Quad(mx-1, quad.x1+1, quad.y0-1, my+1, quad.z0-1, mz+1)
  c6 = Quad(quad.x0-1, mx+1, quad.y0-1, my+1, quad.z0-1, mz+1)

  c7 = Quad(mx-1, quad.x1+1, my-1, quad.y1+1, quad.z0-1, mz+1)
  c8 = Quad(quad.x0-1, mx+1, my-1, quad.y1+1, quad.z0-1, mz+1)

  return [c1,c2,c3,c4,c5,c6,c7,c8]


lines = open('23.in').read().split('\n')
bots = [Bot(Point(*map(int,l[0].split(','))),int(l[1])) 
        for l in [l[5:].split('>, r=') for l in lines]]

x0,x1 = min([p.p.x for p in bots]), max([p.p.x for p in bots])
y0,y1 = min([p.p.y for p in bots]), max([p.p.y for p in bots])
z0,z1 = min([p.p.z for p in bots]), max([p.p.z for p in bots])
box = Quad(x0,x1,y0,y1,z0,z1)


def mktree(quad,parent,children,depth=0):
  if depth > 1:
    c = Node(quad,[],parent, qbs_overlap(quad, parent.covers))
    children.append(c)
    return c
  else:
    ls = []
    par = Node(quad,ls,parent,qbs_overlap(quad, parent.covers))
    parent.children.append(par)
    qs = split(quad)
    for q in qs:
      nn = mktree(q,par,children,depth+1)
      if nn:
        ls.append(nn)

root, children = Node(0,[],[],bots), []
mktree(box,root,children)

for c in children:
  print(len(c.covers))

#def set_max(tree):
#  if len(tree.children) == 0:
#    return tree.covers
#  else:
#    tree.covers = max([set_max(q) for q in tree.children])
#    return tree.covers
#
#root = Node(0,[],[],0)
#mktree(box,root,80000000)
#set_max(root)
#root = root.children[0]
#ls = []
#for c in root.children:
#  for cc in c.children:
#    if cc.covers > 100:
#      ls.append(cc)
#
#lls = []
#for qq in ls:
#  print(qq)
#  qr = Node(0,[],[],0)
#  mktree(qq.quad,qr,8000000)
#  set_max(qr)
#  qr = qr.children[0]
#  for c in qr.children:
#    for cc in c.children:
#      if 13839531 >= cc.quad.x0 and 13839531 <= cc.quad.x1 and \
#          57977321 >= cc.quad.y0 and 57977321 <= cc.quad.y1 and \
#          25999593 >= cc.quad.z0 and 25999593 <= cc.quad.z1 and \
#          cc.covers > 700:
#        print('winner winner')
#        print(cc)
#      if cc.covers > 700:
#        lls.append(cc)
#
#
#llls = []
#for qq in lls:
#  print(qq)
#  qr = Node(0,[],[],0)
#  mktree(qq.quad,qr,8000000)
#  set_max(qr)
#  qr = qr.children[0]
#  for c in qr.children:
#    for cc in c.children:
#      # 953 6 97816445 Point(x=13839531, y=57977321, z=25999593)
#
#      if 13839531 >= cc.quad.x0 and 13839531 <= cc.quad.x1 and \
#          57977321 >= cc.quad.y0 and 57977321 <= cc.quad.y1 and \
#          25999593 >= cc.quad.z0 and 25999593 <= cc.quad.z1 and \
#          cc.covers > 700:
#        print('winner winner')
#      if cc.covers > 700:
#        llls.append(cc)
#
#print([p.quad for p in llls])
#