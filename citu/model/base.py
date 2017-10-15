# Copyright (c) 2017 akhail
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import os
from peewee import Model, PostgresqlDatabase

PATH = os.path.join(os.path.expanduser("~"), 'database.db')
DATABASE_URL = os.environ.get('DATABASE_URL') or PATH

DATABASE = PostgresqlDatabase(DATABASE_URL)

class BaseModel(Model):
    """BaseModel. """
    class Meta:
        """Meta class. """
        database = DATABASE
