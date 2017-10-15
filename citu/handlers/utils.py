# Copyright (c) 2017 akhail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
from functools import wraps

from citu.api import Login
from citu.model import Student

def require_login(func):
    """Decorator require login in web. """
    logger = logging.getLogger(__name__)

    @wraps(func)
    def _require_login(bot, update):
        user = update.message.from_user.username
        try:
            student = Student.get(Student.username == user)
            logger.info(f"The user {Student.username} login.")
            func(Login(student), bot, update)
        except Student.DoesNotExist:
            update.message.reply_text("Inicia sesión para usar esta funcion.")

    return _require_login
