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
    part_1(&data);
    part_2(&data);
    Ok(())
}

fn part_1(data: &Data) {
    let mut count = 0;
    let mut name = START;
    while name != END {
        count += data.instructions.len();
        name = follow_instructions(&data, name)
    }
    println!("Found end after {count} rounds");
}

fn part_2(data: &Data) {
    let mut count = 0;
    let mut names = find_ends_with_a(&data.network);
    let mut cache: HashMap<&str, &str> = HashMap::new();

    loop {
        count += 1;
        let mut all_at_end = true;
        let mut success_count = 0;
        for name in names.iter_mut() {
            let result= cache.entry(name).or_insert_with(|| follow_instructions(&data, *name));
            if !result.ends_with("Z") {
                all_at_end = false;
            } else {
                success_count += 1;
            }
            *name = result;
        }
        if all_at_end {
            break;
        }
        if success_count > 2 {
            println!("success count at {}: {}", count, success_count);
        }
        if count % 1_000_000 == 0 {
            println!("Checked {} sets. Success count: {}", count, success_count)
        }
    }
    println!("Found end after {} rounds", count * data.instructions.len());

}

fn find_ends_with_a(network: &Network) -> Vec<&str> {
    network.keys().filter(|k| k.ends_with("A")).map(String::as_str).collect()
}

fn follow_instructions<'a>(data: &'a Data, mut start: &'a str) -> &'a str {
    for i in &data.instructions {
        start = next(&data.network, start, i)
    }
    start
}

fn next<'a>(network: &'a Network, name: &'a str, direction: &Direction) -> &'a str {
    let pair = network.get(name).expect(format!("Could not find pair for {}", name).as_str());
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
        let result = make_network(&mut "a = (b, c)\ndd = (ee, ff)".lines()).unwrap();
        let mut expected: HashMap<String, (String, String)> = HashMap::new();
        expected.insert("a".to_string(), ("b".to_string(), "c".to_string()));
        expected.insert("dd".to_string(), ("ee".to_string(), "ff".to_string()));
        assert_eq!(expected, result)
    }
}