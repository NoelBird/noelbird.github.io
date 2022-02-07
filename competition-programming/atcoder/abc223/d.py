# 4 3
# 2 1
# 3 4
# 2 4

from collections import defaultdict
from heapq import heappush, heappop

N, M = map(int, input().split())

graph = defaultdict(list)
indegree = defaultdict(int)
for _ in range(M):
    a, b = map(int, input().split())
    graph[a].append(b)
    indegree[b] += 1

result = []
q = []
for key in range(1, N+1):
    if indegree[key] == 0:
        heappush(q, key)

while q:
    cur = heappop(q)
    result.append(cur)

    for item in graph[cur]:
        indegree[item] -= 1
        if indegree[item] == 0:
            heappush(q, item)

if len(result) == N:
    print(*result, sep=" ")
else:
    print(-1)