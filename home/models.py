from django.db import models

# Create your models here.

class UserDetail(models.Model):
    name = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)    
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    status_of_account = models.CharField(max_length=200)



    def __str__(self):
        return self.user_name
    


class ProjectDetail(models.Model):
    # project_u_n = models.CharField(max_length = 200)
    project_name = models.CharField(max_length = 200)
    project_description = models.TextField()
    created_by = models.ForeignKey(UserDetail,null=True, on_delete = models.SET_NULL)
    project_created_time = models.CharField(max_length = 20)
    project_gtihub_link = models.TextField()
    project_phase = models.CharField(max_length = 20)

    def __str__(self):
        return self.project_name



class ProjectFunctionalities(models.Model):
    project = models.ForeignKey(ProjectDetail, on_delete = models.CASCADE)
    project_funcionalities = models.CharField(max_length = 200)




class ProjectMembers(models.Model):
    user = models.ForeignKey(UserDetail, on_delete = models.CASCADE)
    project = models.ForeignKey(ProjectDetail, on_delete = models.CASCADE)
    



class ChatData(models.Model):
    msg_from = models.ForeignKey(UserDetail, on_delete = models.CASCADE)
    project = models.ForeignKey(ProjectDetail, on_delete = models.CASCADE)
    msg = models.TextField()
    time_of_message = models.CharField(max_length = 20)

class LlmData(models.Model):
    user = models.ForeignKey(UserDetail, on_delete = models.CASCADE)
    project = models.ForeignKey(ProjectDetail, on_delete = models.CASCADE)
    question_asked = models.TextField()
    answer_from_api = models.TextField()
    time_of_message = models.CharField(max_length = 20)



class Announcement(models.Model):
    ann_from = models.ForeignKey(UserDetail, on_delete = models.CASCADE, related_name='ann_from_user')
    ann_to = models.ForeignKey(UserDetail, on_delete = models.CASCADE, related_name = 'ann_to_user')
    project = models.ForeignKey(ProjectDetail, on_delete = models.CASCADE)
    announcement_msg = models.CharField(max_length = 200)
    time_of_message = models.CharField(max_length = 20)

class SprintData(models.Model):
    sprint_from = models.ForeignKey(UserDetail, on_delete = models.CASCADE, related_name = "sprint_from_user")
    sprint_to = models.ForeignKey(UserDetail, on_delete = models.CASCADE, related_name = "sprint_to_user")
    sprint_reviewer = models.ForeignKey(UserDetail, null=True, on_delete = models.SET_NULL, related_name = "sprint_reviewer_user")
    project = models.ForeignKey(ProjectDetail, on_delete = models.CASCADE)
    sprint_title = models.CharField(max_length = 200)
    sprint_detail = models.TextField()
    deadline_time = models.CharField(max_length = 20)
    submitted_time = models.CharField(max_length = 20)


class ReportBug(models.Model):
    bug_by = models.ForeignKey(UserDetail, null=True, on_delete = models.SET_NULL)
    project = models.ForeignKey(ProjectDetail, on_delete = models.CASCADE)
    bug_by_detail = models.TextField()


class BugData(models.Model):
    bug_from = models.ForeignKey(UserDetail, on_delete = models.CASCADE, related_name = "bug_from_user")
    bug_to = models.ForeignKey(UserDetail, on_delete = models.CASCADE, related_name = "bug_to_user")
    bug_reviewer = models.ForeignKey(UserDetail,null=True, on_delete = models.SET_NULL, related_name = "bug_reviewer_user")
    bug_reported_by = models.ForeignKey(ReportBug,null=True, on_delete = models.SET_NULL)
    bug_title = models.CharField(max_length = 200)
    bug_detail = models.TextField()
    deadline_time = models.CharField(max_length = 20)
    submitted_time = models.CharField(max_length = 20)


class SprintReviewer(models.Model):
    sprint = models.ForeignKey(SprintData, on_delete = models.CASCADE)
    # pass or fail
    review = models.CharField(max_length=20)
    dAndTime = models.CharField(max_length = 20)

class BugReviewer(models.Model):
    bug = models.ForeignKey(BugData, on_delete = models.CASCADE)
    # pass or fail
    review = models.CharField(max_length=20)
    dAndTime = models.CharField(max_length = 20)
