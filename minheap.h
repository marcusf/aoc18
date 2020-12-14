
/*
    File:   minHeap.c
    Desc:   Program showing various operations on a binary min heap
    Author: Robin Thomas <robinthomas2591@gmail.com>
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "types.h"

#define LCHILD(x) 2 * x + 1
#define RCHILD(x) 2 * x + 2
#define PARENT(x) (x - 1) / 2

typedef struct node { Cover data; } node;
typedef struct MinHeap {
    int size;
    node *elem;
} MinHeap;

MinHeap init_min_heap(int size) {
    MinHeap hp;
    hp.size = 0;
    return hp;
}

void swap(node *n1, node *n2) {
    node temp = *n1;
    *n1 = *n2;
    *n2 = temp;
}

void heapify(MinHeap *hp, int i) {
    int smallest = (LCHILD(i) < hp->size && 
        hp->elem[LCHILD(i)].data.cover < hp->elem[i].data.cover) ? LCHILD(i) : i ;
    if(RCHILD(i) < hp->size && 
        hp->elem[RCHILD(i)].data.cover < hp->elem[smallest].data.cover) {
        smallest = RCHILD(i);
    }
    if(smallest != i) {
        swap(&(hp->elem[i]), &(hp->elem[smallest]));
        heapify(hp, smallest);
    }
}

void insert_node(MinHeap *hp, Cover data) {
    if(hp->size) {
        hp->elem = realloc(hp->elem, (hp->size + 1) * sizeof(node)) ;
    } else {
        hp->elem = malloc(sizeof(node));
    }

    node nd;
    nd.data = data;

    int i = (hp->size)++;
    while(i && nd.data.cover < hp->elem[PARENT(i)].data.cover) {
        hp->elem[i] = hp->elem[PARENT(i)];
        i = PARENT(i);
    }
    hp->elem[i] = nd;
}


Cover pop_node(MinHeap *hp) {
    Cover r;
    if(hp->size) {
        r = hp->elem[0].data;
        hp->elem[0] = hp->elem[--(hp->size)] ;
        hp->elem = realloc(hp->elem, hp->size * sizeof(node)) ;
        heapify(hp, 0) ;
    } else {
        printf("\nMin Heap is empty!\n") ;
        free(hp->elem) ;
    }
    return r;
}


/*
    Function to get maximum node from a min heap
    The maximum node shall always be one of the leaf nodes. So we shall recursively
    move through both left and right child, until we find their maximum nodes, and
    compare which is larger. It shall be done recursively until we get the maximum
    node
*/
Cover get_max_node(MinHeap *hp, int i) {
    if(LCHILD(i) >= hp->size) {
        return hp->elem[i].data ;
    }

    Cover l = get_max_node(hp, LCHILD(i)) ;
    Cover r = get_max_node(hp, RCHILD(i)) ;

    if(l.cover >= r.cover) {
        return l;
    } else {
        return r;
    }
}


/*
    Function to clear the memory allocated for the min heap
*/
void delete_min_heap(MinHeap *hp) {
    free(hp->elem) ;
}
