from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Test, Attempt, Question, Answer, UserAnswer


@login_required
def tests(request):
    tests = Test.objects.all()
    return render(request, 'app/tests.html', {'tests': tests})


@login_required
def get_test(request, test_id):
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return redirect('tests')

    attempt_number = Attempt.objects.filter(user=request.user, test=test).count()
    if attempt_number >= test.max_attempts:
        return redirect('attempts_ended')

    attempt = Attempt.objects.create(user=request.user, test=test)
    attempt.attempt_number = attempt_number
    attempt.unanswered_question_list.set(test.question_set.all())
    attempt.save()
    return redirect('get_question', test_id=test.id)


@login_required
def get_question(request, test_id):
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return redirect('tests')
    attempt = test.attempt_set.last()
    question = attempt.get_unanswered_question()

    if question is None:
        return redirect('result')

    answers = question.answer_set.all()
    count_of_right_answers = answers.filter(is_correct=True).count()
    if count_of_right_answers > 1:
        answers_type = 'checkbox'
    else:
        answers_type = 'radio'

    data = {'question': question,
            'attempt_id': attempt.id,
            'question_id': question.id,
            'answers': answers,
            'answers_type': answers_type,
            'count_of_right_answers': count_of_right_answers
            }
    return render(request, 'app/question_form.html', data)


@login_required
def attempts_ended(request):
    return render(request, 'app/attempts_ended.html')


@login_required
def accept_answer(request):
    if request.method != "POST":
        return redirect('tests')

    answers = request.POST.getlist('answer')

    if len(answers) == 0:
        return redirect('tests')

    try:
        user_answers = Answer.objects.filter(id__in=answers)
        attempt = Attempt.objects.get(id=request.POST.get('attempt_id'))
        question = Question.objects.get(id=request.POST.get('question_id'))
        test = Test.objects.get(id=attempt.test_id)
    except (Attempt.DoesNotExist, Question.DoesNotExist):
        return redirect('tests')

    user_answer = UserAnswer(user=request.user, question=question, attempt=attempt)
    user_answer.save()
    user_answer.answers.set(user_answers)
    attempt.remove_question_from_unanswered_list(question)

    return redirect('get_question', test_id=test.id)


@login_required
def result(request):
    user = request.user
    attempt = user.attempt_set.last()
    if attempt is None:
        return redirect('tests')

    user_answers = list(UserAnswer.objects.filter(attempt=attempt)
                        .select_related('question')
                        .prefetch_related('question__answer_set', 'answers'))
    result_score = 0
    correct_questions = set()

    for user_answer in user_answers:
        scores_for_question = user_answer.question.score_for_question
        right_answers_in_question = user_answer.question.answer_set.filter(is_correct=True)
        score_for_right_answer = scores_for_question / right_answers_in_question.count()

        for answer in user_answer.answers.all():
            if answer in right_answers_in_question:
                result_score += score_for_right_answer
                correct_questions.add(user_answer.question)

    data = {
        'passed': result_score >= attempt.test.min_score,
        'good': len(correct_questions),
        'all': len(user_answers),
        'score': result_score
    }
    return render(request, 'app/result.html', data)

