def make_juice(fruit):
    return f"{fruit}+🥤"

def add_ice(juice):
    return f"{juice}+🧊"

def add_sugar(icde_juice):
    return f"{icde_juice}+🍬"

juice = make_juice("🍎")
cold_juice = add_ice(juice)
perfect_juice = add_sugar(cold_juice)

print()