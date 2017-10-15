# Copyright (c) 2017 akhail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""Base Model.

"""

import os
from peewee import Model
from playhouse.db_url import connect

DATABASE_URL = os.environ.get('DATABASE_URL')

DATABASE = connect(DATABASE_URL)

class BaseModel(Model):
    """BaseModel. """
    class Meta: # pylint: disable=R0903
        """Meta class. """
        database = DATABASE
