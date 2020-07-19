from django.db import models
from django.contrib.auth.models import User
import re

# Create your models here.
class CreateQuiz(models.Model):
    key= models.CharField(max_length=16,blank=False)
    title = models.CharField(max_length=100, blank=False)
    question= models.TextField(blank=False)
    option=models.TextField(blank=False)
    answer=models.CharField(max_length=100, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    User=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return  self.User.username + '_' + self.title + '_' + self.key

    def options(self):
        cleaned_option = self.option.strip()
        options_list = []
        options_list_candidate = re.split('[,\s]', cleaned_option)
        options_list = [option for option in options_list_candidate if option]
        return options_list

class QuizResult(models.Model):
    key = models.CharField(max_length=16,blank=False)
    taker = models.CharField(max_length=100, blank=False)
    score = models.DecimalField(max_digits=5,blank=False, decimal_places=2)
    percentscore = models.IntegerField(blank=False)

    def __str__(self):
        return self.taker + ':' + self.key