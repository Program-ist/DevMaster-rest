from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .geminillmapi import gemini_result
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.db.models import Avg, Max, Min, Sum
from datetime import datetime
from django.conf.urls.static import static
import re
import ciso8601
import time



'''   Home Page  '''
def home(request):
	usern = "notLoggedIn"
	if request.user.is_authenticated:
		user= request.user
		usern = user.username
	diction = {'usern':usern}
	# messages.error(request,"Wrong Credentials")
	return render(request, 'home/index.html',diction)



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

'''		ADMIN 	'''
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
		

'''		Project Members		'''
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
		'username':usern,
		'proj':proj
		
	}

	sta = fuser.status_of_account
	if sta == "MANAGER":
		return render(request,"home/man_projects.html",di)
	if sta == "DEVELOPER":
		return render(request,"home/dev_projects.html",di)

	
	return render(request,"home/dev_projects.html",di)


'''		Chat Page	'''
@login_required
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
	try:
		arg1 = int(arg1)
	except:
		arg1 = 0
	sta = fuser.status_of_account
	

	di = {
		'iden':pk,
		'cha':cha,
		'username':fuser.user_name,
		'userid':fuser.id,
		'highest_time':arg1,
		'na':proj.project_name
		
	}
	return render(request, "home/chat.html" ,di)


'''		LLM Page	'''
@login_required
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
	try:
		proj_func = ProjectFunctionalities.objects.get(project=proj)
	except:
		proj_func = None



	sprint = SprintData.objects.filter(project=proj)
	


	di = {
		'iden':pk,
		'ldata':ldata,
		'username':fuser.user_name,
		'na':na,
		'proj':proj,
		'proj_func':proj_func,
		'sprint':sprint,
		

		

	}

	return render(request, "home/llm.html",di)


'''		Sprint Page	'''
@login_required
def sprint(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name=usern)

	proj = ProjectDetail.objects.get(id = pk)

	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')
	
	spdatadev = SprintData.objects.filter(sprint_to=fuser,project=proj)
	all_project_sprint = SprintData.objects.filter(project=proj).order_by('-sp_created_time')
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


'''		Bug Page	'''
@login_required
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


'''		Review Page	'''
@login_required
def review(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name=usern)

	proj = ProjectDetail.objects.get(id = pk)

	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')
	

	# spreview = SprintReviewer.filter()
	bgdatadev = BugData.objects.filter(bug_to=fuser,project=proj)
	bgdataman = BugData.objects.filter(bug_from=fuser,project=proj)


	all_project_bug = BugData.objects.filter(project=proj)
	bug_set_of_members = set()
	for i in all_project_bug:
		bug_set_of_members.add(i.bug_reviewer)
	

	all_project_sprint = SprintData.objects.filter(project=proj)
	sprint_set_of_members = set()
	for i in all_project_sprint:
		sprint_set_of_members.add(i.sprint_reviewer)


	bugrev = BugReviewer.objects.all()
	sprrev = SprintReviewer.objects.all()

	di = {
		'iden':pk,
		'all_project_bug':all_project_bug,
		'all_project_sprint': all_project_sprint,
		'bug_set_of_members': bug_set_of_members,
		'sprint_set_of_members': sprint_set_of_members,
		'username':fuser,
		'bugrev':bugrev,
		'sprrev':sprrev

	}
	sta = fuser.status_of_account
	if sta == "MANAGER":
		return render(request,"home/man_review.html",di)
	
	return render(request,"home/dev_review.html",di)


'''		Project Details Page	'''
@login_required
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
		'username': fuser,
		'isMana': isMana

	}
	return render(request,"home/details.html",di)

'''		Make Announcement Page	'''
@login_required
def makeAnnouncement(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name = usern)

	proj = ProjectDetail.objects.get(id = pk)

	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')
	di = {
		'iden':pk
	}
	if request.method == 'POST':

		fann_from = UserDetail.objects.get(user_name = username)
		fproject = proj
		fannouncement_msg = request.POST['fannouncement_msg']
		ftime_of_message = int(datetime.now().timestamp())

		temp = Announcement(ann_from = fann_from, project=fproject, announcement_msg=fannouncement_msg, time_of_message=ftime_of_message)
		temp.save()
		messages.success(request, "Announcement Made Successfully")
		
		# temp = ProjectDetail.objects.filter(project_name = fproject_name).all()
		# for i in temp:
		# 	ctemp_id = str(i.id)
			
		# url_val = "/projects/" + ctemp_id
		url_val = "/projects/" + proj.id
		
		
		return redirect(url_val,ctemp_id)
	return render(request,"home/makeAnnouncement.html",di)

