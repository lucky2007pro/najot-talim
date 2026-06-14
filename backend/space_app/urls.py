from django.urls import path
from .views import TopicListView, SectionListView, QuizListView, QuizSubmitView

urlpatterns = [
    path('intro/', TopicListView.as_view(), name='topic-list'),
    path('topic/<int:topic_id>/sections/', SectionListView.as_view(), name='section-list'),
    path('topic/<int:topic_id>/quiz/', QuizListView.as_view(), name='quiz-list'),
    path('topic/<int:topic_id>/quiz/submit/', QuizSubmitView.as_view(), name='quiz-submit'),
]
