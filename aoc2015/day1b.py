# advent of code 2015, day 1, extra credit

def main():
    with open("input/day1.txt", "r") as f:
        data: str = f.read()
        data = data.rstrip()
    print(find_floor(data))


def find_floor(code: str) -> int:
    floor = 0
    for i, c in enumerate(code):
        if c == '(':
            floor += 1
        elif c == ")":
            floor -= 1
        if floor < 0:
            return i + 1
    raise ValueError("Santa never reaches the basement")


if __name__ == "__main__":
    main()
