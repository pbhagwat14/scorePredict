# write your import here

import pandas as pd

class MyModel:
    ground_avg = {}
    stad_list=['Chidambaram', 'Narendra Modi', 
               'Chinnaswamy', 'Arun Jaitley', 
               'Sawai Mansingh', 'Wankhede', 
               'Eden', 'Rajiv Gandhi', 
               'Punjab Cricket Association IS Bindra',
               'Himachal Pradesh Cricket Association',
               'Ekana']
    
    wk_dev = [ 12, 6, 4, -4, -10, -12, -15, -18, -21, -25, -30]
    
    
    def __init__(self):
        MyModel.ground_avg['Ekana'] = 43
        
        
    
    def fit(self,training_data):
        df_bb = training_data[0]
        df_mr = training_data[1]
        
        grouped_ID = df_mr.groupby('Venue')['ID'].apply(list).reset_index(name='IDs')
        
        team_names = ['CSK', 'GT', 'RCB', 'DC','RR','MI','KKR','SRH','PK','PKX']
        team_venues = [['MA Chidambaram Stadium', 'MA Chidambaram Stadium, Chepauk, Chennai'],
                ['Narendra Modi Stadium, Ahmedabad'] ,
                ['M.Chinnaswamy Stadium'],
                ['Arun Jaitley Stadium','Arun Jaitley Stadium, Delhi'],
                ['Sawai Mansingh Stadium'],
                ['Wankhede Stadium, Mumbai'],              
                ['Eden Gardens, Kolkata', 'Eden Gardens'],
                ['Rajiv Gandhi International Stadium'],
                ['Punjab Cricket Association IS Bindra Stadium', 
                  'Punjab Cricket Association IS Bindra Stadium, Mohali'],
                ['Himachal Pradesh Cricket Association Stadium']]
        team_dict = {}
        all_lists = []
        for i, team in enumerate(team_names):
            venues = team_venues[i]
            id_list = []
            for venue in venues:
                id_list.extend(grouped_ID.loc[grouped_ID['Venue'] == venue, 'IDs'].iloc[0])
            all_lists.append(id_list)
            team_dict[team] = all_lists[i]
        
                
        for i in range(10):
            id_list = all_lists[i]
            filtered_df_bb = df_bb[(df_bb['ID'].isin(id_list)) & (df_bb['overs'] <= 5)]
            sum_cols=['total_run']
            grouped_df = filtered_df_bb.groupby(['ID', 'innings'])[sum_cols].agg(['sum', 'count'])
            grouped_df.columns = [f'{col[0]}_{col[1]}' for col in grouped_df.columns]
            avg_runs = grouped_df.loc[grouped_df['total_run_count'] > 35, 'total_run_sum'].median()
            MyModel.ground_avg[MyModel.stad_list[i]] =round(avg_runs)
    
    def predict(self,test_data):
        pred=[]
        
        v = test_data['venue'].iloc[0]
        
        for i in range(11):
            if MyModel.stad_list[i].lower() in v.lower():
                pred_score = MyModel.ground_avg[MyModel.stad_list[i]]
                break
        
        v1 = test_data['batsmen'].iloc[0]
        total_wk_1 = len(v1.split(',')) - 2
        pred_score_1 = pred_score + MyModel.wk_dev[total_wk_1]
        pred.append(pred_score_1)
        
        v2 = test_data['batsmen'].iloc[1]
        total_wk_2 = len(v2.split(',')) - 2
        pred_score_2 = pred_score + MyModel.wk_dev[total_wk_2]
        pred.append(pred_score_2)
        
        return pred
        