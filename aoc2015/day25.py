# advent of code 2015 day 25

def main():
    assert 1 == get_cell_ordinal(1, 1)
    assert 12 == get_cell_ordinal(4, 2)
    assert 15 == get_cell_ordinal(1, 5)
    assert 31916031 == get_next(20151125)

    current = 20151125
    ordinal = get_cell_ordinal(2981, 3075)
    # one less, because we already have the number at field 1
    print(f"Generating value for field {ordinal}")
    for i in range(ordinal - 1):
        current = get_next(current)
    print(current)


def get_cell_ordinal(rows: int, columns: int) -> int:
    diagonal_before = rows + columns - 2
    count_up_to_current_diagonal = diagonal_before * (diagonal_before + 1) // 2
    return count_up_to_current_diagonal + columns


def get_next(current: int) -> int:
    return current * 252533 % 33554393


if __name__ == "__main__":
    main()


