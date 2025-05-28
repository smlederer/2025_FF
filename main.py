from fasthtml.common import *
#import pandas as pd

#internal utils
import utils.db_utils as dbu

import pages.managers as m
import pages.homepage as h
import pages.league_history as lh
import pages.hall_of_fame as hof
import pages.nav as n


app, rt = fast_app(live=True)

#homepage
@rt('/')
def get():
    return h.render()

#managers
@rt('/managers')
def get():
    return m.all_manager_page()

@rt('/managers/{manager_name}')
def get(manager_name:str):
    return m.personal_page(manager_name)

@rt('/league-history')
def get():
    return lh.league_history_landing()

@rt('/hall-of-fame')
def get():
    return hof.hof()

if __name__ == '__main__':
    serve(port=8080)