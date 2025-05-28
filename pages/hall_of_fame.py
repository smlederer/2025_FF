from fasthtml.common import *

import utils.db_utils as dbu

import pages.nav as n


def hof():
    page = Title('Greenwood Games - Hall of Fame'),Main(
    n.nav_bar('Hall of Fame'),'coming soon',_class = 'container')

    return page