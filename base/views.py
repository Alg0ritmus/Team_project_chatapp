from django.shortcuts import render,redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json



from .models import *

from django.views.decorators.csrf import csrf_exempt

# decorators
from .firebaseTokenSer import firebase_token_verification

# Create your views here.
def index(request):

    chatRooms = Chat_room.objects.all()
    rs=[room.pk for room in chatRooms]

    #return HttpResponse("return this string")
    return render(request,'base/index.html',{"rooms": rs})



def room(request, room_name):
    return render(request, "base/room.html", {"room_name": room_name})


####################
# CRUD App
#############################


# Chat_user create (POST)
@csrf_exempt
#@firebase_token_verification
@api_view(['POST'])
def create_chat_user(request):

    # process data from POST request
    
    raw_data = request.body.decode()
    
    json_data = json.loads(raw_data)

    tukbook_usr_uuid = json_data["tukbook_usr_uuid"]
    user_username = json_data["username"]

    try:
        usr1 = Chat_user.objects.create(tukbook_usr_uuid=str(tukbook_usr_uuid),username=user_username)
    except Exception as e:
        return Response({"SimulatedStatus":500,"Error:":str(e)})

    return Response({"Register User Response:":"User was successfully registreted!"})


# Chat_user delete (Get)
@firebase_token_verification
@api_view(['GET'])
def delete_chat_user(request,pk):
    try:
        usr1 = Chat_user.objects.get(tukbook_usr_uuid=pk)
        usr1.delete()
    except Exception as e:
         return Response({"SimulatedStatus":500,"Error:":str(e)})

    return Response({"Deletion of User, Response:":"User was successfully deleted!"})   



# Chat_room create (POST)
@csrf_exempt
#@firebase_token_verification
@api_view(['POST'])
def create_chat_room(request):
    raw_data = request.body.decode()
    json_data = json.loads(raw_data)
    #print(json_data,json_data["username"],json_data["email"],json_data["password"])

    # process data from POST request
    usr1_uuid = json_data["usr_uuid"]
    usr2_uuid = json_data["friends_uuid"]

    # usrs are already created (when they register)
    # get usrs
    try:
        usr1 = Chat_user.objects.get(tukbook_usr_uuid=str(usr1_uuid))
        usr2 = Chat_user.objects.get(tukbook_usr_uuid=str(usr2_uuid))
    except Exception as e:
         return Response({"SimulatedStatus":500,"Error:":str(e)}) 
    
    # create chat_room & add usrs
    try:
        # if chat room exists, then redirect to chat room,
        if Chat_room.objects.filter(chat_room_users=usr1).filter(chat_room_users=usr2).exists() == True:
            roomid=Chat_room.objects.filter(chat_room_users=usr1).filter(chat_room_users=usr2)

            
            return redirect({"SimulatedStatus":200,"roomId":roomid.pk})
        # if not, create room and redirect
        chat1 = Chat_room.objects.create()
        chat1.chat_room_users.add(usr1)
        chat1.chat_room_users.add(usr2)
    except Exception as e:
        return Response({"SimulatedStatus":500,"Error:":str(e)})

    return redirect({"SimulatedStatus":200,"roomId":roomid.pk})


# Chat_room delete (Get)


@firebase_token_verification
@api_view(['GET'])
def delete_chat_room(request,pk):
    try:
        chatroom1 = Chat_room.objects.get(pk=pk)
        chatroom1.delete()
    except Exception as e:
         return Response({"SimulatedStatus":500,"Error:":str(e)})

    return Response({"Deletion of Chat room, Response:":"Chat room was successfully deleted!"})   


# Chat_room list all chat room, for specific user (Get)
@firebase_token_verification
@api_view(['GET'])
def get_users_chat_rooms(request,pk):
    try:
        arr = []
        usr1 = Chat_user.objects.get(tukbook_usr_uuid=pk)
        chatrooms = Chat_room.objects.filter(chat_room_users=usr1)
        for room in chatrooms:
            for user in room.chat_room_users.all():
                if str(user.tukbook_usr_uuid) != str(usr1.tukbook_usr_uuid):
                    usr_json = {"username":user.username,"chat_room_id":chatrooms.pk}
                    arr.append(usr_json)
        
    except Exception as e:
         return Response({"SimulatedStatus":500,"Error:":str(e)})

    return Response({"Getting chatrooms for specific user, Response:":"Chat rooms were successfully optained!","chat_rooms":arr})   


    

# get all msgs for specific room
@firebase_token_verification
@api_view(['GET'])
def get_users_chat_msg(request,pk):
    #print("getting msg")
    try:
        chatroom = Chat_room.objects.get(pk=pk)
        chatroom_msgs = Chat_msg.objects.filter(room_id=chatroom)
        chatroom_msgs_array = []
        for msg in chatroom_msgs:
            if msg.is_text == True:
                chatroom_msgs_array.append({"sender_name":msg.sender_id.username,"sender_uuid":msg.sender_id.tukbook_usr_uuid,"isText":True,"body":msg.text,"timestamp":msg.timestamp.strftime("%d.%m.%Y, %H:%M:%S")})
            else:
                chatroom_msgs_array.append({"sender_name":msg.sender_id.username,"sender_uuid":msg.sender_id.tukbook_usr_uuid,"isText":False,"body":msg.content_file_url,"timestamp":msg.timestamp.strftime("%d.%m.%Y, %H:%M:%S")})


    except Exception as e:
         return Response({"SimulatedStatus":500,"Error:":str(e)})
    #print(chatroom_msgs_array)
    return Response({"Getting messagess for specific room, Response:":"Messages were successfully optained!","messages":chatroom_msgs_array})   




# creating File as MSG will be HTTP/S req.

###########################################################
#
#       WEBSOCKET FUNCTIONS | not http/s    
#
###########################################################



# Msg (create) sa bude robit pomocou WS!!!

# return True if success, False if it fails
def create_chat_room_msg(text,room_id,sender_id):
    is_text_ = True
    text_ = text
    room_id_ = room_id
    sender_id_ = sender_id
    #print("Creating MSG")
    try:
        room = Chat_room.objects.get(pk=room_id_)
        sender = Chat_user.objects.get(tukbook_usr_uuid=sender_id)
        msg = Chat_msg.objects.create(is_text=is_text_,text=text_,room_id=room,sender_id=sender)
        msg.save()
    except Exception as e:
        #print("Creating MSG: error",e)
        return False

    return True

def delete_chat_room_msg(pk,msg_id):
    try:
        msg = Chat_msg.objects.get(pk=msg_id)
        if msg.sender_id == pk:
            msg.delete()
    except Exception as e:
        return False

    return True

def update_chat_room_msg(pk,msg_id,text):
    try:
        msg = Chat_msg.objects.get(pk=msg_id)
        if msg.sender_id == pk:
            msg.text = text
            msg.save()
    except Exception as e:
        return False

    return True