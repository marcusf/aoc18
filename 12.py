d = open('12.in').read().split('\n')

fix = ['.' for _ in range(0, 10000)]
delta = len(fix)

state = fix+list(d[0][15:])+fix

rules = dict([(r[0:5], r[9]) for r in d[2:]])

for generation in range(0,20):
  machine = ''.join(state)
  print(generation, sum([(j-delta) if c == '#' else 0 for j,c in enumerate(state)]))
  for i in range(2,len(state)-3):
    c = machine[i-2:i+3]
    state[i] = rules[c]

print(sum([(j-delta) if c == '#' else 0 for j,c in enumerate(state)]))


# For part 2, we observe that after 96 generations, 
# it just keeps incrementing 32, cyclically, and can just work our way to the answer.
# 91 3391
# 92 3371
# 93 3411
# 94 3411
# 95 3370
# 96 3400
# 3400 + (32*(50000000000-96))
print(3400 + (32*(50000000000-96)))
# 97 3432
# 98 3464
# 99 3496
# 100 3528

