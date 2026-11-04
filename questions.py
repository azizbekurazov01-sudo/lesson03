# -*- coding: utf-8 -*-
"""
Prava (Yo'l Harakati Qoidalari) bo'yicha test savollari
Har bir savolda:
- question: Savol matni
- options: 4 ta variant ro'yxati
- correct: To'g'ri javob indeksi (0, 1, 2, 3)
- explanation: To'g'ri javob izohi
"""

QUESTIONS = [
    {
        "id": 1,
        "question": "Aholi punktlarida (shaharlar va qishloqlarda) yengil avtomobillarning ruxsat etilgan eng yuqori tezligi qancha?",
        "options": [
            "A) 50 km/soat",
            "B) 60 km/soat",
            "C) 70 km/soat",
            "D) 80 km/soat"
        ],
        "correct": 1,  # B
        "explanation": "O'zbekiston Respublikasi YHQ bo'yicha aholi punktlarida ruxsat etilgan maksimal tezlik 60 km/soat etib belgilangan."
    },
    {
        "id": 2,
        "question": "Qaysi yo'l belgisi 'Asosiy yo'l'ni bildiradi?",
        "options": [
            "A) Oq hoshiyali sariq romb",
            "B) Qizil hoshiyali uchburchak",
            "C) Qizil sakkizburchak (STOP)",
            "D) Dumaloq ko'k rangli belgi"
        ],
        "correct": 0,  # A
        "explanation": "Oq hoshiyali sariq romb shaklidagi belgi — bu 'Asosiy yo'l' belgisidir."
    },
    {
        "id": 3,
        "question": "Svetoforning sariq ishorasi yonganda haydovchi nima qilishi kerak?",
        "options": [
            "A) Tezlikni oshirib o'tib ketishi kerak",
            "B) Harakatlanish taqiqlanadi (favqulodda to'xtash hollaridan tashqari)",
            "C) Faqat o'ng tomonga burilishga ruxsat etiladi",
            "D) Tovush signali berib harakatni davom ettiradi"
        ],
        "correct": 1,  # B
        "explanation": "Sariq ishora harakatlanishni taqiqlaydi va bo'lajak ishoralar almashinuvidan ogohlantiradi."
    },
    {
        "id": 4,
        "question": "Tartibga solinmagan piyodalar o'tish joyida haydovchining majburiyati nima?",
        "options": [
            "A) Piyodalarga tovush signali chalib o'tib ketish",
            "B) Piyodalarga yo'l berish va ularni o'tkazib yuborish",
            "C) Avtomobil tezligini oshirish",
            "D) Faralarni yoqib-o'chirish"
        ],
        "correct": 1,  # B
        "explanation": "Tartibga solinmagan piyodalar o'tish joyiga yaqinlashganda haydovchi qatnov qismini kesib o'tayotgan piyodalarga yo'l berishi shart."
    },
    {
        "id": 5,
        "question": "Harakatlanish vaqtida xavfsizlik kamarini kimlar taqishi shart?",
        "options": [
            "A) Faqat avtomobil haydovchisi",
            "B) Faqat old o'rindiqdagi yo'lovchi",
            "C) Konstruksiyasida xavfsizlik kamarlari ko'zda tutilgan bo'lsa, haydovchi va barcha yo'lovchilar",
            "D) Faqat tunda harakatlanganda"
        ],
        "correct": 2,  # C
        "explanation": "Konstruksiyasida xavfsizlik kamarlari ko'zda tutilgan transport vositalarida haydovchi va barcha yo'lovchilar kamar taqishi shart."
    },
    {
        "id": 6,
        "question": "Avtomobilni boshqarayotganda telefondan foydalanish qachon ruxsat etiladi?",
        "options": [
            "A) Har qanday holatda",
            "B) Faqat 'hands-free' (quloqlik yoki karnay) orqali qo'lni band qilmasdan foydalanganda",
            "C) Faqat svetoforning qizil chirog'ida to'xtab turganda",
            "D) Mutlaqo ruxsat berilmaydi"
        ],
        "correct": 1,  # B
        "explanation": "Telefondan faqatgina qo'llarni ishlatmasdan ('hands-free' qurilmalari orqali) foydalanishga ruxsat beriladi."
    },
    {
        "id": 7,
        "question": "Quyidagi joylarning qaysi birida quvib o'tish taqiqlanadi?",
        "options": [
            "A) Bir tomonlama yo'llarda",
            "B) Keng va to'g'ri yo'llarda",
            "C) Temir yo'l kesishmalarida va ulargacha 100 metrdan kam masofa qolganda",
            "D) Kunduzi harakatlanayotganda"
        ],
        "correct": 2,  # C
        "explanation": "Temir yo'l kesishmalarida va ulargacha 100 metrdan kam masofa qolganda quvib o'tish qat'iyan taqiqlanadi."
    },
    {
        "id": 8,
        "question": "Aylanma harakat chorrahasiga (krug) kirishda kim ustunlikka ega?",
        "options": [
            "A) Aylanma harakatda (krug ichida) harakatlanayotgan transport vositalari",
            "B) Aylanma harakatga endi kirib kelayotgan transport vositalari",
            "C) Har doim yuk avtomobillari",
            "D) Chap tomondan kelayotgan har qanday mashina"
        ],
        "correct": 0,  # A
        "explanation": "Belgilarga muvofiq, agar boshqacha ko'rsatilmagan bo'lsa, krug ichida harakatlanayotgan transport vositasi ustunlikka ega."
    },
    {
        "id": 9,
        "question": "Harakatlanish vaqtida orqaga burilish (razvorot) qayerda taqiqlanadi?",
        "options": [
            "A) Faqat katta ko'chalarda",
            "B) Piyodalar o'tish joylarida, tunnellar, ko'priklar va yo'lning ko'rinishi 100 metrdan kam joylarda",
            "C) Har qanday chorrahada",
            "D) Faqat shahar tashqarisida"
        ],
        "correct": 1,  # B
        "explanation": "Piyodalar o'tish joylarida, tunnel, ko'prik, yo'l o'tkazgichlarda va ko'rinishi 100 m dan kam bo'lgan joylarda orqaga burilish taqiqlanadi."
    },
    {
        "id": 10,
        "question": "Kechki payt yoki yetarlicha ko'rinmaydigan sharoitda qanday chiroqlar yoqilishi shart?",
        "options": [
            "A) Faralarning yaqinni yoki uzoqni yorituvchi chiroqlari",
            "B) Faqat avariya chirog'i (migalka)",
            "C) Chiroqlarni yoqish shart emas",
            "D) Faqat ichki salon chirog'i"
        ],
        "correct": 0,  # A
        "explanation": "Kechasi va yetarlicha ko'rinmaydigan sharoitda harakatlanayotgan transport vositalarida yaqinni yoki uzoqni yorituvchi chiroqlar yoqilishi shart."
    }
]

