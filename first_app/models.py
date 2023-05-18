from django.db import models

# Create your models here.
# Program
# class Program(models.Model):
#     title = models.CharField(max_length=20)
#     branch = models.CharField(max_length=50)
 
#     def __str__(self):
#         return self.title + self.branch
# # Student
# class Student(models.Model):
#     roll_number = models.CharField(max_length=20)
#     name = models.CharField(max_length=50)
#     year = models.IntegerField(default=1)
#     dob = models.DateField('date of birth')
#     program = models.ForeignKey(Program, on_delete=models.CASCADE)
#     # __str__ function   
#     def __str__(self):
#         d = self.program
#         return self.roll_number + self.name  + d.title + d. branch
class ClassificationResult(models.Model):
    image_path = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    prediction = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    correct_label = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
# class User(models.Model):
#     user_ip=models.GenericIPAddressField()
#     def __str__(self) -> str:
#         return self.user_ip
    