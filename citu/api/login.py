"""Api Unitec login.

"""
import re
from robobrowser import RoboBrowser
from citu.model import Student

class Login(object):
    """Login in web.

    """
    INTRANET = 'http://www.unitec.edu.ve/'
    CODES = INTRANET + 'inscripcion.jsp?jspContenido=codigopreinscripcion/vercodigo.jsp'
    SCHEDULE = INTRANET + 'horario.jsp?jspContenido=horarios/horariopersonal.jsp'

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
    def schedule(self):
        """schedule from unitec. """
        self.connect()
        self._robo.open(Login.SCHEDULE)
        _schedule = self._robo.select('table.contenido') # pylint: disable=E1102
        _schedule = _schedule[0].select('tr') # get first unique element and list row

        sched = [[
            'Hora', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'
        ]]

        # Capture the schedule class in a pretty format
        for table_row in _schedule[1:]: # [1:] ignore header Lun, Mar..
            sched.append([])

            for idx_column, col in enumerate(table_row.select('td')): # get column
                sel = col.select_one('span')
                if sel is not None:
                    if idx_column == 0: # get hours
                        init, end = sel.text.strip().split(' a  ')
                        text = init + '<br>' + end
                        sched[-1].append(text)

                    else:
                        _class, _, room = sel.contents # class, br, room
                        _class = re.search(r'((?!\: ).)+$', _class.strip())
                        _class = _class.group().strip()

                        room = re.search(r'(.(?!Seccion))+', room.text)
                        room = room.group().strip()

                        room = re.sub(r'- ', ' - ', room)
                        sched[-1].append(_class + '<br>' + room)
                else:
                    sched[-1].append('')
        return sched

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
