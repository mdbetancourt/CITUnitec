#!/usr/bin/env python
#
# Copyright (c) 2017 akhail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""Main app.

"""

import os
import sys
import logging

from telegram.ext import Updater

sys.path.append(".")

from citu.handlers import HANDLERS # pylint: disable=C0413

TOKEN = os.environ.get('TELEGRAM_TOKEN')
PORT = int(os.environ.get('PORT', '5000'))
ENV = os.environ.get('HEROKU', None)

logging.basicConfig(format="%(message)s", level=logging.INFO)

def error(_, update, err):
    """Error handler function. """
    logger = logging.getLogger(__name__)
    logger.warning(f'Update "{update}" caused error "{err}"')

def main():
    """Main app. """
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    for handler in HANDLERS:
        dispatcher.add_handler(handler)

    dispatcher.add_error_handler(error)

    if ENV is not None:
        updater.start_webhook(listen='0.0.0.0',
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook('https://cit-unitec.herokuapp.com/' + TOKEN)
    else:
        updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
