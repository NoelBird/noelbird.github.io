# 4
# 1
# 7
# 10
# 999983

def is_multiple_of_n(n, x):
    if x % n == 0:
        return True
    else:
        return False

def gen_2(n):
    ret = "2"*n
    return int(ret)

for i in range(2, 11):
    print(i, gen_2(i-1))
    print(is_multiple_of_n(i, gen_2(i-1)))