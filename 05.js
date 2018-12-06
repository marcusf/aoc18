const d=require('fs').readFileSync('05.txt','utf8'),
  lc='abcdefghijklmnopqrstuvwxyz'.split(''),l=c=>c.length-1;

const s1=d=>{
  while (true) {
    let o='',i;
    for (i=0;i<l(d);i++) {
      if (32!=Math.abs(d.charCodeAt(i)-d.charCodeAt(i+1))) {
        o += d[i];
      } else i++;
    }
    if (o.length == d.length-1) return l(d)+1;
    d=o+d[l(d)];
  }
}

const drop=(d,l)=>d.replace(new RegExp(l+'|'+l.toUpperCase(),'g'),'');
const s2=d=>lc.reduce((n,l)=>Math.min(n,s1(drop(d,l))),1e6)

console.log(s1(d),s2(d))