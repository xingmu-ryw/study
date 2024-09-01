sum = 0
for m in range(100, 1000):
    i = m
    x = i % 10
    i = int(i // 10)
    y = i % 10
    i = int(i // 10)
    z = i
    if m == x*x*x + y*y*y + z*z*z:
        print(m)