import os
import pickle
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from playwright.async_api import async_playwright
import asyncio
import nest_asyncio

nest_asyncio.apply()

load_dotenv()
TELEGRAM_BOT_API = os.getenv("TELEGRAM_BOT_API")


async def fetch_schedule():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        if os.path.exists("cookies.pkl"):
            with open("cookies.pkl", "rb") as f:
                cookies = pickle.load(f)
            await context.add_cookies(cookies)
        
        page = await context.new_page()
        await page.goto("https://my.itmo.ru/schedule")
        await page.wait_for_load_state("networkidle")
        
        lessons = await page.locator("div.title").all_inner_texts()
        times = await page.locator("span.mr-1").all_inner_texts()
        teachers = await page.locator("a.text-muted").all_inner_texts()
        classrooms = await page.locator("div.max-lines-1").all_inner_texts()
        campuses = await page.locator("div.building.max-lines-1").all_inner_texts()
        
        schedule = [
            f"{times[i]} | {lessons[i]} | {teachers[i]} | {classrooms[i]} | {campuses[i]}"
            for i in range(len(lessons))
        ]
        
        await browser.close()
        return "\n".join(schedule)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 Показать расписание", callback_data="get_schedule")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Привет! Я бот ИТМО 🏫\n\n"
        "Я могу присылать тебе актуальное расписание занятий.\n"
        "Нажми кнопку ниже, чтобы получить расписание:",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text("Получаю расписание... ⏳")
    
    try:
        schedule_text = await fetch_schedule()
        if len(schedule_text) > 4000:
            schedule_text = schedule_text[:4000] + "\n\n(расписание обрезано)"
        await query.edit_message_text(f"📌 Расписание:\n\n{schedule_text}")
    except Exception as e:
        await query.edit_message_text(f"❌ Ошибка при получении расписания:\n{e}")


async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_API).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="get_schedule"))
    
    await app.run_polling()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
