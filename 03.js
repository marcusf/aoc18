const fs = require('fs');
let d = fs.readFileSync('03.txt', 'utf8').split('\n');

//#1336 @ 916,193: 22x27
//id x y w h
const ID=0,X=1,Y=2,W=3,H=4;
let parsed = d.map(l => /#(\d+) @ (\d+),(\d+): (\d+)x(\d+)/.exec(l))
                .map(l => l.slice(1,6).map(x=>parseInt(x)));

let width = 0, height = 0, matrix = [], xproto = [], count = 0;

for (const [_,x,y,w,h] of parsed) {
  width = Math.max(width, x+w)
  height = Math.max(height, y+h)
}

for (let y = 0; y < height; y++) matrix.push(Array(width).fill(0));

// Part One
for (const [_,X,Y,W,H] of parsed) {
  for (let y = Y; y < Y+H; y++) {
    for (let x = X; x < X+W; x++) {
      matrix[y][x]++;
    }
  } 
}

for (const row of matrix) for (const x of row) if (x > 1) count++;


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