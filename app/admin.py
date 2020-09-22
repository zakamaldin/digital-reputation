from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from app.models import *


class AnswerInline(NestedStackedInline):
    model = Answer
    extra = 1


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]


class TestAdmin(NestedModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Test, TestAdmin)
admin.site.register(Question)
admin.site.register(Answer)
