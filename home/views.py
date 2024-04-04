from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .geminillmapi import gemini_result
# Create your views here.

# @login_required

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.db.models import Avg, Max, Min, Sum

from datetime import datetime

from django.conf.urls.static import static

import re
'''   Home Page  '''
def home(request):
	usern = "notLoggedIn"
	if request.user.is_authenticated:
		user= request.user
		usern = user.username
	diction = {'usern':usern}
	# messages.error(request,"Wrong Credentials")
	return render(request, 'home/index.html',diction)




def testbase(request):
	return render(request,'home/testbase.html')



'''  Login Page   '''
def LoginView(request):
	if request.user.is_authenticated:
		return redirect('/dashboard/')
	if request.method == 'POST':
		user_name = request.POST['user_name']
		password = request.POST['password']
		user = authenticate(username= user_name, password= password)
		if user is not None:
			login(request, user)			
			return redirect('/dashboard/')
		else:
			messages.error(request,"Wrong Credentials")
			return render(request, 'home/login.html')
	
	return render(request, 'home/login.html')
		
	
'''		Code to Logout	'''
# # {% url 'logout' %}
# def LogoutView(request):
# 	logout(request)
# 	return redirect('login')

def logoutUser(request):
    logout(request)
    return redirect('/loginview/')



'''		Registration Page	'''
def SignupView(request):
	if request.user.is_authenticated:
		return redirect('/dashboard/')
	if request.method == 'POST':
		fname = request.POST['full_name']
		fuser_name = request.POST['user_name']
		femail = request.POST['email']
		fpassword = request.POST['password']
		fstatus_of_account = request.POST['status_of_account']
		fstatus_of_account = fstatus_of_account.upper()
		fstatus_of_account = fstatus_of_account.upper()
		fstat_vali = 0
		if fstatus_of_account == "DEVELOPER" or fstatus_of_account == "MANAGER" or fstatus_of_account == "ADMIN":
			fstat_vali = 1
		if fstat_vali == 0:
			messages.error(request, 'Unknown status level')
			return render(request, 'home/signup.html')
		email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
		email_vali = 0
		if re.fullmatch(email_regex, femail):
			email_vali = 1
		else: 
			email_vali = 0

		if email_vali == 0:
			messages.error(request, 'Wrong Email Address')
			return render(request, 'home/signup.html')

		# allusers = UserDetail.objects.values_list('user_name')

		if UserDetail.objects.filter(user_name = fuser_name).exists():
			messages.error(request,"User Name already in use")
			return render(request,'home/signup.html')

		member = UserDetail(name = fname, user_name = fuser_name, email = femail, password = fpassword, status_of_account = fstatus_of_account)
		member.save()
		myuser = User.objects.create_user(username=fuser_name, password=fpassword)
		# myuser.set_password(password)
		myuser.save()
		messages.success(request, 'Yay!! Successfully Registered')

		#login registered user
		user = authenticate(username= fuser_name, password= fpassword)
		if user is not None:
			login(request, user)


		return redirect('/dashboard/')
	
	return render(request, 'home/signup.html')

'''		Dashboard		'''
@login_required
def dashboard(request):
	currentUser = request.user #the user
	username = currentUser.username #their username
	Cuser = UserDetail.objects.get(user_name=username)
	stat = Cuser.status_of_account
	mem_projects = ProjectMembers.objects.filter(user=Cuser)
	
	
	tsurl = "home/dev_dashboard.html"
	if stat == "ADMIN":
		tsurl = "home/admin_dashboard.html"
		all_users = UserDetail.objects.all()
		val ={
			'username':username,
			'all_users':all_users
		}
		return render(request, tsurl,val)
		

	elif stat == "MANAGER":
		anno = Announcement.objects.all()
		val = {'username':username,
		'mem_projects':mem_projects,
		'anno':anno
		}
		tsurl = "home/man_dashboard.html"
		return render(request, tsurl,val)

	else:
		anno = Announcement.objects.all()
		val = {'username':username,
		'mem_projects':mem_projects,
		'anno':anno
		}
		tsurl = "home/dev_dashboard.html"
		return render(request, tsurl,val)
		#tsurl = "home/dev_dashboard.html"
		pass	
	
	# return render(request, tsurl, val)
	return render(request, "home/index.html")


def ad(request):
	return render(request, 'home/ad.html')

