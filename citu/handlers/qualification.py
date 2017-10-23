from math import sqrt

from telegram import ParseMode
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, RegexHandler

from citu.handlers.utils import require_login, cancel_handler

PERIOD, RESULT = range(2)


# noinspection PyUnusedLocal
class Qualification(ConversationHandler):
    def __init__(self):
        super().__init__(
            entry_points=[CommandHandler('notas', self.entry)],
            states={
                PERIOD: [RegexHandler(r'Guacara$', self.period)],
                RESULT: [RegexHandler(r'^PDG-', self.result)]
            },
            fallbacks=[CommandHandler('cancel', cancel_handler)]
        )
        self._programs = None
        self._periods = None
        self.login = None

    @require_login
    def entry(self, bot, update, login):
        self.login = login
        chat_id = update.message.chat.id
        username = update.message.from_user.username
        self._programs = self.login.qualification_program()
        if len(self._programs) == 1:
            self._programs = list(self._programs)[0]
            return self.period(bot, update)

        bot.send_message(chat_id, f"@{username} selecciona tu programa estudiantil",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[[
                                 KeyboardButton(text)
                                 for text in self._programs
                             ]],
                             selective=True
                         ))
        return PERIOD

    @require_login
    def period(self, bot, update, login):
        chat_id = update.message.chat.id
        username = update.message.from_user.username
        self._programs = self._programs or update.message.text
        self._periods = self.login.qualification_period(self._programs)
        self._periods = list(self._periods)[:9]
        num = int(sqrt(len(self._periods)))
        keyboard = [[]]
        idx = 0
        for period in self._periods:
            if idx > num:
                idx = 0
                keyboard.append([])
            keyboard[-1].append(KeyboardButton(period))
            idx += 1

        bot.send_message(chat_id, f"@{username} selecciona tu periodo",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=keyboard,
                             selective=True
                         ))
        return RESULT

    @require_login
    def result(self, bot, update, login):
        username = update.message.from_user.username
        chat_id = update.message.chat.id
        self._periods = update.message.text
        qualification = self.login.qualification(self._programs, self._periods)

        text = f"@{username} tus notas del trimestre {self._periods} son:\n"
        for subject, value in qualification.items():
            text += f"<b>{subject}</b>\n"
            for cort, note in value.items():
                text += f"<b>-</b>    {cort}: <b>{note}</b>\n"
            text += "\n"

        bot.send_message(chat_id, text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
