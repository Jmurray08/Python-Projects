print("If the guest had outstanding service (1), calculate a 25 percent tip.")
print("If the guest had good service (2), calculate a 20 percent tip.")
print("If the guest had below average service (3), calculate a custom tip.")

CostOfTheMeal = input("Enter the total cost of the meal: $")

Satisfy = input("How satisfied were you? 1 = Outstanding Service, 2 = Good Service, 3 = Below Average Service: ")


if Satisfy == "1":
    tip = round((float(CostOfTheMeal) * 25)/100, 2)
    print("The tip due to outstanding service will amount to: $" + str(float(tip)))
    total = float(tip) + float(CostOfTheMeal)
    print("The total cost after tip brings the meal amount to: $" + str(round(total, 2)))
elif Satisfy == "2":
    tip = round((float(CostOfTheMeal) * 20)/100, 2)
    print("The tip due to good service will amount to: $" + str(float(tip)))
    total = float(tip) + float(CostOfTheMeal)
    print("The total cost after tip brings the meal amount to: $" + str(round(total, 2)))
elif Satisfy == "3":
    Custom = float(input("Input a custom tip: $"))
    print("The tip due to below average service will amount to: $" + str(round(float(Custom), 2)))
    total1 = float(Custom) + float(CostOfTheMeal)
    print("The total cost after tip brings the meal amount to: $" + str(round(total1, 2)))
else:
    print("Invalid rating. Please try again!")
            



