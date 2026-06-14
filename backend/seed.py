import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from space_app.models import Topic, Section, Question, Choice

def seed():
    # ========================================
    # TOPIC 1: Quyosh tizimi sirlari
    # ========================================
    topic1, _ = Topic.objects.get_or_create(
        title="Quyosh tizimi sirlari",
        defaults={"description": "Quyosh tizimi va sayyoralar haqida qiziqarli faktlar!"}
    )

    # Sections for Topic 1
    if not Section.objects.filter(topic=topic1).exists():
        Section.objects.create(
            topic=topic1,
            title="Quyosh tizimi nima?",
            content="Quyosh tizimi – bu Quyosh va uning atrofida aylanadigan 8 ta sayyora, ularning yo'ldoshlari, asteroidlar va kometalardan iborat ulkan kosmik oila. Quyosh bu oilaning markazi va eng katta a'zosi hisoblanadi.",
            media_url="/static/assets/sun.png",
            order=1
        )
        Section.objects.create(
            topic=topic1,
            title="Ichki sayyoralar",
            content="Merkuriy, Venera, Yer va Mars – bu ichki sayyoralar deyiladi. Ular kichik, tosh va metallardan iborat. Merkuriy eng kichik va tez, Venera eng issiq, Yer hayot bor bo'lgan yagona sayyora, Mars esa qizil sayyora deb ataladi.",
            media_url="/static/assets/earth.png",
            order=2
        )
        Section.objects.create(
            topic=topic1,
            title="Tashqi sayyoralar",
            content="Yupiter, Saturn, Uran va Neptun – tashqi sayyoralar. Ular juda katta va asosan gazlardan iborat. Yupiter eng katta, Saturn halqalari bilan mashhur, Uran yonboshlab aylanadi, Neptun esa eng sovuq sayyora.",
            media_url="/static/assets/mars.png",
            order=3
        )

    # Questions for Topic 1 - 30 ta
    print("Topic 1 uchun savollar yangilanmoqda...")
    Question.objects.filter(topic=topic1).delete()

    questions_topic1 = [
        {"q": "Quyosh tizimida nechta sayyora bor?", "options": [("6 ta", False), ("8 ta", True), ("10 ta", False)]},
        {"q": "Quyoshga eng yaqin sayyora qaysi?", "options": [("Venera", False), ("Merkuriy", True), ("Yer", False)]},
        {"q": "Quyosh tizimidagi eng kichik sayyora qaysi?", "options": [("Mars", False), ("Merkuriy", True), ("Pluton", False)]},
        {"q": "Quyosh tizimidagi eng katta sayyora qaysi?", "options": [("Saturn", False), ("Yupiter", True), ("Neptun", False)]},
        {"q": "Yer Quyoshdan nechanchi sayyora?", "options": [("Ikkinchi", False), ("Uchinchi", True), ("To'rtinchi", False)]},
        {"q": "Qaysi sayyora 'Qizil sayyora' deb ataladi?", "options": [("Yupiter", False), ("Mars", True), ("Venera", False)]},
        {"q": "Qaysi sayyoraning chiroyli halqalari bor?", "options": [("Yupiter", False), ("Saturn", True), ("Uran", False)]},
        {"q": "Quyosh nima hisoblanadi?", "options": [("Sayyora", False), ("Yulduz", True), ("Asteroid", False)]},
        {"q": "Quyosh tizimidagi eng issiq sayyora qaysi?", "options": [("Merkuriy", False), ("Venera", True), ("Mars", False)]},
        {"q": "Quyosh tizimidagi eng sovuq sayyora qaysi?", "options": [("Uran", False), ("Neptun", True), ("Saturn", False)]},
        {"q": "Quyosh asosan qaysi gazdan iborat?", "options": [("Kislorod", False), ("Vodorod", True), ("Azot", False)]},
        {"q": "Oy nima hisoblanadi?", "options": [("Sayyora", False), ("Yulduz", False), ("Tabiiy yo'ldosh", True)]},
        {"q": "Mars sayyorasida nechta tabiiy yo'ldosh bor?", "options": [("1 ta", False), ("2 ta", True), ("3 ta", False)]},
        {"q": "Yupiter sayyorasidagi katta qizil dog' nima?", "options": [("Yangi vulqon", False), ("Ulkan bo'ron", True), ("Suvli okean", False)]},
        {"q": "Qaysi sayyora yonboshlab aylanadi?", "options": [("Neptun", False), ("Uran", True), ("Saturn", False)]},
        {"q": "Asteroid kamar qaysi ikki sayyora orasida joylashgan?", "options": [("Yer va Mars", False), ("Mars va Yupiter", True), ("Yupiter va Saturn", False)]},
        {"q": "Pluton hozir nima deb tasniflanadi?", "options": [("Sayyora", False), ("Mitti sayyora", True), ("Yulduz", False)]},
        {"q": "Quyosh tizimidagi eng yirik tabiiy yo'ldosh qaysi?", "options": [("Oy", False), ("Ganimed", True), ("Titan", False)]},
        {"q": "Qaysi sayyorada suyuq suv bo'lishi mumkin deb taxmin qilinadi?", "options": [("Venera", False), ("Mars", True), ("Merkuriy", False)]},
        {"q": "Yer o'z o'qi atrofida qancha vaqtda bir marta aylanadi?", "options": [("12 soat", False), ("24 soat", True), ("48 soat", False)]},
        {"q": "Yer Quyosh atrofida qancha vaqtda bir marta aylanadi?", "options": [("30 kun", False), ("365 kun", True), ("100 kun", False)]},
        {"q": "Kometa nima?", "options": [("Muzlik va chang aralashmasi", True), ("Kichik sayyora", False), ("Yangi yulduz", False)]},
        {"q": "Quyosh yorug'ligi Yerga yetib kelishi uchun qancha vaqt ketadi?", "options": [("1 sekund", False), ("8 daqiqa", True), ("1 soat", False)]},
        {"q": "Qaysi sayyorada bir kun bir yildan uzun?", "options": [("Mars", False), ("Venera", True), ("Yupiter", False)]},
        {"q": "Saturn halqalari asosan nimadan iborat?", "options": [("Muz va tosh", True), ("Gaz", False), ("Suv", False)]},
        {"q": "Neptun sayyorasi qanday rangda ko'rinadi?", "options": [("Qizil", False), ("Ko'k", True), ("Sariq", False)]},
        {"q": "Quyosh tizimida eng tez aylanadigan sayyora qaysi?", "options": [("Yer", False), ("Yupiter", True), ("Mars", False)]},
        {"q": "Venera sayyorasini yana qanday nom bilan atashadi?", "options": [("Tong yulduzi", True), ("Qizil yulduz", False), ("Shimol yulduzi", False)]},
        {"q": "Merkuriy sayyorasida atmosfera bormi?", "options": [("Ha, juda qalin", False), ("Deyarli yo'q", True), ("Ha, kislorodli", False)]},
        {"q": "Quyosh tizimi qaysi galaktikada joylashgan?", "options": [("Andromeda", False), ("Somon yo'li", True), ("Uchburchak", False)]},
    ]

    for index, q_data in enumerate(questions_topic1):
        q = Question.objects.create(topic=topic1, text=q_data["q"], order=index+1)
        for choice_text, is_correct in q_data["options"]:
            Choice.objects.create(question=q, text=choice_text, is_correct=is_correct)

    print(f"Topic 1: {len(questions_topic1)} ta savol qo'shildi!")

    # ========================================
    # TOPIC 2: Koinot Sirlari
    # ========================================
    topic2, _ = Topic.objects.get_or_create(
        title="Koinot Sirlari",
        defaults={"description": "Bolalar uchun koinot, sayyoralar va yulduzlar haqida qiziqarli sayohat!"}
    )
    
    # Sections for Topic 2
    if not Section.objects.filter(topic=topic2).exists():
        Section.objects.create(
            topic=topic2,
            title="Quyosh tizimi",
            content="Quyosh tizimi – bu Quyosh va uning atrofida aylanadigan sayyoralardan iborat katta oila.",
            media_url="/static/assets/sun.png",
            order=1
        )
        Section.objects.create(
            topic=topic2,
            title="Bizning Uyimiz - Yer",
            content="Yer – Quyosh tizimidagi hayot bor bo'lgan yagona sayyora. U asosan suvdan iborat bo'lgani uchun moviy ko'rinadi.",
            media_url="/static/assets/earth.png",
            order=2
        )
        Section.objects.create(
            topic=topic2,
            title="Qizil Sayyora",
            content="Mars – Yerdan keyingi sayyora. Uning tuprog'ida temir ko'p bo'lgani uchun u qip-qizil bo'lib ko'rinadi.",
            media_url="/static/assets/mars.png",
            order=3
        )

    # Questions for Topic 2 - 30 ta
    print("Topic 2 uchun savollar yangilanmoqda...")
    Question.objects.filter(topic=topic2).delete()

    questions_topic2 = [
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

    for index, q_data in enumerate(questions_topic2):
        q = Question.objects.create(topic=topic2, text=q_data["q"], order=index+1)
        for choice_text, is_correct in q_data["options"]:
            Choice.objects.create(question=q, text=choice_text, is_correct=is_correct)

    print(f"Topic 2: {len(questions_topic2)} ta savol qo'shildi!")
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
