def reduce_num(n):
    if not isinstance(n, int) or n <= 0:
        print('请输入一个正确的数字：')
    print('{} = '.format(n), end="")
    if n == 1:
        print('{}'.format(n))
    else:
        while n != 1:
            for i in range(2, n+1):
                if n % i == 0:
                    n = n // i
                    if n == 1:
                        print(i)
                    else:
                        print('{} * '.format(i), end="")
                    continue


m = int(input('请输入一个整数：'))
reduce_num(m)
