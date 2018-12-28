from collections import defaultdict

def runf(i,regg,a,b,c):
  reg = regg[:]
  if   i == 'addr': reg[c] = reg[a]+reg[b]
  elif i == 'addi': reg[c] = reg[a]+b
  elif i == 'mulr': reg[c] = reg[a]*reg[b]
  elif i == 'muli': reg[c] = reg[a]*b
  elif i == 'banr': reg[c] = reg[a]&reg[b]
  elif i == 'bani': reg[c] = reg[a]&b
  elif i == 'borr': reg[c] = reg[a]|reg[b]
  elif i == 'bori': reg[c] = reg[a]|b
  elif i == 'setr': reg[c] = reg[a]
  elif i == 'seti': reg[c] = a
  elif i == 'gtir': reg[c] = 1 if a > reg[b]       else 0
  elif i == 'gtri': reg[c] = 1 if reg[a] > b       else 0
  elif i == 'gtrr': reg[c] = 1 if reg[a] > reg[b]  else 0
  elif i == 'eqir': reg[c] = 1 if a == reg[b]      else 0
  elif i == 'eqri': reg[c] = 1 if reg[a] == b      else 0
  elif i == 'eqrr': reg[c] = 1 if reg[a] == reg[b] else 0
  else: print(i)
  return reg

instr = ['addr','addi','mulr','muli','banr','bani','borr','bori',
         'setr','seti','gtir','gtri','gtrr','eqir','eqri','eqrr']

def parse_input(fname):
  d = open(fname).read().split('\n')
  iss, instr = d[0:3164],[]
  for i in range(0, len(iss), 4):
    before = [int(v) for v in iss[i][9:-1].split(', ')]
    vals   = [int(v) for v in iss[i+1].split(' ')]
    after  = [int(v) for v in iss[i+2][9:-1].split(', ')]
    opcode, args = vals[0], vals[1:]
    instr.append((opcode,args,before,after))
  code = [[int(s) for s in v.split(' ')] for v in d[3166:]]
  return (instr, code)

def run(inp, outp, params):
  instrs = []
  for f in instr:
    output = runf(f,inp,*params)
    if output == outp: 
      instrs.append(f)
  return instrs

def part1(ins):
  print(sum([1 for (op,arg,bf,af) in ins if len(run(bf, af, arg)) >= 3]))

def part2(ins, code):
  instrlist = defaultdict(list)
  for (op,arg,bf,af) in ins:
    instrlist[op].append(run(bf, af, arg))
  for k, v in instrlist.items():
    sett = set(v[0])
    for l in v[1:]:
      sett = sett.intersection(l)
    instrlist[k] = sett
  
  while sum([len(v) for v in instrlist.values()]) > 16:
    for k, v in instrlist.items():
      if len(v) == 1:
        for kk, vv in instrlist.items():
          if k != kk:
            instrlist[kk] = instrlist[kk].difference(v)

  instrs = ['' for _ in range(16)]
  for k, v in instrlist.items():
    instrs[k] = v.pop()

  reg = [0,0,0,0]
  for line in code:
    reg = runf(instrs[line[0]], reg, *line[1:])
  print(reg[0])

instrs = parse_input('16.in')
part1(instrs[0])
part2(*instrs)