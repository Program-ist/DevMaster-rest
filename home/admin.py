from django.contrib import admin

# Register your models here.

from .models import *



admin.site.register(UserDetail)
admin.site.register(ProjectDetail)
admin.site.register(ProjectFunctionalities)
admin.site.register(ProjectMembers)
admin.site.register(ChatData)
admin.site.register(LlmData)
admin.site.register(Announcement)
admin.site.register(SprintData)
admin.site.register(ReportBug)
admin.site.register(BugData)
admin.site.register(SprintReviewer)
admin.site.register(BugReviewer)
