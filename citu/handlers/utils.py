# Copyright (c) 2017 akhail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
from functools import wraps

from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from citu.api import Login
from citu.model import Student


def require_login(func):
    """Decorator require login in web. """
    logger = logging.getLogger(__name__)

    @wraps(func)
    def _require_login(*args, **kwargs):
        update = args[-1]
        user = update.message.from_user.username
        try:
            student = Student.get(Student.username == user)
            logger.info(f"The user {user} login.")
            return func(*args, login=Login(student), **kwargs)
        except Student.DoesNotExist:
            update.message.reply_text("Inicia sesión para usar esta función.")

    return _require_login


def cancel_handler(_, update):
    """command /cancel. """
    update.message.reply_text("Se ha cancelado la acción",
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