def madeAnn(request):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name = usern)

	if request.method == 'POST':
		fann_from = UserDetail.objects.get(user_name = usern)
		fproject = request.POST['fproject_id']
		fannouncement_msg = request.POST['fannouncement_msg']
		ftime_of_message = int(datetime.now().timestamp())
		proj = ProjectDetail.objects.get(id = fproject)
		temp = Announcement(ann_from = fann_from, project=proj, announcement_msg=fannouncement_msg, time_of_message=ftime_of_message)
		temp.save()
		messages.success(request, "Announcement Made Successfully")
		
		# temp = ProjectDetail.objects.filter(project_name = fproject_name).all()
		# for i in temp:
		ctemp_id = str(proj.id)
			
		# url_val = "/projects/" + ctemp_id
		url_val = "/projects/" + str(proj.id)
		
		
		return redirect(url_val,ctemp_id)
	return redirect("/dashboard/")

'''		Assign Sprint Page	'''
@login_required
def assignSprint(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name = usern)

	proj = ProjectDetail.objects.get(id = pk)
	projMembers = ProjectMembers.objects.filter(project=proj)
	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')
	di = {
		'iden':pk,
		'projMembers':projMembers
	}

	return render(request,"home/assignSprint.html",di)


''' str to timestamp
import ciso8601
t = "2024-04-26 13:07"
ts = ciso8601.parse_datetime(t)
# to get time in seconds:
print(time.mktime(ts.timetuple()))
'''


def assignedSprint(request):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name = usern)

	if request.method == "POST":
		fsprint_from = fuser
		fsprint_to = request.POST['fsprint_to']
		fsprint_reviewer = request.POST['fsprint_reviewer']
		fproject_id = request.POST['fproject_id']
		fsprint_title = request.POST['fsprint_title']
		fsprint_detail = request.POST['fsprint_detail']
		fsp_created_time = int(datetime.now().timestamp())
		fdeadline_time = request.POST['fdeadline_time']
		fdeadline_time = fdeadline_time.replace("T"," ")
		t = fdeadline_time
		ts = ciso8601.parse_datetime(t)
		fdeadline_time = time.mktime(ts.timetuple())
		fdeadline_time = str(fdeadline_time)
		fdeadline_time = float(fdeadline_time)
		fdeadline_time = int(fdeadline_time)
		fdeadline_time = str(fdeadline_time)
		# fsubmitted_time = request.POST['fsubmitted_time']
		

		proj = ProjectDetail.objects.get(id = fproject_id)
		spto = UserDetail.objects.get(id = fsprint_to)
		spreviewer = UserDetail.objects.get(id = fsprint_reviewer)

		temp = SprintData(sprint_from = fsprint_from, sprint_to = spto, sprint_reviewer = spreviewer, project_id = fproject_id, sprint_title = fsprint_title, sprint_detail = fsprint_detail, sp_created_time = fsp_created_time, deadline_time = fdeadline_time)
		temp.save()
		ctemp_id = str(proj.id)
			
		# url_val = "/projects/" + ctemp_id
		url_val = "/projects/" + str(proj.id) + "/sprint/"
		
		
		return redirect(url_val,ctemp_id)
	
	return redirect("/dashboard/")


'''		Assign Bug Page	'''
@login_required
def assignBug(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name = usern)

	proj = ProjectDetail.objects.get(id = pk)
	projMembers = ProjectMembers.objects.filter(project=proj)
	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')
	di = {
		'iden':pk,
		'projMembers': projMembers
	}

	return render(request,"home/assignBug.html",di)

def assignedBug(request):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name = usern)

	if request.method == "POST":
		fbug_from = fuser
		fbug_to = request.POST['fbug_to']
		fbug_reviewer = request.POST['fbug_reviewer']
		fproject_id = request.POST['fproject_id']
		fbug_title = request.POST['fbug_title']
		fbug_detail = request.POST['fbug_detail']
		fbu_created_time = int(datetime.now().timestamp())
		fdeadline_time = request.POST['fdeadline_time']

		try:
			fbugreported_by = request.POST['fbugreported_by']
		except:
			fbugreported_by = ReportBug.objects.get(id = 1)
		# fsubmitted_time = request.POST['fsubmitted_time']

		proj = ProjectDetail.objects.get(id = fproject_id)
		bgto = UserDetail.objects.get(user_name = fbug_to)
		bgreviewer = UserDetail.objects.get(user_name = fbug_reviewer)

		temp =BugData(bug_from = fbug_from, bug_to = bgto, bug_reviewer = bgreviewer,bug_reported_by = fbugreported_by ,bug_title = fbug_title, bug_detail = fbug_detail, bu_created_time = fbu_created_time, deadline_time = fdeadline_time,project = proj)
		temp.save()
		ctemp_id = str(proj.id)
			
		# url_val = "/projects/" + ctemp_id
		url_val = "/projects/" + str(proj.id) +'/bug/'
		
		
		return redirect(url_val,ctemp_id)
	
	return redirect("/dashboard/")


