# advent of code 2015, day 2

def main():
    with open("input/day2.txt", "r") as f:
        total_amount = 0
        for data in f:
            data = data.rstrip()
            total_amount += get_paper_amount(*(int(x) for x in data.split("x")))
        print(total_amount)


def get_paper_amount(x: int, y: int, z: int) -> int:
    sizes = (x * y * 2, y * z * 2, z * x * 2)
    return sum(sizes) + int((min(sizes) / 2))


if __name__ == "__main__":
    main()
