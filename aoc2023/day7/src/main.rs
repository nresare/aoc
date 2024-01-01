mod hand;

use hand::Hand;

fn main() {
    let mut v = parse(include_str!("example.txt"));
    v.sort();
    for (hand, bet) in v {
        println!("{:?}", hand)
    }
}



fn parse(input: &str) -> Vec<(Hand, u32)> {
    input.lines().map(|l| {
        let mut parts = l.split_whitespace();
        (Hand::new(parts.next().unwrap()).unwrap(), parts.next().unwrap().parse::<u32>().unwrap())
    }).collect()
}