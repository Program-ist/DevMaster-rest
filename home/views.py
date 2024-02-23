from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserDetailSerializer

# Create your views here.
# from django.contrib.auth.decorators import login_required

# @login_required

from django.contrib.auth.models import User



def home(request):
    return render(request, 'home/index.html')



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
def taskCreate(request):
	serializer = UserDetailSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)