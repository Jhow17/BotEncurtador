import os 
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
TOKEN_BOT = os.getenv('TELEGRAM_TOKEN')

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE ):
    
    context.user_data['iniciado'] = True

    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Cole a URL que voce deseja encurtar")
    

async def read_url(update:Update, context:ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('iniciado'):
        url = update.message.text
        await context.bot.send_message(chat_id=update.effective_chat.id, text=url)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Você precisa digitar /start primeiro!"
        )
       

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN_BOT).build()

    start_handler = CommandHandler("start", start)
    
    read_url_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), read_url)
    
    app.add_handler(start_handler)
    

    app.add_handler(read_url_handler)

    app.run_polling()