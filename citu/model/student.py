# Copyright (c) 2017 akhail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from peewee import CharField
from .base import BaseModel

class Student(BaseModel):
    username = CharField(unique=True)
    identity = CharField(unique=True)
    password = CharField()
