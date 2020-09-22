from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list


class Test(models.Model):
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    theme = models.CharField(verbose_name='Тема теста', max_length=200)
    max_attempts = models.IntegerField(verbose_name='Максимальное количество попыток сдачи теста', default=10)
    is_available = models.BooleanField(verbose_name='Доступен для прохождения', default=True)
    min_score = models.IntegerField(verbose_name='Минимальное количество баллов, для прохождения теста', default=20)

    def __str__(self):
        return f'{self.theme}'


class Question(models.Model):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    test = models.ForeignKey(Test, verbose_name='Вопрос из теста', on_delete=models.CASCADE)
    question_text = models.CharField(verbose_name='Текст вопроса', max_length=200)
    score_for_question = models.IntegerField(verbose_name='Количество очков за правильный ответ')

    def __str__(self):
        return f"{self.question_text} из теста '{self.test.theme}'"


class Answer(models.Model):
    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    question = models.ForeignKey(Question, verbose_name='Вариант ответа на вопрос', on_delete=models.CASCADE)
    answer_text = models.CharField(verbose_name='Текст варианта ответа', max_length=200)
    is_correct = models.BooleanField(verbose_name='Является правильным вариантом ответа?', default=False)

    def __str__(self):
        return f"{self.answer_text} на вопрос '{self.question.question_text}' в тесте '{self.question.test.theme}'"


class Attempt(models.Model):
    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, verbose_name='Тест', on_delete=models.CASCADE)
    attempt_number = models.IntegerField(verbose_name='Номер попытки', default=0)
    unanswered_question_list = models.ManyToManyField(Question, verbose_name='Список неотвеченных вопросов')

    def get_unanswered_question(self):
        return self.unanswered_question_list.first()

    def remove_question_from_unanswered_list(self, question):
        self.unanswered_question_list.remove(question)


class UserAnswer(models.Model):
    class Meta:
        verbose_name = 'Ответ пользователя на вопрос'
        verbose_name_plural = 'Ответы пользователя на вопросы'

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Пользователь', on_delete=models.CASCADE)
    attempt = models.ForeignKey(Attempt, verbose_name='Попытка', on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer, verbose_name='Варианты ответа, выбранные пользователем')

