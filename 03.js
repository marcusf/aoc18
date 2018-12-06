F=require('fs').readFileSync('03.txt','utf8').split('\n'),P=console.log,
L=F.map(l=>/(\d+) @ (\d+),(\d+): (\d+)x(\d+)/.exec(l).slice(1,6).map(x=>+x)),
S=L.reduce((s,[,X,,W,])=>Math.max(s,X+W),0),M=Array(S*S).fill(0)
for([,X,Y,W,H]of L)for(i=H*W;i--;)M[(~~(i/W)+Y)*S+((i%W)+X)]++;P(M.filter(x=>x>1).length)
for([I,X,Y,W,H]of L){O=0;for(i=H*W;i--;)O|=M[(~~(i/W)+Y)*S+((i%W)+X)]>1;if(!O)P(I)}