import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_start_command

from Post.models import Post 
from states.St import *
    

def name(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    update.message.reply_text(
        'name ')

    return PHOTO

def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    update.message.reply_text(
        'Gorgeous!\n next one is caption'
    )
    return CAPTION


def caption(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    update.message.reply_text('Caption have doneeee!!!!')
    return ConversationHandler.END

def add_post(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("post qoshamiz..\npost nomini kiriting")
    return NAME
    




    

# def name(update: Update, context: CallbackContext) -> int:
#     """Stores the selected gender and asks for a photo."""
#     user = update.message.from_user
#     update.message.reply_text(
#         'name ')

#     return PHOTO

# def photo(update: Update, context: CallbackContext) -> int:
#     """Stores the photo and asks for a location."""
#     user = update.message.from_user
#     photo_file = update.message.photo[-1].get_file()
#     photo_file.download('user_photo.jpg')
#     update.message.reply_text(
#         'Gorgeous!'
#     )
#     return CAPTION


# def caption(update: Update, context: CallbackContext) -> int:
#     """Stores the info about the user and ends the conversation."""
#     user = update.message.from_user
#     update.message.reply_text('Caption have doneeee!!!!')
#     return ConversationHandler.END


def commmand_Post(update: Update, context: CallbackContext) -> None:
    x=Post.objects.all()
    
    for i in x:
        text=str((f'{i.name} : {i.content}\n'))
        # update.message.reply_text(text)
        update.message.reply_photo(photo=i.photo,caption=text)

# def add_post(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text("post qoshamiz..")

#     return NAME
    


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_start_command())




def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )


#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# # context.
# def start(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /start is issued."""
#     user = update.effective_user
#     update.message.reply_markdown_v2(
#         fr'Hi {user.mention_markdown_v2()}\!',
#         reply_markup=ForceReply(selective=True),
#     )


# def help_command(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


# def main() -> None:
#     """Start the bot."""
#     # Create the Updater and pass it your bot's token.
#     updater = Updater("TOKEN")

#     # Get the dispatcher to register handlers
#     dispatcher = updater.dispatcher

#     # on different commands - answer in Telegram
#     dispatcher.add_handler(CommandHandler("start", start))
#     dispatcher.add_handler(CommandHandler("help", help_command))

#     # on non command i.e message - echo the message on Telegram
#     dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

#     # Start the Bot
#     updater.start_polling()

#     # Run the bot until you press Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT. This should be used most of the time, since
#     # start_polling() is non-blocking and will stop the bot gracefully.
#     updater.idle()


# if __name__ == '__main__':
#     main()