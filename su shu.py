sum = 0
for i in range(101, 201):
    a = 0
    for m in range(2,i):
        if i % m == 0:
            a = 1
    if a != 1:
        sum += 1
        print(i)
print('共有%d个素数' %(sum))

