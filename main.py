# -*- coding: utf-8 -*-
import os
import sys
import asyncio
import logging
from aiohttp import web

# Windows konsolida UTF-8 emojilarni bexato chiqarish
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from config import BOT_TOKEN

# Token tekshiruvi: Agar token kiritilmagan bo'lsa
if not BOT_TOKEN or ":" not in BOT_TOKEN:
    print("\n" + "=" * 65)
    print("❌ DIQQAT: TELEGRAM BOT TOKEN KIRITILMAGAN YOKI NOTO'G'RI!")
    print("=" * 65)
    print("Bot ishlashi uchun quyidagi oddiy qadamlarni bajaring:")
    print("1. Telegramda @BotFather ga kiring va yangi bot yarating (/newbot);")
    print("2. U bergan tokenni oling (masalan: 1234567890:ABCdefGhI...)")
    print("3. Loyiha papkasidagi '.env' faylini oching va quyidagicha yozing:")
    print("   BOT_TOKEN=1234567890:ABCdefGhI...")
    print("4. So'ngra 'python main.py' buyrug'ini qayta ishga tushiring.")
    print("=" * 65 + "\n")
    sys.exit(1)

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from questions import QUESTIONS

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispetcher obyektlarini yaratish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Foydalanuvchilarning test holatini saqlash (in-memory)
# Format: user_id -> {"index": int, "score": int, "wrong": int, "answered": bool}
user_sessions = {}


def get_start_reply_keyboard() -> ReplyKeyboardMarkup:
    """Pastda doimiy chiqib turadigan Start tugmasi (Reply Keyboard)"""
    button = KeyboardButton(text="🚀 Start (Testni boshlash)")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


def get_question_markup(question_data: dict) -> InlineKeyboardMarkup:
    """Savol tagidagi 4 ta variant tugmalari (Inline Keyboard)"""
    keyboard = []
    # 4 ta variantni chiroyli tugmalar ko'rinishida chiqaramiz
    for idx, opt in enumerate(question_data["options"]):
        btn = InlineKeyboardButton(
            text=opt,
            callback_data=f"ans_{question_data['id']}_{idx}"
        )
        keyboard.append([btn])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_restart_markup() -> InlineKeyboardMarkup:
    """Test yakunida qayta boshlash tugmasi"""
    btn = InlineKeyboardButton(text="🔄 Testni qayta boshlash", callback_data="start_test")
    return InlineKeyboardMarkup(inline_keyboard=[[btn]])


async def send_question(chat_id: int, user_id: int):
    """Foydalanuvchiga navbatdagi savolni yuborish"""
    session = user_sessions.get(user_id)
    if not session:
        return

    index = session["index"]
    total = len(QUESTIONS)

    # Agar barcha savollar tugagan bo'lsa, natijani chiqaramiz
    if index >= total:
        score = session["score"]
        wrong = session["wrong"]
        percent = round((score / total) * 100, 1)

        result_icon = "🎉" if percent >= 70 else "⚠️"
        status_text = (
            "🏆 Tabriklaymiz! Siz imtihondan muvaffaqiyatli o'tdingiz!"
            if percent >= 70 else
            "📚 Natija yetarli emas. Yana bir oz qoidalarni o'rganib, qayta topshiring!"
        )

        final_text = (
            f"🏁 <b>TEST YAKUNLANDI!</b>\n\n"
            f"📊 <b>Umumiy natijangiz:</b>\n"
            f"🔹 Jami savollar: {total} ta\n"
            f"✅ To'g'ri javoblar: <b>{score} ta</b>\n"
            f"❌ Noto'g'ri javoblar: <b>{wrong} ta</b>\n"
            f"📈 Samaradorlik ko'rsatkichi: <b>{percent}%</b>\n\n"
            f"{result_icon} <i>{status_text}</i>\n\n"
            f"Qayta sinab ko'rish uchun pastdagi tugmani bosing 👇"
        )
        await bot.send_message(
            chat_id=chat_id,
            text=final_text,
            parse_mode="HTML",
            reply_markup=get_restart_markup()
        )
        return

    # Navbatdagi savol
    q = QUESTIONS[index]
    session["answered"] = False  # Yangi savolga hali javob berilmadi

    text = (
        f"🚗 <b>Yo'l Harakati Qoidalari (Prava) Testi</b>\n"
        f"❓ <b>Savol {index + 1} / {total}:</b>\n\n"
        f"<b>{q['question']}</b>\n\n"
        f"<i>Quyidagi 4 ta variantdan birini tanlang:</i>"
    )

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="HTML",
        reply_markup=get_question_markup(q)
    )


