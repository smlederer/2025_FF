from fasthtml.common import *
import os

import pages.nav as n

dirname = os.path.dirname(os.path.dirname(__file__)) #2025_FF
img_path = os.path.join(dirname,'assets/logo.png')


def render():
    page = Main(Div(Title('Greenwood Games'),
            n.nav_bar('Greenwood Games'),
            Div(A(Img(src=img_path,style='width:200px;height:200px'),href='/') ,style='text-align:center;'),
            _class = 'container'))

    return page
