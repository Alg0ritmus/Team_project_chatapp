# chat/consumers.py
import json 
import time

from datetime import datetime
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer

from .models import *

from .firebaseTokenSer import firebase_token_verification_nondecorator

from .views import create_chat_room_msg, delete_chat_room_msg, update_chat_room_msg


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        error_buffer =[]
        #print("WS: connected")
        # +-------------------------------------------------------------+
        # | URL bude obsahovat: room_id, usr1_id, access_token          |    
        # +-------------------------------------------------------------+

        # Tuto pozriem, ci je usr authentifikovany pomocou JWT tokenu (z URL),
        # naledne prebehne overenie tokenu (napisem funkciu tuto v tomto repo napr JWTverify.py)
        # overenie bude prebiehat iba na zaklade firebasu, pricom cerds od firebasu stiahnem v tukebooku...
        # co zabezpeči to, že nemusim menit creds na zakdom serveri...
        # idealne by bolo ceknut creds vzdy ked sa tento server zapne resp. po kazdych 24h atd.
        # (podobne ako pri decoratore na tukebooku, z JWT vytiahnem usera..)
        valid_jwt_token = firebase_token_verification_nondecorator(self.scope["url_route"]["kwargs"]["access_token"])
        if valid_jwt_token[0] == True:
            #print("JWT is valid")
            user_uuid = valid_jwt_token[1]
        else:
            #print(valid_jwt_token[1])
            a = "JWT is NOT valid"
            error_buffer.append(4123)
            
            #return "Invalid JWT"
        # v requeste bude okrem JWT bude aj chat_room_id, a teda:
        # 1) check DB ci existuje taká roomka
        # 1.1) ak ano, checknem ci je req_uzivatel v danej roomke
        # 1.2) ak nie, chybove hlasenie alebo nieco ?
        
        
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = "chat_%s" % self.room_id

        try:
            chatroom1=Chat_room.objects.get(pk=int(self.room_id))
            usr_uuids = [usr.tukbook_usr_uuid for usr in chatroom1.chat_room_users.all()]
            if user_uuid not in usr_uuids:
                #print("E1",user_uuid)
                print("E1")
                #print(usr_uuids)
                #return "Such User is not allowed for this Chat_room"


        except Exception as e:
            print("E2",e)
            #return "Such room does not exists!"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        #print("at the end")
        self.accept()
        # delay alebo urob async
        time.sleep(2)
        if len(error_buffer)>0:
            self.close(code=error_buffer[0])

    def disconnect(self, close_code):
        #print("WS: disconnected")
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # ak chceme zistt ci je uzovatel auth. s platnym JWT pre kazdu spravu,
        #  robime to tuto
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        usr_uuid = text_data_json["usr_uuid"]

        #tuto ulozim spravu do DB
        status = create_chat_room_msg(text=message,room_id=self.room_id,sender_id=usr_uuid)
        #print("ukladanie msg do db:",status)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message,"usr_uuid": usr_uuid}
        )

    # Receive message from room group
    def chat_message(self, event):
        print("WS: msg")
        message = event["message"]
        usr_uuid = event["usr_uuid"]

        # Send message to WebSocket
        now=datetime.now()
        self.send(text_data=json.dumps({"message": message,"timestamp":now.strftime("%d.%m.%Y, %H:%M:%S"),"usr_uuid": usr_uuid}))

       
    
