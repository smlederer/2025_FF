from fasthtml.common import *

import pages.nav as n

def render():
    page = Main(Div(Title('Greenwood Games'),
            n.nav_bar('Greenwood Games'),
            Div(A(Img(src='assets/logo.png',style='width:200px;height:200px'),href='/') ,style='text-align:center;'),
            _class = 'container'))

    return page
