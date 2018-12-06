const parse = l => [+l.substr(15,2), l[19]=='w', /\d+/.exec(l.substr(19))];

const aggregate = lines => {
  let s = [], r = [], guard, start, c;
  for (const [end, wake, g] of lines) {
    guard = g ? g[0] : guard;
    if (wake) s.push([guard, start, end - start]);
    start = end;
  }
  for (const [id, t, d] of s.sort()) {
    if (c != id) {
      r.unshift([id, []]);
      c = id;
    }
    r[0][1].push([t, d]);
  }
  return r;
}

const solve = (l) => {
  const [id,p] = l;
  let t = Array(60).fill(0);
  for (const [s, d] of p) for (let i=0; i < d; i++) t[s+i]++;
  return [id,p.reduce((n,[_,i])=>n+i,0), t.indexOf(Math.max(...t)), Math.max(...t)];
}


let d = require('fs').readFileSync('04.txt','utf8').split('\n').sort();
let answer = aggregate(d.map(parse)).map(solve);

// Solution One
let answer1 = answer.sort((a,b) => b[1]-a[1])[0];
console.log(answer1[0]*answer1[2]);

// Solution Two
let answer2 = answer.sort((a,b) => b[3]-a[3])[0];
console.log(answer2[0]*answer2[2]) 