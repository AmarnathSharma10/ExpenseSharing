from ninja import NinjaAPI
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login as django_login
from .models import Profile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from pydantic import BaseModel
from django.http import JsonResponse
from ninja.responses import Response
from django.shortcuts import get_object_or_404
from ninja import Query

api = NinjaAPI()


class SignupSchema(BaseModel):
    username: str
    password: str
    name: str = None
    phone: str = None
    email: str = None
class LoginSchema(BaseModel):
    username: str
    password: str
@api.post("/signup")
def signup(request, data: SignupSchema):
    try:
        user = User.objects.create_user(username=data.username, password=data.password)
        Profile.objects.create(
            user=user,
            name=data.name,
            phone=data.phone,
            email=data.email
        )
        return {"message": "User and profile created successfully"}
    except Exception as e:
        print("Eroror")
        return JsonResponse({'error': str(e)}, status=400)

@api.post("/login")
def login(request, data:LoginSchema):
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None:
        django_login(request, user)
        return {"message": "Congratulations Logged in successfully"}
    return JsonResponse({"error": "Invalid credentials OOPS"}, status=401)
@api.post("/logout")
def logout_view(request):
    print("Hello")
    logout(request)
    messages.success(request, 'You have been logged out.')
    print("Logged out no issues")
    return {"message":"Logged out no issues"}
@api.get("/profile")
def get_profile(request):
    user=request.user

    profile=get_object_or_404(Profile,user=user)

    if profile:
        return Response({
            "username":user.username,
            "name":profile.name,
            "email":profile.email,
            "phone":profile.phone
        })
    return Response({"error":"profile not found are u even loggedin?"},status=404)
@api.get("/profiles")
def search_profiles(request, username: str):
    profiles = Profile.objects.filter(user__username__icontains=username)

    if not profiles:
        return {"error": "No profiles found for the given username."}, 404

    # Return a list of profiles
    return [{"username": profile.user.username, "name": profile.user.get_full_name(), "phone": profile.phone} for profile in profiles]