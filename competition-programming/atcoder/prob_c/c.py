# 2 3
# GCP
# PPP
# CCC
# PPC

N, M = map(int, input().split())

l = []
scores = [0] * (2*N)
standings = [i for i in range(2*N)]

for i in range(N*2):
    l.append(input())

def sort_key(x):
    return scores[x], -x

for i in range(M):
    next_standings = []
    for j in range(N):
        A, B = standings[2*j], standings[2*j+1]
        if l[A][i] == "G" and l[B][i] == "C":
            scores[A] += 1
        elif l[A][i] == "G" and l[B][i] == "P":
            scores[B] += 1
        elif l[A][i] == "G" and l[B][i] == "G":
            pass
        elif l[A][i] == "C" and l[B][i] == "C":
            pass
        elif l[A][i] == "C" and l[B][i] == "P":
            scores[A] += 1
        elif l[A][i] == "C" and l[B][i] == "G":
            scores[B] += 1
        elif l[A][i] == "P" and l[B][i] == "C":
            scores[B] += 1
        elif l[A][i] == "P" and l[B][i] == "P":
            pass
        elif l[A][i] == "P" and l[B][i] == "G":
            scores[A] += 1
    standings.sort(key=lambda x: sort_key(x), reverse=True)
res = list(map(lambda x: x+1, standings))
for i in res:
    print(i)