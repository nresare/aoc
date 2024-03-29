use crate::HandType::{FullHouse, OnePair, ThreeOfAKind, TwoPair};
use anyhow::anyhow;
use counter::Counter;
use std::cmp::Ordering;
use std::fmt::{Debug, Formatter};

fn main() {
    let mut v = parse(include_str!("input.txt"));
    v.sort_by(part_1_compare);
    println!("part 1: {}", count(&v));
    v.sort_by(part_2_compare);
    println!("part 2: {}", count(&v));
}

fn count(sorted_games: &[(Hand, u32)]) -> u32 {
    sorted_games
        .iter()
        .enumerate()
        .map(|(i, (_, bet))| bet * (i + 1) as u32)
        .sum()
}

const ORDER_PART_2: &[u8] = "AKQT98765432J".as_bytes();

fn part_2_compare(a: &(Hand, u32), b: &(Hand, u32)) -> Ordering {
    let this_type = best_type_with_joker(&a.0);
    let other_type = best_type_with_joker(&b.0);
    match other_type.cmp(&this_type) {
        Ordering::Equal => compare_by_card_value(&b.0, &a.0, ORDER_PART_2),
        ordering => ordering,
    }
}

fn part_1_compare(a: &(Hand, u32), b: &(Hand, u32)) -> Ordering {
    let this_type = a.0.best_type();
    let other_type = b.0.best_type();
    match other_type.cmp(&this_type) {
        Ordering::Equal => compare_by_card_value(&b.0, &a.0, ORDER),
        ordering => ordering,
    }
}

fn convert_jokers(hand: &Hand) -> Hand {
    let freqs = hand
        .values
        .into_iter()
        .map(|i| i as char)
        .collect::<Counter<_>>();
    if !freqs.contains_key(&'J') || freqs[&'J'] == 5 {
        // no jokers to convert
        return hand.clone();
    }

    let by_order = freqs.most_common_ordered();
    let convert_to = if by_order[0].0 == 'J' {
        // jokers are the most common. Turn the jokers into the next most common
        by_order[1].0
    } else {
        // jokers are not the most common, turn them into the most common
        by_order[0].0
    };
    let s = &String::from_utf8_lossy(&hand.values[..])[..];
    let result = s.replace('J', &convert_to.to_string()[..]);
    Hand::new(&result[..]).expect("Failed to construct hand")
}

fn best_type_with_joker(hand: &Hand) -> HandType {
    let hand = convert_jokers(hand);

    let counts = hand.values.into_iter().collect::<Counter<_>>();
    let counts = counts.values().copied().collect::<Vec<_>>();
    counts_to_hand_type(counts)
}

fn counts_to_hand_type(mut counts: Vec<usize>) -> HandType {
    counts.sort();
    match counts[counts.len() - 1] {
        5 => HandType::FiveOfAKind,
        4 => HandType::FourOfAKind,
        3 => {
            if counts.contains(&2) {
                FullHouse
            } else {
                ThreeOfAKind
            }
        }
        2 => {
            if counts[counts.len() - 2] == 2 {
                TwoPair
            } else {
                OnePair
            }
        }
        _ => HandType::HighCard,
    }
}

fn parse(input: &str) -> Vec<(Hand, u32)> {
    input
        .lines()
        .map(|l| {
            let mut parts = l.split_whitespace();
            (
                Hand::new(parts.next().unwrap()).unwrap(),
                parts.next().unwrap().parse::<u32>().unwrap(),
            )
        })
        .collect()
}

const ORDER: &[u8] = "AKQJT98765432".as_bytes();

#[derive(PartialOrd, PartialEq, Ord, Eq, Debug)]
pub enum HandType {
    FiveOfAKind,
    FourOfAKind,
    FullHouse,
    ThreeOfAKind,
    TwoPair,
    OnePair,
    HighCard,
}

