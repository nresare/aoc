use day2::{CubeCount, Game};
use day2::parse::get_games;
use anyhow::Result;
fn main() -> Result<()> {
    println!("Advent of code 2023, day 2 part 2");

    let games = get_games(include_str!("data.txt"))?;
    let sum: u32 = games.iter()
        .map(Game::rounds)
        .map(min_cube_count)
        .map(CubeCount::power)
        .sum();
    println!("Sum of the powers is {}", sum);
    Ok(())
}

fn min_cube_count(rounds: &[CubeCount]) -> CubeCount {
    rounds.iter()
        .map(CubeCount::clone)
        .reduce(|left, right| left.max(right))
        .expect("empty list of rounds")
}

