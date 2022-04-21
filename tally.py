import pandas as pd
import glob

# helper methods for summarize()
# calculates information based on certain criteria
def most_points(df):
    return df.groupby('attacker')['points'].sum().sort_values(ascending = False)

def most_attacks(df):
    return df.groupby('attacker')['attacker'].count().sort_values(ascending = False)

def highest_scores(df):
    return df.sort_values(by = 'points', ascending = False).reset_index(drop = True)

def most_targeted(df):
    return df.groupby('opponent')['opponent'].count().sort_values(ascending = False)

def print_sum(ateam, oteam, flag):
    points = most_points(ateam)
    attacks = most_attacks(ateam)
    scores = highest_scores(ateam)[['attacker', 'points', 'link']]
    targets = most_targeted(oteam)
    
    print('Score:', ateam['points'].sum(), '\n')
    print('# Times Team Prompts Used:', targets.sum(), '\n')
    
    if flag:
        points = points.head(5)
        attacks = attacks.head(5)
        scores = scores.head(5)
        targets = targets.head(5)
    
    print('Most Points:\n', points, '\n')
    print('Most Attacks:\n', attacks, '\n')
    print('Highest Scores:\n', scores.to_string(), '\n')
    print('Most Targeted:\n', targets, '\n')

# helper method for tally()
# inputs:
#       (str) wk : name of local csv file to read data from
# purpose:
#       reads in a specified .csv file, cleans the data, and returns
#       data as a pandas dataframe
# returns:
#       (DataFrame) week : DataFrame containing all attacks made in specified week
def clean_csv(wk):
    # reading in csv, removing header
    week = pd.read_csv(wk, header=[3])
    week.columns = week.columns.str.lower()
    
    # removing unnecessary columns and empty rows
    week = week[week.columns[2:8]].dropna()
    
    # lowercase and remove whitespace in the str columns
    week.iloc[:, 1:] = week.iloc[:, 1:].applymap(str.lower)
    week.iloc[:, 1:] = week.iloc[:, 1:].apply(lambda x : x.str.replace(' ', ''))
    
    return week

# helper method for tally()
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
    # get the team names
    t1 = df['a.team'].unique()[0]
    t2 = df['a.team'].unique()[1]
    
    # split data into two df based on teams
    t1_df = df[df['a.team'] == t1].reset_index(drop = True)
    t2_df = df[df['a.team'] == t2].reset_index(drop = True)
    
    # special dfs for targetting
    t1_o_df = df[df['o.team'] == t1].reset_index(drop = True)
    t2_o_df = df[df['o.team'] == t2].reset_index(drop = True)
    
    print('Team 1 (', t1, '):\n')
    print_sum(t1_df, t1_o_df, flag)
    
    print('Team 2 (', t2, '):\n')
    print_sum(t2_df, t2_o_df, flag)

# main function
# inputs:
#       none
# purpose:
#       creates team summaries (called a tally) based on certain
#       criteria and prints out an easy to read report from data
#       given by local, specially formatted .csv files
# returns:
#       none
def tally():
    # get all csvs in current folder
    csv_list = glob.glob('*.csv')
    
    # set tally dataframe
    tally_df = pd.DataFrame()
    
    # if we want a weekly or overall tally
    tally_flag = bool(int(input("Print weekly or overall tally? 1 (weekly) or 0 (overall) ")))
    
    # if we want all of the data rather than the top 5
    top5_flag = bool(int(input("Only show top 5? 1 (Yes) or 0 (No) ")))
    
    # clean and split scoring sheet based on weekly or overall summary
    if tally_flag: # weekly summary
        wk = (int(input('Choose from Week 1 to ' + str(len(csv_list)) + ': '))) - 1
        tally_df = clean_csv(csv_list[wk])
        print('WEEK', wk, 'TALLY:\n\n')
    else: # overall summary
        for wk in csv_list:
            cleaned = clean_csv(wk)
            temp = pd.concat([cleaned, tally_df])
            tally_df = pd.DataFrame(temp)
    
    # create summaries for each team
    summarize(tally_df, top5_flag)
