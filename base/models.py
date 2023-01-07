from django.db import models

# Create your models here.

#Chat_user  <--M:M-->  Chat_room

#Chat_room  <--1:M-->  Chat_msg

class Chat_user(models.Model):
    tukbook_usr_uuid = models.TextField(max_length=50,blank=True)
    username = models.TextField(max_length=100,blank=True)
    timestamp_activity = models.DateField(auto_now_add=True)

class Chat_room(models.Model):
    # M:M relation ship, bcs. we will have exactly 2 persons
    # for regular chat
    chat_room_users = models.ManyToManyField("Chat_user", blank=True)


class Chat_msg(models.Model):
    is_text = models.BooleanField(default=True)
    text = models.TextField(null=True, blank=False)
    content_file_url= models.URLField(max_length=400, blank=True)
    #M:1
    room_id = models.ForeignKey(Chat_room,on_delete=models.CASCADE)
    # sender / msg 1:M
    sender_id = models.ForeignKey(Chat_user,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

