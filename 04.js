const fs = require('fs');

const START = 'start', SLEEPS = 'sleeps', WAKES = 'wakes';

let parse = line => {
  let date = line.substr(1,16); // [1518-09-29 00:18]
  let rest = line.substr(19);
  let guard = -1, state = START;
  if (rest == 'wakes up') {
    state = WAKES;
  } else if (rest == 'falls asleep') {
    state = SLEEPS;
  } else {
    guard = parseInt(/Guard #(\d+) begins shift/.exec(rest)[1]);
  }
  return {date: new Date(date), state: state, guard: guard};
}

let sleep = lines => {
  let output = [], guard = -1;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].guard != -1) guard = lines[i].guard;
    if (lines[i].state == WAKES) {
      if (lines[i-1].state != SLEEPS) {
      }
      let mins = (lines[i].date.getMinutes() - lines[i-1].date.getMinutes());
      output.push([guard, lines[i-1].date.getMinutes(), mins]);
    }
  }
  return output;
}

let calcSleep = (data, map) => {
  for (const line of data) {
    map[line[0]].time += line[2];
    for (let i = 0; i < line[2]; i++) {
      map[line[0]].sleep[line[1]+i]++;
    }
  }
}

let buildMap = (data) => {
  let hproto = [], guardmap = {};
  for (let i = 0; i < 60; i++) hproto[i] = 0;
  data.forEach(v => guardmap[v[0]] = { time: 0, sleep: hproto.slice(0) })
  calcSleep(data, guardmap);
  return guardmap;
}

let buildDurationsAndMaxMinutes = (map) => {
  let massaged = [];
  for (const [k, v] of Object.entries(map)) {
    massaged.push([parseInt(k), v.time, 
      v.sleep.indexOf(Math.max(...v.sleep)),
      Math.max(...v.sleep)])
  }
  return massaged;
}


let d = fs.readFileSync('04.txt', 'utf8').split('\n')
            .map(parse).sort((a,b) => a.date - b.date);

let data = sleep(d).sort((a,b) => a[0] - b[0]);

let guardmap = buildMap(data);
let answer = buildDurationsAndMaxMinutes(guardmap);

// Solution One
let answer1 = answer.sort((a,b) => b[1]-a[1]);
console.log(answer1[0][0]*answer1[0][2]);

// Solution Two
let answer2 = answer.sort((a,b) => b[3]-a[3]);
console.log(answer2[0][0]*answer2[0][2]) 