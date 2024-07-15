from django.shortcuts import render

# Create your views here.
def circle (request):
    return render(request, 'circlemaker/circle.html')

def line (request):
    return render(request, 'circlemaker/line.html')

def home (request):
    user = request.user
    return render(request, 'circlemaker/index.html',{'user':user})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            if not username or not password:
                raise ValueError("Both fields are required.")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')  # Redirect to a home page or any other page after login
            else:
                raise ValueError("Invalid username or password.")
        
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "An unexpected error occurred: " + str(e))
    
    return render(request, 'circlemaker/login.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import logout
from .models import UserProfile

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        refral = request.POST['referal']
        
        try:
            if not username or not password or not email:
                raise ValueError("All fields are required.")
            
            if User.objects.filter(username=username).exists():
                raise ValueError("Username already exists.")
            
            if User.objects.filter(email=email).exists():
                raise ValueError("Email already in use.")
            point=0
            # 15f7f32a
            if refral and UserProfile.objects.filter(referral_link=refral).exists():
                point+=25
                user=UserProfile.objects.get(referral_link=refral)
                user.refralcoin+=25
                user.save()
            
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            UserProfile.objects.create(user=user , refralcoin=point)
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('home')  # Redirect to a home page or any other page after signup
        
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "An unexpected error occurred: " + str(e))
        
    return render(request, 'circlemaker/index.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def profile(request):
    userprof = UserProfile.objects.get(user=request.user)
    return render(request, 'circlemaker/profile.html', {'userprofile': userprof})
import json

def addcoin(request):
    user=request.user
    if not user.is_authenticated:
        return redirect('circle')
    user_profile = UserProfile.objects.get(user=request.user)  # Get the UserProfile instance
    data = json.loads(request.body)
    points = data.get('coins', 0)
    points=float(points)
    point=0
    if(points>=80 and points<90):
        point += 5
    elif(points>=90 and points<=95):
        point += 8
    elif(points>95):
        point += 10
    user_profile.coin += point  # Increment the coin value
    user_profile.save()  # Save the UserProfile instance
    
    return redirect('profile')
from django.shortcuts import render
from .models import UserProfile
from django.shortcuts import render
from .models import UserProfile
from django.shortcuts import render
from .models import UserProfile
from django.shortcuts import render
from .models import UserProfile, prize

def leaderboard(request):
    # Get all user profiles ordered by coins in descending order
    profiles = UserProfile.objects.all().order_by('-coin', 'user__username')

    # Initialize variables for ranking
    rank = 0
    previous_coins = None
    previous_rank = 0

    for profile in profiles:
        if previous_coins is None or profile.coin < previous_coins:
            rank += 1  # Increment rank only when coins change
            previous_rank = rank  # Update previous rank
        else:
            # Assign the same rank for the same coin count
            profile.rank = previous_rank

        profile.rank = previous_rank  # Assign the current rank
        previous_coins = profile.coin  # Update previous coins for next comparison
    prizes=prize.objects.all().order_by('-id')
    today_prize=''
    for i in prizes:
        today_prize=i.prize
        break
    print(today_prize)
    return render(request, 'circlemaker/leaderboard.html', {'profiles': profiles , 'prize':today_prize})

from .models import WinnerList
from django.shortcuts import redirect
from .models import WinnerList, UserProfile
from django.shortcuts import redirect
from .models import WinnerList, UserProfile
from django.shortcuts import redirect

def resetcounts(request):
    # Find the user with the highest coins
    highest_profile = UserProfile.objects.order_by('-coin').first()
    
    # Check if there is a profile with the highest coins
    if highest_profile:
        # Get the current prize (assuming only one exists)
        prize_instance = prize.objects.first()
        
        if prize_instance:
            # Add the winner with the existing prize
            WinnerList.objects.create(user=highest_profile.user, prizewon=prize_instance)
            # Delete the prize after awarding it
            prize_instance.delete()
    
    # Reset all user coin counts
    profiles = UserProfile.objects.all()
    for profile in profiles:
        profile.coin = 0
        profile.save()
    
    # Optionally, create a new prize for the next day
    # Example: Prize.objects.create(prize="New Prize Name")
    
    return redirect('leaderboard')