# 1. /start buyrug'i uchun handler
@dp.message(CommandStart())
@dp.message(Command("help"))
async def cmd_start(message: Message):
    """
    1-TALAB:
    Telegram botga kirganda bu bot nimalar qilish mumkinligini aytadi
    va pastda 'Start' yozuvi chiqib turadi.
    """
    welcome_text = (
        f"Assalomu alaykum, <b>{message.from_user.full_name}</b>! 🚗🚦\n\n"
        f"📋 <b>Ushbu bot — Haydovchilik guvohnomasi (Prava) imtihoniga tayyorlovchi rasmiy test boti!</b>\n\n"
        f"🔹 <b>Botda nimalar qilish mumkin:</b>\n"
        f"1. Yo'l harakati qoidalariga oid eng muhim savollarni yechish;\n"
        f"2. Har bir savol ostidagi 4 ta variantdan to'g'risini tanlash;\n"
        f"3. Variantni tanlaganingizda to'g'ri javob va uning qonuniy izohini ko'rish;\n"
        f"4. Javob berilgach, bot avtomatik tarzda keyingi savolga o'tadi;\n"
        f"5. Test so'ngida to'g'ri va noto'g'ri javoblaringiz hisoblab beriladi.\n\n"
        f"Testni boshlash uchun pastdagi <b>'🚀 Start (Testni boshlash)'</b> tugmasini bosing!"
    )

    start_inline = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🚀 Testni boshlash", callback_data="start_test")
        ]]
    )

    await message.answer(
        text=welcome_text,
        parse_mode="HTML",
        reply_markup=get_start_reply_keyboard()  # Pastdagi doimiy 'Start' klaviaturasi
    )


