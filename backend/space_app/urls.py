from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    TopicListView, SectionListView, QuizListView, QuizSubmitView,
    RegisterView, ProfileView
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    path('intro/', TopicListView.as_view(), name='topic-list'),
    path('topic/<int:topic_id>/sections/', SectionListView.as_view(), name='section-list'),
    path('topic/<int:topic_id>/quiz/', QuizListView.as_view(), name='quiz-list'),
    path('topic/<int:topic_id>/quiz/submit/', QuizSubmitView.as_view(), name='quiz-submit'),
]
