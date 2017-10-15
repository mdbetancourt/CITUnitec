"""Api Unitec login.

"""

from robobrowser import RoboBrowser
from citu.model import Student

class Login(object):
    """Login in web.

    """
    WEB_PAGE = 'http://portal.unitec.edu.ve/'
    SUCCESS, ERROR_PASSWORD, ERROR_LOGIN = 0, -3, -2

    def __init__(self, student):
        assert isinstance(student, Student)
        self.student = student
        self._robo = RoboBrowser(parser='html5lib')
        self._state = Login.ERROR_LOGIN
        self._login = False

    def connect(self):
        """Connect to web. """
        if not self._login:
            self._robo.open(Login.WEB_PAGE)
            form = self._robo.get_forms()[1]
            form.fields['TID'].value = self.student.identity
            form.fields['TClave'].value = self.student.password
            self._robo.submit_form(form)
            self._state = int(self._robo.url[50:])
            self._login = True

    @property
    def state(self):
        """Return state of login."""
        self.connect()
        return self._state
