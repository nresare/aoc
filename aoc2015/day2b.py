# advent of code 2015, day 2b

def main():
    with open("input/day2.txt", "r") as f:
        total_amount = 0
        for data in f:
            data = data.rstrip()
            total_amount += get_string_length(*(int(x) for x in data.split("x")))
        print(total_amount)


def get_string_length(x: int, y: int, z: int) -> int:
    sorted_sides = sorted((x, y, z))
    return (x * y * z) + (2 * sorted_sides[0]) + (2 * sorted_sides[1])


if __name__ == "__main__":
    main()
