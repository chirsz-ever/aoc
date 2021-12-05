#[allow(unused_imports)]

use std::io;
use std::collections::HashSet;
use std::cmp::Ordering::*;

fn main() {
    let nums = {
        let mut nums = Vec::with_capacity(106);
        let mut s = String::new();
        io::stdin().read_line(&mut s).unwrap();
        while !s.trim().is_empty() {
            nums.push(s.trim().parse::<i32>().unwrap());
            s.clear();
            io::stdin().read_line(&mut s).unwrap();
        }
        nums.push(0);
        nums.sort();
        nums.push(nums.last().unwrap() + 3);
        nums
    };
    let mut jd1 = 0;
    let mut jd3 = 0;
    for w in nums.windows(2) {
        match w[1] - w[0] {
            1 => jd1 += 1,
            3 => jd3 += 1,
            _ => {}
        }
    }
    dbg!(jd1);
    dbg!(jd3);
    dbg!(jd1*jd3);
}
