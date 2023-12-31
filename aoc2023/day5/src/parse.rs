use crate::{Map, Step};
use std::str::Lines;
pub fn parse(input: &str) -> (Vec<u64>, Vec<Step>) {
    let mut lines = input.lines();
    let seeds = lines.next().expect("Missing seeds line");
    let empty = lines.next().expect("Missing empty line after seeds");
    assert_eq!(empty, "");
    let parts = seeds
        .split(": ")
        .nth(1)
        .expect("seeds line has invalid format");
    let seeds: Vec<u64> = parts
        .split(' ')
        .map(|x| x.parse().expect("could not parse int"))
        .collect();

    (seeds, make_steps(lines))
}

fn make_steps(lines: Lines) -> Vec<Step> {
    let mut result: Vec<Step> = Vec::new();
    let mut maps: Vec<Map> = Vec::new();

    for line in lines {
        if line.contains("map") {
            continue;
        } else if line == "" {
            result.push(Step { maps: maps.clone() });
            maps.clear();
        } else {
            let parts: Vec<u64> = line
                .split(' ')
                .map(|x| x.parse().expect("couldn't parse"))
                .collect();
            assert_eq!(3, parts.len());
            maps.push(Map {
                dest_start: parts[0],
                source_start: parts[1],
                range_length: parts[2],
            })
        }
    }
    result.push(Step { maps: maps.clone() });
    result
}

#[cfg(test)]
mod tests {
    use crate::parse::parse;
    use crate::{Map, Step};

    #[test]
    fn test_parse() {
        let (seeds, steps) = parse(include_str!("short_example.txt"));
        assert_eq!(vec![79, 14, 55, 13], seeds);
        assert_eq!(
            vec![
                Step {
                    maps: vec![Map::new(50, 98, 2), Map::new(52, 50, 48),]
                },
                Step {
                    maps: vec![
                        Map::new(0, 15, 37),
                        Map::new(37, 52, 2),
                        Map::new(39, 0, 15),
                    ]
                },
            ],
            steps
        );
    }
}
