from django.shortcuts import render
from .serializer import ChatAdminSerializer
from .models import Code,ChatAdmin
import random
import string
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.decorators import api_view
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
def Chat(request):
    return render(request,'Chat/chat.html')
def generate_verification_code():
    code = ''.join(random.choices(string.digits, k=6))
    return code

class AdminRegister(APIView):
    def post(self, request):

        serializer = ChatAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = generate_verification_code()
        subject = "Kaz ni Kaz Chat Account Created"
        message = f"Your account has been created with the username: {request.POST['username']},password:  {request.POST['password']},code: {code}"
        recipient_list = [request.data['email']]
        from_email = settings.EMAIL_HOST_USER
        if serializer.is_valid():
            admin_user = serializer.save()
            
            
            try:
                code =Code.objects.create(user=admin_user,code=code)
                sent = send_mail(subject, message, from_email, recipient_list)
                if sent > 0:
                
                    
                    
                    # token,_ = AuthToken.objects.create(admin_user)
                    return Response({
                    'user_info': {
                        'id': admin_user.id,
                        'username': admin_user.username,
                        'email': admin_user.email,
                        # 'phone_number': admin_user.phone_number,
                    },
                    # 'token': token
                })
                else:
                    return Response("failed to send Email", status=500)

            except Exception as e:
                return Response(str(e), status=500)
        else:
            return Response(serializer.errors, status=400)
@api_view(['POST'])
def CodeVerify(request):
    code = request.POST.get('code')
    user = request.POST.get('user')
    # print(code, email)
    try:
        datacode = Code.objects.get(code=code, user=user)
    except:
        return Response("no matching Code", status=404)

    time = timezone.now()
    saved = datacode.created
    difference = time-saved

    if (difference.total_seconds() > 10*60):

        return Response("expired", status=401)
    else:
        try:
            getuser=ChatAdmin.objects.get(pk=user)
            getuser.status=True
            
            getuser.save()
            recipient_list = [request.data['email']]
            from_email = settings.EMAIL_HOST_USER
            send_mail('Chat Account activate', 'Your account has been verified succesfully', from_email, [getuser.email])
        except ObjectDoesNotExist:

            return Response("user not exists", status=201)
        
class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not any([username]):
            return Response({'error': 'Please provide either username, email, or phone number.'}, status=400)

        user = None
        if username:
            user = ChatAdmin.objects.filter(username=username).first()
        if not user and '@' in username:
            user = ChatAdmin.objects.filter(email=username).first()
        

        if not user or not check_password(password,user.password):
            return Response({'error': 'Invalid credentials.'}, status=400)

        # _, token = AuthToken.objects.create(user)
        refresh=RefreshToken.for_user(user)
        token_response={'refresh':str(refresh),'access':str(refresh.access_token)}
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                
            },
             'token': token_response
        })