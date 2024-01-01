fn main() {
    let data = include_str!("input.txt");

    println!("part 1: {}", calculate(parse(data)));
    println!("part 2: {}", calculate(parse_part_2(data)));
}

#[derive(PartialEq, Debug)]
struct Race {
    distance: u64,
    time: u64,
}

fn calculate(races: Vec<Race>) -> u64 {
    races.iter().map(count_winning_variants).product()
}

fn count_winning_variants(race: &Race) -> u64 {
    let mut count = 0;
    for speed in 1..race.time {
        let distance = speed * (race.time - speed);
        if distance > race.distance {
            count += 1;
        }
    }
    count
}

fn parse_part_2(data: &str) -> Vec<Race> {
    let lines: Vec<_> = data.lines().collect();
    assert_eq!(2, lines.len());
    let time: u64 = lines[0]["Time: ".len()..]
        .replace(' ', "")
        .parse()
        .expect("failed to parse time");
    let distance: u64 = lines[1]["Distance: ".len()..]
        .replace(' ', "")
        .parse()
        .expect("failed to parse distance");
    vec![Race { time, distance }]
}

fn parse(data: &str) -> Vec<Race> {
    let lines: Vec<_> = data.lines().collect();
    assert_eq!(2, lines.len());
    let mut times = lines[0].split_whitespace();
    let mut distances = lines[1].split_whitespace();
    // skip the "Time:" and "Distance:" prefix
    times.next();
    distances.next();
    let mut result = Vec::new();
    for time in times {
        let distance = distances
            .next()
            .expect("too few distances")
            .parse()
            .expect("failed to parse distance");
        let time = time.parse().expect("failed to parse time");
        result.push(Race { distance, time })
    }
    result
}

#[cfg(test)]
mod tests {
    use crate::{count_winning_variants, parse, Race};

    #[test]
    fn test_parse() {
        let s = "Time: 1 2 3\nDistance: 4 5 6";
        assert_eq!(
            vec![
                Race {
                    time: 1,
                    distance: 4
                },
                Race {
                    time: 2,
                    distance: 5
                },
                Race {
                    time: 3,
                    distance: 6
                },
            ],
            parse(s)
        );
    }

    #[test]
    fn test_count_winning_variants() {
        assert_eq!(
            4,
            count_winning_variants(&Race {
                distance: 9,
                time: 7
            })
        );
    }
}
