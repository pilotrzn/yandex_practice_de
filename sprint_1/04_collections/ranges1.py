def planting_plan(rows):
    rng = range(2, 2 + rows * 2, 2)
    return list(rng)


print(planting_plan(5))
