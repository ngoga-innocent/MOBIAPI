import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from django.contrib.auth import get_user_model
import os
from django.conf import settings
from ProductApi.models import DeviceTokens,Notification
from rest_framework.response import Response
from firebase_admin._messaging_utils import UnregisteredError
User=get_user_model()
credential_path = os.path.join(settings.BASE_DIR, 'API', 'ServiceAccountKey.json')
logopath=os.path.join(settings.BASE_DIR, 'API', 'logo.png')
cred = credentials.Certificate(credential_path)
firebase_admin.initialize_app(cred)

# def get_all_device_tokens():
#     users=User.objects.all()
#     all_device_tokens=[]

#     for user in users:
#         token=user.device_token

#         all_device_tokens.append(token)

#     return all_device_tokens
# def send_push_to_all(title,body):
#      all_devices_tokens=get_all_device_tokens()

#      for token in all_devices_tokens:
#          send_push_notification(token,title,body)

# def send_to_individual(token,title,body):
#     send_push_notification(token,title,body)


def send_push_notification(token, title, body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body, image=logopath),
            data={
                "title": title,
                "body": body
            },
            token=token,
        )

        response = messaging.send(message)
        print("Successfully sent message:", response)
    
    except UnregisteredError:
        # Handle unregistered token: remove or mark as inactive in your database
        print("Unregistered token:", token)
        # Example: Assuming you have a DeviceTokens model with a 'token' field
        # You can mark it as inactive (e.g., set 'active' field to False)
        delete=DeviceTokens.objects.filter(deviceToken=token).delete()
        if delete:
            pass
        else:
            pass
    except Exception as e:
        # Handle other exceptions (e.g., network errors)
        print("Error sending message:", str(e))
def send_to_all_tokens(title,body):
    tokens=DeviceTokens.objects.all()

    for token in tokens:
        toke=token.deviceToken
        send_push_notification(toke,title,body)

def create_and_send_notification_one(title,body,owner,type):
    not_owner=User.objects.get(id=owner)
    if not_owner:
        save_not= Notification.objects.create(name=title,recipient=not_owner,type=type,message=body)
        if save_not:
           return send_push_notification(not_owner.device_token,title,body)
        else:
           return Response({'message':'not sent notification'})
def create_and_send_notification_all(title,body,type):
    users=User.objects.all()
    for user in users:
        save_notifications=Notification.objects.create(name=title,recipient=user,type=type,message=body)
        if save_notifications:
            send_push_notification(user.device_token,title,body)
