const fs = require('fs');
let d = fs.readFileSync('03.txt', 'utf8').split('\n');

//#1336 @ 916,193: 22x27
//id x y w h
const ID=0,X=1,Y=2,W=3,H=4;
let parsed = d.map(l => /#(\d+) @ (\d+),(\d+): (\d+)x(\d+)/.exec(l))
                .map(l => l.slice(1,6).map(x=>parseInt(x)));

let maxw = 0, maxh = 0, matrix = [], xproto = [], count = 0;

for (let line of parsed) {
  maxw = Math.max(maxw, line[X]+line[W]+1)
  maxh = Math.max(maxh, line[Y]+line[H]+1)
}

for (let x = 0; x < maxw; x++) xproto[x] = 0;
for (let y = 0; y < maxh; y++) matrix.push(xproto.slice(0));

// Part One
for (let line of parsed) {
  for (let y = line[Y]; y < line[Y]+line[H]; y++) {
    for (let x = line[X]; x < line[X]+line[W]; x++) {
      matrix[y][x]++;
    }
  } 
}

for (let x = 0; x < maxw; x++) {
  for (let y = 0; y < maxh; y++) {
    if (matrix[y][x] > 1) count++;
  }
}

console.log(count);

// Part Two
for (let line of parsed) {
  let broken = false;
  seeker:
  for (let y = line[Y]; y < line[Y]+line[H]; y++) {
    for (let x = line[X]; x < line[X]+line[W]; x++) {
      if (matrix[y][x] != 1) {
        broken = true;
        break seeker;
      }
    }
  } 
  if (!broken) console.log(line[ID]);
}