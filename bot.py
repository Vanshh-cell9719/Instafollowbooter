import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Fake web server for Render
web_app = Flask("")

@web_app.route("/")
def home():
    return "Bot is running"

def run():
    web_app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run).start()

# Telegram Bot
TOKEN = os.getenv("TOKEN")

insta_tasks = [
    ("Follow Insta Page 1", "https://instagram.com/page1"),
    ("Follow Insta Page 2", "https://instagram.com/page2"),
    ("Follow Insta Page 3", "https://instagram.com/page3"),
]

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Welcome to InstaFollowBooster\n\n"
        "Type /earn to get Instagram tasks."
    )

async def earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for name, link in insta_tasks:
        keyboard.append([InlineKeyboardButton(name, url=link)])
    keyboard.append([InlineKeyboardButton("✅ I Followed", callback_data="done")])

    await update.message.reply_text(
        "🔒 Follow all Instagram pages:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    users[uid] = users.get(uid, 0) + 10
    await query.answer()
    await query.edit_message_text("✅ Verified! Use /earn again.")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("earn", earn))
app.add_handler(CallbackQueryHandler(done))

app.run_polling()
