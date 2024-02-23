from rest_framework import serializers
from .models import *

class UserDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserDetail
		fields ='__all__'

class ChatDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = ChatData
		fields = '__all__'
		# fields = 'msg_from, msg, time_of_message'


class AnnouncementSerializer(serializers.ModelSerializer):
	class Meta:
		model = Announcement
		fields = '__all__'
