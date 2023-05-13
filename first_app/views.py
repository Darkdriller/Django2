from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# 'request' name is convention. It can be some other name too.
clicked = 1
def index(request) :
  global clicked
  my_dict = { 'message' : "This is an injected content",'count' : clicked}
  clicked += 1
  response = render(request,'index.html',context=my_dict)
  return response
def help(request):
  response = render(request,'help.html')
  return response
def upload_image(request):
    return render(request, 'image.html')
def classify_image(request):
    
    return render(request, 'image.html')