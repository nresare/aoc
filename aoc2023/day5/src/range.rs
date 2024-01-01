// range operations

use crate::{Map, Step};
use std::cmp::{max, min};

#[derive(PartialEq, Debug, Clone)]
pub struct Range {
    /// the start value
    pub(crate) start: u64,
    /// the value after the end value
    end: u64,
}

impl Range {
    pub fn new(start: u64, end: u64) -> Self {
        Range { start, end }
    }

    fn delta(start: u64, end: u64, delta: i64) -> Self {
        Range {
            start: start
                .checked_add_signed(delta)
                .expect("can't subtract delta"),
            end: end.checked_add_signed(delta).expect("can't subtract delta"),
        }
    }
}

pub fn apply_step(ranges: &[Range], step: &Step) -> Vec<Range> {
    let mut inputs: Vec<Range> = ranges.to_vec();
    let mut outputs = Vec::new();

    for map in step.maps.iter() {
        let mut new_inputs = Vec::new();
        for input in inputs.iter() {
            let result = apply_map(input, map);
            new_inputs.extend(result.rest);
            if let Some(mapped) = result.mapped {
                outputs.push(mapped);
            }
        }
        inputs = new_inputs;
    }
    // the input that was not mapped gets copied to outputs
    outputs.extend(inputs);
    outputs
}

#[derive(PartialEq, Debug)]
struct ApplyResult {
    rest: Vec<Range>,
    mapped: Option<Range>,
}

#[cfg(test)]
impl ApplyResult {
    fn new(rest: Vec<Range>, mapped: Option<Range>) -> Self {
        ApplyResult { rest, mapped }
    }
}

fn apply_map(range: &Range, map: &Map) -> ApplyResult {
    assert!(range.start < range.end);

    let map_end = map.source_start + map.range_length;

    let mut rest = Vec::new();

    if range.start < map.source_start {
        rest.push(Range::new(range.start, min(map.source_start, range.end)));
    }
    if range.end > map_end {
        rest.push(Range::new(max(map_end, range.start), range.end));
    }

    if range.start < map_end && range.end > map.source_start {
        ApplyResult {
            rest,
            mapped: Some(Range::delta(
                max(map.source_start, range.start),
                min(map_end, range.end),
                map.dest_start as i64 - map.source_start as i64,
            )),
        }
    } else {
        ApplyResult { rest, mapped: None }
    }
}

#[cfg(test)]
mod tests {
    use crate::range::{apply_map, apply_step, ApplyResult, Range};
    use crate::{Map, Step};

    #[test]
    fn test_apply_map() {
        // it is easier to reason about a Map that doesn't have a delta
        let m = &Map::new(10, 10, 3);
        // case 1, entire range is before map
        assert_eq!(
            ApplyResult::new(vec![Range::new(1, 5)], None),
            apply_map(&Range::new(1, 5), m)
        );
        // case 2, range starts before map but is also inside part of the map
        assert_eq!(
            ApplyResult::new(vec![Range::new(8, 10)], Some(Range::new(10, 11))),
            apply_map(&Range::new(8, 11), m)
        );
        // case 3, range is entirely within the map
        assert_eq!(
            ApplyResult::new(vec![], Some(Range::new(10, 11))),
            apply_map(&Range::new(10, 11), m)
        );
        // case 4, range is both before and after map
        assert_eq!(
            ApplyResult::new(
                vec![Range::new(8, 10), Range::new(13, 14)],
                Some(Range::new(10, 13))
            ),
            apply_map(&Range::new(8, 14), m)
        );
        // case 5, range is completely after the map
        assert_eq!(
            ApplyResult::new(vec![Range::new(13, 15)], None),
            apply_map(&Range::new(13, 15), m)
        );
    }

    #[test]
    fn test_apply_step() {
        let r = &vec![Range::new(96, 100)];
        let s = Step {
            maps: vec![Map::new(50, 98, 2), Map::new(52, 50, 48)],
        };
        let result = apply_step(r, &s);
        assert_eq!(vec![Range::new(50, 52), Range::new(98, 100)], result);
    }
}
