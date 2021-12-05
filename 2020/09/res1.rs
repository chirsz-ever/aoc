use std::io;
use std::collections::HashSet;
use std::cmp::Ordering::*;

fn main() {
    let nums = {
        let mut nums = Vec::with_capacity(1000);
        let mut s = String::new();
        io::stdin().read_line(&mut s).unwrap();
        while !s.trim().is_empty() {
            nums.push(s.trim().parse::<u64>().unwrap());
            s.clear();
            io::stdin().read_line(&mut s).unwrap();
        }
        nums
    };
    let mut n = 0;
    for i in 25..nums.len() {
        if !check_two_sum(nums[i], &nums[i-25..i]) {
            println!("{}", nums[i]);
            n = nums[i];
            break;
        }
    }
    let mut l = 0usize;
    let mut r = 1usize;
    while l < r && r < nums.len() {
        let sum_range: u64 = nums[l..=r].iter().sum();
        match sum_range.cmp(&n) {
            Less => {
                r += 1;
            }
            Greater => {
                l += 1;
            }
            Equal => break,
        }
    }
    dbg!(l..=r);
    let subnums = &nums[l..=r];
    let max = subnums.iter().max().unwrap();
    let min = subnums.iter().min().unwrap();
    dbg!(max, min);
    dbg!(max + min);
}

fn check_two_sum(n: u64, ns: &[u64]) -> bool {
    let mut m = HashSet::with_capacity(25);
    for &ln in ns {
        if n >= ln {
            if m.contains(&(n - ln)) {
                return true;
            } else {
                m.insert(ln);
            }
        }
    }
    return false;
}
