from django.shortcuts import render

# Create your views here.

from ninja import NinjaAPI
from pydantic import BaseModel
from django.http import JsonResponse

api = NinjaAPI(urls_namespace="validation_api")
#Equal split Input: amount, number of people

class EqualSplitRequest(BaseModel):
    amount: float
    n: int

class ValidPercentagesRequest(BaseModel):
    percentages: list

class ValidAmountsRequest(BaseModel):
    total: float
    contributions: list

@api.post("/equalsplit")
def equal_split(request, payload: EqualSplitRequest):
    amount = payload.amount
    n = payload.n
    if n <= 0:
        return JsonResponse({"error": "Number of participants must be greater than zero."}, status=400)
    splits = equalsplit(amount, n)
    return {"splits": splits}

@api.post("/validpercentages")
def validate_percentages(request, payload: ValidPercentagesRequest):
    percentages = payload.percentages
    if validPercentages(percentages):
        return {"valid": True}
    return {"valid": False, "error": "Percentages must sum up to 100."}

@api.post("/validamounts")
def validate_amounts(request, payload: ValidAmountsRequest):
    total = payload.total
    contributions = payload.contributions
    if validAmounts(total, contributions):
        return {"valid": True}
    return {"valid": False, "error": "Contributions must sum up to the total amount."}

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

