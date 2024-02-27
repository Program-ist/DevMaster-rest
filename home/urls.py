from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name="home"),
	path('loginview/',views.LoginView, name = "loginview"),
    path('signup/', views.SignupView, name = "signup"),
    path('logoutUser/', views.logoutUser, name = "logoutUser"),
    path('dashboard/', views.dashboard, name = "dashboard"),
    path('editProfile',views.editProfile, name = "editProfile"),

    path('ap', views.ap, name = "ap"),
	path('api/', views.apiOverview, name="api-overview"),
    path('testbase/',views.testbase, name = 'testbase'),
    path('logout/', LogoutView.as_view(next_page= settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('llm', views.llm, name = "llm"),
    path('llm_ans',views.llm_ans, name="llm_ans"),
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
    path('task-create/', views.taskCreate, name="task-create"),    




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
