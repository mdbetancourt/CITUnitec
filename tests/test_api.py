# Copyright (c) 2017 Michel Betancourt
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os

import pytest

from citu.api import Login
from citu.model import Student

USER, PASSWORD = os.environ.get("SAMPLE_LOGIN").split(":")


@pytest.mark.parametrize("user,password,code", [
    (1245855, 234223, Login.ERROR_LOGIN),
    (USER, 123123, Login.ERROR_PASSWORD),
    (USER, PASSWORD, Login.SUCCESS)
])
def test_login_state(user, password, code):
    login = Login(Student(username=None, identity=user, password=password))

    assert login.state == code
