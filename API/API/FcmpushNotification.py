import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from django.contrib.auth import get_user_model
import os
from django.conf import settings
User=get_user_model()
credential_path = os.path.join(settings.BASE_DIR, 'API', 'ServiceAccountKey.json')
logopath=os.path.join(settings.BASE_DIR, 'API', 'logo.png')
cred = credentials.Certificate(credential_path)
firebase_admin.initialize_app(cred)

def get_all_device_tokens():
    users=User.objects.all()
    all_device_tokens=[]

    for user in users:
        token=user.device_token
        all_device_tokens.append(token)

    return all_device_tokens
def send_push_to_all(title,body):
     all_devices_tokens=get_all_device_tokens()

     for token in all_devices_tokens:
         send_push_notification(token,title,body)

def send_to_individual(token,title,body):
    send_push_notification(token,title,body)


def send_push_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body,image=logopath),
        data={
            "title":title,
            "body":body
        },
        token=token,
    )

    response = messaging.send(message)
    print("Successfully sent message:", response)
