from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('ap', views.ap, name = "ap"),
	path('api/', views.apiOverview, name="api-overview"),
	path('login/',views.LoginView, name = "login"),
    path('register/', views.RegisterView, name = "register"),
    path('testbase/',views.testbase, name = 'testbase'),
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
