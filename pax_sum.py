from tally import clean_csv

# self contained function that prints each participant's stats:
# name, team, points earned so far, how many times they were attacked
# and the attacks they have made (along with the points earned, opponent and link to work)
# it also prints out the participants who havent made an attack
# but have been attacked themselves
def pax_sum():
    # gets local .csv files (formatted)
    csv_list = glob.glob('*.csv')

    # set dataframe
    df = pd.DataFrame()

    # aggregate data
    for wk in csv_list:
        cleaned = clean_csv(wk)
        temp = pd.concat([cleaned, df])
        df = pd.DataFrame(temp)

    df_a = df.groupby(['a.team', 'attacker']) # grouped by attacker names
    df_o = df.groupby(['o.team', 'opponent']) # grouped by opponent names
    df_keys = df_a.groups.keys()

    for team, name in df_keys:
        attacked = 0
        if (team, name) in df_o.groups.keys():
            attacked = df_o.get_group((team, name))['opponent'].count()
        print(name.upper(), \
              ', Team ', team.upper(), \
              '| points earned: ', df_a.get_group((team, name))['points'].sum(), \
              '| times attacked: ', attacked, '\n', \
              df_a.get_group((team, name))[['points', 'opponent', 'o.team', 'link']].to_string(), '\n')

    for team, name in df_o.groups.keys():
        if (team, name) not in df_keys:
            print(name.upper(), \
              ', Team ', team.upper(), \
              '| times attacked: ', df_o.get_group((team, name))['opponent'].count())
