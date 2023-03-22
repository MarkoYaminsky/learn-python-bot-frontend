from settings.bot import bot

import handlers.message_handlers
import handlers.start_handler
import handlers.callback_handlers

if __name__ == "__main__":
    bot.infinity_polling()
