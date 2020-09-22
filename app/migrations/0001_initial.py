# Generated by Django 3.1.1 on 2020-09-22 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=200, verbose_name='Текст варианта ответа')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Является правильным вариантом ответа?')),
            ],
            options={
                'verbose_name': 'Вариант ответа',
                'verbose_name_plural': 'Варианты ответа',
            },
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_number', models.IntegerField(default=0, verbose_name='Номер попытки')),
            ],
            options={
                'verbose_name': 'Попытка',
                'verbose_name_plural': 'Попытки',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200, verbose_name='Текст вопроса')),
                ('score_for_question', models.IntegerField(verbose_name='Количество очков за правильный ответ')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=200, verbose_name='Тема теста')),
                ('max_attempts', models.IntegerField(default=10, verbose_name='Максимальное количество попыток сдачи теста')),
                ('is_available', models.BooleanField(default=True, verbose_name='Доступен для прохождения')),
                ('min_score', models.IntegerField(default=20, verbose_name='Минимальное количество баллов, для прохождения теста')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ManyToManyField(to='app.Answer', verbose_name='Варианты ответа, выбранные пользователем')),
                ('attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.attempt', verbose_name='Попытка')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question', verbose_name='Пользователь')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Ответ пользователя на вопрос',
                'verbose_name_plural': 'Ответы пользователя на вопросы',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.test', verbose_name='Вопрос из теста'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.test', verbose_name='Тест'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='unanswered_question_list',
            field=models.ManyToManyField(to='app.Question', verbose_name='Список неотвеченных вопросов'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question', verbose_name='Вариант ответа на вопрос'),
        ),
    ]