from fasthtml.common import *

def nav_bar(title):
    nav_bar = Nav(Ul(Li(H1(title))),
                Ul(Li(A('HOME',role = 'button',href='/')),
                    Li(A('MANAGERS',role = 'button',href='/managers')),
                    Li(A('LEAGUE HISTORY',role = 'button')),
                    Li(A('HALL OF FAME',role = 'button')))
                
                )
    return nav_bar