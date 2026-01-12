import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Token will be taken from Render Environment Variable
TOKEN = os.getenv("TOKEN")

insta_tasks = [
    ("Follow Insta Page 1", "https://www.instagram.com/dearfit2025?igsh=MTlobHVrMnZwaTFmaw=="),
    ("Follow Insta Page 2", "https://www.instagram.com/jellyjel2026?igsh=MzBzZGJ2NjhlODZw"),
    ("Follow Insta Page 3", "https://www.instagram.com/__vanshh__x?igsh=aGFtcTFxNTAxaGhv"),
]

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Welcome to InstaFollowBooster\n\n"
        "Complete Instagram tasks and grow your account.\n"
        "Type /earn to start."
    )

async def earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for name, link in insta_tasks:
        keyboard.append([InlineKeyboardButton(name, url=link)])
    keyboard.append([InlineKeyboardButton("✅ I Followed", callback_data="done")])

    await update.message.reply_text(
        "🔒 Follow all Instagram pages below to unlock:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    users[uid] = users.get(uid, 0) + 10

    await query.answer()
    await query.edit_message_text(
        "✅ Verified!\nYou earned 10 points.\nUse /profile"
    )

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    points = users.get(uid, 0)
    await update.message.reply_text(
        f"👤 Your Profile\n⭐ Points: {points}\nUse /earn to get more."
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("earn", earn))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CallbackQueryHandler(done))

app.run_polling()
