use std::collections::{HashMap, HashSet};
use anyhow::{anyhow, Result};

#[derive(PartialEq, Debug)]
struct Card {
    winners: HashSet<i32>,
    numbers: Vec<i32>,
}

impl Card {
    fn parse(input: &str) -> Result<Self> {
        let parts: Vec<&str> = input.split(": ").collect();
        if parts.len() != 2 {
            return Err(anyhow!("Invalid format"))
        }
        let input = parts[1];
        let parts: Vec<_> = input.split(" | ").collect();
        if parts.len() != 2 {
            return Err(anyhow!("Invalid format"))
        }
        let winners: HashSet<i32> = parts[0].split_whitespace().map(
            |s| s.parse().unwrap()
        ).collect();
        let numbers: Vec<i32> = parts[1].split_whitespace().map(|s| s.parse().unwrap()).collect();
        Ok(Card{winners, numbers})
    }

    fn points(&self) -> i32 {
        match self.winners() {
            0 => 0,
            i => 1 << i - 1,
        }
    }

    fn winners(&self) -> i32 {
        let mut count = 0;
        for i in self.numbers.iter() {
            if self.winners.contains(i) {
                count += 1;
            }
        }
        count
    }
}

fn main() -> Result<()> {
    let cards: Vec<Card> = include_str!("example.txt").lines().map(Card::parse).collect::<Result<_>>()?;
    println!("part 1: {}", cards.iter().map(Card::points).sum::<i32>());
    let mut m = HashMap::new();
    for (i, card) in cards.iter().enumerate() {
        let number = i + 1;
        m.entry(number).and_modify(|i| i.increment()).or_insert(1);
        println!("{} {:?}", number, card);
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::Card;

    #[test]
    fn test_parse() {
        let card = Card::parse("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53").unwrap();
        assert_eq!(Card{
            winners: [41, 48, 83, 86, 17].into_iter().collect(),
            numbers: vec![83, 86, 6, 31, 17, 9, 48, 53]
        }, card);
    }

}