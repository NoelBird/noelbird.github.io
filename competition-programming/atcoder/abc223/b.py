x = input()
 
max_x = x
min_x = x
for _ in range(len(x)):
  new_x = x[-1] + x[0:-1]
  if new_x > max_x:
    max_x = new_x
  if new_x < min_x:
    min_x = new_x
  x = new_x

print(min_x)
print(max_x)