import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from space_app.models import Topic, Section, Question, Choice

def seed():
    # Topics
    topic, created = Topic.objects.get_or_create(
        title="Koinot Sirlari",
        description="Bolalar uchun koinot, sayyoralar va yulduzlar haqida qiziqarli sayohat!"
    )
    
    # Sections
    if not Section.objects.filter(topic=topic).exists():
        Section.objects.create(
            topic=topic,
            title="Quyosh tizimi",
            content="Quyosh tizimi – bu Quyosh va uning atrofida aylanadigan sayyoralardan iborat katta oila.",
            media_url="/static/assets/sun.png",
            order=1
        )
        Section.objects.create(
            topic=topic,
            title="Bizning Uyimiz - Yer",
            content="Yer – Quyosh tizimidagi hayot bor bo'lgan yagona sayyora. U asosan suvdan iborat bo'lgani uchun moviy ko'rinadi.",
            media_url="/static/assets/earth.png",
            order=2
        )
        Section.objects.create(
            topic=topic,
            title="Qizil Sayyora",
            content="Mars – Yerdan keyingi sayyora. Uning tuprog'ida temir ko'p bo'lgani uchun u qip-qizil bo'lib ko'rinadi.",
            media_url="/static/assets/mars.png",
            order=3
        )

    # Questions - Reset and recreate to ensure we have the new bank of questions
    print("O'chirilyapti: Eski savollar...")
    Question.objects.filter(topic=topic).delete()

    print("Qo'shilyapti: Yangi 30+ ta savollar...")
    questions_data = [
        {"q": "Quyosh tizimida biz yashaydigan sayyora qaysi?", "options": [("Mars", False), ("Yer", True), ("Oy", False)]},
        {"q": "Mars sayyorasi qanday rangda?", "options": [("Ko'k", False), ("Yashil", False), ("Qizil", True)]},
        {"q": "Quyosh nima?", "options": [("Sayyora", False), ("Yulduz", True), ("Sun'iy yo'ldosh", False)]},
        {"q": "Quyosh tizimidagi eng katta sayyora qaysi?", "options": [("Yupiter", True), ("Saturn", False), ("Venera", False)]},
        {"q": "Yerdan tungi osmonda ko'rinadigan eng yorug' jism nima?", "options": [("Quyosh", False), ("Mars", False), ("Oy", True)]},
        {"q": "Qaysi sayyoraning atrofida chiroyli halqalari bor?", "options": [("Yer", False), ("Saturn", True), ("Merkuriy", False)]},
        {"q": "Koinotga birinchi bo'lib qaysi jonivor uchgan?", "options": [("Maymun", False), ("It (Layka)", True), ("Mushuk", False)]},
        {"q": "Odamzot birinchi marta qayerga qadam bosgan?", "options": [("Oyga", True), ("Marsga", False), ("Quyoshga", False)]},
        {"q": "Quyoshga eng yaqin joylashgan sayyora qaysi?", "options": [("Merkuriy", True), ("Venera", False), ("Yer", False)]},
        {"q": "Bizning galaktikamiz nima deb ataladi?", "options": [("Somon yo'li", True), ("Qora tuynuk", False), ("Andromeda", False)]},
        {"q": "Teleskop yordamida nimalarni ko'ramiz?", "options": [("Kichik hasharotlarni", False), ("Uzoqdagi yulduzlar va sayyoralarni", True), ("Dengiz ostini", False)]},
        {"q": "Quyosh tizimida nechta sayyora bor?", "options": [("7 ta", False), ("8 ta", True), ("9 ta", False)]},
        {"q": "Eng issiq sayyora qaysi?", "options": [("Venera", True), ("Merkuriy", False), ("Mars", False)]},
        {"q": "Qaysi sayyora yonboshlab aylanadi?", "options": [("Uran", True), ("Neptun", False), ("Saturn", False)]},
        {"q": "Koinot kemasini boshqaradigan odam nima deyiladi?", "options": [("Uchuvchi", False), ("Fazogir", True), ("Dengizchi", False)]},
        {"q": "Quyosh asosan qaysi gazlardan iborat?", "options": [("Kislorod va karbonat angidrid", False), ("Vodorod va geliy", True), ("Azot va metan", False)]},
        {"q": "Yer o'z o'qi atrofida bir marta aylanib chiqishi uchun qancha vaqt ketadi?", "options": [("24 soat", True), ("1 yil", False), ("1 oy", False)]},
        {"q": "Yer Quyosh atrofida bir marta aylanib chiqishi uchun qancha vaqt ketadi?", "options": [("24 soat", False), ("1 yil (365 kun)", True), ("1 oy", False)]},
        {"q": "Qaysi sayyorada hayot borligi aniq tasdiqlangan?", "options": [("Mars", False), ("Yer", True), ("Hech qaysisida", False)]},
        {"q": "Koinotda havo bormi?", "options": [("Ha, ko'p", False), ("Faqat bulutlarda", False), ("Yo'q, u yerda havo yo'q (vakuum)", True)]},
        {"q": "Quyosh botganidan keyin osmonda nimalar ko'rinadi?", "options": [("Yulduzlar", True), ("Kamalak", False), ("Quyosh", False)]},
        {"q": "Galaktika bu nima?", "options": [("Katta yulduzlar, sayyoralar va gazlar to'plami", True), ("Katta muz qismi", False), ("Faqat bitta sayyora", False)]},
        {"q": "Oy o'zidan yorug'lik tarqatadimi?", "options": [("Ha, chiroqdek", False), ("Yo'q, Quyosh nurini qaytaradi", True), ("Faqat kunduzi", False)]},
        {"q": "Qaysi sayyorani 'Moviy sayyora' deb atashadi?", "options": [("Neptun", False), ("Yer", True), ("Uran", False)]},
        {"q": "Qora tuynuk nima qiladi?", "options": [("Hamma narsani, hattoki yorug'likni ham o'ziga tortadi", True), ("Yorug'lik tarqatadi", False), ("Sayyoralarni yaratadi", False)]},
        {"q": "Koinotga uchish uchun qanday ulov kerak?", "options": [("Samolyot", False), ("Raketa", True), ("Havo shari", False)]},
        {"q": "Yerdan turib ko'rish mumkin bo'lgan eng katta yulduz turkumi qaysi?", "options": [("Katta Ayiq (Cho'mich)", True), ("Kichik Ayiq", False), ("Egizaklar", False)]},
        {"q": "Meteorit nima?", "options": [("Koinotdan Yerga tushgan tosh", True), ("Kichik sayyora", False), ("Yangi yulduz", False)]},
        {"q": "Quyoshga eng uzoq joylashgan sayyora qaysi?", "options": [("Neptun", True), ("Uran", False), ("Saturn", False)]},
        {"q": "Sayyoralar nima atrofida aylanadi?", "options": [("Oy atrofida", False), ("Yer atrofida", False), ("Quyosh atrofida", True)]}
    ]

    for index, q_data in enumerate(questions_data):
        q = Question.objects.create(topic=topic, text=q_data["q"], order=index+1)
        for choice_text, is_correct in q_data["options"]:
            Choice.objects.create(question=q, text=choice_text, is_correct=is_correct)

    print(f"Jami {len(questions_data)} ta savol bazaga kiritildi!")
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
