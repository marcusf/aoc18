import re
from collections import namedtuple, defaultdict
from operator import attrgetter, methodcaller
from math import floor

class Group:

  def __init__(self,typ,idx,units,hp,damage,damage_type,initative,weak_to,immune_to):
    self.typ='Infection' if typ == 'inf' else 'Immune System'
    self.idx = idx + 1
    self.units=units
    self.hp=hp
    self.damage=damage
    self.damage_type=damage_type
    self.initative=initative
    self.weak_to=weak_to
    self.immune_to=immune_to

  def boost(self,boost):
    self.damage += boost

  def is_infection(self): return self.typ == 'Infection'

  def enemy(self):
    return 'Infection' if self.typ == 'Immune System' else 'Immune System'

  def damage_multiplier(self,enemy):
    if self.damage_type in enemy.immune_to: return 0
    elif self.damage_type in enemy.weak_to: return 2
    else: return 1

  def strength(self, enemy):
    return self.damage_multiplier(enemy) * self.effective_power()

  def decide_enemy(self, enemies, verbose):
    eligible = [e for e in enemies if self.damage_multiplier(e) > 0]
    if len(eligible) > 0:
      targets = sorted(sort_ep(eligible), key=lambda a: self.damage_multiplier(a), reverse=True)
      if verbose:
        for t in targets:
          print("{} group {} would deal defending group {} {} damage".format(self.typ, self.idx, t.idx, self.strength(t)))
      return targets[0]
    else:
      return None

  def attack(self, enemy, verbose):
    units_killed = floor(self.strength(enemy) / enemy.hp)
    units_killed = min(enemy.units, units_killed)
    enemy.units -= units_killed
    if verbose:
      print("{} group {} attacks defending group {}, killing {} units".format(self.typ, self.idx,enemy.idx, units_killed))
    return enemy.units

  def __str__(self):
    return "{} {}: units={}, ep={}, initiative={}".format(
      self.typ,self.idx,self.units,self.effective_power(),self.initative)

  def __repr__(self): return self.__str__() 
  def effective_power(self): return self.units * self.damage


def get_basic(typ,idx,line):
  m = r'(?P<units>\d+) units each with (?P<hp>\d+) hit points( \((?P<extra>.+)\))? with an attack that does (?P<damage>\d+) (?P<damage_type>\w+) damage at initiative (?P<initiative>\d+)'
  n = re.match(m,line)
  return typ, idx, int(n.group('units')),int(n.group('hp')), int(n.group('damage')), \
    n.group('damage_type'), int(n.group('initiative')), pweak(n.group('extra')), pimmune(n.group('extra'))

def pextr(extra, rexp):
  res = []
  if not extra: return res
  weak = rexp
  m = re.match(weak, extra)
  if m:
    res.append(m.group(1))
    if m.group(3):
      res.append(m.group(3))
  return res

def pweak(extra): return pextr(extra, r'.*weak to (\w+),?( (\w+))*')
def pimmune(extra): return pextr(extra, r'.*immune to (\w+),?( (\w+))*')

def parse(f):
  lines = open(f).read().split('\n')
  immune = [Group(*get_basic('im',i,l)) for i,l in enumerate(lines[1:lines.index('Infection:')-1])]
  infect = [Group(*get_basic('inf',i,l)) for i,l in enumerate(lines[lines.index('Infection:')+1:])]
  return list(immune)+list(infect)

def sort_ep(groups): return sorted(sort_initiative(groups), key=methodcaller('effective_power'), reverse=True)
def sort_initiative(groups): return sorted(groups, key=attrgetter('initative'), reverse=True)

def one_pass(groups, verbose):
  attack_pairs = defaultdict(None)
  selection_order = sorted(sort_ep(groups), key=attrgetter('typ'), reverse=True)
  selected = set()
  for group in selection_order:
    targets = [g for g in groups if g.typ == group.enemy() and g not in selected]
    attackee = group.decide_enemy(targets, verbose)
    attack_pairs[group] = attackee
    selected.add(attackee)

  if verbose: print('')

  attack_order = sort_initiative(groups)

  killed = set()
  attackers = 0

  for group in attack_order:
    if attack_pairs[group]:
      attackers += 1
      hp = group.attack(attack_pairs[group], verbose)
      if hp == 0: killed.add(attack_pairs[group])

  return [g for g in groups if not g in killed], attackers

def game(groups,verbose=True):
  remaining = groups
  while True:
    if verbose:
      print("Immune System:")
      for g in [g for g in remaining if not g.is_infection()]:
        print("Group {} contains {} units".format(g.idx,g.units))
      print("Infection:")
      for g in [g for g in remaining if g.is_infection()]:
        print("Group {} contains {} units".format(g.idx,g.units))
      print("")
    remaining, attackers = one_pass(remaining,verbose)

    if attackers == 0:
      if verbose:
        print("No attacks possible")
      return False,0

    infected_remaining = [g for g in remaining if g.is_infection()]
    immune_remaining = [g for g in remaining if not g.is_infection()]
    if len(infected_remaining) == 0:
      if verbose:
        print('')
        print('Immune won:', sum([u.units for u in immune_remaining]))
      return (True, sum([u.units for u in immune_remaining]))
    elif len(immune_remaining) == 0:
      if verbose:
        print('')
        print('Infected won:',sum([u.units for u in infected_remaining]))
      return (False,sum([u.units for u in infected_remaining]))
    if verbose:
      print("--------------------------------------------------------------")


def part1():
  groups = parse('24.in')
  game(groups)

def part2():
  boost = 60
  min_win = 0
  min_boost = 10000000
  max_lost = 0
  while True:
    groups = parse('24.in')
    [g.boost(boost) for g in groups if not g.is_infection()]
    we_won, score = game(groups,  False)
    if not we_won:
      max_lost = max(max_lost, boost)
      boost = floor(boost + 1)
    else:
      if boost < min_boost:
        min_win = score
        min_boost = boost
        print('Min Boost',min_boost,'min win',min_win)
      boost = floor(boost - 1)
    if min_boost - max_lost == 1:
      return

#part1()
part2()