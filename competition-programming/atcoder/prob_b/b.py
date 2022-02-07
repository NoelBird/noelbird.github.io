N, P = map(int, input().split())
print(sum(map(lambda x: int(x) < P, input().split())))
