fn main() {
    let data = parse(include_str!("data.txt"));
    println!("Part 1: {}", data.iter().map(get_next).sum::<i32>());
}

fn get_next(numbers: &Vec<i32>) -> i32 {
    let mut numbers = numbers.clone();
    let mut sum = 0;
    while !all_zeroes(&numbers) {
        sum += numbers.last().expect("needs at least one");
        numbers = differences(&numbers);
    }
    sum
}

fn parse(input: &str) -> Vec<Vec<i32>> {
    input.lines().map(parse_line).collect()
}

fn parse_line(line: &str) -> Vec<i32> {
    line.split(' ')
        .map(|s| s.parse().expect("Could not parse as int"))
        .collect()
}

fn differences(numbers: &Vec<i32>) -> Vec<i32> {
    let mut numbers = numbers.iter();
    let mut result = Vec::new();
    let mut prev = numbers.next().expect("must have ate least one number");
    for number in numbers {
        result.push(number - prev);
        prev = number
    }
    result
}

fn all_zeroes(numbers: &Vec<i32>) -> bool {
    for n in numbers {
        if *n != 0 {
            return false;
        }
    }
    true
}
