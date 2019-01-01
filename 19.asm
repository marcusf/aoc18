    #ip 1
0   addi 1 16 1     ip += 16+1 (jmp START)                        go to START

;LABEL6
1   seti 1 4 5      R[5] = 1                                      R5 = 1
;LABEL3
2   seti 1 4 2      R[2] = 1                                      R2 = 1
;LABEL5
3   mulr 5 2 4      R[4] = R[2]*R[5]                              R4 = R5*R2 = 1

;;;; if-else thingybob
4   eqrr 4 3 4      if R[3] = R[4]: R[4] = 1 else R[4] = 0
5   addr 4 1 1      ip += R[4] skip next if R[3] == R[4]
6   addi 1 1 1      ip += 1 (jmp to LABEL2)                       if R3 != R4: GOTO LABEL2
7   addr 5 0 0      R[0] += R[5]                                  R0 += R5

; LABEL2
8   addi 2 1 2      R[2] += 1                                     R2 += 1
9   gtrr 2 3 4      if R[2] > R[3] R[4] = 1 else R[4] = 0
10  addr 1 4 1      p += R[4] skip next if R[2] > R[3]
11  seti 2 6 1      ip = 2+1 (jmp LABEL3)                         if R2 <= R3: GOTO LABEL5
12  addi 5 1 5      R[5] += 1                                     R5 += 1
13  gtrr 5 3 4      if R[5] > R[3]: R[4] = 1 else R[4] = 0
14  addr 4 1 1      ip += R[4] skip next if R[5] > R[3]

15  seti 1 7 1      jmp LABEL3                                    if R5 <= R3: GOTO LABEL3
16  mulr 1 1 1      ip = ip*ip => ip = 32 => jmp LABEL4           GOTO LABEL4

; START
17  addi 3 2 3      R[3] += 2
18  mulr 3 3 3      R[3] = R[3]*R[3]
19  mulr 1 3 3      R[3] = ip*R[3] => 19*R[3]
20  muli 3 11 3     R[3] = R[3] * 11                              R3 = 11*19*(R3+2)^2 = 209*(R3+2)^2
21  addi 4 3 4      R[4] += R[3]
22  mulr 4 1 4      R[4] = ip*R[4] => 22*R[4]
23  addi 4 18 4     R[4] += 18                                    R4 = 22*(R4+R3)+18
24  addr 3 4 3      R[3] = R[3] + R[4]                            R3 = R3+R4
25  addr 1 0 1      ip += R[0] ; jmp R[0] (revealed later?)
26  seti 0 7 1      ip = 0 (start over.)

27  setr 1 4 4      R[4] = 27
28  mulr 4 1 4      R[4] = R[4]*28
29  addr 1 4 4      R[4] += 29
30  mulr 1 4 4      R[4] *= 30
31  muli 4 14 4     R[4] *= 14                                    
32  mulr 4 1 4      R[4] *= 32                                    R4 = (27*28+29)*30*14*32 = 10550400 

; LABEL4
33  addr 3 4 3      R[3] += R[4]                                  R3 += R4
34  seti 0 0 0      R[0] = 0                                      R0 = 0
35  seti 0 1 1      jmp 0 (Start over.)                           jmp LABEL6