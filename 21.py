from operator import itemgetter

def parse_input(fname,instr):
  lines = open(fname).read().split('\n')
  ip = int(lines[0][4])
  instr = [(instr[row[0]],list(map(int,row[1:]))) for row in [line.split(' ') for line in lines[1:]]]
  return (ip, instr)

def addr(reg,a,b,c): reg[c] = reg[a]+reg[b]
def addi(reg,a,b,c): reg[c] = reg[a]+b
def mulr(reg,a,b,c): reg[c] = reg[a]*reg[b]
def muli(reg,a,b,c): reg[c] = reg[a]*b
def banr(reg,a,b,c): reg[c] = reg[a]&reg[b]
def bani(reg,a,b,c): reg[c] = reg[a]&b
def borr(reg,a,b,c): reg[c] = reg[a]|reg[b]
def bori(reg,a,b,c): reg[c] = reg[a]|b
def setr(reg,a,b,c): reg[c] = reg[a]
def seti(reg,a,b,c): reg[c] = a
def gtir(reg,a,b,c): reg[c] = 1 if a > reg[b]       else 0
def gtri(reg,a,b,c): reg[c] = 1 if reg[a] > b       else 0
def gtrr(reg,a,b,c): reg[c] = 1 if reg[a] > reg[b]  else 0
def eqir(reg,a,b,c): reg[c] = 1 if a == reg[b]      else 0
def eqri(reg,a,b,c): reg[c] = 1 if reg[a] == b      else 0
def eqrr(reg,a,b,c): reg[c] = 1 if reg[a] == reg[b] else 0

instr = dict()
instr['addr'] = addr
instr['addi'] = addi
instr['mulr'] = mulr
instr['muli'] = muli
instr['banr'] = banr
instr['bani'] = bani
instr['borr'] = borr
instr['bori'] = bori
instr['setr'] = setr
instr['seti'] = seti
instr['gtir'] = gtir
instr['gtri'] = gtri
instr['gtrr'] = gtrr
instr['eqir'] = eqir
instr['eqri'] = eqri
instr['eqrr'] = eqrr

def run(regg,instr,verbose):
  ip, program = parse_input('21.in',instr)  
  ticks = 0
  while regg[ip] < len(program):
    ticks += 1
    if regg[ip]==28 and verbose:
      print(regg[1])
    opcode, params = program[regg[ip]]
    opcode(regg,*params)
    regg[ip] += 1

  return ticks, True

def find_numbers(regg,instr):
  ip, program = parse_input('21.in',instr)  
  ticks = 0
  res = []
  rss = set()
  while regg[ip] < len(program):
    ticks += 1
    if regg[ip]==28:
      res.append(regg[1])
      rss.add(regg[1])
      if len(res) != len(rss):
        print("Cycle found")
        return rss
    opcode, params = program[regg[ip]]
    opcode(regg,*params)
    regg[ip] += 1

  return rss

# Part 1: After observing line 28, we see that this number halts it.
run([2525738,0,0,0,0,0],instr,True)

res = find_numbers([0,0,0,0,0,0],instr)
print(res[-1])
