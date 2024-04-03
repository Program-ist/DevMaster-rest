def review(request,pk):
	# fuser = request.user
	# usern = fuser.username
	# fuser = UserDetail.objects.get(user_name=usern)

	# proj = ProjectDetail.objects.get(id = pk)

	# if not ProjectMembers.objects.filter(project=proj,user=fuser).exists():
	# 	messages.error(request, "Forbidden project")
	# 	return redirect('/dashboard/')
	
	# spreview = SprintReviewer.objects.filter(bug_to=fuser,project=proj)
	# bgdataman = BugData.objects.filter(bug_from=fuser,project=proj)

	# spda = SprintData.objects.filter(sprint_reviewer=fuser,project=proj)
	# sprevir = SprintReviewer.objecs.filter(sprint= spda)


	isMana = 0
	# sta = fuser.status_of_account
	# if sta == "MANAGER":
	# 	isMana = 1

	di ={
		'isMana':isMana,
		


	}
	# 'spda':spda,
	# 	'sprevir':sprevir
	return render(request, "home/review.html",di)