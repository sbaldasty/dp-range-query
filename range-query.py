import pandas as pd
import numpy as np
from dataclasses import dataclass

@dataclass
class Node:
    low: int
    high: int
    cnt: int
    noisy_cnt: float=0

@dataclass
class Solution:
    addition_nodes: list[Node]
    subtraction_nodes: list[Node]

# epsilon-DP mechanism
def laplace_mech(v, sensitivity, epsilon):
    return v + np.random.laplace(loc=0, scale=sensitivity / epsilon)

# The query function performs the query using the query_nodes function
# on a non-noisy tree, so it receives the counts from the cnt attribute of the node
def query(data: list[Node], a: float, b: float) -> int:
    nodes= query_nodes(data, a, b)
    count=0
    for n in nodes:
        count += n.cnt
    return count

# The noisy_query function performs the query using the query_nodes function
# on a noisy tree, so it receives the counts from the noisy_cnt attribute of the node
def noisy_query(data: list[Node], a: float, b: float) -> int:
    nodes= query_nodes(data, a, b)
    count=0
    for n in nodes:
        count += n.noisy_cnt
    return count

# The query_nodes function performs the query provided on each node of the tree,
# returning the amount of items within the range provided in the query
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

# The counts function calculates what the count should be for each node
# The count is the amount of items within the range of that node
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

# The noisy_counts function adds noise to the count of each node in the tree
def noisy_counts(tree: list[Node], epsilon: float) -> list[Node]:
    # Big-O(N)
    i= len(tree)-1
    e = epsilon / np.log2(len(tree))
    while i >=0:
        tree[i].noisy_cnt=laplace_mech(tree[i].cnt,1, e)
        i -=1
    return tree

def build_tree(lower_bound: int, upper_bound: int):
    rng = upper_bound - lower_bound
    pot = 1
    lst = [pot]
    while pot < rng:
        pot *= 2
        lst.insert(0, pot)

    tree = []
    for x in lst:
        for y in range(lower_bound, lower_bound + pot, x):
            tree.append(Node(y, x + y - 1, 0))

    return tree

def epsilon_gen(num):
    epsilons = np.geomspace(0.2,1,num)
    return np.delete(epsilons, 0)

if __name__ =='__main__':
    epsilons = epsilon_gen(50)
    print(epsilons)
    exit(0)
    #1. built a tree
    lst = build_tree(0, 100)

    #2. load the dataset to a dataframe
    adult = pd.read_csv('https://github.com/jnear/cs3110-data-privacy/raw/main/homework/adult_with_pii.csv')
    df = adult['Age']

    #3. populate the tree
    tree=counts(lst,df)
    #4. populate the noisy tree
    noisy_tree = noisy_counts(tree, 1.0)
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
