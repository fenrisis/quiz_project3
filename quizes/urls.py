from django.urls import path
from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view,   
)
from . import views

app_name = 'quizes'

urlpatterns = [
    path('', QuizListView.as_view(), name='main-view'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('<pk>/', quiz_view, name='quiz-view'),
    path('<pk>/save/', save_quiz_view, name='save-view'),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),
]