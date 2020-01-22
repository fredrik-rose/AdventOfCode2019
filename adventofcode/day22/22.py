# Day 22: Slam Shuffle
import functools as ftools


def parse(file_path, parser):
    with open(file_path) as f:
        return [parse_instruction(line.rstrip('\n'), parser) for line in f]


def parse_instruction(instruction, parser):
    if instruction.startswith("deal into new stack"):
        return parser['deal']()
    elif instruction.startswith("cut"):
        return parser['cut'](int(instruction.split(' ')[-1]))
    elif instruction.startswith("deal with increment"):
        return parser['shuffle'](int(instruction.split(' ')[-1]))
    else:
        print("ERROR: Invalid instruction.", flush=True)


def apply_linear_function(a, b, x):
    return a * x + b


def compose_linear_with_modulo(n, *coefficients):
    # Coefficients is a list of pairs:
    # [(a1, b1), (a2, b2), ..., (aN, bN)]
    # where each pair defines an equation: y = a*x + b % n.
    (a, b) = ftools.reduce(lambda x, y: ((y[0] * x[0]) % n, (y[0] * x[1] + y[1]) % n), coefficients)
    return a, b


def modular_inverse(a, m):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def exp_by_squaring(mul_func, x, n):
    assert n >= 0
    if n == 0:
        return 1
    elif n == 1:
        return x
    elif is_even(n):
        return exp_by_squaring(mul_func, mul_func(x, x), n // 2)
    elif is_odd(n):
        return mul_func(x, exp_by_squaring(mul_func, mul_func(x, x), (n - 1) // 2))


def is_even(x):
    return (x % 2) == 0


def is_odd(x):
    return not is_even(x)


def part_one():
    deck_size = 10007
    card = 2019
    linear_equation_parser = {'deal': lambda: (-1, deck_size - 1),
                              'cut': lambda x: (1, -x),
                              'shuffle': lambda x: (x, 0)}
    instructions = parse('22.txt', linear_equation_parser)
    a, b = compose_linear_with_modulo(deck_size, *instructions)
    position = apply_linear_function(a, b, 2019) % deck_size
    print("Position of card {}: {}".format(card, position))


def part_two():
    deck_size = 119315717514047
    number_of_shuffles = 101741582076661
    card_position = 2020
    reverse_linear_equation_parser = {'deal': lambda: (-1, deck_size - 1),
                                      'cut': lambda x: (1, x),
                                      'shuffle': lambda x: (modular_inverse(x, deck_size), 0)}
    instructions = parse('22.txt', reverse_linear_equation_parser)[::-1]
    a, b = compose_linear_with_modulo(deck_size, *instructions)
    a, b = exp_by_squaring(lambda a, b: compose_linear_with_modulo(deck_size, a, b), (a, b), number_of_shuffles)
    card = apply_linear_function(a, b, card_position) % deck_size
    print("Card at position {}: {}".format(card_position, card))


def main():
    part_one()
    part_two()


if __name__ == "__main__":
    main()
