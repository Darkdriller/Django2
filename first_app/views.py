from django.shortcuts import render
import base64
from django.shortcuts import redirect
from django.http import HttpResponse
# 'request' name is convention. It can be some other name too.
from io import BytesIO
from PIL import Image
from .model import ImageClassifier
from .models import ClassificationResult
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import time
clicked = 1
def save_uploaded_image(image):
  fs = FileSystemStorage(location=settings.STATIC_DIR)
  timestr = time.strftime("%Y%m%d-%H%M%S")
  filename = fs.save(timestr+'upload'+image.name, image)
  image_path = os.path.join(settings.STATIC_URL, filename)
  return image_path
def index(request) :
  global clicked
  my_dict = { 'message' : "This is an injected content",'count' : clicked}
  clicked += 1
  # classifications = ImageClassification.objects.all()
  # classification_list = [
  #     {
  #         "image": classification.image_data,
  #         "ip_address": classification.ip_address,
  #         "classification": classification.label,
  #     }
  #     for classification in classifications
  # ]
  # table = ImageClassificationTable(classifications)
  # print(classifications)
  def binaryToDataURL(binaryData):
        base64String = base64.b64encode(binaryData).decode('utf-8')
        return base64String
  my_dict = { 'message' : "This is an injected content",'count' : clicked, 'binaryToDataURL': binaryToDataURL}
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
        image_path = save_uploaded_image(image_file)
        classifier = ImageClassifier()
        image_bytes = BytesIO()
        image.save(image_bytes, format='JPEG')
        predicted_classes = classifier.predict(image_bytes)
        # classification = ImageClassification(
        #     image_data=image_file.read(),
        #     ip_address=request.META.get('REMOTE_ADDR', ''),
        #     label=predicted_classes[0][1]
        # )
        # classification.save()
        # do something with the predicted classes, e.g. return as JSON response
        prediction=predicted_classes[0][1]
        return render(request,'result.html', context={'image_path':image_path, 'predicted_class':prediction})
    else:
        return render(request, 'image.html')
def classification_feedback(request):
    if request.method == 'POST':
        image_path = request.POST.get('image')
        ip_address = request.POST.get('ip_address')
        prediction = request.POST.get('prediction')
        is_correct = request.POST.get('is_correct')
        correct_label = request.POST.get('correct_label', '')

        result = ClassificationResult(
            image_path=image_path,
            ip_address=ip_address,
            prediction=prediction,
            is_correct=is_correct == 'yes',
            correct_label=correct_label
        )
        result.save()

    return redirect('index')
def statistics(request):
    total_results = ClassificationResult.objects.count()
    correct_results = ClassificationResult.objects.filter(is_correct=True).count()
    accuracy_percentage = 0

    if total_results > 0:
        accuracy_percentage = (correct_results / total_results) * 100

    results = ClassificationResult.objects.all()
    
    context = {
        'accuracy_percentage': accuracy_percentage,
        'results': results,
    }
    if request.method == 'POST' and 'delete-button' in request.POST:
        ClassificationResult.objects.all().delete()
        return redirect('statistics')
    return render(request, 'stats.html', context)
