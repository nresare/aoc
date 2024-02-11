use std::collections::HashMap;
use std::str::Lines;
use anyhow::{Result, anyhow};
use lazy_static::lazy_static;
use regex::Regex;

const START: &str = "AAA";
const END: &str = "ZZZ";

lazy_static! {
    static ref NET_LINE: Regex = Regex::new(r"(\w+) = \((\w+), (\w+)\)").expect("failed to compile");
}

fn main() -> Result<()> {
    let data = parse(include_str!("input.txt"))?;
    let mut count = 0;
    let mut name = START;
    while name != END {
        count += data.instructions.len();
        name = follow_instructions(&data, name)
    }
    println!("Found end after {count} rounds");
    Ok(())
}

fn follow_instructions<'a>(data: &'a Data, mut start: &'a str) -> &'a str {
    for i in &data.instructions {
        start = next(&data.network, start, i)
    }
    start
}

fn next<'a>(network: &'a Network, name: &'a str, direction: &Direction) -> &'a str {
    let pair = network.get(name).expect("Could not find pair");
    match direction {
        Direction::LEFT => pair.0.as_str(),
        Direction::RIGHT => pair.1.as_str(),
    }
}

#[derive(PartialEq, Debug)]
enum Direction {
    LEFT,
    RIGHT
}

type Network = HashMap<String, (String, String)>;

struct Data {
    instructions: Vec<Direction>,
    network: Network,
}

fn parse(input: &str) -> Result<Data> {
    let lines = &mut input.lines();
    let instructions = lines.next().expect("At least one line of input is required");
    Ok(Data { instructions: make_instructions(instructions)?, network: make_network(lines)?})
}

fn make_network(lines: &mut Lines) -> Result<HashMap<String, (String, String)>> {
    lines.filter(|l| l.len() > 0).map(inner_network).collect()
}

fn inner_network(line: &str) -> Result<(String, (String, String))> {
    let result = NET_LINE.captures(line)
        .ok_or(anyhow!("Wrong format: '{line}'"))?;
    Ok((result[1].into(), (result[2].into(), result[3].into())))
}


fn make_instructions(line: &str) -> Result<Vec<Direction>> {
    line.chars().map(|c| {
        match c {
            'R' => Ok(Direction::RIGHT),
            'L' => Ok(Direction::LEFT),
            _ => Err(anyhow!("Invalid letter")),
        }
    }).collect()
}

#[cfg(test)]
mod test {
    use std::collections::HashMap;
    use crate::{Direction, make_instructions, make_network};

    #[test]
    fn test_make_instructions() {
        let result = make_instructions("RL").unwrap();
        assert_eq!(vec!(Direction::RIGHT, Direction::LEFT), result);
    }

    #[test]
    fn test_make_network() {
        let result = make_network("a = (b, c)\ndd = (ee, ff)".lines()).unwrap();
        let mut expected: HashMap<&str, (&str, &str)> = HashMap::new();
        expected.insert("a", ("b", "c"));
        expected.insert("dd", ("ee", "ff"));
        assert_eq!(expected, result)
    }
}