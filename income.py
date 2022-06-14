"""
Calculate hourly, monthly, or yearly pay,
as well as the highest income of affordable rent possible.
There's also the option to subtract taxes and other expenses.
"""

from math import ceil
from re import sub


def get_income():
    """Get hourly, monthly, or yearly income as a dollar amount."""

    income = -1.0
    while income < 0:
        prompt = "Enter income in dollars and cents: $"
        income = input(prompt)
        income = sub("[^0-9.]", "", income)

        if not income:
            print("Income = $0.")
            income = 0.0

        elif income.count('.') <= 1 and income.replace('.', '').isdigit():
            income = float(income)
            income = round(income, 2)

        else:
            print("Error: The value entered is not a valid dollar amount.")
            income = -1.0

    return income


def get_rate():
    """Get a string to indicate pay rate."""

    rates = ["hourly", "monthly", "yearly"]
    rate = ""
    while rate not in rates:
        prompt = "Specify an hourly, monthly, or yearly pay rate: "
        rate = input(prompt)
        rate = rate.lower()

        if rate not in rates:
            print(f"Error: {rate} is not a valid pay rate.")

    return rate


def get_tax():
    """Get tax rate as a percentage."""

    tax = -1.0
    while tax < 0:
        prompt = "Enter a tax rate from 0 to 100%, " \
                    "or to skip taxes, press enter: "
        tax = input(prompt)

        if not tax:
            tax = 0.0

        # Check for valid numbers with decimal points
        elif tax.count('.') <= 1 and tax.replace('.', '').isdigit():
            tax = float(tax)

        else:
            print("Error: The value entered is not a valid tax rate. ")
            tax = -1.0

        # Check if given tax rate is over 100%
        if ceil(tax) > 100:
            print("Error: Tax rate must not excede 100%.")
            tax = -1.0

    return tax


def get_expenses():
    """Parse any additional expenses into a list."""

    expenses = []
    prompt =         "List all other expenses as percentages from 0 to 100, "\
        "separated by spaces. If there are no other expenses, press enter: "
    expense_str = input(prompt)

    # Remove non-numeric characters and split into a list
    expense_str =  sub("[^0-9. ]", "", expense_str)
    expense_str = expense_str.split()

    for exp in expense_str:
        exp = exp.strip()
        if exp.count('.') <= 1 and exp.replace('.', '').isdigit():
            exp = float(exp)
            expenses.append(exp)

        else:
            print(f"Warning: {exp} is an invalid expense percentage. "
                        "It will be excluded from the list of expenses.")
            continue

        if ceil(exp) > 100:
            print(f"Error: No single expense may exceed 100%. The value {exp} "
                                    "will be excluded from the list of expenses.")
            expenses.remove(exp)

    # Ensure that the expenses don't add up to more than 100%
    if sum(expenses) > 100:
        print("Error: The expenses must not exceed 100%. "
                    "Defaulting to no additional expenses.")
        expenses.clear()

    return expenses


def main():
    """Driver function"""

    try:
        income = get_income()
        rate = get_rate()
        tax = get_tax()
        expenses = get_expenses()

        # Include tax rate to total expenses
        expenses.append(tax)
        total_expenses = sum(expenses) / 100.0
        if total_expenses > 1.0:
            print("Error: total expenses may not exceed 100%. "
                "Defaulting to tax rate as the only expense.")
            total_expenses = tax / 100.0

        # Recalculate income
        original_income = income
        income = income - round(income * total_expenses, 2)

        # Calculate hourly, monthly, and yearly pay
        if rate == "hourly":
            hourly = income
            monthly = round(hourly * 160, 2)
            yearly = round(monthly * 12, 2)

        elif rate == "monthly":
            monthly = income
            hourly = round(monthly / 160, 2)
            yearly = round(monthly * 12, 2)

        elif rate == "yearly":
            yearly = income
            hourly = round(yearly / 1920, 2)
            monthly = round(yearly / 12, 2)

        # Calculate maximum affordable rent
        rent = round(monthly / 3, 2)

        # Print income info
        print(f"""
            Take-home pay for income of ${original_income} per {rate[:-2]}:

            ${hourly} per hour.
            ${monthly} per month.
            ${yearly} per year.
        Highest affordable rent = ${rent} per month.""")

        return hourly, monthly, yearly, rent

    except ValueError:
        print("One of the values is invalid. Please try again.")

    except:
        print("Something went wrong. Please try again.")


if __name__ == "__main__":
    main()
