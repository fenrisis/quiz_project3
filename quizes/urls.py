from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizListView, quiz_view, quiz_data_view, save_quiz_view, registerPage, loginPage, logoutPage, leaderboard, faq_view, QuizViewSet


router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)

app_name = 'quizes'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', QuizListView.as_view(), name='main-view'),
    path("login/", loginPage, name="login"),
    path("logout/", logoutPage, name="logout"),
    path('', QuizListView.as_view(), name='main-view'),
    path("register/", registerPage, name="register"),
    path('<int:pk>/', quiz_view, name='quiz-view'),  
    path('<int:pk>/save/', save_quiz_view, name='save-view'),  
    path('<int:pk>/data/', quiz_data_view, name='quiz-data-view'),  
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('faq/', faq_view, name='faq'),
]