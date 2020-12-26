# advent of code 2015, day 12
import json
from typing import Iterator, Dict, Any, List


def main():
    with open("input/day12.txt", "r") as f:
        data = json.load(f)
        print(sum_numbers(data))


def sum_numbers_list(data: List[Any]) -> int:
    summa = 0
    for item in data:
        if type(item) is dict:
            summa += sum_numbers(item)
        if type(item) is list:
            summa += sum_numbers_list(item)
        if type(item) is int:
            summa += item
    return summa


def sum_numbers(data: Dict[Any, Any]) -> int:
    for value in data.values():
        if value == "red":
            return 0
    summa = 0
    for value in data.values():
        if type(value) is dict:
            summa += sum_numbers(value)
        if type(value) is list:
            summa += sum_numbers_list(value)
        if type(value) is int:
            summa += value
    return summa


if __name__ == "__main__":
    main()
