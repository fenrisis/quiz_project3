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
from rest_framework import viewsets
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer
from .forms import createuserform
from django.db.models import Sum
from django.contrib import messages
from django.urls import reverse


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


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')  # Add error message
        context = {}
        return render(request, 'quizes/login.html', context)


# Logout Page
def logoutPage(request):
    logout(request)
    return redirect('/')


def leaderboard(request):
    top_results = Result.objects.values('user__username').annotate(total_score=Sum('score')).order_by('-total_score')[:500]
    total_count = top_results.count()
    context = {
        'top_results': top_results,
        'total_count': total_count,
    }
    return render(request, 'quizes/leaderboard.html', context=context)

def faq_view(request):
    return render(request, 'quizes/faq.html')

# Quiz List View
class QuizListView(ListView):
    model = Quiz 
    template_name = 'quizes/main.html'


# Quiz View
def quiz_view(request, pk):
    if pk == 'favicon.ico':
        # Handle the favicon.ico request here
        return HttpResponse(status=204)  # Return a blank response

    if pk == 'leaderboard':
        # Handle the leaderboard request here
        return leaderboard(request)
    
    if pk == 'faq':
        # Handle the FAQs request here
        return faq_view(request)

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


#serialize
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer



# Save Quiz View (requires login)
@login_required
def save_quiz_view(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'To get results, you need to be logged in')
        return HttpResponseRedirect(reverse('quizes:login'))

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




