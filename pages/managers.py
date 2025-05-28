from fasthtml.common import *

import utils.db_utils as dbu

import pages.nav as n


def all_manager_page():
    raw_managers_data = dbu.get_list_of_managers()
    managers = raw_managers_data['username'].unique().tolist()
    page = Title('Greenwood Games - Managers'),Main(
    n.nav_bar('Managers'),
    Div(*[Card(Div(B(A(i,href=f'/managers/{i}',role='button')),style='text-align:center;font-size:24px;'),
    header='',        
    footer='',
    style='text-align:start;font-size:max(1rem,1vw)')
    for i in sorted(managers)]
    ,_class='grid'
    ,style='grid-template-columns:1fr 1fr 1fr 1fr')
    ,_class = 'container')
    return page



def personal_page(manager_name):

    data = dbu.user_info(manager_name)

    page = (Title(manager_name + ' - Greenwood Games'),
        #navigation
        Main(
        n.nav_bar(manager_name),
        
        #Trophy Case
        Div(H4('TROPHY CASE')),
        Div(*[Card(Div(dbu.trophy_converter(i['trophy']),style='font-size:3vw'),
                    header=Button(B(f"{i['season']}"),_class='contrast'),
                    style='width:fit-content;text-align:center;margin:5px;') for _,i in data.trophy_case.iterrows() if i['trophy'] != 'Null']
                    ,_class='box',style='display:flex;justify-content:center;height:175px;'),
        #Div('tmp',id='trophy_case',style = 'width:fill;height:100px;background-color:#3e1c00;color:black;'),

        Div(H4('RESULTS BY SEASON'+f" | {data.total_wins}W - {data.total_losses}L")),
        #Results By Season
        Div(*[Card(H4(f"{i[1]['wins']}-{i[1]['losses']}")
                        ,header=Button(B(f"{i[1]['season']}"),_class='contrast')
                        ,footer=f"{dbu.ordinal(i[1]['result'])}"
                        ,style='width:100px;margin:5px;')
                    for i in data.results_by_season.items()],_class='box',style='display:flex;padding:5px;justify-content:center;text-align:center;'),

        #Manager Head to Head
        Div(H4('MANAGER HEAD TO HEAD')),
        Div(*[Card(Div(B(f'{i[1]["wins"]}-{i[1]["losses"]}'),style='text-align:center;font-size:24px;'),
                    header=Div(B(A(i[0],_class='secondary',href='/managers/'+str(i[0]))),style='text-align:center;font-size:clamp(1rem, 1vw, 2rem)',role='button',_class='outline'),
                    footer= Div(f'{(i[1]["lineage"]).replace("1","🟩").replace("0","🟥")}',
                                style='text-align:start;font-size:max(1rem,1vw)'))
                    for i in data.results_head_to_head.items()]
                    ,_class='grid'
                    ,style='grid-template-columns:1fr 1fr 1fr 1fr'),

        #Div('tmp',id='results_graph',style = 'width:fill;height:300px;background-color:white;color:black;'),





        #Favorite Players
        Div(H4('FAVORITE PLAYERS')),
        Div(*[Card(Img(src=f'https://a.espncdn.com/i/headshots/nfl/players/full/{int(i["espn_id"])}.png'),header=B(i['name']),footer=f'{i["tot"]} Starts',style='text-align:center;font-size:clamp(1rem, 1vw, 2rem)') for _,i in data.favorite_players.iterrows()],_class='grid',style='overflow-x:auto;'),
            
        #Best Starts
        Div(H4('BEST STARTS')),
        Div(*[Card(Img(src=f'https://a.espncdn.com/i/headshots/nfl/players/full/{int(i["espn_id"])}.png'),header=B(i['name']),footer=f'{i["season"]}, Week {i["week"]}: {i["points"]}',style='text-align:center;font-size:clamp(1rem, 1vw, 2rem)') for _,i in data.best_starts.iterrows()],_class='grid',style='overflow-x:auto;'),


        #Oops I should have Started
        Div(H4('OOPS SHOULD HAVE STARTED...')),
        Div(*[Card(Img(src=f'https://a.espncdn.com/i/headshots/nfl/players/full/{int(i["espn_id"])}.png'),header=B(i['name']),footer=f'{i["season"]}, Week {i["week"]}: {i["points"]}',style='text-align:center;font-size:clamp(1rem, 1vw, 2rem)') for _,i in data.oops.iterrows()],_class='grid',style='overflow-x:auto;'),




        #Div(*[Button('t'*(i+1),_class = 'contrast', style = 'width:20%;') for i in range(15)],_class = 'grid-container'),




        _class = 'container')
        
        
        )
    return page


if __name__ == '__main__':
    print(all_manager_page())