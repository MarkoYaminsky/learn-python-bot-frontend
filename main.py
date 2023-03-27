from app.settings.bot import bot

import app.handlers.message_handlers
import app.handlers.start_handler
import app.handlers.callback_handlers

if __name__ == "__main__":
    bot.infinity_polling()
