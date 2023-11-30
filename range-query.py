from dataclasses import dataclass
import math
import pandas as pd
import numpy as np

@dataclass
class Node:
    low: float
    high: float
    cnt: int
    noisy_cnt: float=0

# epsilon-DP mechanism
def laplace_mech(v, sensitivity, epsilon):
    return v + np.random.laplace(loc=0, scale=sensitivity / epsilon)

def query(data: list[Node], a: float, b: float) -> int:
    nodes= query_nodes(data, a, b)
    count=0
    for n in nodes:
        count += n.cnt
    return count

def noisy_query(data: list[Node], a: float, b: float) -> int:
    nodes= query_nodes(data, a, b)
    count=0
    for n in nodes:
        count += n.noisy_cnt
    return count

def query_nodes(data: list[Node], a: float, b: float) -> list[Node]:
    result = []
    for e in data:
        if a <= e.low and b >= e.high:
            if e.low - a > 0:
                result += query_nodes(data, a, e.low - 1)
            result.append(e)
            if b - e.high > 0:
                result += query_nodes(data, e.high + 1, b)
            break
    return result

def counts(tree: list[Node],df) -> list[Node]:
    # Big-O(N)
    i= len(tree)-1
    while i >=0:
        if tree[i].low == tree[i].high:
            tree[i].cnt = df[df == tree[i].low].count()
            tree[i].cnt = df[df == tree[i].low].count()
        else:
            tree[i].cnt +=tree[2*i+1].cnt
            tree[i].cnt +=tree[2*i+2].cnt
        i -=1
    return tree

def noisy_counts(tree: list[Node],df) -> list[Node]:
    # Big-O(N)
    i= len(tree)-1
    while i >=0:
        tree[i].noisy_cnt=laplace_mech(tree[i].cnt,1, (1/np.log2(128)))
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

    #3. populate the tree
    tree=counts(lst,df)
    #4. populate the noisy tree
    noisy_tree = noisy_counts(tree, df)
    #5. query samples, testing section
    # print the root node count, should return the whole df count
    print("count: ",query(tree, 0,128))
    print("noisy_count: ",noisy_query(noisy_tree, 0, 128))
    #
    # print(query(tree, 1, 1))
    # print(df[df==1].count())
    #
    # print(query(tree, 0, 50))
    # print(df[(df >= 0) & (df <= 50)].count())
    #
    # print(query(tree, 0, 90))
    # print(df[(df >= 0) & (df <= 90)].count())
    #
    # # test DP query on our range tree
    # x=laplace_mech(query(tree, 0, 90), 1, 0.1) # count query sens =1/ epsilon=1
    # print("noisy count ",x)
