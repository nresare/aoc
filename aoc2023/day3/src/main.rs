use std::io::{BufRead, Cursor};
use anyhow::Result;

const DATA: &[u8] = include_bytes!("input.txt");

fn main() -> Result<()> {
    println!("Hello, world!");
    let m = Matrix::from_newline_separated(DATA).expect("Couldn't read input");
    let mut sum = 0;
    for coordinates in find_numbers(&m)? {
        sum += check_candidate(&m, &coordinates)?.unwrap_or(0);
    }
    println!("The sum is {}", sum);
    Ok(())
}

fn check_candidate(matrix: &Matrix, coords: &(Coord, Coord)) -> Result<Option<i32>> {
    for c in get_adjacent(coords) {
        if matrix.found_other_than_dot(&c) {
            let n = matrix.get_number(coords)?;
            return Ok(Some(n));
        }
    }
    Ok(None)
}

#[derive(PartialEq)]
enum State {
    OUT, IN
}

#[derive(Debug, Clone, PartialEq)]
struct Coord {
    i: i32,
    j: i32,
}

impl Coord {
    fn new(i: i32, j: i32) -> Self {
        Coord{i, j}
    }
}

fn find_numbers(matrix: &Matrix) -> Result<Vec<(Coord, Coord)>> {
    let mut state = State::OUT;
    let mut start = Coord { i: 0, j: 0};
    let mut result = Vec::new();
    for (i, s) in matrix.data.iter().enumerate() {
        for (j, c) in s.chars().enumerate() {
            match state {
                State::OUT => {
                    if c.is_digit(10) {
                        start = Coord::new(i.try_into()?, j.try_into()?);
                        state = State::IN
                    }
                },
                State::IN => {
                    if !c.is_digit(10) {
                        result.push((start.clone(), Coord::new(i.try_into()?, j.try_into()?)));
                        state = State::OUT
                    }
                }
            }
        }
        if state == State::IN {
            state = State::OUT;
            result.push((start.clone(), Coord::new(i.try_into()?, s.len().try_into()?)))
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
        Ok(Matrix{data})
    }

    fn get_number(&self, coords: &(Coord, Coord)) -> Result<i32> {
        assert_eq!(coords.0.i, coords.1.i);
        Ok(self.data[coords.0.i as usize][coords.0.j as usize..coords.1.j as usize].parse()?)
    }

    fn found_other_than_dot(&self, coord: &Coord) -> bool{
        if coord.i < 0 || coord.j < 0  {
            return false
        }
        if coord.i + 1 > self.data.len() as i32 {
            return false
        }
        let line = &self.data[coord.i as usize];
        if line.len() < (coord.j + 1) as usize {
            return false
        }
        let c = line.chars().nth(coord.j as usize).expect("boundary checking error");
        return c != '.'
    }
}

fn get_adjacent(coords: &(Coord, Coord)) -> Vec<Coord> {
    let mut result = Vec::new();
    for x in coords.0.j-1..=coords.1.j {
        result.push(Coord::new(coords.0.i - 1, x))
    }
    for x in coords.0.i..=coords.1.i {
        result.push(Coord::new(x, coords.0.j-1));
        result.push(Coord::new(x, coords.1.j));

    }
    for x in coords.0.j-1..=coords.1.j {
        result.push(Coord::new(coords.1.i + 1, x))
    }
    result
}

#[cfg(test)]
mod tests {
    use crate::{Coord, get_adjacent};

    #[test]
    fn test_get_adjacent() {
        let result = get_adjacent(&(Coord {i: 1, j: 3}, Coord {i: 1, j: 6}));
        assert_eq!(vec![
            Coord {i: 0, j: 2},
            Coord {i: 0, j: 3},
            Coord {i: 0, j: 4},
            Coord {i: 0, j: 5},
            Coord {i: 0, j: 6},
            Coord {i: 1, j: 2},
            Coord {i: 1, j: 6},
            Coord {i: 2, j: 2},
            Coord {i: 2, j: 3},
            Coord {i: 2, j: 4},
            Coord {i: 2, j: 5},
            Coord {i: 2, j: 6},
        ], result);
    }

    #[test]
    fn test_get_adjacent_negative() {
        let result = get_adjacent(&(Coord::new(0, 0), Coord::new(0, 1)));
        assert_eq!(vec![
            Coord {i: -1, j: -1},
            Coord {i: -1, j: 0},
            Coord {i: -1, j: 1},
            Coord {i: 0, j: -1},
            Coord {i: 0, j: 1},
            Coord {i: 1, j: -1},
            Coord {i: 1, j: 0},
            Coord {i: 1, j: 1}
        ], result);
    }
}