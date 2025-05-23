import sqlite3 as sql
import pandas as pd 


def cnx_and_query(query,database = 'database/gg.db'):
    cnx = sql.connect(database)
    data = pd.read_sql_query(query,con=cnx)
    cnx.close()
    return data


def get_list_of_managers():
    query = '''select * from users'''
    data = cnx_and_query(query)
    return data


#helper functions


def trophy_converter(placement):
    conv = {0:'🐴',1:'🥇',2:'🥈',3:'🥉'}
    if int(placement) in conv.keys():
        return conv[int(placement)]
    
def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

#User Metrics


def username_to_id_info(username:str): #->dict(list,pd.DataFrame)
    query = f'''select distinct user_id,roster_id,season,league_id from users where username = "{username}"'''
    data = cnx_and_query(query)
    user_id = data['user_id'].unique().tolist() #might break if the user id changes for someone year to year?
    roster_id = data[['roster_id','season','league_id']]
    return {'user_ids':user_id,'roster_ids':roster_id}


class user_info():
    def __init__(self,username):
        tmp_info = username_to_id_info(username)
        self.user_ids = tmp_info['user_ids']
        self.roster_ids = tmp_info['roster_ids']

        self.trophy_case = self.get_final_standings()

        self.results = self.results_history()
        self.results_by_season = self.results_by_season_helper(self.results)
        self.results_head_to_head = self.head_to_head_helper(self.results)
        self.total_wins, self.total_losses = self.total_helper(self.results)

        self.player_history = self.player_history_raw()
        self.favorite_players = self.favorite_player_helper(self.player_history)
        self.best_starts = self.best_starts_helper(self.player_history)
        self.oops = self.oops_should_have_started_helper(self.player_history)


    #trophy case

    def get_final_standings(self):
        query = f'''
                with tmp as (
                select fr.season,u.user_id,u.username, fr.result, 
                case when fr.result = max(fr.result) over (partition by fr.season) then 1 else 0 end as the_megan
                from final_results fr
                join users u on u.roster_id = fr.roster_id and u.league_id = fr.league_id
                where true
                group by 1,2,3
                order by fr.season desc, result asc)

                select *
                from tmp
                where user_id in ({",".join(self.user_ids)})
                '''
        data = cnx_and_query(query)
        data = data[['season','result','the_megan']]
        data['trophy'] = data.apply(lambda x: 0 if x['the_megan']==1 else x['result'],axis=1) #0 = megan, 1,2,3 = respective
        data['trophy'] = data['trophy'].apply(lambda x: x if x <4 else 'Null')
        return data


    #results and head to head data

    def results_history(self):
        query = f'''
                select
                league_id, 
                week, 
                season, 
                user_id_root, 
                username_root,
                user_id_challenger,
                username_challenger,
                points_root,
                points_challenger,
                case when points_root > points_challenger then 1 else 0 end as win_flag,
                points_root - points_challenger as delta
                from matchup
                where user_id_root in ({",".join(self.user_ids)})
                '''
        data = cnx_and_query(query)
        return data

    def results_by_season_helper(self,results_history:pd.DataFrame):
        agg = results_history.groupby('season')['win_flag'].agg(wins='sum',losses=lambda x: (x==0).sum())
        agg = agg.merge(self.trophy_case[['season','result','trophy']], left_index=True, right_on='season')
        return agg.sort_values('season',ascending=False).to_dict(orient='index')
    
    def head_to_head_helper(self,results_history:pd.DataFrame):
        agg = results_history.groupby('username_challenger')['win_flag'].agg(wins='sum',losses=lambda x: (x==0).sum(),lineage=lambda x: ''.join(x.astype(str)))
        return agg.sort_index(ascending=True).to_dict(orient='index')

    def total_helper(self,results_history:pd.DataFrame):
        agg = results_history.groupby('user_id_root')['win_flag'].agg(wins='sum',losses=lambda x: (x==0).sum())
        wins = sum(agg['wins'])
        losses = sum(agg['losses'])
        return wins,losses

    #player data - most starts, bench warmer game, 


    def player_history_raw(self):
        query = f'''
                select 
                season,
                name,
                position, 
                r.player_id, 
                espn_id,
                points, 
                is_starter,
                week
                from results r
                join (select player_id, 
                first_name || ' ' || last_name as name,
                fantasy_positions as position,
                espn_id
                from nfl_players
                )np
                on r.player_id = np.player_id
                where user_id in ({",".join(self.user_ids)})
                and espn_id is not Null
        '''
        data = cnx_and_query(query)
        return data


    def favorite_player_helper(self,player_history:pd.DataFrame):
        data = player_history.groupby(['name','espn_id'],as_index=False)['is_starter'].agg(tot='sum')
        return data.sort_values('tot',ascending=False).head(5)

    def best_starts_helper(self,player_history:pd.DataFrame):
        data = player_history[player_history['is_starter']==1][['name','espn_id','week','season','points']]
        return data.sort_values('points',ascending=False).head(5)
    
    def oops_should_have_started_helper(self,player_history:pd.DataFrame):
        data = player_history[player_history['is_starter']==0][['name','espn_id','week','season','points']]
        return data.sort_values('points',ascending=False).head(5)
    

if __name__ == '__main__':
    u = user_info('smlederer')
    print(u.results_by_season)
    print(u.results_head_to_head)
    print(u.trophy_case)
    print(len(u.trophy_case))