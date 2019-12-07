# Day 4: Secure Container
import collections as coll
import numpy as np


def get_numbers_that_meet_crteria(start, end, critera):
    return [n for n in range(start, end + 1) if critera(n)]


def password_critera_1(password):
    digits = [int(c) for c in str(password)]
    diff = list(np.diff(digits))
    return any(d == 0 for d in diff) and all(d >= 0 for d in diff)


def password_critera_2(password):
    digits = [int(c) for c in str(password)]
    diff = list(np.diff(digits))
    counts = coll.Counter(digits)
    return all(d >= 0 for d in diff) and any(c == 2 for c in counts.values())


def main():
    start = 130254
    end = 678275
    for i, criteria in enumerate((password_critera_1, password_critera_2)):
        numbers = get_numbers_that_meet_crteria(start, end, criteria)
        print("Number of passwords that meet criteria {}: {}".format(i + 1, len(numbers)))


if __name__ == "__main__":
    main()
