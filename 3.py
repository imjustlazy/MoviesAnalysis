def fibonacci(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    return fibonacci(n-1) + fibonacci(n-2)

if __name__=="__main__":
    n = int(input())
    # print(fibonacci(n))
    f = [x for x in range(100000)]
    f[0] = 1; f[1] = 2
    for i in range(len(f)):
        if i > 1:
            f[i] = f[i-1] + f[i-2]
    print(f[n-1])