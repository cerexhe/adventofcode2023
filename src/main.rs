use std::env;
mod q1;
mod utils;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("usage: [1-25]")
    }
    match args[1].parse::<i32>().unwrap() {
        1 => q1::solve(),
        day => panic!("unexpected day {}", day),
    }
}
