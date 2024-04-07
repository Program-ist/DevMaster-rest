from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name="home"),
    path('task-create/', views.taskCreate, name="task-create"),  
    path('ad/',views.ad, name = "ad"),
    path('adProject/',views.adProject, name = "adProject"),
	path('loginview/',views.LoginView, name = "loginview"),
    path('signup/', views.SignupView, name = "signup"),
    path('logoutUser/', views.logoutUser, name = "logoutUser"),
    path('dashboard/', views.dashboard, name = "dashboard"),
    path('editProfile/',views.editProfile, name = "editProfile"),
    path('createProjectt/',views.createProjectt, name = "createProjectt"),
    path('projects/<int:pk>/',views.projects, name = "projects"),
    path('projects/<int:pk>/chat/',views.chat, name = "chat"),
    path('projects/<int:pk>/llm/',views.llm, name = "llm"),
    path('projects/<int:pk>/makeAnnouncement/',views.makeAnnouncement, name = "makeAnnouncement"),
    path('madeAnn/',views.madeAnn, name = "madeAnn"),
    path('projects/<int:pk>/assignSprint/',views.assignSprint, name = "assignSprint"),
    path('assignedSprint/',views.assignedSprint, name = "assignedSprint"),
    path('projects/<int:pk>/assignBug/',views.assignBug, name = "assignBug"),
    path('assignedBug/',views.assignedBug, name = "assignedBug"),
    path('projects/<int:pk>/sprint/',views.sprint, name = "sprint"),
    path('projects/<int:pk>/bug/',views.bug, name = "bug"),
    path('projects/<int:pk>/review/',views.review, name = "review"),
    path('projects/<int:pk>/details/',views.details, name = "details"),
    path('projects/<int:pk>/members/',views.members, name = "members"),
    path('post_chat/',views.post_chat, name="post_chat"),
    path('chat_check/',views.chat_check, name="chat_check"),
    path('llm_api/',views.llm_api, name="llm_api"),
    path('llm_ans/',views.llm_ans, name="llm_ans"),

    path('ap', views.ap, name = "ap"),
	path('api/', views.apiOverview, name="api-overview"),
    path('testbase/',views.testbase, name = 'testbase'),
    path('logout/', LogoutView.as_view(next_page= settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('llm', views.llm, name = "llm"),
    # path('logout',views.logout, name = 'logout'),
    # path('registrationview/',views.RegistrationView, name = 'registrationview'),
	# path('project/<str:pk>', views.project, name="project"),
    # path('dashboard/',views.dashboard, name = "dashboard"),
    # path('sprint-data/',views.sprintData, name = "sprint-data"),
    # path('bug-data/',views.bugData ,name = "bug-data"),
    # path('chat-message/',views.chatMessage, name = "chat-message"),
    # path('review',views.review,name = "review"),
    # path('llm/',views.llm,name = "llm"),
    # path('announcements/',views.announcements, name = "announcements"),
    # path('llm-api/', views.llmApi, name = "llm-api"),
    # path('sprint-data-api/',views.sprintDataApi, name = "sprint-data-api"),
    # path('bug-data-api/',views.bugDataApi ,name = "bug-data-api"),
    # path('chat-message-api/',views.chatMessageApi, name = "chat-message-api"),
    # path('announcement-api/',views.announcements, name = "announcement-api"),
      




	# path('task-list/', views.taskList, name="task-list"),
	# path('task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
	# path('task-create/', views.taskCreate, name="task-create"),

	# path('task-update/<str:pk>/', views.taskUpdate, name="task-update"),
	# path('task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
]

'''
##login
##register

(simple)
project details
llm-api


(setInterval)
sprint_data
bug_data
chat message
announcement

'''
