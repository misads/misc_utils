from functools import reduce
from heapq import heappush as hpush, heappop as hpop, heapify as hpify
from bisect import bisect_right as br, bisect_left as bl, insort_right as ir, insort_left as il

arounds = [(-1, 0), (1, 0), (0, -1), (0, 1)]
V = lambda n, default=0: [default for _ in range(n)]
V2 = lambda m, n, default=0: [[default for _ in range(n)] for _ in range(m)]
V3 = lambda l, m, n, default=0: [V2(m, n, default) for _ in range(l)]
V4 = lambda k, l, m, n, default=0: [V3(l, m, n, default) for _ in range(k)]

product = lambda a: reduce(lambda x, y: x * y, a)  # 数组的累乘

lst = lambda b, a=0: list(range(a, b))
make_idx = lambda a: [[num, i] for i, num in enumerate(a)]

push = lambda a, num: list.append(a, num)
lpush = lambda a, num: list.insert(a, 0, num)
pop = lambda a: list.pop(a)
cp = lambda a: list.copy(a)

add = lambda s, num: set.add(s, num)
rm = lambda s, num: set.remove(s, num)

rsort = lambda a: sorted(a, reverse=True)
def bin(num, bits=None):
    res = __builtins__.bin(num)[2:]
    return res if bits is None else '0' * (bits - len(res)) + res
