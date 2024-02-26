use anyhow::{anyhow, Result};
use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashMap;
use std::str::Lines;

const START: &str = "AAA";
const END: &str = "ZZZ";

lazy_static! {
    static ref NET_LINE: Regex =
        Regex::new(r"(\w+) = \((\w+), (\w+)\)").expect("failed to compile");
}

fn main() -> Result<()> {
    let data = parse(include_str!("input.txt"))?;
    part_1(&data);
    part_2(&data);
    Ok(())
}

fn part_1(data: &Data) {
    let mut count = 0;
    let mut name = START;
    while name != END {
        count += data.instructions.len();
        name = follow_instructions(data, name)
    }
    println!("Found end after {count} rounds");
}

fn part_2(data: &Data) {
    let names = find_ends_with_a(&data.network);

    let periods: Vec<_> = names.into_iter().map(|n| get_iterations(n, data)).collect();
    println!(
        "Part two: {}",
        find_lcm(periods) * data.instructions.len() as u64
    )
}

fn get_iterations(name: &str, data: &Data) -> u64 {
    let mut count = 0u64;
    let mut result = name;
    loop {
        count += 1;
        result = follow_instructions(data, result);
        if result.ends_with('Z') {
            return count;
        }
    }
}

fn find_lcm(numbers: Vec<u64>) -> u64 {
    let mut numbers = numbers.into_iter();
    let first = numbers.next();
    let mut lcm = first.expect("at least one number is needed");
    for i in numbers {
        lcm = num::integer::lcm(i, lcm);
    }
    lcm
}

fn find_ends_with_a(network: &Network) -> Vec<&str> {
    network
        .keys()
        .filter(|k| k.ends_with('A'))
        .map(String::as_str)
        .collect()
}

fn follow_instructions<'a>(data: &'a Data, mut start: &'a str) -> &'a str {
    for i in &data.instructions {
        start = next(&data.network, start, i)
    }
    start
}

fn next<'a>(network: &'a Network, name: &'a str, direction: &Direction) -> &'a str {
    let pair = network
        .get(name)
        .unwrap_or_else(|| panic!("Could not find pair for {}", name));
    match direction {
        Direction::Left => pair.0.as_str(),
        Direction::Right => pair.1.as_str(),
    }
}

#[derive(PartialEq, Debug)]
enum Direction {
    Left,
    Right,
}

type Network = HashMap<String, (String, String)>;

struct Data {
    instructions: Vec<Direction>,
    network: Network,
}

fn parse(input: &str) -> Result<Data> {
    let lines = &mut input.lines();
    let instructions = lines
        .next()
        .expect("At least one line of input is required");
    Ok(Data {
        instructions: make_instructions(instructions)?,
        network: make_network(lines)?,
    })
}

fn make_network(lines: &mut Lines) -> Result<HashMap<String, (String, String)>> {
    lines.filter(|l| !l.is_empty()).map(inner_network).collect()
}

fn inner_network(line: &str) -> Result<(String, (String, String))> {
    let result = NET_LINE
        .captures(line)
        .ok_or(anyhow!("Wrong format: '{line}'"))?;
    Ok((result[1].into(), (result[2].into(), result[3].into())))
}

fn make_instructions(line: &str) -> Result<Vec<Direction>> {
    line.chars()
        .map(|c| match c {
            'R' => Ok(Direction::Right),
            'L' => Ok(Direction::Left),
            _ => Err(anyhow!("Invalid letter")),
        })
        .collect()
}

#[cfg(test)]
mod test {
    use crate::{make_instructions, make_network, Direction};
    use std::collections::HashMap;

    #[test]
    fn test_make_instructions() {
        let result = make_instructions("RL").unwrap();
        assert_eq!(vec!(Direction::Right, Direction::Left), result);
    }

    #[test]
    fn test_make_network() {
        let result = make_network(&mut "a = (b, c)\ndd = (ee, ff)".lines()).unwrap();
        let mut expected: HashMap<String, (String, String)> = HashMap::new();
        expected.insert("a".to_string(), ("b".to_string(), "c".to_string()));
        expected.insert("dd".to_string(), ("ee".to_string(), "ff".to_string()));
        assert_eq!(expected, result)
    }
}
