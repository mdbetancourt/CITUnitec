"""Api Unitec login.

"""

from robobrowser import RoboBrowser
from citu.model import Student

class Login(object):
    """Login in web.

    """
    INTRANET = 'http://www.unitec.edu.ve/'
    CODES = INTRANET + 'inscripcion.jsp?jspContenido=codigopreinscripcion/vercodigo.jsp'
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
    def codes(self):
        """Return codes. """
        self.connect()
        self._robo.open(Login.CODES)
        codes = self._robo.find_all('table', attrs={'class':'contenido'}) # pylint: disable=E1102
        tables = {}
        for table in codes:
            _cod = table.find('td', attrs={'align':'center'}).text
            _subject = map(lambda x: x.text, table.find_all('li'))
            tables[_cod] = list(_subject)
        return tables

    @property
    def state(self):
        """Return state of login."""
        self.connect()
        return self._state
