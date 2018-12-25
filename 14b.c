#import <stdio.h>
#import <stdlib.h>

int MAX_SIZE = 100*1000*1000;

int is_match(unsigned short *r, int i) {
  return r[i  ]==5 && r[i+1]==0 && 
         r[i+2]==9 && r[i+3]==6 && 
         r[i+4]==7 && r[i+5]==1;
}

int add_n_to_arr(int n, int i, unsigned short *l) {
  switch (n) {
    case 0: case 1: case 2: case 3: case 4: 
    case 5: case 6: case 7: case 8: case 9: l[i] = n; return 1;
    case 10: l[i] = 1; l[i+1] = 0; return 2;
    case 11: l[i] = 1; l[i+1] = 1; return 2;
    case 12: l[i] = 1; l[i+1] = 2; return 2;
    case 13: l[i] = 1; l[i+1] = 3; return 2;
    case 14: l[i] = 1; l[i+1] = 4; return 2;
    case 15: l[i] = 1; l[i+1] = 5; return 2;
    case 16: l[i] = 1; l[i+1] = 6; return 2;
    case 17: l[i] = 1; l[i+1] = 7; return 2;
    case 18: l[i] = 1; l[i+1] = 8; return 2;
    default: printf("Number out of bounds: %d\n", n); return -1;
  }
}

int main(int argc, char **argv) {
  unsigned short *recipes = malloc(MAX_SIZE*sizeof(unsigned short));
  int e1 = 0, e2 = 1, len = 2;

  recipes[0] = 3;
  recipes[1] = 7;

  while (len < MAX_SIZE && (len < 1000 || 0 == is_match(recipes, len-7))) {
    int next = recipes[e1] + recipes[e2];
    len += add_n_to_arr(next, len, recipes);
    e1 = (e1+1+recipes[e1]) % len;
    e2 = (e2+1+recipes[e2]) % len;
  }
  printf("Match found at %d\n", len);
  return 0;
}
