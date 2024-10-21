from django.db import models
from accounts.models import Profile
from django.utils import timezone
class Expense(models.Model):
    service = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=3)
    creator = models.ForeignKey(Profile, related_name='created_expenses', on_delete=models.CASCADE)
    participants = models.ManyToManyField(Profile, related_name='shared_expenses',blank=True)
    split_method = models.CharField(max_length=20,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ParticipantExpense(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)



# Create your models here.
