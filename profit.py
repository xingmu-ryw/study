# 1.用连两个列表，一个代表利率，一个代表区间
# 2.列表需要倒过来写，先写较大数，从上到下取
i = int(input('净利润：'))
arr = [1000000, 600000, 400000, 200000, 100000, 0]
arr_1 = [0.01, 0.015, 0.03, 0.05, 0.075, 0.1]
r = 0
for idx in range(0, 6):
    if i > arr[idx]:
        r = r + (i-arr[idx])*arr_1[idx]
        print((i-arr[idx])*arr_1[idx])
        i = arr[idx]
print(r)