def adProject(request):
	return render(request,'home/adProject.html')





'''		EditProfile		'''
@login_required
def editProfile(request):
	if request.method == 'POST':
		fname = request.POST['full_name']
		fuser_name = request.POST['user_name']
		femail = request.POST['email']
		fpassword = request.POST['password']
		fstatus_of_account = request.POST['status_of_account']
		#check if username in use and then update
		user = request.user
		udun = user.username
		if UserDetail.objects.filter(user_name = fuser_name).exists():
			messages.error(request,"User Name already in use")
			return render(request,'home/editProfile.html',user)
		tempUD = UserDetail.objects.filter(user_name = udun).first()
		tempUD.name = fname
		tempUD.user_name = fuser_name
		tempUD.email = femail
		tempUD.password = fpassword
		tempUD.status_of_account = fstatus_of_account
		tempUD.save()
		tempU = User.objects.filter(username = udun).first()
		tempU.username = fuser_name
		tempU.set_password(fpassword)
		tempU.save()
		return redirect('/dashboard/')
	user = request.user
	user = UserDetail.objects.get(user_name=user.username)
	di = {'user': user}
	return render(request, 'home/editProfile.html',di)



'''		Create Project		'''
@login_required
def createProjectt(request):
	user = request.user
	username = user.username
	if not UserDetail.objects.filter(user_name = username,status_of_account = "MANAGER").exists():
		messages.error(request,"You are not authorized to create a Project")
		return render(request,"home/createProject.html")
	if request.method == 'POST':
		fproject_name = request.POST['fproject_name']
		fproject_description = request.POST['fproject_description']
		fcreated_by = UserDetail.objects.get(user_name = username)
		fproject_created_time = int(datetime.now().timestamp())
		fproject_gtihub_link = request.POST['fproject_gtihub_link']
		fproject_phase = request.POST['fproject_phase'] 
		if ProjectDetail.objects.filter(created_by = fcreated_by, project_name = fproject_name).exists():
			messages.error(request,"Project with name exists")
			return redirect(request, "home/createProject.html")
		temp = ProjectDetail(project_name = fproject_name,  project_description = fproject_description,  created_by = fcreated_by,  project_created_time = fproject_created_time,  project_gtihub_link = fproject_gtihub_link,  project_phase = fproject_phase )
		temp.save()
		messages.success(request, "Project Successfully Created")
		
		temp = ProjectDetail.objects.filter(project_name = fproject_name).all()
		for i in temp:
			ctemp_id = str(i.id)
			
		url_val = "/projects/" + ctemp_id
		
		# returl = f'home/project/{temp.id}/projectMembers.html'
		'''********** May break ************'''
		
		return redirect(url_val,ctemp_id)
	return render(request, "home/createProject.html")
		


def members(request,pk):
	pass

'''		Page for Individual Project	'''





@login_required
def projects(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name=usern)

	proj = ProjectDetail.objects.get(id = pk)

	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')

	anno = Announcement.objects.filter(project=proj)
	isMana = 0
	di = {
		'iden':pk,
		'anno': anno,
		'username':usern
		
	}

	sta = fuser.status_of_account
	if sta == "MANAGER":
		return render(request,"home/man_projects.html",di)
	if sta == "DEVELOPER":
		return render(request,"home/dev_projects.html",di)

	
	return render(request,"home/dev_projects.html",di)


def chat(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name=usern)

	proj = ProjectDetail.objects.get(id = pk)
	
	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')

	cha = ChatData.objects.filter(project=proj)
	arg1 = ChatData.objects.filter(project=proj).aggregate(Max('time_of_message'))
	arg1 = arg1['time_of_message__max']
	arg1 = int(arg1)
	sta = fuser.status_of_account
	

	di = {
		'iden':pk,
		'cha':cha,
		'username':usern,
		'highest_time':arg1
		
	}
	return render(request, "home/chat.html" ,di)


def llm(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name=usern)

	proj = ProjectDetail.objects.get(id = pk)

	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')

	ldata = LlmData.objects.filter(user=fuser,project=proj)
	na = proj.project_name
	di = {
		'iden':pk,
		'ldata':ldata,
		
		'na':na
		

	}

	return render(request, "home/llm.html",di)

