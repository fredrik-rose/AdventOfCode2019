# Day 1: The Tyranny of the Rocket Equation
def calculate_fuel_req(module):
    req = module // 3 - 2
    if req <= 0:
        return 0
    return req + calculate_fuel_req(req)


def part_one(fuel):
    req = sum(e // 3 - 2 for e in fuel)
    print("Fuel requirement: {}".format(req))


def part_two(fuel):
    req = sum(calculate_fuel_req(e) for e in fuel)
    print("Fuel requirement 2: {}".format(req))


def main():
    with open('1.txt') as f:
        fuel = [int(line) for line in f]
    part_one(fuel.copy())
    part_two(fuel.copy())


if __name__ == "__main__":
    main()
