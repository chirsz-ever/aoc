#[derive(Debug, Clone, Copy, Default)]
struct Node {
    next: u32,
}

const fn node(next: u32) -> Node {
    Node { next }
}

fn main() {
    let mut cups = makecups();
    let mut cur = cups[CUPS].next;
    for _ in 0..MOVES {
        cur = step(&mut cups, cur);
    }
    let n1 = cups[1].next as u64;
    let n2 = cups[cups[1].next as usize].next as u64;
    println!("result: {} * {} = {}", n1, n2, n1 * n2);
}

const CUPS: usize = 1_000_000;
const MOVES: usize = 10_000_000;

fn makecups() -> Vec<Node> {
    let mut cups = Vec::with_capacity(CUPS + 1);
    cups.push(node(0));
    let args = std::env::args().collect::<Vec<_>>();
    let init_cups = args[1]
        .chars()
        .map(|c| c.to_digit(10).unwrap() as usize)
        .collect::<Vec<_>>();
    let init_len = init_cups.len();
    cups.resize_with(init_len + 1, Default::default);
    for s in init_cups.windows(2) {
        cups[s[0]].next = s[1] as _;
    }
    cups[init_cups.last().copied().unwrap()].next = (init_len + 1) as _;
    for n in (init_len as u32 + 2)..(CUPS as u32 + 1) {
        // cups[n - 1].next = n;
        cups.push(node(n));
    }
    cups.push(node(init_cups[0] as _));
    cups
}

fn step(cups: &mut [Node], cur: u32) -> u32 {
    let cur = cur as usize;
    let mut tgt = cur;
    let n1 = cups[cur].next as usize;
    let n2 = cups[n1].next as usize;
    let n3 = cups[n2].next as usize;
    let n4 = cups[n3].next;
    while tgt == cur || tgt == n1 || tgt == n2 || tgt == n3 {
        tgt -= 1;
        if tgt == 0 {
            tgt = CUPS;
        }
    }
    let tgt_next = cups[tgt].next;
    cups[cur].next = n4;
    cups[tgt].next = n1 as _;
    cups[n3].next = tgt_next;
    n4
}
