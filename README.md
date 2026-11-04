# 🚗 Prava Test Savollari Telegram Boti

Ushbu loyiha Python dasturlash tili va zamonaviy **aiogram 3** kutubxonasi yordamida yaratilgan Telegram bot bo'lib, foydalanuvchilarga Yo'l Harakati Qoidalari (Prava imtihoni) bo'yicha interaktiv test savollarini taqdim etadi.

---

## 🌟 Botning Asosiy Imkoniyatlari

1. **Kirish va yo'riqnoma (/start)**:
   - Botga kirganda u nimalar qila olishini batafsil va tushunarli tushuntiradi.
   - Pastki menyuda doimiy **`🚀 Start (Testni boshlash)`** tugmasi chiqib turadi.
2. **Savollar va 4 ta variant**:
   - Savollar birin-ketin, tartibli va chiroyli dizaynda chiqadi.
   - Har bir savol ostida 4 ta inline variant (A, B, C, D) mavjud.
3. **Darhol natija va avtomatik keyingi savol**:
   - Foydalanuvchi variantni tanlaganda, savol tagidan to'g'ri javob va qonuniy izoh chiqadi (`✅ To'g'ri` yoki `❌ Noto'g'ri`).
   - Tugmalar rang bilan belgilanadi (to'g'risi yashil `✅`, noto'g'risi qizil `❌`).
   - Foydalanuvchiga to'g'ri javobni o'qib olishi uchun 2 soniya vaqt beriladi va bot **avtomatik ravishda keyingi savolga o'tadi**!
4. **Yakuniy Natija**:
   - Test so'ngida to'g'ri va noto'g'ri javoblar soni, umumiy foiz va imtihondan o'tganlik darajasi hisoblab beriladi.
   - `🔄 Testni qayta boshlash` tugmasi orqali testni istalgancha qayta topshirish mumkin.

---

## 📁 Loyiha Tuzilishi

```text
azizbek/
│
├── main.py           # Botning asosiy boshqaruv kodi va barcha mantiq
├── questions.py      # Prava bo'yicha 4 talik variantli test savollari bazasi
├── config.py         # Sozlamalar va .env faylini yuklash
├── .env              # Bot tokeni saqlanadigan maxfiy fayl
├── .env.example      # Namunaviy .env fayli
├── requirements.txt  # Kerakli Python kutubxonalari
└── README.md         # Loyiha qo'llanmasi
```

---

## 🚀 Ishga Tushirish Bo'yicha Qo'llanma

### 1-qadam: Kutubxonalarni o'rnatish
Agar kutubxonalar hali o'rnatilmagan bo'lsa, terminalda quyidagi buyruqni bering:
```bash
pip install -r requirements.txt
```

### 2-qadam: Telegramdan Bot Token olish
1. Telegramda [@BotFather](https://t.me/BotFather) botiga kiring;
2. `/newbot` buyrug'ini yuboring;
3. Botingizga nom va `@username` bering (oxiri `bot` bilan tugashi kerak);
4. BotFather sizga API Token beradi (masalan: `7123456789:AAEjK9...`).

### 3-qadam: Tokenni `.env` fayliga yozish
Loyiha papkasidagi `.env` faylini oching va tokenni yozing:
```env
BOT_TOKEN=7123456789:AAEjK9...
```

### 4-qadam: Botni ishga tushirish
Terminalda quyidagi buyruqni ishga tushiring:
```bash
python main.py
```

Endi Telegramdagi botingizga kiring va `/start` tugmasini bosing! 🚦

---

## ➕ Yangi savollar qo'shish

Yangi savollar qo'shish juda oson. `questions.py` faylini ochib, `QUESTIONS` ro'yxatiga quyidagi formatda yangi savol qo'shishingiz mumkin:

```python
{
    "id": 11,
    "question": "Savol matni shu yerga yoziladi?",
    "options": [
        "A) 1-variant",
        "B) 2-variant",
        "C) 3-variant",
        "D) 4-variant"
    ],
    "correct": 0,  # 0: A, 1: B, 2: C, 3: D (to'g'ri javob indeksi)
    "explanation": "To'g'ri javobning qisqacha tushuntirishi yoki qoida bandi"
}
```

