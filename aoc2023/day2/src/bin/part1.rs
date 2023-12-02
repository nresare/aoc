use day2::parse::get_games;
use anyhow::Result;
use day2::{CubeCount, Game};

fn main() -> Result<()> {
    println!("advent of code 2023, day 2 part 1");

    let games = get_games(include_str!("data.txt"))?;
    let true_count = &CubeCount::new(12, 13, 14);
    let sum: u32 =  games.into_iter()
        .filter(|g| valid_game(g.rounds(), true_count))
        .map(Game::id)
        .sum();
    println!("Sum of ids of valid games {}", sum);
    Ok(())
}

fn valid_game(rounds: &[CubeCount], true_count: &CubeCount) -> bool {
    !rounds.iter().any(|x| !x.valid_for(true_count))
}

#[cfg(test)]
mod tests {
    use day2::CubeCount;
    use crate::valid_game;

    #[test]
    fn test_valid_game() {
        assert_eq!(true, valid_game(
            &vec![CubeCount::new(4, 3, 9)],
            &CubeCount::new(4, 5, 10)
        ));

        assert_eq!(false, valid_game(
            &vec![
                CubeCount::new(4, 3, 9),
                CubeCount::new(5, 5, 10)
            ],
            &CubeCount::new(4, 5, 10)
        ));

    }
}