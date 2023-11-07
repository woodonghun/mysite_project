from django.contrib import admin
from .models import Question, Answer


# 검색 기능 추가
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


# 검색 기능 추가
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
