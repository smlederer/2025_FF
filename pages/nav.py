from fasthtml.common import *

def nav_bar(title):
    nav_bar = Nav(Ul(Li(H1(title))),
                Ul(Li(A('HOME',role = 'button',href='/')),
                    Li(A('MANAGERS',role = 'button',href='/managers')),
                    Li(A('LEAGUE HISTORY',role = 'button',href='/league-history')),
                    Li(A('HALL OF FAME',role = 'button',href='/hall-of-fame')))
                
                )
    return nav_bar


def home_nav_bar():
    nav_bar = Nav(
                Ul(
                    Li(A('MANAGERS',role = 'button',href='/managers')),
                    Li(A('LEAGUE HISTORY',role = 'button')),
                    Li(A('HALL OF FAME',role = 'button')))
                ,style='justify-content:center;'
                )
    return nav_bar