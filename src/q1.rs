use std::collections::HashMap;
use super::utils;

pub fn solve() {
    let digits: HashMap<String, i32> = HashMap::from_iter((1..10).map(|i| -> (String, i32) {
        (format!("{}", i), i)
    }));
    let mut candidates = HashMap::from([
        ("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
    ].map(|(k, v)| -> (String, i32) {
        (k.into(), v)
    }));

    candidates.extend(digits);
    
    
    let reverse_candidates: HashMap<String, i32> = HashMap::from_iter(candidates.clone().into_iter()
        .map(|(k, v)| -> (String, i32) {
            (utils::reverse_chars(&k[..]), v)
        }));

    let mut sum1 = 0;
    let mut sum2 = 0;
    let lines = utils::read_lines("input1.txt");
    for maybe_line in lines {
        if let Ok(line) = maybe_line {
            let rev = utils::reverse_chars(&line[..]);
            sum1 += find_digit(&line) * 10 + find_digit(&rev);
            sum2 += find_candidate_digit(&line, &candidates) * 10 + find_candidate_digit(&rev, &reverse_candidates);
        }
    }
    println!("{}", sum1);
    println!("{}", sum2);
}

fn find_digit(s: &String) -> i32 {
    for c in s.bytes() {
        if b'0' <= c && c <= b'9' {
            return (c - b'0').into();
        }
    }
    panic!("unreachable");
}

fn find_candidate_digit(s: &String, candidates: &HashMap<String, i32>) -> i32 {
    for i in 0..s.len() {
        for (c, num) in candidates {
            let sub = &s[i..];
            if sub.starts_with(c) {
                return *num;
            }
        }
    }
    panic!("unreachable");
}
