# Copyright (c) 2017 Michel Betancourt
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Module for codes.

"""
from io import BytesIO

import plotly.plotly as py
import plotly.figure_factory as ff
from telegram import ChatAction
from telegram.ext import CommandHandler

from citu.handlers.utils import require_login

class ScheduleHandler(CommandHandler):
    """Schedule handler. """
    def __init__(self):
        super().__init__(
            command='horario',
            callback=ScheduleHandler.schedule
        )

    @staticmethod
    @require_login
    def schedule(login, bot, update):
        """Get schedule. """
        chat_id = update.message.chat.id
        bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_PHOTO)
        data = login.schedule
        colorscale = [[0, '#4d004c'], [.5, '#f2e5ff'], [1, '#ffffff']]
        table = ff.create_table(data, colorscale=colorscale)
        table.layout.width = 230*7 + 230/2
        table.layout.height = 720
        for idx, elem in enumerate(table.layout.annotations):
            if idx < 7:
                elem.font.size = 24
            else:
                elem.font.size = 16
            elem.width = 230
            elem.align = 'center'
        image = BytesIO(py.image.get(table, format='png', scale=4))
        image.name = 'horario.png'
        image.seek(0)
        bot.send_photo(chat_id, photo=image)
