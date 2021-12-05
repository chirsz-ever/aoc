import sys


def modexp(M, s, n):
    '''calculate s**n % M'''
    assert n >= 0
    assert M > 2
    s %= M
    def loop(k):
        if k == 0:
            return 1
        elif k == 1:
            return s
        h = loop(k // 2)
        if k % 2 == 0:
            return h * h % M
        else:
            return h * h * s % M
    return loop(n)

def modlog(M, s, t):
    '''find n make s**n % M == t'''
    assert M > 2
    s %= M
    t %= M
    t1 = 1
    for n in range(0, M):
        if t1 == t:
            return n
        t1 *= s
        t1 %= M
    raise RuntimeError(f"Can't calculate modlog({M}, {s}, {t})")


P = 20201227

def main():
    c_pbk = 0
    d_pbk = 0
    if len(argv := sys.argv) > 2:
        c_pbk = int(argv[1])
        d_pbk = int(argv[2])
    else:
        c_pbk = int(input("card public key:"))
        d_pbk = int(input("door public key:"))

    c_lpsz = modlog(P, 7, c_pbk)
    d_lpsz = modlog(P, 7, d_pbk)
    print(f"{c_lpsz=}")
    print(f"{d_lpsz=}")

    ecrypk = modexp(P, d_pbk, c_lpsz)

    print(f"encryption key = {ecrypk}")

if __name__ == '__main__':
    main()
