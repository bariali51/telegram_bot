import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

BOT_TOKEN = "8322436103:AAGGeKDe7eFLmwX1vnYNdOJkSAK2l45oNhs"

# أسئلة الشركات الناشئة
QUESTIONS = [
    {
        "question": "ما هو تعريف الـ MVP في عالم الشركات الناشئة؟",
        "choices": ["منتج نهائي", "منتج أولي للتجربة", "خطة عمل", "دراسة جدوى"],
        "answer": "منتج أولي للتجربة"
    },
    {
        "question": "ما الهدف الأساسي من الـ Pivot في الشركات الناشئة؟",
        "choices": ["تغيير الفريق", "تغيير النموذج التجاري", "زيادة الميزانية", "تقليل التكاليف"],
        "answer": "تغيير النموذج التجاري"
    },
    {
        "question": "ما هو دور المستثمر الملائكي (Angel Investor)؟",
        "choices": ["استثمار مبالغ صغيرة في البداية", "قيادة الشركة", "خدمة العملاء", "إدارة التسويق"],
        "answer": "استثمار مبالغ صغيرة في البداية"
    },
    {
        "question": "ما أهم عنصر لنجاح الشركة الناشئة في البداية؟",
        "choices": ["الفريق", "الزينة", "موقع المكتب", "عدد الموظفين"],
        "answer": "الفريق"
    },
    {
        "question": "ما هو الـ Pitch Deck؟",
        "choices": ["عرض تقديمي للمستثمرين", "تقرير مالي", "خطة إنتاج", "كتيب المستخدم"],
        "answer": "عرض تقديمي للمستثمرين"
    }
]

# لتخزين نقاط المستخدمين
user_scores = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_scores[user_id] = 0
    await update.message.reply_text("مرحباً! 🎓\nلنبدأ اختبار الشركات الناشئة.\nاضغط /quiz لبدء أول سؤال.")

async def send_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    question_data = random.choice(QUESTIONS)

    context.user_data["current_question"] = question_data

    keyboard = [
        [InlineKeyboardButton(choice, callback_data=choice)]
        for choice in question_data["choices"]
    ]

    await update.message.reply_text(
        f"❓ السؤال:\n{question_data['question']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    selected = query.data
    correct = context.user_data["current_question"]["answer"]

    if selected == correct:
        user_scores[user_id] += 1
        reply = "✅ إجابة صحيحة! ممتاز 👏"
    else:
        reply = f"❌ إجابة خاطئة.\nالإجابة الصحيحة هي: {correct}"

    await query.edit_message_text(
        reply + f"\n\nنقاطك: {user_scores[user_id]}\n\nاضغط /quiz للسؤال التالي."
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", send_quiz))
    app.add_handler(CallbackQueryHandler(answer))

    print("✅ Quiz Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