# Testni boshlash (Inline tugma orqali)
@dp.callback_query(F.data == "start_test")
async def handle_start_test(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_sessions[user_id] = {
        "index": 0,
        "score": 0,
        "wrong": 0,
        "answered": False
    }
    await callback.answer("🚦 Test boshlanmoqda! Omad!")
    await send_question(chat_id=callback.message.chat.id, user_id=user_id)


# Testni boshlash (Pastdagi Reply Start tugmasi orqali)
@dp.message(F.text == "🚀 Start (Testni boshlash)")
async def handle_reply_start(message: Message):
    user_id = message.from_user.id
    user_sessions[user_id] = {
        "index": 0,
        "score": 0,
        "wrong": 0,
        "answered": False
    }
    await message.answer("🚦 <b>Test boshlandi! Omad tilaymiz!</b>", parse_mode="HTML")
    await send_question(chat_id=message.chat.id, user_id=user_id)


# 2-TALAB:
# Savollar birin-ketin chiqadi, tagida 4 ta variant,
# user bosganda tagidan to'g'ri javob chiqadi va keyingi savolga avtomatik o'zi o'tadi!
@dp.callback_query(F.data.startswith("ans_"))
async def handle_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    session = user_sessions.get(user_id)

    if not session:
        user_sessions[user_id] = {
            "index": 0,
            "score": 0,
            "wrong": 0,
            "answered": False
        }
        session = user_sessions[user_id]

    # Bir savolga ikki marta bosib yuborishdan himoya
    if session.get("answered", False):
        await callback.answer("Siz bu savolga javob bergansiz. Keyingi savol yuklanmoqda...", show_alert=False)
        return

    session["answered"] = True

    # Ma'lumotlarni ajratib olamiz: ans_{question_id}_{chosen_idx}
    parts = callback.data.split("_")
    q_id = int(parts[1])
    chosen_idx = int(parts[2])

    current_idx = session["index"]
    if current_idx >= len(QUESTIONS):
        await callback.answer()
        return

    q = QUESTIONS[current_idx]
    correct_idx = q["correct"]
    correct_option_text = q["options"][correct_idx]
    chosen_option_text = q["options"][chosen_idx]
    explanation = q.get("explanation", "")

    # To'g'ri / Noto'g'ri ekanligini aniqlash
    is_correct = (chosen_idx == correct_idx)
    if is_correct:
        session["score"] += 1
        result_title = "✅ <b>TO'G'RI JAVOB!</b> 🎉"
        await callback.answer("✅ Barakalla, to'g'ri javob!", show_alert=False)
    else:
        session["wrong"] += 1
        result_title = f"❌ <b>NOTO'G'RI JAVOB!</b> (Siz tanladingiz: <i>{chosen_option_text}</i>)"
        await callback.answer("❌ Noto'g'ri javob!", show_alert=False)

    # 4 ta variant tugmalariga to'g'ri va noto'g'ri belgilarni qo'yish
    updated_keyboard = []
    for idx, opt in enumerate(q["options"]):
        if idx == correct_idx:
            btn_text = f"✅ {opt}"
        elif idx == chosen_idx and not is_correct:
            btn_text = f"❌ {opt}"
        else:
            btn_text = opt
        # Bosilgandan so'ng qayta bosilmaydigan qilish
        updated_keyboard.append([InlineKeyboardButton(text=btn_text, callback_data="disabled_btn")])

    # Savol tagidan to'g'ri javob va izohni chiqaramiz
    updated_text = (
        f"🚗 <b>Yo'l Harakati Qoidalari (Prava) Testi</b>\n"
        f"❓ <b>Savol {current_idx + 1} / {len(QUESTIONS)}:</b>\n\n"
        f"<b>{q['question']}</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{result_title}\n\n"
        f"🎯 <b>To'g'ri javob:</b> <b>{correct_option_text}</b>\n"
        f"💡 <b>Izoh:</b> <i>{explanation}</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⏳ <i>Keyingi savolga avtomatik o'tilmoqda...</i>"
    )

    try:
        await callback.message.edit_text(
            text=updated_text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=updated_keyboard)
        )
    except Exception as e:
        logging.error(f"Xabarni yangilashda xato: {e}")

    # Keyingi savol indeksiga o'tamiz
    session["index"] += 1

    # AVTOMATIK KEYINGI SAVOLGA O'TISH:
    # Foydalanuvchi to'g'ri javobni o'qib olishi uchun 2 soniya kutadi
    await asyncio.sleep(2.0)
    await send_question(chat_id=callback.message.chat.id, user_id=user_id)


@dp.callback_query(F.data == "disabled_btn")
async def handle_disabled(callback: CallbackQuery):
    await callback.answer("Javob berildi. Keyingi savol ochilmoqda...", show_alert=False)


async def start_web_server():
    """Render port tekshiruvi (port binding) uchun kichik veb-server."""
    async def handle_ping(request):
        return web.Response(text="🚗 Prava Test Boti faol!")

    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)

    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Veb-server {port}-portda ishga tushirildi.")


async def main():
    print("🚗 Prava Test Boti muvaffaqiyatli ishga tushirildi...")
    
    # Render port tekshiruvidan muvaffaqiyatli o'tish uchun veb-server
    try:
        await start_web_server()
    except Exception as e:
        print(f"Veb-serverni ishga tushirishda ogohlantirish: {e}")

    print("Bot xabarlarni kutmoqda...")
    # Eski xabarlarni tozalash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi!")

