import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """انت مساعد برمجة شاطر ومحترم، بتتكلم بالعربي المصري ببساطة.
مهمتك: تعلم المستخدم البرمجة من الصفر للاحتراف، تشرح، تحل أكواد، وتعمل مشاريع.
ردودك قصيرة وواضحة ومفيدة، وادي أمثلة كود لما ينفع."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا بيك في منصة البرمجة 🔥\nانا هعلمك برمجة من الصفر لحد الاحتراف.\nابعتلي أي سؤال.")
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"حصلت مشكلة، جرب تاني بعد شوية.\n{e}"
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()
if __name__ == "__main__":
    main()
