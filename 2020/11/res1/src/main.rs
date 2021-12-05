#![allow(unused_imports)]
#![allow(dead_code)]
use std::cmp::Ordering::*;
use std::collections::HashSet;
use std::io::{self, prelude::*};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Grid {
    Floor,
    Empty,
    Occupied,
}

use Grid::*;

fn main() {
    let mut grids: Vec<Vec<Grid>> = io::stdin()
        .lock()
        .lines()
        .map(|line| {
            line.unwrap()
                .chars()
                .map(|c| match c {
                    'L' => Empty,
                    '#' => Occupied,
                    '.' => Floor,
                    _ => unreachable!(),
                })
                .collect()
        })
        .collect();

    while step(&mut grids) {
        // print_grids(&grids);
        // println!("----------");
    }
    let seats: usize = grids
        .iter()
        .map(|r| r.iter().filter(|g| matches!(g, Occupied)).count())
        .sum();
    // print_grids(&grids);
    dbg!(seats);
}

fn print_grids(grids: &[Vec<Grid>]) {
    for row in grids {
        for g in row {
            let c = match g {
                Floor => '.',
                Empty => 'L',
                Occupied => '#',
            };
            print!("{}", c);
        }
        println!();
    }
}

fn step(grids: &mut Vec<Vec<Grid>>) -> bool {
    let mut changed = false;
    let next_grids = (0..grids.len())
        .map(|row| {
            (0..grids[row].len())
                .map(|col| {
                    let g = step_grid(grids, row, col);
                    if g != grids[row][col] {
                        changed = true;
                    }
                    g
                })
                .collect()
        })
        .collect();
    *grids = next_grids;
    changed
}

fn step_grid(grids: &[Vec<Grid>], row: usize, col: usize) -> Grid {
    match (grids[row][col], count_neighber(grids, row, col)) {
        (Empty, 0) => Occupied,
        (Occupied, n) if n >= 4 => Empty,
        (g, _) => g,
    }
}

fn count_neighber(grids: &[Vec<Grid>], row: usize, col: usize) -> usize {
    let rows = grids.len() as i32;
    let cols = grids[0].len() as i32;
    let get = |r: i32, c: i32| {
        if (0..rows).contains(&r) && (0..cols).contains(&c) {
            grids[r as usize][c as usize]
        } else {
            Floor
        }
    };
    let mut n = 0;
    let row = row as i32;
    let col = col as i32;
    for c in [-1, 0, 1].iter() {
        if let Occupied = get(row - 1, col + c) {
            n += 1;
        }
        if let Occupied = get(row + 1, col + c) {
            n += 1;
        }
    }
    for c in [-1, 1].iter() {
        if let Occupied = get(row, col + c) {
            n += 1;
        }
    }
    n
}
