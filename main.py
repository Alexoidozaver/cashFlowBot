#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import random

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.constants import DICE_DICE
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

STOCK = 'News'
BID = 'Bid'

images = {
    STOCK: "stock",
    BID: "bid",
}


def game(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [
        [BID, STOCK],
    ]
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    context.chat_data["photos"] = []
    update.message.reply_text(
        'Starting the game.', reply_markup=ReplyKeyboardMarkup(reply_keyboard),
    )
    return 1


def game_handler(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    message = update.message.text
    if not context.chat_data.get("photos"):
        context.chat_data["photos"] = []
    print(context.chat_data)
    if message in images:
        directory = images[message]
        path = f"images/{directory}"
        path_images = os.listdir(path)
        path_images = [f"{path}/{image}" for image in path_images]
        unique_path_images = os.listdir("images/unique/")
        print(unique_path_images)
        unique_path_images = [
            f"images/unique/{image}" for image in unique_path_images
            if f"images/unique/{image}" not in context.chat_data["photos"]
        ]
        print(unique_path_images)
        if message == BID:
            path_images += unique_path_images
        print(path_images)
        file_path = random.choice(path_images)
        if file_path in unique_path_images:
            context.chat_data["photos"].append(file_path)
        update.message.reply_photo(open(os.path.abspath(file_path), 'rb'))
    return 1


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1465697626:AAGs7JZJOeDAS11LzaofYsjlim2O0lh7uPk", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO

    dispatcher.add_handler(CommandHandler("start_game", game))
    dispatcher.add_handler(MessageHandler(Filters.text, game_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()