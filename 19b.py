def orig():
  result = 0
  inner = 0
  big_num = 920#10551320
  outer = 0
  
  while outer <= big_num:
    inner = 1
    while inner <= big_num:
        if inner*outer == big_num:
          result += outer
        inner += 1
    outer += 1
  print(result)

def trimmed():
  result = 0
  big_num = 10551320

  for x0 in range(1,big_num+1):
    if big_num % x0 == 0:
      result += x0
  print(result)

orig()
trimmed()