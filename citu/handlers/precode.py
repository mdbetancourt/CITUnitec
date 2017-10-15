# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from telegram.ext import CommandHandler
from citu.handlers.utils import require_login

class PreCodeSubjects(CommandHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command='codigos',
            callback=PreCodeSubjects.precode_handler
        )

    @staticmethod
    @require_login
    def precode_handler(login, bot, update):
        pass
