from telegram import update
from telegram.ext import ApplicationBuilder, CommandHandler, ContenxtTypes
from parse import lesson

def show_schedule():
    pass

def main():
    app = ApplicationBuilder().token("7604608554:AAHVCTY61aYBWxzra8lbCiSpD9dxsIUdS2U").build()

    app.run_polling()

if __name__ == "__main__":
    main()
