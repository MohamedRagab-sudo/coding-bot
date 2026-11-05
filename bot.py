import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا بيك في منصة البرمجة 🤖\nاسألني أي سؤال في البرمجة وهجاوبك بالعربي وبأمثلة كود.")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.reply_text("ثواني بفكر... 🤔")
    try:
        prompt = f"انت مدرس برمجة شاطر، اشرح بالعربي المصري البسيط وبمثال كود. السؤال: {question}"
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text[:4000])
    except Exception:
        await update.message.reply_text("حصل مشكلة، جرب تاني بعد شوية.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
    print("البوت اشتغل...")
    app.run_polling()
