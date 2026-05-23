import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
from database import register_user, get_all_books, search_books_by_title

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    telegram_id = user.id
    full_name = user.full_name

    register_user(telegram_id, full_name)

    await update.message.reply_text(
        f"Assalomu alaykum, {full_name}!\n"
        "Kutubxona botiga xush kelibsiz.\n\n"
        "/books - barcha kitoblar ro'yxati\n"
        "/search <kitob nomi> - kitob qidirish"
    )


async def books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    books = get_all_books()
    if not books:
        await update.message.reply_text("Hozircha kutubxonada kitoblar mavjud emas.")
        return

    message = "📖 Kutubxonamizdagi kitoblar ro'yxati:\n\n"
    for book in books:
        message += f"📘 {book['title']} (Muallif: {book['author_name']}) — Soni: {book['available_copies']} ta\n"

    await update.message.reply_text(message)


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Iltimos, qidirish uchun kitob nomini kiriting.\nMisol: /search Xamsa")
        return

    search_term = " ".join(context.args)
    books = search_books_by_title(search_term)

    if not books:
        await update.message.reply_text("📭 Kutubxonamizda bunday kitob topilmadi.")
        return

    response = f"🔍 '{search_term}' bo'yicha qidiruv natijalari:\n\n"
    for book in books:
        status = "✅ Mavjud" if book['available_copies'] > 0 else "❌ Ayni damda qolmagan"
        response += f"📘 {book['title']} (Muallif: {book['author_name']}) — {status} — Soni: {book['available_copies']} ta\n"

    await update.message.reply_text(response)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.startswith("/"):
        return

    books = search_books_by_title(text)
    if not books:
        await update.message.reply_text("📭 Kutubxonamizda bunday kitob topilmadi.")
        return

    response = f"🔍 '{text}' bo'yicha qidiruv natijalari:\n\n"
    for book in books:
        status = "✅ Mavjud" if book['available_copies'] > 0 else "❌ Ayni damda qolmagan"
        response += f"📘 {book['title']} (Muallif: {book['author_name']}) — {status} — Soni: {book['available_copies']} ta\n"

    await update.message.reply_text(response)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("books", books))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()