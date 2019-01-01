from itertools import count

def parse_input(fname):
  lines = open(fname).read().split('\n')
  ip = int(lines[0][4])
  instr = [(row[0],list(map(int,row[1:]))) for row in [line.split(' ') for line in lines[1:]]]
  return (ip, instr)

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

def run(regg):
  ip, program = parse_input('19.in')  
  while regg[ip] < len(program):
    print(program[regg[ip]], regg)
    opcode, params = program[regg[ip]]
    regg = runf(opcode,regg,*params)
    regg[ip] += 1

  return regg


#print(run([0 for _ in range(0,6)]))
print(run([1,0,0,0,0,0]))