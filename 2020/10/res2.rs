#[allow(unused_imports)]
use std::cmp::Ordering::*;
use std::collections::HashSet;
use std::io;

fn main() {
    let nums = {
        let mut nums = Vec::with_capacity(106);
        let mut s = String::new();
        io::stdin().read_line(&mut s).unwrap();
        while !s.trim().is_empty() {
            nums.push(s.trim().parse::<u32>().unwrap());
            s.clear();
            io::stdin().read_line(&mut s).unwrap();
        }
        nums.push(0);
        nums.sort();
        nums.push(nums.last().unwrap() + 3);
        nums
    };
    let mut ways = vec![0u64; nums.len()];
    ways[0] = 1;
    ways[1] = calc_ways(nums[1], &[(0, 1)]);
    ways[2] = calc_ways(nums[2], &[(0, 1), (nums[1], ways[1])]);
    for i in 3..nums.len() {
        ways[i] = calc_ways(
            nums[i],
            &[
                (nums[i - 3], ways[i - 3]),
                (nums[i - 2], ways[i - 2]),
                (nums[i - 1], ways[i - 1]),
            ],
        )
    }
    let total_ways = ways.last().unwrap();
    dbg!(total_ways);
}

fn calc_ways(n: u32, nws: &[(u32, u64)]) -> u64 {
    let mut wn = 0;
    for (sn, w) in nws {
        if n - sn <= 3 {
            wn += w;
        }
    }
    wn
}
