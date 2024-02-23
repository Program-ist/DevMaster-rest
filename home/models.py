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
    project_id = models.CharField(max_length = 200)
    project_name = models.CharField(max_length = 200)
    project_description = models.TextField()
    created_by = models.CharField(max_length = 200)
    project_created_time = models.CharField(max_length = 20)
    project_gtihub_link = models.TextField()
    project_phase = models.CharField(max_length = 20)

    def __str__(self):
        return self.project_name



class ProjectFunctionalities(models.Model):
    project_id = models.CharField(max_length = 200)
    project_funcionalities = models.CharField(max_length = 200)

class ProjectMembers(models.Model):
    pass

class ChatData(models.Model):
    msg_from = models.CharField(max_length = 200)
    project_id = models.CharField(max_length = 200)
    msg = models.TextField()
    time_of_message = models.CharField(max_length = 20)

class LlmData(models.Model):
    pass



class Announcements(models.Model):
    pass

class SprinData(models.Model):
    pass


class BugData(models.Model):
    pass





