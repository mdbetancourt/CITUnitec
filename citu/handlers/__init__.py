# Copyright (c) 2017 akhail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""All handlers of bot

"""

from .login import ConversationLogin, HandlerLogout

HANDLERS = [
    ConversationLogin(),
    HandlerLogout()
]