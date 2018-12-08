const d = require('fs').readFileSync('07.txt','utf8')

const vertices = d.split('\n').map(s => / ([A-Z]).*step ([A-Z])/.exec(s).slice(1,3).map(a => a.charCodeAt(0)-65));

const bfs = (graph) => {
  let queue = [], results = [];
  const indegree = Array(new Set(graph.map(([a,b]) => a).concat(graph.map(([a,b]) => b))).size).fill(0);
  for (const [a,b] of graph) indegree[b] = indegree[b]+1;
  for (const [node,i] of indegree.entries()) if (i == 0) queue.push(node);

  while (queue.length > 0) {
    queue = queue.sort((a, b) => a - b);
    let vertex = queue.shift();
    results.push(vertex);

    for (const [a,b] of graph) {
      if (a == vertex) {
        indegree[b]--;
        if (indegree[b] == 0) queue.push(b);
      }
    }
  }
  return results;
}

console.log(bfs(vertices).map(n => String.fromCharCode(n+65)).join(''));

const WORKERS = 5, DELAY = 60;

const delayed_bfs = (graph) => {
  let queue = [], elves = Array(WORKERS).fill([]).map((a,i) => [-1, 0]), ticks = -1;

  const indegree = Array(new Set(graph.map(([a,b]) => a).concat(graph.map(([a,b]) => b))).size).fill(0);
  for (const [a,b] of graph) indegree[b] = indegree[b]+1;
  for (const [node,i] of indegree.entries()) if (i == 0) queue.push(node);

  do {
    ticks++;
    elves = elves.map(([e,t,i]) => [e, Math.max(0, t-1)]);

    while (queue.length > 0 && elves[0][1] == 0) {
      queue = queue.sort((a, b) => a - b);
      let vertex = queue.shift();
      elves[0] = [vertex, DELAY + (1 + vertex)];
      elves = elves.sort(([,t0],[,t1]) => t0 - t1);
    }

    for (const [vertex, time] of elves) {
      if (time == 1 && vertex >= 0) {
        for (const [a,b] of graph) {
          if (a == vertex) {
            indegree[b]--;
            if (indegree[b] == 0) {
              queue.push(b);
            }
          }
        }
      }
    }
  } while (elves.reduce((a,[,b,]) => a+b, 0) > 0 || queue.length > 0);

  return ticks;
}

console.log(delayed_bfs(vertices));
