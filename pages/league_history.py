from fasthtml.common import *

import utils.db_utils as dbu

import pages.nav as n


def league_history_landing():
    page = Title('Greenwood Games - League History'),Main(
    n.nav_bar('League History'),'coming soon',_class = 'container')

    return page