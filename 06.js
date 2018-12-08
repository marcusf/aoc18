const d = require('fs').readFileSync('06.txt','utf8')
const points = d.split('\n').map(l=>l.split(', ').map(i=>+i));
const xs = points.map(([w,h])=>w), ys = points.map(([w,h])=>h);

const width = Math.max(...xs), height = Math.max(...ys);
const maxw = Math.max(...xs), maxh = Math.max(...ys), 
      minw = Math.min(...xs), minh = Math.min(...ys);
 
const grid = Array(width * height).fill(-19);

const dist = (x1,y1,x2,y2) => Math.abs(x2-x1)+Math.abs(y2-y1);
const closest = (x,y,points) => {
  let distances = points.map(([x2,y2],i) => [dist(x,y,x2,y2), i]).sort((a,b) => a[0]-b[0]);
  let min = distances[0][0];
  return distances.filter(([x,]) => x == min);
}

for (let point = 0; point <= grid.length-1; point++) {
  const x = point % width, y = ~~(point / width);
  const distances = closest(x, y, points);
  grid[point] = distances.length == 1 ? distances[0][1] : -19;
}

const boundary = [-19];
for (let point = 0; point <= grid.length-1; point++) {
  const x = point % width, y = ~~(point / width);
  if (x == maxw || x == minw || y == maxh || y == minh) 
    boundary.push(grid[point]);
}

const output = grid.sort().filter(l => boundary.indexOf(l) < 0);

let winner = -2, length = 0, current = -2, curlen = 0;
for (const cell of output) {
  if (cell != current) {
    curlen = 0;
    current = cell;
  }
  curlen++;
  if (curlen > length) {
    length = curlen;
    winner = current;
  }
}

console.log(winner, length);
