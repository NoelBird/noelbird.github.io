N = int(input())

l = []
for i in range(N):
    l.append(list(map(int, input().split())))

target_time = sum(map(lambda x: x[0]/x[1], l)) / 2

dist = 0
for i in range(N):
    cur_item = l[i]
    cur_time = cur_item[0] / cur_item[1]
    if target_time - cur_time >= 0:
        target_time -= cur_time
        dist += cur_item[0]
    else:
        dist += target_time*cur_item[1]
        break

print(dist)
