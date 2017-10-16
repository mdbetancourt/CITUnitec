# Copyright (c) 2017 Michel Betancourt
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Module for codes.

"""
import logging
from telegram import ChatAction
from telegram.ext import CommandHandler
from citu.handlers.utils import require_login

class PreCodeSubjects(CommandHandler):
    """Get pre inscription codes. """
    def __init__(self):
        super().__init__(
            command='codigos',
            callback=PreCodeSubjects.precode_handler
        )

    @staticmethod
    @require_login
    def precode_handler(login, bot, update):
        """Handler code. """
        _logger = logging.getLogger(__name__)
        _logger.info(f"{login.student.username} get codes")
        bot.send_chat_action(chat_id=update.message.chat.id, action=ChatAction.TYPING)

        items = login.codes.items()
        if items:
            for code, values in items:
                subjects = '\n'.join(values)
                update.message.reply_text(f"{code}:\n{subjects}")
        else:
            update.message.reply_text("No hay codigos.")
