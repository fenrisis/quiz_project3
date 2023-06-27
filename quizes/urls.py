from django.urls import path
from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
    registerPage,
    loginPage,
    logoutPage,
    leaderboard,   
)


app_name = 'quizes'

urlpatterns = [
    path('', QuizListView.as_view(), name='main-view'),
    path("login/", loginPage, name="login"),
    path("logout/", logoutPage, name="logout"),
    path("register/", registerPage, name="register"),
    path('<pk>/', quiz_view, name='quiz-view'),
    path('<pk>/save/', save_quiz_view, name='save-view'),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('leaderboard/', leaderboard, name='leaderboard'),
]