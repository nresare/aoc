pub mod parse;
use std::cmp::max;

#[derive(Debug)]
pub struct Game {
    id: u32,
    rounds: Vec<CubeCount>,
}

impl Game {
    pub fn id(self) -> u32 {
        self.id
    }

    pub fn rounds(&self) -> &Vec<CubeCount> {
        &self.rounds
    }
}
#[derive(PartialEq, Debug, Clone)]
pub struct CubeCount {
    red: u32,
    green: u32,
    blue: u32,
}

impl CubeCount {
    pub fn new(red: u32, green: u32, blue: u32) -> Self {
        CubeCount{red, green, blue}
    }

    pub fn valid_for(&self, other: &CubeCount) -> bool {
        self.red <= other.red && self.green <= other.green && self.blue <= other.blue
    }

    pub fn max(self, other: CubeCount) -> CubeCount {
        CubeCount{
            red: max(self.red, other.red),
            green: max(self.green, other.green),
            blue: max(self.blue, other.blue),
        }
    }

    pub fn power(self) -> u32 {
        self.red * self.green * self.blue
    }
}