use anyhow::{anyhow, Result};

fn main() -> Result<()> {
    let mut sum: u32 = 0;
    for line in include_str!("data.txt").lines() {
        sum += number_from_line(line)?;
    }
    println!("{}", sum);
    Ok(())
}

fn number_from_line(line: &str) -> Result<u32> {
    let s = format!(
        "{}{}",
        get_first_number(line.chars())?,
        get_first_number(line.chars().rev())?
    );
    Ok(s.parse()?)
}

fn get_first_number(chars: impl Iterator<Item = char>) -> Result<char> {
    for c in chars {
        if c.is_ascii_digit() {
            return Ok(c);
        }
    }
    Err(anyhow!("Could not find a number in chars"))
}

#[cfg(test)]
mod tests {
    use crate::*;

    #[test]
    fn test_get_first_number() {
        assert_eq!('4', get_first_number("abc4de".chars()).unwrap());
    }

    #[test]
    fn test_get_last_number() {
        assert_eq!('7', get_first_number("abc4de77si".chars().rev()).unwrap());
    }

    #[test]
    fn test_number_from_line() {
        assert_eq!(12, number_from_line("1abc2").unwrap());
    }
}
