from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Topic, Section, Question, Choice, UserAttempt
from .serializers import TopicSerializer, SectionSerializer, QuestionSerializer

class TopicListView(generics.ListAPIView):
    """
    Kirish ekrani ma'lumotlari
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class SectionListView(generics.ListAPIView):
    """
    O'rgatuvchi qism: Berilgan mavzu bo'yicha bo'limlar ro'yxati
    """
    serializer_class = SectionSerializer

    def get_queryset(self):
        topic_id = self.kwargs.get('topic_id')
        if topic_id:
            return Section.objects.filter(topic_id=topic_id)
        return Section.objects.none()

class QuizListView(generics.ListAPIView):
    """
    Interaktiv qism: Berilgan mavzu bo'yicha savollar va variantlar (to'g'ri javobsiz)
    """
    serializer_class = QuestionSerializer

    def get_queryset(self):
        topic_id = self.kwargs.get('topic_id')
        if topic_id:
            # Return 10 random questions for the quiz
            return Question.objects.filter(topic_id=topic_id).order_by('?')[:10]
        return Question.objects.none()

class QuizSubmitView(APIView):
    """
    Yakuniy qism: Foydalanuvchi javoblarini tekshirish va natijani hisoblash
    """
    def post(self, request, topic_id):
        # request.data format expected:
        # {
        #   "username": "Eshmat",
        #   "answers": {
        #      "question_id_1": "choice_id_1",
        #      "question_id_2": "choice_id_2"
        #   }
        # }
        username = request.data.get('username', '')
        answers = request.data.get('answers', {})
        total_questions = int(request.data.get('total_questions', len(answers)))
        
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response({"error": "Mavzu topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        score = 0

        for q_id, c_id in answers.items():
            try:
                choice = Choice.objects.get(id=c_id, question_id=q_id)
                if choice.is_correct:
                    score += 1
            except Choice.DoesNotExist:
                pass
        
        # Save attempt
        UserAttempt.objects.create(
            username=username,
            topic=topic,
            score=score,
            max_score=total_questions
        )

        # Generate encouragement message
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        if percentage == 100:
            message = "Ajoyib! Sen koinot sirlarini juda yaxshi bilar ekansan!"
        elif percentage >= 60:
            message = "Yaxshi natija! Lekin yana ozgina izlanishing kerak."
        else:
            message = "Xafa bo'lma! Darslarni qaytadan o'qib chiq va bilimingni oshir!"

        return Response({
            "score": score,
            "max_score": total_questions,
            "percentage": round(percentage, 2),
            "message": message
        })
