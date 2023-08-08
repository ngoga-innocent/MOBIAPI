from django.shortcuts import render

# Create your views here.
def Chat(request):
    return render(request,'Chat/chat.html')