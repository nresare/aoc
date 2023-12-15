use crate::{CubeCount, Game};
use anyhow::{anyhow, Result};
use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    static ref GAME_RE: Regex = Regex::new(r"Game (\d+): (.*)").expect("failed to compile");
    static ref ROUND_RE: Regex = Regex::new(r"(\d+) (\w+)").expect("failed to compile");
}
pub fn get_games(input: &str) -> Result<Vec<Game>> {
    let result = input.lines();
    let result: Result<Vec<_>, _> = result.map(get_game).collect();
    let result = result?;
    Ok(result)
}

fn get_round(input: &str) -> Result<CubeCount> {
    let mut red = 0u32;
    let mut green = 0u32;
    let mut blue = 0u32;
    for i in input.split(", ") {
        let c = ROUND_RE.captures(i).unwrap();
        let count: u32 = c.get(1).unwrap().as_str().parse()?;
        match c.get(2).unwrap().as_str() {
            "red" => red = count,
            "green" => green = count,
            "blue" => blue = count,
            _ => return Err(anyhow!("illegal colour")),
        }
    }
    Ok(CubeCount { red, green, blue })
}

fn get_game(line: &str) -> Result<Game> {
    let captures = GAME_RE.captures(line).unwrap();
    let id: u32 = captures.get(1).unwrap().as_str().parse()?;
    let input = captures.get(2).unwrap().as_str();
    let rounds: Vec<CubeCount> = input.split("; ").map(get_round).collect::<Result<_, _>>()?;
    Ok(Game { id, rounds })
}

#[cfg(test)]
mod test {
    use super::get_round;
    use crate::CubeCount;
    use anyhow::Result;

    #[test]
    fn test_get_round() -> Result<()> {
        assert_eq!(CubeCount::new(4, 0, 3), get_round("3 blue, 4 red")?);
        Ok(())
    }
}
