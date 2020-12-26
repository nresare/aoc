# advent of code 2015, day 11

def main():
    candidate = next_password("hepxxyzz")
    i = 1
    while not is_good(candidate):
        candidate = next_password(candidate)
        print(f"trying {candidate} {i}")
        i += 1
    print(candidate )


A_POS = ord("a")
Z_POS = ord("z")


def next_password(current: str) -> str:
    if current == 8 * "z":
        return 8 * "a"
    if len(current) != 8:
        raise ValueError(f"{current} is not 8 chars long")
    ords = [ord(x) for x in reversed(current)]
    for i, n in enumerate(ords):
        if n < Z_POS:
            ords[i] += 1
            return "".join(chr(x) for x in reversed(ords))
        else:
            ords[i] = A_POS
    raise ValueError("Logic error")


def find_three_increasing(s: str) -> bool:
    for i in range(len(s)):
        if i + 3 > len(s):
            return False
        if ord(s[i]) == ord(s[i + 1]) - 1 and ord(s[i + 1]) == ord(s[i + 2]) - 1:
            return True
    return False


def find_two_repeats(s: str) -> bool:
    first_repeated = False
    inside_repeat = False
    for i in range(len(s)):
        if i + 2 > len(s):
            return False
        if inside_repeat:
            inside_repeat = False
        if s[i] == s[i + 1]:
            if first_repeated and s[i] != first_repeated:
                return True
            first_repeated = s[i]
    return False


def is_good(candidate: str) -> bool:
    for bad in "iol":
        if bad in candidate:
            return False
    if not find_three_increasing(candidate):
        return False
    if not find_two_repeats(candidate):
        return False
    return True


if __name__ == "__main__":
    main()
