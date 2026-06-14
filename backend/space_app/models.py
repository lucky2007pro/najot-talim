from django.db import models

class Topic(models.Model):
    title = models.CharField(max_length=200, verbose_name="Mavzu nomi")
    description = models.TextField(verbose_name="Qisqa tushuntirish")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"

class Section(models.Model):
    topic = models.ForeignKey(Topic, related_name="sections", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Bo'lim sarlavhasi")
    content = models.TextField(verbose_name="Matn/Ma'lumot")
    media_url = models.URLField(blank=True, null=True, verbose_name="Rasm yoki Video URL")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order']
        verbose_name = "O'rgatuvchi bo'lim"
        verbose_name_plural = "O'rgatuvchi bo'limlar"

    def __str__(self):
        return f"{self.topic.title} - {self.title}"

class Question(models.Model):
    topic = models.ForeignKey(Topic, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=500, verbose_name="Savol matni")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order']
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(max_length=200, verbose_name="Javob varianti")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javobmi?")

    class Meta:
        verbose_name = "Javob varianti"
        verbose_name_plural = "Javob variantlari"

    def __str__(self):
        return self.text

class UserAttempt(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Foydalanuvchi ismi")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(verbose_name="To'plagan ball")
    max_score = models.PositiveIntegerField(verbose_name="Maksimal ball")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Foydalanuvchi natijasi"
        verbose_name_plural = "Foydalanuvchi natijalari"

    def __str__(self):
        name = self.username if self.username else "Noma'lum"
        return f"{name} - {self.score}/{self.max_score}"

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    xp = models.PositiveIntegerField(default=0, verbose_name="Tajriba balli (XP)")
    level = models.PositiveIntegerField(default=1, verbose_name="Daraja")
    badges = models.JSONField(default=list, blank=True, verbose_name="Nishonlar")

    class Meta:
        verbose_name = "Foydalanuvchi Profili"
        verbose_name_plural = "Foydalanuvchi Profillari"

    def __str__(self):
        return f"{self.user.username} (Lvl {self.level} - {self.xp} XP)"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    is_unlocked = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'topic')
        verbose_name = "O'zlashtirish"
        verbose_name_plural = "O'zlashtirishlar"

    def __str__(self):
        return f"{self.user.username} -> {self.topic.title} (Ochiq: {self.is_unlocked})"
