import sys

def step(cups, cur):
    pickup = cups[1:4]
    ccup = cups[0]
    ncup = ccup - 1
    while ncup in pickup or ncup not in cups:
        ncup -= 1
        if ncup < min(cups):
            ncup = max(cups)
    tgt = cups.index(ncup)
    #print(f"{ncup=}, {tgt=}")
    cups[1:(tgt-2)] = cups[4:(tgt+1)]
    cups[(tgt-2):(tgt+1)] = pickup
    cups.append(cups.pop(0))
    return cups, 0


def genresult(cups):
    n1 = []
    n2 = []
    l = len(cups)
    i = 0
    while cups[i] != 1 and i < l:
        n1.append(cups[i])
        i += 1
    i += 1
    while i < l:
        n2.append(cups[i])
        i += 1
    return ''.join(str(n) for n in n2 + n1)
        

def main():
    # cups = [int(c) for c in input("initial numbers:")]
    # N = int(input("moves:"))
    cups = [int(c) for c in sys.argv[1]]
    N = int(sys.argv[2])
    cur = 0
    for _ in range(N):
        if N < 20:
            print(f"{cups=}")
        cups, cur = step(cups, cur)
    print(f"after {N} moves: {genresult(cups)}")


if __name__ == '__main__':
    main()