def sprint(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name=usern)

	proj = ProjectDetail.objects.get(id = pk)

	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')
	
	spdatadev = SprintData.objects.filter(sprint_to=fuser,project=proj)
	all_project_sprint = SprintData.objects.filter(project=proj)
	set_of_members = set()
	for i in all_project_sprint:
		set_of_members.add(i.sprint_to)
	
	
	spdataman = SprintData.objects.filter(sprint_from=fuser,project=proj)
	isMana = 0
	di = {
		'iden':pk,
		'spdatadev':spdatadev,
		'all_project_sprint': all_project_sprint,
		'set_of_members':set_of_members,
		'username':fuser

	}
	sta = fuser.status_of_account
	if sta == "MANAGER":
		return render(request, "home/man_sprint.html",di)
	elif sta == "DEVELOPER":
		return render(request, "home/dev_sprint.html",di)
	
	return render(request, "home/dev_sprint.html", di)



def bug(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name=usern)

	proj = ProjectDetail.objects.get(id = pk)

	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')
	
	bgdatadev = BugData.objects.filter(bug_to=fuser,project=proj)
	
	all_project_bug = BugData.objects.filter(project=proj)
	set_of_members = set()
	for i in all_project_bug:
		set_of_members.add(i.bug_to)
	isMana = 0
	sta = fuser.status_of_account
	di = {
		'iden':pk,
		'bgdatadev':bgdatadev,
		'all_project_bug': all_project_bug,
		'set_of_members':set_of_members,
		'username':fuser

	}
	if sta == "MANAGER":
		return render(request,"home/man_bug.html",di)
	elif sta == "DEVELOPER":
		return render(request,"home/dev_bug.html",di)
	return render(request,"home/bug.html",di)


	
def review(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name=usern)

	proj = ProjectDetail.objects.get(id = pk)

	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')
	
	bgdatadev = BugData.objects.filter(bug_to=fuser,project=proj)
	bgdataman = BugData.objects.filter(bug_from=fuser,project=proj)
	isMana = 0
	sta = fuser.status_of_account
	if sta == "MANAGER":
		isMana = 1
	di = {
		'iden':pk,
		'bgdatadev':bgdatadev,
		'bgdataman': bgdataman,
		'isMana': isMana

	}
	return render(request,"home/review.html",di)

def details(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name=usern)

	proj = ProjectDetail.objects.get(id = pk)

	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')
	
	bgdatadev = BugData.objects.filter(bug_to=fuser,project=proj)
	bgdataman = BugData.objects.filter(bug_from=fuser,project=proj)
	isMana = 0
	sta = fuser.status_of_account
	if sta == "MANAGER":
		isMana = 1
	di = {
		'iden':pk,
		'bgdatadev':bgdatadev,
		'bgdataman': bgdataman,
		'isMana': isMana

	}
	return render(request,"home/details.html",di)


'''		LLM API		'''

@api_view(['POST'])
def llm_api(request):
	d = request.data

	funcs = ""
	for i in d['project_func']:
		funcs = funcs + i +","
	questi = d['project_name'] +" which is "+ d['project_details'] +" with functionalities "+ funcs + " in "+d['project_phase'] + " phase. "+ d['quest']
	ans = gemini_result(questi)
	an = {
		'ans':ans
	}
	return Response(an)
	'''
	test_str = "I **like** **bananas** bananas"

# initializing substring 
test_sub = "**"

# printing original string 
print("The original string is : " + test_str) 

# printing substring 
print("The substring to find : " + test_sub) 

# using list comprehension + startswith() 
# All occurrences of substring in string 
res = [i for i in range(len(test_str)) if test_str.startswith(test_sub, i)] 

# printing result 
print("The start indices of the substrings are : " + str(res)) 
fla = 2
for i in reversed(res):
    print(fla)
    if fla % 2 == 0:
        test_str = test_str[:i+1] + "" + test_str[i+2:]
        test_str = test_str[:i] + "</br>" + test_str[i+1:]
        fla += 1
        print(fla)
    elif fla % 2 == 1:
        test_str = test_str[:i+1] + "" + test_str[i+2:]
        test_str = test_str[:i] + "<br>" + test_str[i+1:]
        fla += 1
        print(fla)
    
print(test_str)

	'''





