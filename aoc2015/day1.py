# advent of code 2015, day 1

def main():
    with open("input/day1.txt", "r") as f:
        data: str = f.read()
        data = data.rstrip()
    print(find_floor(data))


def find_floor(code: str) -> int:
    lefts = rights = 0
    for c in code:
        if c == '(':
            lefts += 1
        elif c == ")":
            rights += 1
    return lefts - rights


if __name__ == "__main__":
    main()
