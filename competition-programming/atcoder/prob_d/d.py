# TLE - 6/21

# 2
# 1 1
# 2 3
from collections import defaultdict
N = int(input())

A = list(map(int, input().split()))
B = list(map(int, input().split()))

cache = {} # state i, score

start_list = list(range(A[0], B[0]+1))


prev_res = defaultdict(int)
for i in range(A[0], B[0]+1):
    prev_res[i] = 1
sum_prev = sum(prev_res.values())
for k in range(N-1):
    res = defaultdict(int)
    for i in range(A[k+1], B[k+1]+1):
        if i >= B[k]:
            res[i] = sum_prev
        else:
            for j in range(A[k], B[k]+1):
                if i >= j:
                    res[i] += prev_res[j]
        res[i] %= 998244353
    prev_res = res
    sum_prev = sum(prev_res.values())

print(sum(res.values()) % 998244353)
