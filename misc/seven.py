from random import random


def rand7():
    while True:
        rand25 = rand5() + rand5() * 5
        if rand25 < 7 * 3:
            return rand25 % 7


def rand5():
    return int(random() * 5)


def test():
    counts = [0] * 7
    for i in range(1_000_000):
        value = rand7()
        counts[value] += 1
    print(counts)


if __name__ == "__main__":
    test()
