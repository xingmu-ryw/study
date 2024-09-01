for i in range(1, 10):
    print()
    # 为了跟乘法口诀表一样的格式，不加此print的话，只有一个print且有end，那么就会都在一行
    for j in range(1, i+1):
        print("%d*%d=%d" % (i, j, i*j), end=" ")
