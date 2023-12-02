use std::collections::HashMap;
use anyhow::{Result, anyhow};
use phf::phf_map;
fn main() -> Result<()> {
    let mut sum: u32 = 0;
    let m = build_map();
    let rev_map = reverse_keys(&m);
    for line in include_str!("data.txt").lines() {
        sum += number_from_line(line, &m, &rev_map)?;
    }
    println!("{}", sum);
    Ok(())
}

fn build_map() -> HashMap<String, u8>{
    let mut map = HashMap::new();
    for (i, w) in [
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
    ].into_iter().enumerate() {
        map.insert(String::from(w), i as u8 + 1);
    }

    for i in 0..10 {
        map.insert(i.to_string(), i);
    }
    map
}

fn reverse_keys(map: &HashMap<String, u8>) -> HashMap<String, u8> {
    let mut result = HashMap::with_capacity(map.len());
    for (k, v) in map {
        result.insert(rev(k), *v);
    }
    result
}

fn rev(s: impl Into<String>) -> String
{
    s.into().chars().rev().collect()
}

fn number_from_line(
    line: &str,
    map: &HashMap<String, u8>,
    rev_map: &HashMap<String, u8>,
) -> Result<u32> {
    let s = format!(
        "{}{}",
        get_first_number(line, &map)?,
        get_first_number(rev(line), &rev_map)?
    );
    dbg!(&s, &line);
    Ok(s.parse()?)
}

fn get_first_number(line: impl Into<String>, map: &HashMap<String, u8>) -> Result<u8> {
    let line = line.into();
    for i in 0..line.len() {
        for (k, v) in map {
            if Some(i) == line.find(k) {
                return Ok(*v);
            }
        }
    }
    Err(anyhow!("Couldn't find number in '{line}'"))
}

#[cfg(test)]
mod tests {
    use crate::{build_map, get_first_number};

    #[test]
    fn test_get_first_number() {
        let map = build_map();
        assert_eq!(3, get_first_number("ab3", &map).unwrap());
        assert_eq!(8, get_first_number("eightwo", &map).unwrap());
    }

}