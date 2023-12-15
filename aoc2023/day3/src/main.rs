use anyhow::Result;
use std::collections::HashMap;
use std::io::{BufRead, Cursor};

const DATA: &[u8] = include_bytes!("input.txt");

fn main() -> Result<()> {
    println!("Hello, world!");
    let m = Matrix::from_newline_separated(DATA).expect("Couldn't read input");
    let mut sum = 0;
    let numbers = find_numbers(&m)?;
    for coordinates in &numbers {
        sum += check_candidate(&m, coordinates)?.unwrap_or(0);
    }
    println!("Part 1 answer: {}", sum);
    let map = make_star_to_numbers(&numbers, &m)?;
    println!(
        "Part 2 answer: {}",
        find_gear_ratios(map).iter().sum::<i32>()
    );
    Ok(())
}

fn find_gear_ratios(map: HashMap<Coord, Vec<i32>>) -> Vec<i32> {
    let mut result: Vec<i32> = Vec::new();
    for entry in map.iter() {
        if entry.1.len() == 2 {
            result.push(entry.1.iter().product());
        }
    }
    result
}

fn make_star_to_numbers(
    numbers: &Vec<(Coord, Coord)>,
    matrix: &Matrix,
) -> Result<HashMap<Coord, Vec<i32>>> {
    let mut result = HashMap::new();
    for coordinates in numbers {
        for adjacent in get_adjacent(coordinates) {
            if let Some('*') = matrix.get_symbol(&adjacent) {
                let n = matrix.get_number(coordinates)?;
                result
                    .entry(adjacent)
                    .and_modify(|v: &mut Vec<i32>| v.push(n))
                    .or_insert(vec![n]);
            }
        }
    }
    Ok(result)
}

fn check_candidate(matrix: &Matrix, coords: &(Coord, Coord)) -> Result<Option<i32>> {
    for c in get_adjacent(coords) {
        if matrix.get_symbol(&c).is_some() {
            let n = matrix.get_number(coords)?;
            return Ok(Some(n));
        }
    }
    Ok(None)
}

#[derive(PartialEq)]
enum State {
    Out,
    In,
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct Coord {
    i: i32,
    j: i32,
}

impl Coord {
    fn new(i: i32, j: i32) -> Self {
        Coord { i, j }
    }
}

fn find_numbers(matrix: &Matrix) -> Result<Vec<(Coord, Coord)>> {
    let mut state = State::Out;
    let mut start = Coord { i: 0, j: 0 };
    let mut result = Vec::new();
    for (i, s) in matrix.data.iter().enumerate() {
        for (j, c) in s.chars().enumerate() {
            match state {
                State::Out => {
                    if c.is_ascii_digit() {
                        start = Coord::new(i.try_into()?, j.try_into()?);
                        state = State::In
                    }
                }
                State::In => {
                    if !c.is_ascii_digit() {
                        result.push((start.clone(), Coord::new(i.try_into()?, j.try_into()?)));
                        state = State::Out
                    }
                }
            }
        }
        if state == State::In {
            state = State::Out;
            result.push((
                start.clone(),
                Coord::new(i.try_into()?, s.len().try_into()?),
            ))
        }
    }
    Ok(result)
}

#[derive(Debug)]
struct Matrix {
    data: Vec<Box<str>>,
}

impl Matrix {
    fn from_newline_separated(input: &[u8]) -> Result<Self> {
        let mut data: Vec<Box<str>> = Vec::new();

        for line in Cursor::new(input).lines() {
            let s = line?;
            let boxed = s.into_boxed_str();
            data.push(boxed);
        }
        Ok(Matrix { data })
    }

    fn get_number(&self, coords: &(Coord, Coord)) -> Result<i32> {
        assert_eq!(coords.0.i, coords.1.i);
        Ok(self.data[coords.0.i as usize][coords.0.j as usize..coords.1.j as usize].parse()?)
    }

    fn get_symbol(&self, coord: &Coord) -> Option<char> {
        if coord.i < 0 || coord.j < 0 {
            return None;
        }
        if coord.i + 1 > self.data.len() as i32 {
            return None;
        }
        let line = &self.data[coord.i as usize];
        if line.len() < (coord.j + 1) as usize {
            return None;
        }
        let c = line
            .chars()
            .nth(coord.j as usize)
            .expect("boundary checking error");
        if c == '.' {
            None
        } else {
            Some(c)
        }
    }
}

fn get_adjacent(coords: &(Coord, Coord)) -> Vec<Coord> {
    let mut result = Vec::new();
    for x in coords.0.j - 1..=coords.1.j {
        result.push(Coord::new(coords.0.i - 1, x))
    }
    for x in coords.0.i..=coords.1.i {
        result.push(Coord::new(x, coords.0.j - 1));
        result.push(Coord::new(x, coords.1.j));
    }
    for x in coords.0.j - 1..=coords.1.j {
        result.push(Coord::new(coords.1.i + 1, x))
    }
    result
}

#[cfg(test)]
mod tests {
    use crate::{get_adjacent, Coord};

    #[test]
    fn test_get_adjacent() {
        let result = get_adjacent(&(Coord { i: 1, j: 3 }, Coord { i: 1, j: 6 }));
        assert_eq!(
            vec![
                Coord { i: 0, j: 2 },
                Coord { i: 0, j: 3 },
                Coord { i: 0, j: 4 },
                Coord { i: 0, j: 5 },
                Coord { i: 0, j: 6 },
                Coord { i: 1, j: 2 },
                Coord { i: 1, j: 6 },
                Coord { i: 2, j: 2 },
                Coord { i: 2, j: 3 },
                Coord { i: 2, j: 4 },
                Coord { i: 2, j: 5 },
                Coord { i: 2, j: 6 },
            ],
            result
        );
    }

    #[test]
    fn test_get_adjacent_negative() {
        let result = get_adjacent(&(Coord::new(0, 0), Coord::new(0, 1)));
        assert_eq!(
            vec![
                Coord { i: -1, j: -1 },
                Coord { i: -1, j: 0 },
                Coord { i: -1, j: 1 },
                Coord { i: 0, j: -1 },
                Coord { i: 0, j: 1 },
                Coord { i: 1, j: -1 },
                Coord { i: 1, j: 0 },
                Coord { i: 1, j: 1 }
            ],
            result
        );
    }
}
