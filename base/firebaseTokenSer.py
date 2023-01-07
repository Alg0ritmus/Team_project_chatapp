from rest_framework.response import Response
import json
import pyrebase
from .models import Chat_user
from dotenv import load_dotenv
from pathlib import Path
import os
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


firebaseConfig = json.loads(os.environ['firebase_cfg'])

firebase=pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()


#from .views import authe

def firebase_token_verification_nondecorator(token):
    
    tokenId = token
    #print(tokenId)


    # check if token is valid
    # using firebase IdToken verification func 

    # isIdTokenVerified = authe.verify(idToken_from_response)
    isIdTokenVerified = [False,]

    # https://github.com/thisbejim/Pyrebase/blob/7a652e6bd9d148da5ff6dbe7548c6d5d0dfa1109/pyrebase/pyrebase.py#L126
    try:
        decoded_token = authe.get_account_info(tokenId)
    except:
        pass
    #print(decoded_token)
    #uid = decoded_token['uid']

    
    if Chat_user.objects.filter(tukbook_usr_uuid=decoded_token["users"][0]["localId"]).exists():
        isIdTokenVerified = [True,decoded_token["users"][0]["localId"]]

    return isIdTokenVerified



def firebase_token_verification(view_func):
    def func_to_return(request, *args, **kwargs):
        raw_token_form_req = (request.headers['Authorization'])
        tokenId = raw_token_form_req[1:-1].split()[1]
        print(tokenId)


        # check if token is valid
        # using firebase IdToken verification func 

        # isIdTokenVerified = authe.verify(idToken_from_response)

        # https://github.com/thisbejim/Pyrebase/blob/7a652e6bd9d148da5ff6dbe7548c6d5d0dfa1109/pyrebase/pyrebase.py#L126
        decoded_token = authe.get_account_info(tokenId)
        print(decoded_token)
        #uid = decoded_token['uid']

        isIdTokenVerified = False
        if Chat_user.objects.filter(tukbook_usr_uuid=decoded_token["users"][0]["localId"]).exists():
            isIdTokenVerified = True

        if isIdTokenVerified == False:
            return Response({"Failure":"Invalid token or token has expired!"})

        return view_func(request, *args, **kwargs)

    return func_to_return