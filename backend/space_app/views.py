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

class QuizListView(APIView):
    """
    Interaktiv qism: Berilgan mavzu bo'yicha 10 ta tasodifiy savol va variantlar
    """

    def get(self, request, topic_id):
        # Barcha savollarni olish va 10 ta tasodifiy tanlash
        questions = list(
            Question.objects.filter(topic_id=topic_id).order_by('?')[:10]
        )
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

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
        if request.user.is_authenticated:
            UserAttempt.objects.create(
                username=request.user.username,
                topic=topic,
                score=score,
                max_score=total_questions
            )
            
            # Update Gamification Profile
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            # 1 to'g'ri javob uchun 10 XP
            earned_xp = score * 10
            profile.xp += earned_xp
            
            # Level Up Logic (Har 100 XP da 1 level)
            new_level = (profile.xp // 100) + 1
            if new_level > profile.level:
                profile.level = new_level
                # Level up animation or badge could be triggered here
            profile.save()
            
            # Update Progress
            progress, _ = UserProgress.objects.get_or_create(user=request.user, topic=topic)
            if score == total_questions:
                progress.is_completed = True
            progress.save()
            
        else:
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
            "message": message,
            "earned_xp": score * 10 if request.user.is_authenticated else 0
        })

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserProgressSerializer

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"error": "Username va parol kiritilishi shart"}, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(username=username).exists():
            return Response({"error": "Bu ism allaqachon band"}, status=status.HTTP_400_BAD_REQUEST)
            
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Muvaffaqiyatli ro'yxatdan o'tdingiz!",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "user": UserSerializer(user).data
        })

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        progress = UserProgress.objects.filter(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "progress": UserProgressSerializer(progress, many=True).data
        })
