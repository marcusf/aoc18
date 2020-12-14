#import <stdio.h>
#import <math.h>
#import <stdlib.h>
#import <stdint.h>
#import <stdbool.h>
#import "types.h"
#import "minheap.h"

#define SCATTER 10000
#define POINTS 4

// shortest dist is 97816347

int read_file(char fname[], Bot ps[1000]) {
  FILE *input = fopen(fname, "r");
  char line[50];
  int i=0;
  while (fgets(line, 50, input) != NULL) {
    sscanf(line, "pos=<%lld,%lld,%lld>, r=%lld",
      &ps[i].p.x, &ps[i].p.y, &ps[i].p.z, &ps[i].r);
    i++;
  }
  return i;
}

int64_t d(Point p0, Point p1) {
  return llabs(p1.x-p0.x)+llabs(p1.y-p0.y)+llabs(p1.z-p0.z);
}

int in_range(Point p, Bot bots[], int nbots) {
  int amount=0;
  for (int i = 0; i<nbots; i++) {
    if (d(p, bots[i].p) <= bots[i].r) {
      amount++;
    }
  }
  if (amount == 1000) {
    printf("%lld\n",d(p, bots[100].p));
  }
  return amount;
}

int64_t max(int64_t a, int64_t b) {
  return a > b ? a : b;
}

int64_t mrand(int64_t clamp) {
  return -clamp + (rand() % (2*clamp));
}

void generate_points(Point p, Point points[], int npoints, int range) {
  int delta = range/100, i = 0;
  for (int i = 0; i < npoints; i++) {
    points[i].x = p.x + mrand(range);
    points[i].y = p.y + mrand(range);
    points[i].z = p.z + mrand(range);
  }
}

Cover new_cover(Bot bots[], int nbots) {
  Point start_point;
  Cover start_cover;
  int cover;
  start_point.x=mrand(5000000);
  start_point.y=mrand(5000000);
  start_point.z=mrand(5000000);
  cover = in_range(start_point, bots, nbots);
  start_cover.p=start_point; 
  start_cover.cover=cover; 
  start_cover.var=100000000;
  return start_cover;
}

int main(int argc, char **argv) {

  Bot points[1000];

  Point scatter[SCATTER];

  int npoints, cover;
  Point start_point;
  Cover start_cover;
  
  srand(time(NULL));
  npoints = read_file("23.in", points);

  Cover queue[POINTS];
  int cpoint = 0;

  for (int i = 0; i < POINTS; i++) {
    queue[i] = new_cover(points, npoints);
  }

  Point max_point;
  int max_cover, max_max = 0, since_reset = 0;
  int64_t shortest_dist = 9999999999;
  Point max_max_point = queue[0].p;
  bool reset_variance = false;


  while (1) {
    Cover point = queue[cpoint%POINTS];

    generate_points(point.p, scatter, SCATTER, point.var);
    max_cover = point.cover;
    max_point = point.p;
    int64_t shortest_d = 999999999999;

    for (int i = 0; i < SCATTER; i++) {
      cover = in_range(scatter[i], points, npoints);
      if (cover > max_cover) {
        max_cover = cover;
        max_point = scatter[i];
      }
      if (cover == max_cover) {
        int64_t dist = llabs(max_point.x)+llabs(max_point.y)+llabs(max_point.z);
        if (dist < shortest_d) {
          max_cover = cover;
          max_point = scatter[i];
        }
      }
    }
    if (max_cover >= max_max) {
      int64_t dist = llabs(max_point.x)+llabs(max_point.y)+llabs(max_point.z);
      if (dist < shortest_dist || max_cover > max_max) {
        shortest_dist = dist;
        printf("Shortest distance is %lld\n", shortest_dist);
      }
    }
    if (max_cover > max_max) {
      max_max = max_cover;
      max_max_point = max_point;
      since_reset = 0;
      printf("Max cover is: %d at (%lld,%lld,%lld)\n", 
        max_max, 
        max_max_point.x,
        max_max_point.y,
        max_max_point.z);
    } else {
      since_reset++;
    }

    point.p = max_point;
    point.cover = max_cover;
    point.var = max(100,ceil(since_reset < 100 ? point.var / 1.05 : point.var * 1.05));

    queue[cpoint%POINTS] = point;
    cpoint++;

  }

  return 0;
}