from fasthtml.common import *
#import pandas as pd

#internal utils
import utils.db_utils as dbu


app, rt = fast_app(live=True)

manager_name = 'smlederer'
managers = dbu.get_list_of_managers()['username'].unique().tolist()



@rt('/')
def get():
    return A('smlederer',href='managers/smlederer')

@rt('/managers/{manager_name}')
def get(manager_name:str):

    #load data
    data = dbu.user_info(manager_name)

    page = (Title(manager_name + ' - Greenwood Games'),
        #navigation
        Main(
        Nav(Ul(Li(Select(*[Option(manager_name,selected=True)]+[Option(i) for i in managers if i != manager_name]))),
            Ul(Li(Button('HOME')),
               Li(Button('HALL OF FAME')),
               Li(Button('MANAGERS')),
               Li(Button('LEAGUE HISTORY')))
            
            ),
        
        #Trophy Case
        Div(H4('TROPHY CASE')),
        Div(*[Card('🥇',footer='2021',style='width:fit-content;text-align:center;margin:5px;') for i in range(4)],_class='box',style='display:flex;justify-content:center;'),
        #Div('tmp',id='trophy_case',style = 'width:fill;height:100px;background-color:#3e1c00;color:black;'),

        Div(H4('RESULTS BY SEASON V2')),
        #Results By Season
        Div(*[Card(H4(f"{i[1]['wins']}-{i[1]['losses']}")
                     ,header=Button(B(f"{i[0]}"),_class='contrast')
                     ,footer=f"{'3rd'}"
                     ,style='width:100px;margin:5px;')
                  for i in data.results_by_season.items()],_class='box',style='display:flex;padding:5px;justify-content:center;'),


        # Div(H4('RESULTS BY SEASON V1')),
        # #Reuslts by season v1
        # Nav(
        #     Ul(
        #         Li(
        #         Div(*[Button(B(f"{i[0]}"),f" | {i[1]['wins']}-{i[1]['losses']}",
        #              hx_post=f"/managers/{manager_name}/results_by_season/{i[0]}",
        #              hx_target="#results_graph",
        #              hx_swap='innerHTML',
        #              id=f'results_by_season_button',
        #              _class = 'contrast',
        #              style = 'font-size:min(1.5vw,32px);') 
        #              for i in data.results_by_season.items()],style = 'overflow-x:auto;white-space:nowrap;')),
        
        
        # Li(Button('Go To Season',_class='outline'))
        # )),


        #Div(data.results,id='results_graph',style = 'width:fill;height:300px;background-color:white;color:black;'),

        #Manager Head to Head
        Div(H4('MANAGER HEAD TO HEAD')),
        Div(*[Card(Div(A(i[0],_class='secondary',href='/managers/'+str(i[0])),style='text-align:center;font-size:1.5vw;',role='button',_class='outline')
                   ,footer=Div(Div(f'{i[1]["wins"]}-{i[1]["losses"]}',style='text-align:center;font-size:2vw;'),
                            Div(f'{("W"*i[1]["wins"]+"L"*i[1]["losses"]).replace("W","🟩").replace("L","🟥")}',
                                style='text-align:start;font-size:1.5vw'),_class='grid',style='grid-template-columns:1fr 3fr')) 
                   for i in data.results_head_to_head.items()]
                   ,_class='grid'
                   ,style='grid-template-columns:1fr 1fr 1fr 1fr'),

        #Div('tmp',id='results_graph',style = 'width:fill;height:300px;background-color:white;color:black;'),





        #Favorite Players
        Div(H4('FAVORITE PLAYERS')),
        Div(*[Card(Img(src=f'https://a.espncdn.com/i/headshots/nfl/players/full/{int(i["espn_id"])}.png'),header=i['name'],footer=f'{i["tot"]} Starts') for _,i in data.favorite_players.iterrows()],_class='grid',style='overflow-x:auto;'),
            
        #Best Starts
        Div(H4('BEST STARTS')),
        Div(*[Card(Img(src=f'https://a.espncdn.com/i/headshots/nfl/players/full/{int(i["espn_id"])}.png'),header=i['name'],footer=f'{i["season"]}, Week {i["week"]}: {i["points"]}') for _,i in data.best_starts.iterrows()],_class='grid',style='overflow-x:auto;'),


        #Oops I should have Started
        Div(H4('OOPS SHOULD HAVE STARTED...')),
        Div(*[Card(Img(src=f'https://a.espncdn.com/i/headshots/nfl/players/full/{int(i["espn_id"])}.png'),header=i['name'],footer=f'{i["season"]}, Week {i["week"]}: {i["points"]}') for _,i in data.oops.iterrows()],_class='grid',style='overflow-x:auto;'),




        #Div(*[Button('t'*(i+1),_class = 'contrast', style = 'width:20%;') for i in range(15)],_class = 'grid-container'),




        _class = 'container')
        
        
        )

    return page


@rt('/managers/{manager_name}/results_by_season/{season}')
def post(manager_name:str,season:int):
    
    return 


@rt('/managers/{player_name}/head_to_head/{name}')
def post(player_name:str,name:str):
    print(player_name + ' ' + name)
    #return player_name + ' ' + manager




if __name__ == '__main__':
    serve(port=6429)



        #     Div(Nav(
        #         Ul(*[Li(
        #             Button(o.upper(),hx_post=f'/navlist/{o}',hx_target = '#content',hx_swap = 'innerHTML',style=f.button_style())
        #             ) for o in ['Managers','League History']],Li(A(Button('Hall of Fame'.upper(),style=f.button_style()),href='/hof')))
        #             )) ,style='width:80%;margin-left:10%;display:flex;justify-content:center;')
        #     ,Div(P(f'''{f.get_tzu().upper()}''',
        #            style='text-align:center;font-size:24px;font-family: "Times New Roman", Times, serif;font-style: italic;'),
        #            P(NotStr(''' Sun Hoe Tzu, <i><a href='https://www.amazon.com/Fantasy-Football-Dummies-Martin-Signore/dp/0470125071'>The Art of Fantasy Football</a></i>'''),
        #              style='text-align:center;font-family: "Times New Roman", Times, serif;')
        #          ,style='width:80%;margin-left:10%;padding:10px 0px 10px 10px;border-radius:20px;',id='content')
        # )
