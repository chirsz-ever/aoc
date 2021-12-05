
input1 = None
with open('input') as f:
    input1 = [int(w) for w in f.readline().strip().split(',')]
N = int(input('N: '))

last_index = {n: i for i, n in enumerate(input1[:-1])}

def getnext(nextn, last_index, cnt):
    lnextni = last_index.get(nextn, None)
    if lnextni == None:
        nnextn = 0
    else:
        nnextn = cnt - lnextni
    return nnextn

cnt = len(input1) - 1
nextn = input1[-1]

while cnt < N - 1:
    # if cnt <= 10:
    #     print(f"{cnt=}, {nextn=}, {last_index=}")

    nnextn = getnext(nextn, last_index, cnt)
    last_index[nextn] = cnt
    nextn = nnextn
    cnt += 1



print(f"when {N}, {nextn=}")
