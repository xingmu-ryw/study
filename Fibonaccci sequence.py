def fib(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fib(n-1)+fib(n-2)


n = int(input('需输出第几个斐波那契数：'))
print(fib(n))
