from dataclasses import dataclass
import math

@dataclass
class Node:
    low: float
    high: float
    cnt: int

lst = []
for x in [128, 64, 32, 16, 8, 4, 2, 1]:
    for y in range(0, 128, x):
        lst.append(Node(y, x + y - 1, 3))

def query(data: list[Node], a: float, b: float) -> int:
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

cases = [(125, 125), (1, 125)]
for a, b in cases:
    print(a, b, query(lst, a, b))