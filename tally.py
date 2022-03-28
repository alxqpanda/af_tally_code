import pandas as pd
import glob

# helper class for tally()
# inputs:
#       (str) wk : name of local csv file to read data from
#       (str) t1 : first letter of team 1
#       (str) t2 : first letter of team 2
# purpose:
#       reads in a specified .csv file, cleans the data, and returns
#       two pandas dataframe
# returns:
#       (DataFrame) t1df : DataFrame containing all attacks made by team 1
#       (DataFrame) t2df : DataFrame containing all attacks made by team 2
def clean_csv(wk, t1, t2):
    # reading in csv, removing header
    week = pd.read_csv(wk, header=[3])
    week.columns = week.columns.str.lower()
    
    # removing unnecessary columns and empty rows
    week = week[week.columns[2:8]]
    week = week[week['points'] > 0]
    
    # lowercase and remove whitespace in the str columns
    week['attacker'] = week['attacker'].str.lower().str.replace(' ', '')
    week['opponent'] = week['opponent'].str.lower().str.replace(' ', '')
    week['a.team'] = week['a.team'].str.lower().str.replace(' ', '')
    week['o.team'] = week['o.team'].str.lower().str.replace(' ', '')
    
    # split into the two teams
    t1df = week.groupby('a.team').get_group(t1).reset_index(drop = True)
    t2df = week.groupby('a.team').get_group(t2).reset_index(drop = True)
    
    return t1df, t2df

# helper class for tally()
# inputs:
#       (DataFrame) df : team data on attacks (points, name, links, etc.)
#       (bool) flag : shows only the top 5 rows of data
# purpose:
#       using the given team data, sorts the information based on the following:
#             1. most points per person
#             2. most attacks per person
#             3. highest scored attacks
#       and prints out a summary of the information
# returns:
#       none
def summarize(df, flag):
    # get top five highest overall scorers
    most_points = df.groupby('attacker')['points'].sum().sort_values(ascending = False)
    if flag:
        most_points = most_points.head(5)
    
    # get top five most attack counts
    most_attacks = df.groupby('attacker')['attacker'].count().sort_values(ascending = False)
    if flag:
        most_attacks = most_attacks.head(5)
    
    # get top five highest scoring attacks
    highest_attacks = df.sort_values(by = 'points', ascending = False).reset_index(drop = True)
    if flag:
        highest_attacks = highest_attacks[0:5]
    highest_attacks = highest_attacks[['attacker', 'points', 'link']].to_string()
    
    # print out values
    print("\nTEAM", df['a.team'][0].upper(), "\n")
    print("most points: \n", most_points, "\n")
    print("most attacks: \n", most_attacks, "\n")
    print("highest points: \n", highest_attacks)

# main function
# inputs:
#       none
# purpose:
#       asks for the team letters and tally types to print out a summary
#       on attacks created during the event
# returns:
#       none
def tally():
    # get all csvs in current folder
    csv_list = glob.glob('*.csv')
    
    # choose team names
    t1 = str(input("First letter of Team 1: "))
    t2 = str(input("First letter of Team 2: "))
    
    # set team dataframes
    t1df = pd.DataFrame()
    t2df = pd.DataFrame()
    
    # if we want a weekly or overall tally
    flag = bool(int(input("Print weekly or overall tally? 1 (weekly) or 0 (overall) ")))
    
    # clean and split scoring sheet based on weekly or overall summary
    if flag: # weekly summary
        wk = (int(input("Choose from Week 1 to " + str(len(csv_list)) + ": "))) - 1
        t1df, t2df = clean_csv(csv_list[wk], t1, t2)
    else: # overall summary
        for wk in csv_list:
            wk_t1df, wk_t2df = clean_csv(wk, t1, t2)
            temp = pd.concat([wk_t1df, t1df])
            t1df = pd.DataFrame(temp)
            temp = pd.concat([wk_t2df, t2df])
            t2df = pd.DataFrame(temp)
    
    # if we want all of the data rather than the top 5
    flag = bool(int(input("Only show top 5? 1 (Yes) or 0 (No) ")))
    
    # create summaries for each team
    summarize(t1df.reset_index(drop = True), flag)
    summarize(t2df.reset_index(drop = True), flag)
