from django.urls import path
from .views import tests, get_test, get_question, attempts_ended, accept_answer, result
urlpatterns = [
    path('', tests, name='tests'),
    path('tests/<int:test_id>/', get_test, name='get_test'),
    path('tests/<int:test_id>/get_question/', get_question, name='get_question'),
    path('attempts_ended/', attempts_ended, name='attempts_ended'),
    path('accept_answer/', accept_answer, name='accept_answer'),
    path('result/', result, name='result'),
]
