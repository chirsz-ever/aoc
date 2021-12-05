
tst = int(input())

ids = [ int(w) for w in input().split(',') if w != 'x' ]

def wait_time(bus_id):
    return (bus_id - tst % bus_id, bus_id)

min_id = min(map(wait_time, ids))

print(f"{min_id=}")
