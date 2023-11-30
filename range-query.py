from dataclasses import dataclass
import math
import pandas as pd

@dataclass
class Node:
    low: float
    high: float
    cnt: int


    

def query(data: list[Node], a: float, b: float) -> list[Node]:
    result = []
    for e in data:
        if a <= e.low and b >= e.high:
            if e.low - a > 0:
                result += query(data, a, e.low - 1)
            result.append(e)
            if b - e.high > 0:
                result += query(data, e.high + 1, b)
            break
    return result

#def counts(data: list[Node], a: float, b: float) -> list[Node]:
#    s = 0
#    for e in query(data, a, b):
#
#cases = [(1, 125)]
#for a, b in cases:
#    print(a, b, query(lst, a, b))

def counts(tree: list[Node],df) -> list[Node]:
    # Big-O(N)
    i= len(tree)-1
    while i >=0:
        if tree[i].low == tree[i].high:
            tree[i].cnt= df[df == tree[i].low].count()
        else:
            tree[i].cnt +=tree[2*i+1].cnt
            tree[i].cnt +=tree[2*i+2].cnt
        i -=1
    return tree

if __name__ =='__main__':

    #1. built a tree
    lst = []
    for x in [128, 64, 32, 16, 8, 4, 2, 1]:
        for y in range(0, 128, x):
            # set our base count values to 0 "null"
            lst.append(Node(y, x + y - 1, 0))

    #2. load the dataset to a dataframe
    adult = pd.read_csv('https://github.com/jnear/cs3110-data-privacy/raw/main/homework/adult_with_pii.csv')
    df = adult['Age']
            