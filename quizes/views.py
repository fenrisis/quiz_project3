from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer
from results.models import Result
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from .models import User
from .forms import createuserform


# Register Page
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/') 
    else: 
        form=createuserform()
        if request.method=='POST':
            form=createuserform(request.POST)
            if form.is_valid() :
                user=form.save()
                return redirect('login')
        context={
            'form':form,
        }
        return render(request,'quizes/register.html',context)


# Login Page
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'quizes/login.html',context)


# Logout Page
def logoutPage(request):
    logout(request)
    return redirect('/')


# Quiz List View
class QuizListView(ListView):
    model = Quiz 
    template_name = 'quizes/main.html'


# Quiz View
def quiz_view(request, pk):
    if pk == 'favicon.ico':
        # Handle the favicon.ico request here
        return HttpResponse(status=204)  # Return a blank response

    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'quizes/quiz.html', {'obj': quiz})


# Quiz Data View
def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


# Save Quiz View (requires login)
@login_required
def save_quiz_view(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        
        # Extract the questions from the POST data
        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user  # Ensure that the user is authenticated
        quiz = get_object_or_404(Quiz, pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

       
       # Evaluate the user's answers and calculate the score
        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier

        # Save the quiz result to the database
        Result.objects.create(quiz=quiz, user=user, score=score_)

        # Return the result as JSON response
        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})




