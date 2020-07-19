from django.contrib import admin
from .models import CreateQuiz, QuizResult

# Register your models here.
admin.site.register(CreateQuiz)
admin.site.register(QuizResult)
