from fasthtml.common import *
import random

import pages.nav as n

quotes = 'database/sun_hoe_tzu.txt'

#images
logo= 'assets/logo.png'
sun= 'assets/sunhow.png'



def read_tzu(path):
    with open(path) as o:
        quotes = o.readlines()
    return random.choice([quotes[0]])

def render():

    page = Title('Greenwood Games'),Main(Div(
            Div(A(Img(src=logo,style='width:20%'),href='/') ,style='text-align:center;'),
            n.home_nav_bar(),
            Div(Img(src=sun,_style='height:fill;border-radius: 20px;'),Div(I(Div(read_tzu(quotes),style='text-align:left;font-size:50px;margin:auto;'),
                                   I(Div(B('- Sun Hoe Tzu'),
                                         ' , ',
                                         A('The Art of Fantasy Football',href = 'https://www.amazon.com/Fantasy-Football-Dummies-Martin-Signore/dp/0470125071')
                                         ,style='text-align:left;font-size:30px')))
                                         ,style='margin-top: 20px;margin-left:20px;')
                                         ,_class='grid',
                style='''grid-template-columns:1fr 3fr;  background-color: #1e1e1e;color: white;padding: 20px 30px;
  margin-top: 20px;
  border-radius: 50px;
  font-family: 'Georgia', serif;
  font-size: 1.2em;
  line-height: 1.6;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);'''),
            _class = 'container'))

    return page



if __name__ =='__main__':
    print(read_tzu(quotes))