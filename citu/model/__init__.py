# Copyright (c) 2017 akhail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import peewee

from .base import DATABASE
from .student import Student

DATABASE.connect()
try:
    DATABASE.create_tables([
        Student
    ])
except peewee.OperationalError:
    pass
