#![allow(dead_code)]

use std::io;
use std::time;

type Map = Vec<Vec<char>>;

fn do_slide(map: &mut Map, move_step: (i32, i32)) {
    let height = map.len();
    let width = map[0].len();

    let (d1_size, d2_size, d2_step);
    let get_map: fn(&Map, usize, usize) -> char;
    let set_map: fn(&mut Map, usize, usize, char);
    if move_step.0 != 0 {
        d1_size = width;
        d2_size = height;
        get_map = |map, d1, d2| map[d2][d1];
        set_map = |map, d1, d2, v| map[d2][d1] = v;
        d2_step = -move_step.0;
    } else {
        d1_size = height;
        d2_size = width;
        get_map = |map, d1, d2| map[d1][d2];
        set_map = |map, d1, d2, v| map[d1][d2] = v;
        d2_step = -move_step.1;
    }

    let (d2_begin, d2_end): (i32, i32) = if d2_step > 0 {
        (0, d2_size as i32)
    } else {
        (d2_size as i32 - 1, -1)
    };

    for d1 in 0..d1_size {
        let mut slide_target = None;
        let mut d2 = d2_begin;
        while d2 != d2_end {
            let d2u = d2 as usize;
            match (get_map(map, d1, d2u), slide_target) {
                ('#', _) => slide_target = None,
                ('.', None) => slide_target = Some(d2u),
                ('O', Some(st)) if st < d2_size => {
                    set_map(map, d1, st, 'O');
                    set_map(map, d1, d2u, '.');
                    slide_target = Some((st as i32 + d2_step) as _);
                }
                _ => {}
            }
            d2 += d2_step;
        }
    };
}

fn calc_load(map: &Map) -> usize {
    let height = map.len();
    let mut load = 0;
    for (i, row) in map.iter().enumerate() {
        load += (height - i) * row.iter().filter(|&&c| c == 'O').count();
    }
    return load;
}

fn print_map(map: &Map) {
    for row in map.iter() {
        for c in row.iter() {
            print!("{c}");
        }
        println!();
    }
}

fn main() {
    let mut input = {
        let mut input = Vec::new();
        let mut s = String::new();
        io::stdin().read_line(&mut s).unwrap();
        while !s.trim().is_empty() {
            input.push(s.trim().bytes().map(|b| b as char).collect());
            s.clear();
            io::stdin().read_line(&mut s).unwrap();
        }
        input
    };

    const N: usize = 1000000000;
    // const N: usize = 3;
    const T: usize = 1000;
    let mut last_time = time::Instant::now();
    for k in 0..N {
        do_slide(&mut input, (-1, 0));
        do_slide(&mut input, (0, -1));
        do_slide(&mut input, (1, 0));
        do_slide(&mut input, (0, 1));
        // print_map(&input);
        // println!();
        if k % (N / T) == 0 {
            let now = time::Instant::now();
            println!("{}/{} need {:?}", k / (N / T), T, now.duration_since(last_time) * T as u32);
            last_time = now;
        }
    }
    println!("load = {}", calc_load(&input));
}
