# Copyright (c) 2017 akhail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""All handlers of bot

"""

from .login import ConversationLogin, HandlerLogout
from .precode import PreCodeSubjects
from .qualification import Qualification
from .schedule import ScheduleHandler

HANDLERS = [
    ConversationLogin(),
    HandlerLogout(),
    PreCodeSubjects(),
    ScheduleHandler(),
    Qualification()
]
