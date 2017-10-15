# Copyright (c) 2017 akhail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Login handler on unitec.

"""

import logging
from telegram.ext import (
    ConversationHandler,
    Filters,
    RegexHandler,
    MessageHandler,
    CommandHandler
)

from citu.api import Login
from citu.model import Student
from citu.handlers.utils import require_login

USER, PASSWORD = range(2)

class HandlerLogout(CommandHandler):
    """Logout handler. """
    def __init__(self):
        super().__init__(
            command='logout',
            callback=HandlerLogout.logout
        )

    @staticmethod
    @require_login
    def logout(student, _, update):
        """Logout. """
        student.delete_instance()
        update.message.reply_text("Cerraste sesión")


class ConversationLogin(ConversationHandler):
    """Login conversation. """
    def __init__(self):
        """Login class. """
        super().__init__(
            entry_points=[CommandHandler('start', self.start_handler)],
            states={
                USER: [RegexHandler(r'^[0-9]{5,9}', self.user_handler)],
                PASSWORD: [MessageHandler(Filters.text, self.password_handler)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel_handler)]
        )
        self._user, self._password = None, None
        self._logger = logging.getLogger(__name__)

    def start_handler(self, _, update):
        """command /start. """
        _next = ConversationHandler.END
        send = update.message.reply_text
        chat_type = update.message.chat.type
        username = update.message.from_user.username

        try:
            Student.get(Student.username == username)
            send(f"@{username} ya has iniciado sesión.")
        except Student.DoesNotExist:
            if chat_type == "private":
                send("Introduce tus datos de la unitec. "
                     "Envia /cancel para detenerte.\n"
                     "Introduce tu cedula:")
                self._logger.info(f"The user {username} try login")
                _next = USER
            else:
                send("Solo puedes iniciar sesión en mensajeria privada.")

        return _next

    def user_handler(self, _, update):
        """Intro user. """
        self._user = update.message.text
        update.message.reply_text("Contraseña:")
        return PASSWORD

    def password_handler(self, bot, update):
        """Intro password. """
        send = update.message.reply_text
        username = update.message.from_user.username

        self._password = update.message.text
        if Login(self._user, self._password).state == Login.SUCCESS:
            send("Has sido registrado sastifactoriamente.")
            self._logger.info(f"{username} registered successfuly")

            Student(username=username,
                    identity=self._user,
                    password=self._password).save()

            return ConversationHandler.END
        else:
            update.message.reply_text("Los datos son incorrectos.")
            return self.cancel_handler(bot, update)

    def cancel_handler(self, _, update):
        """command /cancel. """
        update.message.reply_text("Se ha cancelado el inicio de sesion\n"
                                  "/start para volver a iniciar.")
        return ConversationHandler.END