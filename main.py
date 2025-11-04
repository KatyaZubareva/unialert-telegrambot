from telegram import update
from telegram.ext import ApplicationBuilder, CommandHandler, ContenxtTypes
from parse import lesson

def show_schedule():
    pass

def main():
    app = ApplicationBuilder().token("TELEGRAM_BOT_API").build()

    app.run_polling()

if __name__ == "__main__":
    main()
