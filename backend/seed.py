import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from space_app.models import Topic, Section, Question, Choice

def seed():
    print("Seeding database...")
    topic, created = Topic.objects.get_or_create(
        title="Quyosh tizimi sirlari",
        description="Bizning Quyosh tizimimizda nimalar bor? Keling, sayyoralar bilan tanishamiz!"
    )
    
    # Sections
    if not Section.objects.filter(topic=topic).exists():
        Section.objects.create(
            topic=topic,
            title="Quyosh - bizning yulduzimiz",
            content="Quyosh juda katta issiq gaz shari. U bizga yorug'lik va issiqlik beradi. Usiz yerda hayot bo'lmas edi.",
            media_url="./assets/sun.png",
            order=1
        )
        Section.objects.create(
            topic=topic,
            title="Yer - bizning uyimiz",
            content="Yer Quyosh tizimidagi yagona hayot bor sayyoradir. Uning to'rtdan uch qismi suv bilan qoplangan.",
            media_url="./assets/earth.png",
            order=2
        )
        Section.objects.create(
            topic=topic,
            title="Mars - qizil sayyora",
            content="Mars qizil tuproq va toshlar bilan qoplangan. Olimlar u yerda qachonlardir suv bo'lgan deb hisoblashadi.",
            media_url="./assets/mars.png",
            order=3
        )

    # Questions
    if not Question.objects.filter(topic=topic).exists():
        q1 = Question.objects.create(topic=topic, text="Quyosh tizimida biz yashaydigan sayyora qaysi?", order=1)
        Choice.objects.create(question=q1, text="Mars", is_correct=False)
        Choice.objects.create(question=q1, text="Yer", is_correct=True)
        Choice.objects.create(question=q1, text="Oy", is_correct=False)

        q2 = Question.objects.create(topic=topic, text="Mars sayyorasi qanday rangda?", order=2)
        Choice.objects.create(question=q2, text="Ko'k", is_correct=False)
        Choice.objects.create(question=q2, text="Yashil", is_correct=False)
        Choice.objects.create(question=q2, text="Qizil", is_correct=True)
        
        q3 = Question.objects.create(topic=topic, text="Quyosh nima?", order=3)
        Choice.objects.create(question=q3, text="Sayyora", is_correct=False)
        Choice.objects.create(question=q3, text="Yulduz", is_correct=True)
        Choice.objects.create(question=q3, text="Sun'iy yo'ldosh", is_correct=False)

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
