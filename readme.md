## Schema
https://excalidraw.com/#json=X_Zu2-ZuZEjqMKnBCD8uB,jYtJTehsVJQtBmZp7uIr5g


# JWT on WS
https://www.linode.com/docs/guides/authenticating-over-websockets-with-jwt/


# TODO: 

1) WS authentifikacia cez firepase JWT (lokalne), pricom creds sa stiahnu zo servera na heroku


    def ready(self):
        if os.environ.get('RUN_MAIN'):
            from dotenv import load_dotenv
            from pathlib import Path
            import requests
            import json
            print("Exec once")
            dotenv_path = Path('.env')
            load_dotenv(dotenv_path=dotenv_path)
            response_from_request = ....

            os.environ['firebase_cfg'] = json.loads(response_from_request)




2) Databaza, kt. bude ukladat roomky, usrs, msgs atd...
https://channels.readthedocs.io/en/latest/topics/databases.html

3) Prepojit frontend s backendom

4) deploy na https://www.pythonanywhere.com/ 

5) pridaj dekoraory na secured routes(views.py) :checeked:

6) urob consumer Async kvoli exceptions // cakat 2 sec pred close asi neni optimalne



# prikazy

usr1 = Chat_user.objects.create(tukbook_usr_uuid="abcd",username="pato")
usr2 = Chat_user.objects.create(tukbook_usr_uuid="dcba",username="mato")

chat1 = Chat_room.objects.create()

chat1.chat_room_users.add(usr1)
chat1.chat_room_users.add(usr2)


chat1.chat_room_users.all()[0].username

# queries

get all chat rooms, in which user1 participate

Chat_room.objects.filter(chat_room_users = usr1)



get all usrers in specific "[0]" chat_room

Chat_room.objects.filter(chat_room_users = usr1)[0].chat_room_users.all()


get all msg from that room

Chat_msg.objects.filter(room_id = chat1)














# reg. creds.
{
  "username": "testing_chat_urs1",
  "password": "testing_chat_urs1",
  "email": "testing_chat_urs1@adresa.com"
}



{
  "password": "testing_chat_urs1",
  "email": "testing_chat_urs1@adresa.com"
}



{
    "tukbook_usr_uuid": "",
    "username": ""
}