'''		Post Chat 	'''
@login_required
@api_view(['POST'])
def post_chat(request):
	d = request.data
	userd = request.user
	username = userd.username
	user = UserDetail.objects.get(user_name=username)
	pro = ProjectDetail.objects.get(id=d['proid'])
	temp = ChatData(msg_from=user,project=pro,msg = d['chat_m'],time_of_message=int(datetime.now().timestamp()))
	temp.save()
	an = {
		'ans':"donnnnnn"
	}
	return Response(an)




@login_required
def ap(request):
	if request.user.isanonymous:
		return redirect("/home")
	else:
		return HttpResponse("appppp")



'''		Page for Api Overview		'''
@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'Chat':'/chat_check/',
		'Announcement':'/announcement_check/',
		'Sprint':'/sprint_check/',
		'Bug':'/bug_check/',
		'Dashboard':'dash_check',
		'LLM':'llm_ans',
		}
		

	return Response(api_urls)


'''		api		'''
@api_view(['POST'])

def taskCreate(request):
	# serializer = UserDetailSerializer(data=request.data)

	# if serializer.is_valid():
	# 	serializer.save()
	d = request.data
	print(d)
	dit = {
		"w":"x",
		"y":"z"
	}
	return Response(dit)








'''		API to see update in dashboard'''
'''		

Income:
announcement_unix
sprint_unix
chat_unix

Return:
announcement_bit
sprint_bit
chat_bit



'''

@api_view(['POST'])
def dash_check(request):
	income_data = eval(request.data)
	arg1 = Announcement.objects.aggregate(Max('time_of_message'))
	# arg2 = SprintData.objects.aggregate(Max('time_of_message'))
	arg3 = ChatData.objects.aggregate(Max('time_of_message'))

	
	send_data = {
		'announcement_bit':0,
		# 'sprint_bit': 0,
		'chat_bit': 0
	}
	

	if arg1>income_data['announcement_unix']:
		send_data['announcement_bit'] = 1
	# if arg2>income_data['sprint_unix']:
	# 	send_data['sprint_bit'] = 1
	if arg3>income_data['chat_unix']:
		send_data['chat_bit'] = 1

	return Response(json.dumps(send_data))


'''

Income
chat_unix

Return
chat_bit
new_chat_unix
data

'''
@api_view(['POST'])
def chat_check(request):
	d = request.data
	proo = d['proid']
	proo = ProjectDetail.objects.get(id = proo)
	arg1 = ChatData.objects.filter(project=proo).aggregate(Max('time_of_message'))
	send_data = {
		'chat_bit':0,
		'new_chat_unix':"",
		'chat_data':{}
	}

	old_unix = d['highest']
	old_unix = int(old_unix)
	
	arg = arg1['time_of_message__max']
	arg = int(arg)
	if arg>old_unix:
		send_data['chat_bit'] = 1
		send_data['new_chat_unix'] = arg
		que = ChatData.objects.filter(time_of_message__gt = old_unix, time_of_message__lt = arg1 )
		serializer = ChatDataSerializer(que,many = True)
		send_data['chat_data'] = serializer
	else:
		pass
	return Response(json.dumps(send_data))



'''
Income:
announcement_unix

Return:
announcement_bit
new_announcement_unix
announcement_data

'''


@api_view(['POST'])
def announcement_check(request):
	income_data = eval(request.data)
	arg1 = Announcement.objects.aggregate(Max('time_of_message'))
	send_data = {
		'announcement_bit':0,
		'new_announcement_unix':"",
		'announcement_data':{}
	}

	old_unix = income_data['announcement_unix']
	if arg1>income_data['announcement_unix']:
		send_data['announcement_bit'] = 1
		send_data['new_announcement_unix'] = arg1
		que = Announcement.objects.filter(time_of_message__gt = old_unix, time_of_message__lt = arg1 )
		serializer = AnnouncementSerializer(que,many = True)
		send_data['announcement_data'] = serializer

	return Response(json.dumps(send_data))






@api_view(['POST'])
def llm_ans(request):

	#income_data = request.data 
	#ans = gemini_result(income_data)
	ans = {'a':'b',
		'b':'c'}
	user = reques.user
	usernam = user.username
	user = UserDetail.objects.get(user_name = usernam)
	
	da = request.data
	self.project = ProjectDetail.objects.get(id = da['pro_id'])
	self.functionalities = ProjectFunctionalities.object.filter(project = self.project)
	self.questionString = ""
	# append
	question = da['ques']
	answer = gemini_result(question)
	return Response(answer)
	

