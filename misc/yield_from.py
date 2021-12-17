from typing import Iterator


def outer_generator(source: Iterator[int]):
    return (x for x in source if x % 2 == 0)


if __name__ == "__main__":
    print(list(outer_generator(range(10))))
