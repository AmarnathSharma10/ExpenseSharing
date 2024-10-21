from django.shortcuts import render
from typing import List,Optional,Dict,Union
from pydantic import BaseModel
from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Expense,ParticipantExpense
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from validation.views import equalsplit,validAmounts,validPercentages
import csv
from django.http import HttpResponse
api = NinjaAPI(urls_namespace="main_api")
class ExpenseIn(BaseModel):#required user inputs to add a expense
    service:str
    amount:float
    split_type:Optional[str]=None
    participants: Optional[Union[List[str],Dict[str,float]]]=None #list for equal split dictionary for other splits
class ExpenseUpdate(BaseModel):
    amount:Optional[float]=None
    split_type:Optional[str]=None
    participants: Optional[Union[List[str], Dict[str, float]]] = None

@login_required
@api.post("/expense")
def create_expense(request,expense_data:ExpenseIn):
    user=request.user
    creator=get_object_or_404(Profile,user=user)
    service=expense_data.service
    amount=expense_data.amount
    split=expense_data.split_type
    participants=expense_data.participants
    if not split or split.lower() not in ["equal","exact","percentage"]:
        expense=Expense.objects.create(service=service,cost=amount,creator=creator)
        return {"message":"Added expense"},201
    expense=Expense.objects.create(service=service,cost=amount,creator=creator,split_method=split)
    if not participants:
        return {"message":"expense added but no participants"},201
    if split.lower()=="equal":
        if isinstance(participants,list):
            equalSplit(expense,participants)
        else:
            return {"error":"For equal split list is needed "},400

    elif split.lower() =="exact" :
        if isinstance(participants, dict):
            if exactSplit(expense,participants):
                return {"message":"added successfully"},201
            else:return {"error":"invalid contribution  data"},400
        else:
            return {"error": "For exact split dictionary is needed "}, 400
    else:
        if isinstance(participants, dict):
            if percentSplit(expense,participants):
                return {"message":"added successfully"},201
            else:return {"error":"invalid percent data"},400
        else:
            return {"error": "For percent split dictionary is needed "}, 400


@login_required
@api.put("/expense/{expense_id}")
def update_expense(request, expense_id: int, expense_data: ExpenseUpdate):

    user = request.user
    profile = get_object_or_404(Profile, user=user)
    expense = get_object_or_404(Expense, id=expense_id, creator=profile)
    if expense_data.amount is not None:
        expense.cost = expense_data.amount

    if expense_data.split_type is not None:
        expense.split_method = expense_data.split_type

    expense.save()
    if expense_data.participants is not None:
        participants=expense_data.participants
        expense.participants.clear()
    else:
        if isinstance(expense.participants,list):
            participants=[participant.user.username for participant in expense.participants]
        else:
            participants={participant.user.username: contrib  for participant, contrib in expense.participants.items()} 
    split=expense.split_method
    if not participants:
        return {"message":"expense edited but no participants"},201
    if split.lower()=="equal":
        if isinstance(participants,list):
            equalSplit(expense,participants)
        else:
            return {"error":"For equal split list is needed "},400

    elif split.lower() =="exact" :
        if isinstance(participants, dict):
            if exactSplit(expense,participants):
                return {"message":"added successfully"},201
            else:return {"error":"invalid contribution  data"},400
        else:
            return {"error": "For exact split dictionary is needed "}, 400
    else:
        if isinstance(participants, dict):
            if percentSplit(expense,participants):
                return {"message":"added successfully"},201
            else:return {"error":"invalid percent data"},400
        else:
            return {"error": "For percent split dictionary is needed "}, 400

@login_required
@api.get("/expenses")
def retrieve_expenses(request):
    user=request.user
    profile=get_object_or_404(Profile,user=user)
    expenses=ParticipantExpense.objects.filter(profile=profile)
    expenses_list = [
        {
            "service_name": expense.expense.item_service,
            "amount_owed": expense.amount_owed,
            "date_timestamp": expense.expense.created_at,
        }
        for expense in expenses
    ]

    return {"expenses": expenses_list}


@login_required
@api.get("/download-csv")
def csv_download(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    expenses = ParticipantExpense.objects.filter(profile=profile)
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="My_expenses.csv"'
    writer = csv.writer(response)
    writer.writerow(["service_name", "amount_owed", "date_timestamp"])
    for expense in expenses:
        writer.writerow([
            expense.expense.item_service,
            expense.amount_owed,
            expense.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response
@login_required
@api.get("/overall-expenses")
def get_all_expenses(request):
    expenses=Expense.objects.all()
    overall_expenses_list = []

    for expense in expenses:
        participants = expense.participants.all()
        overall_expenses_list.append({
            "service_name": expense.item_service,
            "total_cost": expense.cost,
            "date": expense.created_at,
            "participants": [participant.user.username for participant in participants]
        })
        return {"overall_expenses": overall_expenses_list}

@login_required
@api.get("/download_overall_csv")
def download_overall_expenses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="overall_expenses.csv"'
    writer = csv.writer(response)

    writer.writerow(['Service Name', 'Total Cost', 'Date', 'Participants'])

    expenses = Expense.objects.all()

    for expense in expenses:
        participants = expense.participants.all()
        participant_names = ', '.join([participant.user.username for participant in participants])

        writer.writerow([
            expense.item_service,
            expense.cost,
            expense.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            participant_names
        ])

    return response
#<-----------------------------------------Helper functions---------------------------------------------------------------->
def equalSplit(expense,participants):
    contributions=equalsplit(expense.cost,len(participants))
    i=0

    for participant in participants:
        participant_user = get_object_or_404(User, username=participant)
        profile=get_object_or_404(Profile, user=participant_user)
        expense.participants.add(profile)
        part_expense=ParticipantExpense.objects.create(expense=expense,profile=profile,amount_owed=contributions[i])
        i+=1

def exactSplit(expense,participants):
    if(validAmount(expense.cost,[value for key,value in participants.items()])):
        for participant,contribution in participants.items():
            participant_user = get_object_or_404(User, username=participant)
            profile = get_object_or_404(Profile, user=participant_user)
            expense.participants.add(profile)
            part_expense = ParticipantExpense.objects.create(expense=expense, profile=profile,amount_owed=contribution)
        return True
    return False

def percentSplit(expense,participants):
    if validPercentages([value for key,value in participants.items()]):
        amount=expense.cost
        for participant,contribution in participants.items():
            participant_user = get_object_or_404(User, username=participant)
            profile = get_object_or_404(Profile, user=participant_user)
            expense.participants.add(profile)
            part_expense = ParticipantExpense.objects.create(expense=expense, profile=profile,amount_owed=round(contribution*0.01*amount,3))
        return True
    return False


# Create your views here.
