"""Api Unitec login.

"""

from robobrowser import RoboBrowser

class Login(object):
    """Login in web.

    """
    WEB_PAGE = 'http://portal.unitec.edu.ve/'
    SUCCESS, ERROR_PASSWORD, ERROR_LOGIN = 0, -3, -2

    def __init__(self, user, password):
        self.user, self.password = user, password
        self._robo = RoboBrowser(parser='html5lib')
        self._robo.open(Login.WEB_PAGE)
        form = self._robo.get_forms()[1]
        form.fields['TID'].value = user
        form.fields['TClave'].value = password
        self._robo.submit_form(form)
        self._state = int(self._robo.url[50:])


    @property
    def state(self):
        """Return state of login."""
        return self._state
