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

        self.results = self.results_history()
        self.results_by_season = self.results_by_season_helper(self.results)
        self.results_head_to_head = self.head_to_head_helper(self.results)

        self.player_history = self.player_history_raw()
        self.favorite_players = self.favorite_player_helper(self.player_history)
        self.best_starts = self.best_starts_helper(self.player_history)
        self.oops = self.oops_should_have_started_helper(self.player_history)

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
        return agg.sort_index(ascending=False).to_dict(orient='index')
    
    def head_to_head_helper(self,results_history:pd.DataFrame):
        agg = results_history.groupby('username_challenger')['win_flag'].agg(wins='sum',losses=lambda x: (x==0).sum())
        return agg.sort_index(ascending=True).to_dict(orient='index')


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
    print(u.player_history)
    print(u.favorite_players)