#[derive(Clone, PartialEq)]
pub struct Hand {
    pub(crate) values: [u8; 5],
}

impl Hand {
    pub fn new(data: &str) -> anyhow::Result<Self> {
        if data.len() != 5 {
            return Err(anyhow!("Wrong length of data: {}", data.len()));
        }
        for c in data.as_bytes() {
            if !ORDER.contains(c) {
                return Err(anyhow!("Invalid character {}", *c as char));
            }
        }
        Ok(Hand {
            values: data
                .as_bytes()
                .try_into()
                .expect("input has incorrect length"),
        })
    }

    pub(crate) fn best_type(&self) -> HandType {
        let counts = self.values.into_iter().collect::<Counter<_>>();
        let counts = counts.values().copied().collect::<Vec<_>>();
        counts_to_hand_type(counts)
    }
}

impl Debug for Hand {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        f.debug_tuple("")
            .field(&std::str::from_utf8(&self.values[..]).unwrap())
            .finish()
    }
}

fn get_card_value(card: u8, positions: &[u8]) -> u32 {
    positions
        .iter()
        .position(|i| *i == card)
        .expect("invalid card") as u32
}
pub(crate) fn compare_by_card_value(a: &Hand, b: &Hand, positions: &[u8]) -> Ordering {
    let a = a.values.into_iter().map(|x| get_card_value(x, positions));
    let mut b = b.values.into_iter().map(|x| get_card_value(x, positions));
    for a_value in a {
        let b_value = b.next().expect("a and be not equally long");
        match a_value.cmp(&b_value) {
            Ordering::Greater => return Ordering::Greater,
            Ordering::Less => return Ordering::Less,
            Ordering::Equal => {}
        }
    }
    Ordering::Equal
}

#[cfg(test)]
mod tests {
    use crate::Hand;
    use crate::HandType;
    use crate::HandType::*;
    use crate::{convert_jokers, part_1_compare};
    use std::cmp::Ordering;

    #[test]
    fn test_new_hand() {
        let error = Hand::new("A").unwrap_err();
        assert_eq!(error.to_string(), "Wrong length of data: 1");
        let error = Hand::new("fooba").unwrap_err();
        assert_eq!(error.to_string(), "Invalid character f");

        let _hand = Hand::new("AAAAK").unwrap();
    }

    #[test]
    fn test_best_kind() {
        best_kind("AAAAA", FiveOfAKind);
        best_kind("AAAA2", FourOfAKind);
        best_kind("AAAKK", FullHouse);
        best_kind("AAA24", ThreeOfAKind);
        best_kind("AAKK2", TwoPair);
        best_kind("AA234", OnePair);
        best_kind("23456", HighCard);
    }

    fn best_kind(input: &str, t: HandType) {
        let hand = Hand::new(input).unwrap();
        assert_eq!(t, hand.best_type())
    }

    #[test]
    fn test_cmp() {
        cmp("AAAAA", "23456", Ordering::Greater);
        cmp("AAKKK", "AAKK2", Ordering::Greater);
        cmp("2355A", "AAA34", Ordering::Less);
        cmp("AAAAA", "KKKKK", Ordering::Greater);
        cmp("AAAAA", "AAAAA", Ordering::Equal);
        cmp("KK677", "KTJJT", Ordering::Greater);
    }

    fn cmp(first: &str, second: &str, expected: Ordering) {
        assert_eq!(
            expected,
            part_1_compare(
                &(Hand::new(first).unwrap(), 0),
                &(Hand::new(second).unwrap(), 0)
            ),
        )
    }

    #[test]
    fn test_convert_jokers() {
        cj("AAAKK", "AAAKK");
        cj("AAAJJ", "AAAAA");
        cj("JJJJA", "AAAAA");
    }

    fn cj(from: &str, to: &str) {
        let result = convert_jokers(&Hand::new(from).unwrap());
        assert_eq!(Hand::new(to).unwrap(), result);
    }
}
