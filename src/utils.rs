use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

pub fn read_lines<P>(filename: P) -> io::Lines<io::BufReader<File>>
where P: AsRef<Path>, {
    let file = File::open(filename).unwrap();
    io::BufReader::new(file).lines()
}

pub fn reverse_chars(s: &str) -> String {
    s.chars().rev().collect::<String>()
}

// pub fn prefix<T>(haystack: Iterator, needle: Iterator) -> bool {
//     for (h, n) in zip(haystack, needle) {
//         if i >= haystack.len() || c != haystack[i] {
//             return false;
//         }
//     }
//     return needle.next().is_none();
// }
