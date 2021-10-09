# 2
# 1 1
# 2 3

# TLE - 6/21

import sys
sys.setrecursionlimit(1000000000)

N = int(input())

A = list(map(int, input().split()))
B = list(map(int, input().split()))

cache = {} # state i, score

def solution(n_step, val):
    if n_step == 0:
        return 1
    elif cache.get((n_step, val)):
        return cache[(n_step, val)]
    
    res = 0
    for i in range(A[n_step-1], B[n_step-1] + 1):
        if i > val:
            continue
        res += solution(n_step-1, i)
    res %= 998244353
    cache[(n_step, val)] = res
    return res

res = 0
for i in range(A[-1], B[-1]+1):
    res += solution(N-1, i)

print(res % 998244353)
