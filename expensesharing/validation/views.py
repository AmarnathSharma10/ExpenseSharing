from django.shortcuts import render

# Create your views here.

#Equal split Input: amount, number of people
def equalsplit(amount,n):
    split=round(amount/n,3)
    splits=[split]*n
    total=round(sum(splits),3)
    if total!=round(amount,3):
        difference=round(amount,3)-total
        splits[-1]=round(splits[-1]+difference,3)

    return splits
def validPercentages(percentages):
    return sum(percentages) == 100
def validAmounts(total,contributions):
    return sum(contributions)==total

