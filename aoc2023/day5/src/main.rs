use crate::parse::parse;
use crate::range::Range;
mod parse;
mod range;

fn main() {
    let (numbers, steps) = parse(include_str!("input.txt"));

    println!("Part 1: {}", smallest(numbers.clone(), &steps));
    let ranges = apply_steps_to_ranges(make_ranges(&numbers), &steps);
    println!("Part 2: {}", smallest_from_ranges(ranges));
}

fn apply_steps_to_ranges(mut ranges: Vec<Range>, steps: &Vec<Step>) -> Vec<Range> {
    for step in steps.iter() {
        ranges = range::apply_step(&ranges, step)
    }
    ranges
}

fn smallest_from_ranges(ranges: Vec<Range>) -> u64 {
    let mut smallest = u64::MAX;
    for r in ranges {
        if r.start < smallest {
            smallest = r.start;
        }
    }
    smallest
}

// deprecated
fn smallest(seeds: Vec<u64>, steps: &Vec<Step>) -> u64 {
    let mut smallest = u64::MAX;
    for seed in seeds {
        let mut s = seed;
        for step in steps {
            s = apply_step(s, step);
        }
        if s < smallest {
            smallest = s;
        }
    }
    smallest
}

fn make_ranges(numbers: &Vec<u64>) -> Vec<Range> {
    let mut result = Vec::new();
    let mut numbers = numbers.iter();
    loop {
        if let Some(start) = numbers.next() {
            let length =  *numbers.next().expect("numbers must be even pairs");
            result.push(Range::new(*start, start + length));
        } else {
            break;
        }
    }
    result
}

#[derive(Clone, PartialEq, Debug)]
struct Map {
    dest_start: u64,
    source_start: u64,
    range_length: u64,
}

impl Map {
    #[cfg(test)]
    fn new(dest_start: u64, source_start: u64, range_length: u64) -> Self {
        Map {
            dest_start,
            source_start,
            range_length,
        }
    }
}

#[derive(PartialEq, Debug)]
struct Step {
    maps: Vec<Map>,
}

fn try_map(input: u64, map: &Map) -> Option<u64> {
    if input < map.source_start || input > map.source_start + map.range_length {
        None
    } else {
        Some(map.dest_start + input - map.source_start)
    }
}

fn apply_step(seed: u64, step: &Step) -> u64 {
    for map in step.maps.iter() {
        if let Some(i) = try_map(seed, map) {
            return i;
        }
    }
    seed
}

#[cfg(test)]
mod tests {
    use crate::{apply_step, try_map, Map, Step, make_ranges};
    use crate::range::Range;

    #[test]
    fn test_try_map() {
        let map = &Map::new(88, 55, 4);
        assert_eq!(None, try_map(32, map));
        assert_eq!(Some(88), try_map(55, map));
        assert_eq!(Some(90), try_map(57, map));
    }

    #[test]
    fn test_apply_step() {
        let s = Step {
            maps: vec![Map::new(50, 98, 2), Map::new(52, 50, 48)],
        };
        assert_eq!(57, apply_step(55, &s));
        assert_eq!(13, apply_step(13, &s));
        assert_eq!(14, apply_step(14, &s));
        assert_eq!(81, apply_step(79, &s));
    }

    #[test]
    fn test_make_ranges() {
        let result = make_ranges(&vec![55, 8, 19, 7]);
        assert_eq!(vec![Range::new(55, 63), Range::new(19, 26)], result);
    }

}
