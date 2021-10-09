# top-down, bottom-up both method failed
# TLE...

from collections import defaultdict
N = int(input())

A = list(map(int, input().split()))
B = list(map(int, input().split()))


MOD = 998244353
INT_MAX = 3000
 
dp = [1] * (INT_MAX + 1)
for i in range(N):
    dp_i = [0] * (INT_MAX + 1)
    for j in range(A[i], B[i] + 1):
        dp_i[j] = dp[j]
    dp = dp_i
    for j in range(INT_MAX):
        dp[j + 1] += dp[j]
        dp[j + 1] %= MOD
 
print(dp[-1])