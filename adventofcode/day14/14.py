# Day 14: Space Stoichiometry
import collections as coll
import math


RAW_MATERIEL = 'ORE'
FUEL = 'FUEL'


def parse_reactions(path):
    chemicals = {}
    with open(path) as file:
        for line in file:
            chemicals.update(parse_sigle_reaction(line.rstrip('\n')))
    return chemicals


def parse_sigle_reaction(reaction):
    def parse_chemical(chemical):
        amount, name = chemical.split(' ')
        return int(amount), name

    inputs, output = reaction.split(' => ')
    amount, name = parse_chemical(output)
    return {name: (amount, [parse_chemical(c) for c in inputs.split(', ')])}


def chemial_cost(name, amount, chemicals, excess):
    if name == RAW_MATERIEL:
        return amount
    amount_to_take_from_excess = min(excess[name], amount)
    excess[name] -= amount_to_take_from_excess
    amount -= amount_to_take_from_excess
    amount_per_batch = chemicals[name][0]
    batches = int(math.ceil(amount / amount_per_batch))
    actual_amount = batches * amount_per_batch
    excess[name] += actual_amount - amount
    return sum(chemial_cost(chemical[1], chemical[0] * batches, chemicals, excess) for chemical in chemicals[name][1])


def part_one(chemicals):
    excess = coll.defaultdict(int)
    cost = chemial_cost(FUEL, 1, chemicals, excess)
    print("Cost to create 1 fuel: {}".format(cost))


def part_two(chemicals):
    ore = 1000000000000
    # Do a binary search.
    min_fuel = ore // chemial_cost(FUEL, 1, chemicals, coll.defaultdict(int))  # Lower limit of fuel amount.
    max_fuel = min_fuel * 2  # It is very unlikely that the excess should be enough for doubling the amount of fuel.
    while min_fuel < max_fuel:
        fuel = (max_fuel + min_fuel) // 2
        cost = chemial_cost(FUEL, fuel, chemicals, coll.defaultdict(int))
        if cost > ore:
            max_fuel = fuel - 1
        else:
            min_fuel = fuel
    assert(min_fuel == max_fuel)
    print("Max fuel from a trillion ore: {}".format(max_fuel))


def main():
    chemicals = parse_reactions('14.txt')
    part_one(chemicals.copy())
    part_two(chemicals.copy())


if __name__ == "__main__":
    main()
