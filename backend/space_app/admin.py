from django.contrib import admin
from .models import Topic, Section, Question, Choice, UserAttempt

class SectionInline(admin.StackedInline):
    model = Section
    extra = 1

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [SectionInline, QuestionInline]

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'order')
    list_filter = ('topic',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'order')
    list_filter = ('topic',)
    inlines = [ChoiceInline]

@admin.register(UserAttempt)
class UserAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'topic', 'score', 'max_score', 'created_at')
    list_filter = ('topic', 'created_at')
