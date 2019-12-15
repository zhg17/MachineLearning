import pandas as pd
raw_data = pd.read_csv('data.csv',sep = ",")

raw_data.dropna(how="any", axis = 0, inplace = True)
raw_data = raw_data.reset_index()

#remove all columns that contain data about each fighters previous opponents
opponents_col = []

for column in raw_data: 
    if 'opp' in column:
        opponents_col.append(column)

raw_data.drop(opponents_col, axis=1, inplace = True)


#no need to track the subtype of decision victories
red_list = ['R_win_by_Decision_Majority', 'R_win_by_Decision_Split','R_win_by_Decision_Unanimous']
blue_list = ['B_win_by_Decision_Majority', 'B_win_by_Decision_Split','B_win_by_Decision_Unanimous']

raw_data['R_win_by_Decision'] = raw_data[red_list].sum(axis=1)
raw_data['B_win_by_Decision'] = raw_data[blue_list].sum(axis=1)

raw_data.drop(red_list, axis=1, inplace = True)
raw_data.drop(blue_list, axis=1, inplace = True)

#remove the column 'number of rounds', we are predicting based on past data, not current data
raw_data.drop(['no_of_rounds'], axis=1, inplace = True)

#total rounds fought and total time fought both essentially measure the same feature
raw_data.drop(['B_total_time_fought(seconds)', 'R_total_time_fought(seconds)'], axis=1, inplace = True)

#idk wether to remove these or not
#PASS is no. times the guard was passed, REV is the no. of Reversals landed (seem like too specific stats)
to_remove = ['R_avg_PASS', 'B_avg_PASS', 'R_avg_REV', 'B_avg_REV']

#significant strikes landed and attempted are further broken down into subcategories by
#body part : BODY, LEG, HEAD and distance: CLINCH, GROUND, DISTANCE
#I think that this is unnecessary

to_remove.extend([
    'B_avg_BODY_att', 'B_avg_BODY_landed','R_avg_BODY_att', 'R_avg_BODY_landed',
    'B_avg_LEG_att', 'B_avg_LEG_landed', 'R_avg_LEG_att', 'R_avg_LEG_landed',
    'B_avg_HEAD_att', 'B_avg_HEAD_landed', 'R_avg_HEAD_att', 'R_avg_HEAD_landed'
    ])

to_remove.extend([
    'B_avg_CLINCH_att', 'B_avg_CLINCH_landed','R_avg_CLINCH_att', 'R_avg_CLINCH_landed',
    'B_avg_GROUND_att', 'B_avg_GROUND_landed', 'R_avg_GROUND_att', 'R_avg_GROUND_landed',
    'B_avg_DISTANCE_att', 'B_avg_DISTANCE_landed', 'R_avg_DISTANCE_att', 'R_avg_DISTANCE_landed'
    ])

raw_data.drop(to_remove, axis=1, inplace = True)

#create new column for average total strikes percentage landed
blue_total_att = raw_data['B_avg_TOTAL_STR_att']
blue_total_landed = raw_data['B_avg_TOTAL_STR_landed']
red_total_att = raw_data['R_avg_TOTAL_STR_att']
red_total_landed = raw_data['R_avg_TOTAL_STR_landed']
blue_total_pct = []
red_total_pct = []

for i in range(len(blue_total_att)):
    att = blue_total_att[i]
    landed = blue_total_landed[i]
    if (att == 0):
        blue_total_pct.append(0)
    else:
        blue_total_pct.append(landed / att)

for i in range(len(red_total_att)):
    att = red_total_att[i]
    landed = red_total_landed[i]
    if (att == 0):
        red_total_pct.append(0)
    else:
        red_total_pct.append(landed / att)

raw_data['B_avg_TOTAL_STR_pct'] = blue_total_pct
raw_data['R_avg_TOTAL_STR_pct'] = red_total_pct

#check
print(raw_data)
for column in raw_data:
    print(column)
