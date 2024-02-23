from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserDetailSerializer

# Create your views here.

# @login_required

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *


def home(request):
    return render(request, 'home/test.html')


def LoginView(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == 'POST':
		user_name = request.POST['user_name']
		password = request.POST['password']
		user = authenticate(username= user_name, password= password)
		if user is not None:
			login(request, user)
			# convert home to dashboard
			return redirect(request,'home')
		else:
			messages.error(request,"Wrong Credentials")
	
	return render(request, 'home/login.html')
		
	


def RegisterView(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == 'POST':

		name = request.POST['name']
		user_name = request.POST['user_name']
		email = request.POST['email']
		password = request.POST['password']
		status_of_account = request.POST['status_of_account']

		#checksssss

		member = UserDetail(name = name, user_name = user_name, email = email, password = password, status_of_account = status_of_account)
		member.save()
		myuser = User.objects.create_user(username=user_name, password=password)
		# myuser.set_password(password)
		myuser.save()
		messages.success(request, 'suc ses')
		return redirect('home')
	


# {% url 'logout' %}
def LogoutView(request):
	logout(request)
	return redirect('login')



def project(request, pk):
    return render(request, 'home/index.html')


@login_required
def ap(request):
	if request.user.isanonymous:
		return redirect("/home")
	else:
		return HttpResponse("appppp")




@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/task-list/',
		'Detail View':'/task-detail/<str:pk>/',
		'Create':'/task-create/',
		'Update':'/task-update/<str:pk>/',
		'Delete':'/task-delete/<str:pk>/',
		}

	return Response(api_urls)



@api_view(['POST'])
@login_required
def taskCreate(request):
	# serializer = UserDetailSerializer(data=request.data)

	# if serializer.is_valid():
	# 	serializer.save()

	print(request.data)
	return Response("done")