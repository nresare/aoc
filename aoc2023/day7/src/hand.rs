use anyhow::anyhow;
use counter::Counter;
use std::cmp::Ordering;
use std::fmt::{Debug, Formatter};


const VALID: &[u8] = "AKQJT98765432".as_bytes();


#[derive(PartialOrd, PartialEq, Ord, Eq, Debug)]
enum HandType {
    FiveOfAKind,
    FourOfAKind,
    FullHouse,
    ThreeOfAKind,
    TwoPair,
    OnePair,
    HighCard
}


#[derive(Eq)]
pub struct Hand {
    values: [u8; 5],
}

impl Hand {
    pub fn new(data: &str) -> anyhow::Result<Self> {
        if data.len() != 5 {
            return Err(anyhow!("Wrong length of data: {}", data.len()))
        }
        for c in data.as_bytes() {
            if ! VALID.contains(c) {
                return Err(anyhow!("Invalid character {}", *c as char))
        }
        }
        Ok(Hand{values: data.as_bytes().try_into().expect("input has incorrect length")})
    }

    fn best_type(&self) -> HandType {
        let counts = self.values.into_iter().collect::<Counter<_>>();
        let counts = counts.values().map(|x| *x).collect::<Vec<_>>();
        if counts.contains(&5) {
            HandType::FiveOfAKind
        } else if counts.contains(&4) {
            HandType::FourOfAKind
        } else if counts.contains(&3) {
            if counts.contains(&2) {
                HandType::FullHouse
            } else {
                HandType::ThreeOfAKind
            }
        } else if counts.contains(&2) {
            let mut pair_count = 0;
            for c in counts {
                if c == 2 {
                    pair_count += 1;
                }
            }
            if pair_count == 2 {
                HandType::TwoPair
            } else {
                HandType::OnePair
            }
        } else {
            HandType::HighCard
        }
    }
}

impl Debug for Hand {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        f.debug_tuple("")
            .field(&std::str::from_utf8(&self.values[..]).unwrap())
            .finish()
    }
}

impl PartialEq<Self> for Hand {
    fn eq(&self, other: &Self) -> bool {
        self.values == other.values
    }
}



impl PartialOrd<Self> for Hand {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Hand {
    fn cmp(&self, other: &Self) -> Ordering {
        let this_type = self.best_type();
        let other_type = other.best_type();
        match other_type.cmp(&this_type) {
            Ordering::Equal => compare_by_card_value(other, self),
            ordering => ordering,
        }
    }
}

fn get_card_value(card: u8) -> u32 {
    VALID.iter().position(|i| *i == card).expect("invalid card") as u32
}
fn compare_by_card_value(a: &Hand, b: &Hand) -> Ordering{
    let mut a = a.values.into_iter().map(get_card_value);
    let mut b = b.values.into_iter().map(get_card_value);
    while let Some(a_value) = a.next() {
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
    use std::cmp::Ordering;
    use crate::hand::HandType;
    use crate::hand::Hand;
    use crate::hand::HandType::*;

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
        assert_eq!(expected, Hand::new(second).unwrap().cmp(&Hand::new(first).unwrap()))
    }

    #[test]
    fn test_sort() {
        let mut v = vec![
            Hand::new("AAAAA").unwrap(),
            Hand::new("KK677").unwrap(),
            Hand::new("KTJJT").unwrap(),
        ];
        v.sort();
        assert_eq!(
            vec![
                Hand::new("KTJJT").unwrap(),
                Hand::new("KK677").unwrap(),
                Hand::new("AAAAA").unwrap(),
            ],
            v
        );
    }

}