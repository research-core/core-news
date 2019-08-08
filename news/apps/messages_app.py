from confapp import conf
from pyforms_web.widgets.django import ModelAdminWidget

from news.models import Message

class MessagesApp(ModelAdminWidget):

    UID   = 'messages'
    TITLE = 'Messages'
    MODEL = Message

    SEARCH_FIELDS = ['name__icontains']

    LIST_FILTER = ['subject', 'is_event', 'publish_start', 'publish_end']

    LIST_HEADERS = ['Subject', 'Order', 'Name', 'Is an event', 'Publish start', 'Publish end']
    LIST_DISPLAY = ['subject', 'order', 'name', 'is_event', 'publish_start', 'publish_end']

    FIELDSETS = [
        ('is_event', 'publish_start', 'publish_end', 'order'),
        'subject',
        ('name', 'date'),
        'image',
        'text',
        'location',
        'start',
        'end',
        'mailing_lists',
    ]


    ########################################################
    #### ORQUESTRA CONFIGURATION ###########################
    ########################################################
    LAYOUT_POSITION      = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU       = 'left'
    ORQUESTRA_MENU_ORDER = 0
    ORQUESTRA_MENU_ICON  = 'sticky note outline'
    ########################################################