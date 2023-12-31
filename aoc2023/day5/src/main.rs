use crate::parse::parse;
use std::vec::IntoIter;
mod parse;

fn main() {
    let (numbers, steps) = parse(include_str!("input.txt"));

    println!("Part 1: {}", smallest(numbers.iter().map(|i| *i), &steps));
    println!("Part 2: {}", smallest(make_seed_iterator(numbers), &steps))
}

fn smallest(seeds: impl Iterator<Item=u64>, steps: &Vec<Step>) -> u64 {
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

fn make_seed_iterator(seeds: Vec<u64>) -> SeedIterator {
    SeedIterator {
        seeds: seeds.into_iter(),
        next: 0,
        count: 0,
        total: 0,
    }
}

struct SeedIterator {
    seeds: IntoIter<u64>,
    next: u64,
    count: u64,
    total: u64,
}

impl Iterator for SeedIterator {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        if self.count < 1 {
            self.try_fill();
        }
        if self.count < 1 {
            return None;
        }
        self.count -= 1;
        let i = self.next;
        self.next += 1;
        self.total += 1;
        if self.total % 10_000_000 == 0 {
            println!("Progression: {}", self.total as f32 / 2037733040f32)
        }
        Some(i)
    }
}

impl SeedIterator {
    fn try_fill(&mut self) {
        if let Some(next) = self.seeds.next() {
            let count = self.seeds.next().expect("seeds needs to come in pairs");
            assert_ne!(0, count);
            self.next = next;
            self.count = count;
        }
    }
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
    use crate::{apply_step, make_seed_iterator, try_map, Map, Step};

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
    fn test_seed_iterator() {
        let iter = make_seed_iterator(vec![1, 3, 5, 5]);
        assert_eq!(vec![1, 2, 3, 5, 6, 7, 8, 9], iter.collect::<Vec<_>>());
    }

    #[test]
    fn test_count_part2_seeds() {
        let iter = make_seed_iterator(vec![858905075, 56936593, 947763189, 267019426, 206349064, 252409474, 660226451, 92561087, 752930744, 24162055, 75704321, 63600948, 3866217991, 323477533, 3356941271, 54368890, 1755537789, 475537300, 1327269841, 427659734]);
        let mut n = 0;
        for i in iter {
            n += 1;
        }
        println!("total number of seeds: {}", n);
}
}
