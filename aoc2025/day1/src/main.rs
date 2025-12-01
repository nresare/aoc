use anyhow::{anyhow, bail, Result};
use lazy_static::lazy_static;
use regex::{Match, Regex};

lazy_static! {
    static ref PATTERN: Regex = Regex::new(r"([LR])(\d+)").expect("invalid regex");
}

fn main() -> Result<()> {
    let mut zero_count = 0;
    let mut current_value = 50;
    for line in include_str!("input1.txt").lines() {
        let delta = parse(line)?;
        current_value += delta;
        while current_value > 99 {
            current_value -= 100;
        }
        while current_value < 0 {
            current_value += 100;
        }
        if current_value == 0 {
            zero_count += 1;
        }
    }
    println!("Part 1: {}", zero_count);
    let mut current_value = 0;
    let mut zero_count = 0;
    for line in include_str!("input1.txt").lines() {
        let delta = parse(line)?;
        let count;
        (current_value, count) = modify(current_value, delta);
        zero_count += count;
    }
    println!("Part 2: {}", zero_count);

    Ok(())
}

fn modify(mut current: i32, delta: i32) -> (i32, i32) {
    let mut count = 0;
    if current == 0 && delta < 0 {
        count -= 1;
    }
    current += delta;
    while current > 99 {
        current -= 100;
        count += 1;
    }
    while current < 0 {
        current += 100;
        count += 1;
    }
    if current == 0 && delta < 0 {
        count += 1;
    }
    (current, count)
}


fn parse(input: &str) -> Result<i32> {
    let c = PATTERN.captures(input).ok_or_else(|| anyhow!("invalid input format"))?;
    let num = as_i32(c.get(2))?;
    Ok(match c.get(1).ok_or_else(|| anyhow!("invalid input format"))?.as_str() {
        "L" => -num,
        "R" => num,
        _ => bail!("invalid input"),
    })
}

fn as_i32(value: Option<Match>) -> Result<i32> {
    let value = value.ok_or_else(|| anyhow!("no value"))?;
    let value = value.as_str();
    Ok(value.parse().map_err(|e| anyhow!("Could not parse {} as int {}", value, e))?)
}

#[cfg(test)]
mod tests {
    use crate::modify;

    #[test]
    fn test_modify() {
        assert_eq!(modify(50, 1000), (50, 10));
        assert_eq!(modify(50, -100), (50, 1));
        assert_eq!(modify(0, -5), (95, 0));
        assert_eq!(modify(50, -3), (47, 0));
        assert_eq!(modify(47, 49), (96, 0));
        assert_eq!(modify(96, 11), (7, 1));

        assert_eq!(modify(50, -50), (0, 1));
        assert_eq!(modify(0, 50), (50, 0));

        assert_eq!(modify(50, -50), (0, 1));
        assert_eq!(modify(0, -50), (50, 0));

        assert_eq!(modify(50, 50), (0, 1));
        assert_eq!(modify(0, -50), (50, 0));

        assert_eq!(modify(50, 50), (0, 1));
        assert_eq!(modify(0, 50), (50, 0));

        assert_eq!(modify(50, -150), (0, 2));
        assert_eq!(modify(0, 50), (50, 0));
    }
}