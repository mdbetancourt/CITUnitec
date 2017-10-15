# Copyright (c) 2017 akhail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""Base Model.

"""
import os
from os.path import join, expanduser

from peewee import Model, SqliteDatabase
from playhouse.db_url import connect

DATABASE_URL = os.environ.get('DATABASE_URL') or join(expanduser("~"), '.bot_database.db')
HEROKU = os.environ.get('HEROKU')

if HEROKU is not None:
    DATABASE = connect(DATABASE_URL)
else:
    DATABASE = SqliteDatabase(DATABASE_URL)

class BaseModel(Model):
    """BaseModel. """
    class Meta: # pylint: disable=R0903
        """Meta class. """
        database = DATABASE
