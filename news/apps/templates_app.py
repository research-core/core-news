from confapp import conf
from pyforms_web.widgets.django import ModelAdminWidget

from news.models import Template

class TemplatesApp(ModelAdminWidget):

    UID   = 'templates'
    TITLE = 'Templates'
    MODEL = Template

    SEARCH_FIELDS = ['name__icontains']
    LIST_DISPLAY = ['name']

    FIELDSETS = ['name', 'code']

    ########################################################
    #### ORQUESTRA CONFIGURATION ###########################
    ########################################################
    LAYOUT_POSITION      = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU       = 'left>MessagesApp'
    ORQUESTRA_MENU_ORDER = 0
    ORQUESTRA_MENU_ICON  = 'flag checkered'
    ########################################################