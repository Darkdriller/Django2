from django.shortcuts import render
import django_tables2 as tables
from .models import ImageClassification


# Create your views here.
from django.http import HttpResponse
# 'request' name is convention. It can be some other name too.
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from .model import ImageClassifier
from .models import ImageClassification

class ImageClassificationTable(tables.Table):
    id = tables.Column()
    image = tables.Column()
    ip_address = tables.Column()
    label = tables.Column()
    
    class Meta:
        model = ImageClassification
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "image", "ip_address", "label")¸
clicked = 1
def index(request) :
  global clicked
  my_dict = { 'message' : "This is an injected content",'count' : clicked}
  clicked += 1
  classifications = ImageClassification.objects.all()
  table = ImageClassificationTable(classifications)
  my_dict = { 'message' : "This is an injected content",'count' : clicked, 'table':table}
  response = render(request,'index.html',context=my_dict)
  return response
def help(request):
  response = render(request,'help.html')
  return response
def upload_image(request):
    return render(request, 'image.html')
def classify_image(request):
    if request.method == 'POST':
        # read the uploaded image file from the POST request
        image_file = request.FILES['image']
        
        # create an in-memory file-like object from the uploaded image file
        image_buffer = BytesIO(image_file.read())
        image = Image.open(image_buffer)
        
        
        # preprocess and classify the image using the ImageClassifier class
        classifier = ImageClassifier()
        image_bytes = BytesIO()
        image.save(image_bytes, format='JPEG')
        predicted_classes = classifier.predict(image_bytes)
        classification = ImageClassification(
            image_data=image_file.read(),
            ip_address=request.META.get('REMOTE_ADDR', ''),
            label=predicted_classes[0][1]
        )
        classification.save()
        # do something with the predicted classes, e.g. return as JSON response
        return HttpResponse(predicted_classes[0][1])