'''		Assign Bug Page	'''
@login_required
def reportBug(request,pk):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name = usern)

	proj = ProjectDetail.objects.get(id = pk)

	if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
		messages.error(request, "Forbidden project")
		return redirect('/dashboard/')
	di = {
		'iden':pk
	}

	return render(request,"home/reportBug.html",di)

def reportedBug(request):
	fuser = request.user
	usern = fuser.username
	fuser = UserDetail.objects.get(user_name = usern)

	if request.method == "POST":
		fbug_from = fuser
		fbug_to = request.POST['fbug_to']
		fbug_reviewer = request.POST['fbug_reviewer']
		fproject_id = request.POST['fproject_id']
		fbug_title = request.POST['fbug_title']
		fbug_detail = request.POST['fbug_detail']
		fbu_created_time = int(datetime.now().timestamp())
		fdeadline_time = request.POST['fdeadline_time']

		try:
			fbugreported_by = request.POST['fbugreported_by']
		except:
			fbugreported_by = ReportBug.objects.get(id = 1)
		# fsubmitted_time = request.POST['fsubmitted_time']

		proj = ProjectDetail.objects.get(id = fproject_id)
		bgto = UserDetail.objects.get(user_name = fbug_to)
		bgreviewer = UserDetail.objects.get(user_name = fbug_reviewer)

		temp =BugData(bug_from = fbug_from, bug_to = bgto, bug_reviewer = bgreviewer,bug_reported_by = fbugreported_by ,bug_title = fbug_title, bug_detail = fbug_detail, bu_created_time = fbu_created_time, deadline_time = fdeadline_time,project = proj)
		temp.save()
		ctemp_id = str(proj.id)
			
		# url_val = "/projects/" + ctemp_id
		url_val = "/projects/" + str(proj.id) +'/bug/'
		
		
		return redirect(url_val,ctemp_id)
	
	return redirect("/dashboard/")


'''		LLM API		'''

@api_view(['POST'])
def llm_api(request):

	us = request.user
	fusern = us.username
	fuser = UserDetail.objects.get(user_name = fusern)
	


	d = request.data
	pk = d['pk']
	funcs = ""
	for i in d['project_func']:
		funcs = " "+funcs + i +","
	# questi = d['project_name'] +" which is "+ d['project_details'] +" with functionalities "+ funcs + " in "+d['project_phase'] + " phase. "+ d['quest']
	questi = d['project_name'] +" which is "+ d['project_details'] +" with functionalities "+ funcs +". "+ d['quest']
	ans = gemini_result(questi)
	a = ans
	a = a.replace("\n","<br>")
	test_str = a 
	test_sub = "**"
	res = [i for i in range(len(test_str)) if test_str.startswith(test_sub, i)]
	fla = 0
	for i in reversed(res):
		if fla % 2 == 0:
			test_str =  test_str[:i+1] + "" + test_str[i+2:]
			test_str = test_str[:i] + "</b>" + test_str[i+1:]
			fla += 1
		elif fla % 2 == 1:
			test_str = test_str[:i+1] + "" + test_str[i+2:]
			test_str = test_str[:i] + "<b>" + test_str[i+1:]
			fla += 1
	test_str = test_str.replace("*","")
	ans = test_str

	temp = LlmData(user=fuser ,question_asked=d['quest'],project_id=d['pk'],answer_from_api=ans,time_of_message=int(datetime.now().timestamp()))
	temp.save()

	an = {
		'ans':ans
	}
	print(ans)
	return Response(an)

	



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
	




'''		API for Sprint (Mark as Done)	'''
@api_view(['POST'])
def sprint_done(request):
	da = request.data
	a = SprintData.objects.get(id = da['clicked_id'])
	a.submitted_time = int(datetime.now().timestamp())
	a.save()
	done = {
		'done':'done'
	}
	return Response(done)

'''		API for Bug (Mark as Done)	'''
@api_view(['POST'])
def bug_done(request):
	da = request.data
	a = BugData.objects.get(id = da['clicked_id'])
	a.submitted_time = int(datetime.now().timestamp())
	a.save()
	done = {
		'done':'done'
	}
	return Response(done)