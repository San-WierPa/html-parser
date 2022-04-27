# def fibo(n):
#    if not isinstance(n, int):
#        raise TypeError("Fibonacci sequence is only defined for integer values.")
#    elif n < 0:
#        raise ValueError("Fibonacci sequence is only defined for non-negative n.")
#    elif n < 2:
#        return 1
#    else:
#        return fibo(n - 1) + fibo(n - 2)


def fibo(n):
    _fibo = [1, 1]
    if not isinstance(n, int):
        raise TypeError("Fibonacci sequence is only defined for integer values.")
    elif n < 0:
        raise ValueError("Fibonacci sequence is only defined for positive n.")
    else:
        while len(_fibo) <= n:
            _fibo.append(_fibo[-1] + _fibo[-2])
        return _fibo[n]
