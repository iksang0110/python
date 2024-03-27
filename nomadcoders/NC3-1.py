# # 👇🏻 Write your code here 👇🏻:
# def get_yearly_revenue(monthly_revenue):
#     yearly_revenue = monthly_revenue * 12
#     return yearly_revenue

# def get_yearly_expenses(monthly_expenses):
#     yearly_expenses = monthly_expenses * 12
#     return yearly_expenses

# def get_tax_amount(profit):
#     if profit > 100000:
#         tax_amount = profit * 0.25
#     else:
#         tax_amount = profit * 0.15
#     return tax_amount

# def apply_tax_credits(tax_amount, tax_credits):
#     discount_amount = tax_amount * tax_credits
#     return discount_amount

#     # ❌ Don't touch anthing below this line ❌


# monthly_revenue = 5500000
# monthly_expenses = 2700000
# tax_credits = 0.01

# yearly_revenue = get_yearly_revenue(monthly_revenue)
# yearly_expenses = get_yearly_expenses(monthly_expenses)

# profit = yearly_revenue - yearly_expenses

# tax_amount = get_tax_amount(profit)

# final_tax_amount = tax_amount - apply_tax_credits(tax_amount, tax_credits)

# print(f"Your tax bill is: ${final_tax_amount}"

# 👇🏻 Write your code here 👇🏻:
def get_yearly_revenue(monthly_revenue):
    return monthly_revenue*12


def get_yearly_expenses(monthly_expenses):
    return monthly_expenses*12


def get_tax_amount(profit):
    if profit > 100000:
        return profit*0.25
    else:
        return profit*0.15


def apply_tax_credits(tax_amount, tax_credits):
    return tax_amount * tax_credits

# ❌ Don't touch anthing below this line ❌


monthly_revenue = 5500000
monthly_expenses = 2700000
tax_credits = 0.01

yearly_revenue = get_yearly_revenue(monthly_revenue)
yearly_expenses = get_yearly_expenses(monthly_expenses)

profit = yearly_revenue - yearly_expenses

tax_amount = get_tax_amount(profit)

final_tax_amount = tax_amount - apply_tax_credits(tax_amount, tax_credits)

print(f"Your tax bill is: ${final_tax_amount}")
