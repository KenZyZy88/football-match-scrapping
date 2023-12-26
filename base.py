import requests
import pandas as pd
import numpy as np
import time
import logging
import sys
import os 
from bs4 import BeautifulSoup
from lxml import etree
import warnings
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


pd.options.mode.chained_assignment = None 
warnings.simplefilter(action='ignore', category=FutureWarning)

#Variable foe league and season
season =  "2022-2023"
fbrefleagueid = 20
#  Doing
# 2022-2023"
# Done
# 9 - "2020-2021" "2021-2022" "2022-2023"
# 11 - "2021-2022" "2020-2021" "2022-2023"
# 12 - "2020-2021" "2021-2022" "2022-2023"
# 13 - "2020-2021" "2021-2022" "2022-2023" 
# 20 - "2021-2022"  "2020-2021" "2022-2023"

league_mapping = {
    9: 'English Premier League',
    11: 'Italian Serie A',
    12: 'Spanish La Liga 1',
    13: 'French Ligue 1',
    20: 'German Bundesliga 1'
}
leaguename = league_mapping[fbrefleagueid]

url = f"https://fbref.com/en/comps/{fbrefleagueid}/{season}/schedule/"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

####
# Implement this to the code if fail
# session = requests.Session()
# retry = Retry(connect=3, backoff_factor=0.5)
# adapter = HTTPAdapter(max_retries=retry)
# session.mount('http://', adapter)
# session.mount('https://', adapter)
# session.get(url)
# response = session.get(url, headers=headers)


response = requests.get(url, headers=headers)

html_content = response.text
main_table = pd.read_html(html_content)


if len(main_table) > 1:
    merged_df = pd.DataFrame(main_table[1])
    table =1
else:
    merged_df = pd.DataFrame(main_table[0])
    table =0

soup = BeautifulSoup(html_content, features="lxml")
stu = etree.HTML(str(soup)) 



# Creating tables for insertion

main_table = pd.DataFrame(columns=['Wk','Day','Date','Time','Home','xG','Score','xG.1','Away','Attendance','Venue','Referee','Notes'])
matchsummary_table = pd.DataFrame(columns=['matchid','homeid','awayid'])
teamsummaryfooter_table = pd.DataFrame(columns=['matchid','teamid','gls','ast','pk','pkatt','sh','sot','crdy','crdr','touches','tkl','int','blocks','xg','npxg','xag','sca','gca','cmp','passatt','cmp%','prgp','carries','prgc','takeonatt','succ'])
teamsummary_table= pd.DataFrame(columns=['matchid','teamid','playerid','player', 'no','nation','pos','age','min','gls','ast','pk','pkatt','sh','sot','crdy','crdr','touches','tkl','int','blocks','xg','npxg','xag','sca','gca','cmp','passatt','cmp%','prgp','carries','prgc','takeonatt','succ'])
teampassingfooter_table= pd.DataFrame(columns=['matchid','teamid','totalcmp', 'totalatt', 'totalpasscompletionpct', 'totaltotdist', 'totalprgdist', 'shortcmp', 'shortatt', 'shortpasscompletionpct', 'mediumcmp', 'mediumatt', 'mediumpasscompletionpct', 'longcmp', 'longatt', 'longpasscompletionpct', 'ast', 'xag', 'xa', 'kp', 'passtofinalthird', 'PPA', 'crspa', 'prgp'])
teampassing_table =pd.DataFrame(columns=['matchid','teamid','playerid','player', 'no','nation','pos','age','min','totalcmp', 'totalatt', 'totalpasscompletionpct', 'totaltotdist', 'totalprgdist', 'shortcmp', 'shortatt', 'shortpasscompletionpct', 'mediumcmp', 'mediumatt', 'mediumpasscompletionpct', 'longcmp', 'longatt', 'longpasscompletionpct', 'ast', 'xag', 'xa', 'kp', 'passtofinalthird', 'PPA', 'crspa', 'prgp'])
teampasstypefooter_table =pd.DataFrame(columns=['matchid','teamid','Att','Live','Dead','FK','TB','Sw','Crs','TI','CK','In','Out','Str','Cmp','Off','Blocks'])
teampasstype_table = pd.DataFrame(columns=['matchid','teamid','playerid','Player','no','Nation','Pos','Age','Min','Att','Live','Dead','FK','TB','Sw','Crs','TI','CK','In','Out','Str','Cmp','Off','Blocks'])
teamdefencefooter_table=pd.DataFrame(columns=['matchid','teamid','Tkl','TklW','Def3rd','Mid3rd','Att3rd','DribbleTkl','Att','Tkl%','Lost','Blocks','Sh','Pass','Int','Tkl+Int','Clr','Err'])
teamdefence_table =pd.DataFrame(columns=['matchid','teamid','playerid','Player','no','Nation','Pos','Age','Min','Tkl','TklW','Def3rd','Mid3rd','Att3rd','DribbleTkl','Att','Tkl%','Lost','Blocks','Sh','Pass','Int','Tkl+Int','Clr','Err'])
teamposessionfooter_table =pd.DataFrame(columns=['matchid','teamid','Touches','DefPen','Def3rd','Mid3rd','Att3rd','AttPen','Live','Att','Succ','Succ%','Tkld','Tkld%','Carries','TotDist','PrgDist','PrgC','OneThird','CPA','Mis','Dis','Rec','PrgR'])
teamposession_table =pd.DataFrame(columns=['matchid','teamid','playerid','Player','no','Nation','Pos','Age','Min','Touches','DefPen','Def3rd','Mid3rd','Att3rd','AttPen','Live','Att','Succ','Succ%','Tkld','Tkld%','Carries','TotDist','PrgDist','PrgC','CarryIntoFinal3rd','CPA','Mis','Dis','Rec','PrgR'])
teammiscfooter_table =pd.DataFrame(columns=['matchid','teamid','CrdY','CrdR','2CrdY','Fls','Fld','Off','Crs','Int','TklW','PKwon','PKcon','OG','Recov','Won','Lost','Won%'])
teammisc_table =pd.DataFrame(columns=['matchid','teamid','playerid','Player','no','Nation','Pos','Age','Min','CrdY','CrdR','2CrdY','Fls','Fld','Off','Crs','Int','TklW','PKwon','PKcon','OG','Recov','Won','Lost','Won%'])       
goalkeeper_table = pd.DataFrame(columns=['matchid','teamid','playerid','Player','Nation','Age','Min','SoTA','GA','Saves','Save%','PSxG','LaunchedCmp','LaunchedAtt','LaunchedCmp%','Att(GK)','Thr','PassesLaunch%','PassesAvgLen','GoalKicksAtt','GoalKicksLaunch%','GoalKicksAvgLen','Opp','Stp','Stp%','#OPA','AvgDist']) 
shots_table = pd.DataFrame(columns=['matchid','Minute','playerid','Player','TeamId','Team','xG','PSxG','Outcome', 'Distance','Body Part','Notes','Sca1PlayerId','Sca1Player','Sca1Event','Sca2PlayerId','Sca2Player', 'Sca2Event'])
home_formation_table = pd.DataFrame(columns=['home_formation'])
away_formation_table = pd.DataFrame(columns=['away_formation'])
matchsummarymain_table = pd.DataFrame(columns=['home_possession','away_possession','home_passing_accuracy','away_passing_accuracy','home_shot_on_target','away_shot_on_target','home_save','away_save'])


main_table['Wk'] = merged_df['Wk']
main_table['Day'] = merged_df['Day']
main_table['Date'] = merged_df['Date']
main_table['Time'] = merged_df['Time']
main_table['Home'] = merged_df['Home']
main_table['xG'] = merged_df['xG']
main_table['Score'] = merged_df['Score']
main_table['xG.1'] = merged_df['xG.1']
main_table['Away'] = merged_df['Away']
main_table['Attendance'] = merged_df['Attendance']
main_table['Venue'] = merged_df['Venue']
main_table['Referee'] = merged_df['Referee']
main_table['Notes'] = merged_df['Notes']
main_table.dropna(subset=['Away', 'Home'], inplace=True)


id_table = pd.DataFrame(columns=['matchid','homeid','awayid'])
# matchs = soup.find_all('tr')
matchs = soup.find_all('table')[table].find_all('tr')
# print(matchs)

for match in matchs[1:]:
    match_record = match.find(attrs={"data-stat": "match_report"})
    home_team = match.find(attrs={"data-stat": "home_team"})
    away_team = match.find(attrs={"data-stat": "away_team"})

        
    if match_record is not None and match_record.find('a') is not None:
        match_href= match_record.find('a').get('href')
        matchid=match_href.split('/')[3]
        home_team_href = home_team.find('a').get('href')
        homeid=home_team_href.split('/')[3]
        away_team_href = away_team.find('a').get('href')
        awayid=away_team_href.split('/')[3]

        id_table = id_table._append({'matchid': matchid,'homeid': homeid,'awayid':awayid,'season':season,'league':leaguename}, ignore_index=True)
        
        
main_table=main_table.reset_index(drop=True)
merged_df = pd.merge(main_table, id_table, left_index=True, right_index=True)
print(merged_df)

# for x in range(0, len(id_table))[0:2]:
for x in range(0, len(id_table)):
    matchid = id_table['matchid'][x]
    homeid= id_table['homeid'][x]
    awayid= id_table['awayid'][x]
    ## Enale if/else statement if there is no data in table
    if matchid == 'c34bbc21':
        continue
    else: 
        match_data_url=f"https://fbref.com/en/matches/{matchid}/"
    # match_data_url=f"https://fbref.com/en/matches/{matchid}/" # If there is no issue then use this as main
    # match_data_url=f"https://fbref.com/en/matches/ae69d7a7/" #Test URL
    # match_data_url=f"https://fbref.com/en/matches/2358f8c4/"

    print(f"{x} : {match_data_url}")

    #Retry if fetch fail. try 3 times where the wait is 50% longer the next time it waits. 
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    # session.get(url)
    response = session.get(match_data_url, headers=headers)


    # response = requests.get(match_data_url, headers=headers)
    html_content = response.text
    match_data_table = pd.read_html(html_content)
    match_data_table_df = pd.concat(match_data_table)
    matchsoup = BeautifulSoup(html_content, features="lxml")
    dom = etree.HTML(str(matchsoup)) 


    homeid_href=(dom.xpath('//*[@id="content"]/div[2]/div[1]/div[1]/strong/a')[0].get('href'))
    matchhomeid=homeid_href.split('/')[3]
    awayid_href=(dom.xpath('//*[@id="content"]/div[2]/div[2]/div[1]/strong/a')[0].get('href'))
    matchawayid=awayid_href.split('/')[3]
    match_href=(dom.xpath('/html/head/link[2]')[0].get('href'))
    matchmatchid= match_href.split('/')[5]
    


    # Looping thru the tables
    for x in range(0, len(match_data_table)):
        
        data_table= match_data_table[x]

        if x in [0,1,2]: #Match Summary

            if x == 0: 
                home_formation=match_data_table[x].columns
                home_formation = home_formation[0]
                # home_formation = str(home_formation)
                home_formation = home_formation.split('(')[1]
                home_formation = home_formation.replace(')','')

                matchsummary_table=matchsummary_table._append({'matchid':matchmatchid,'homeid':matchhomeid,'awayid':matchawayid},ignore_index=True)
                home_formation_table=home_formation_table._append({'home_formation':home_formation},ignore_index=True)
            if x == 1:
                away_formation=match_data_table[x].columns
                away_formation = away_formation[0]
                away_formation = away_formation.split('(')[1]
                away_formation = away_formation.replace(')','')
                away_formation_table=away_formation_table._append({'away_formation':away_formation},ignore_index=True)
                # matchsummary_table = pd.concat([matchsummary_table, pd.DataFrame([away_formation], columns=['away_formation'])], axis=1)

            if x ==2:
                home_possession = data_table.iloc[0, 0]
                away_possession = data_table.iloc[0, 1]
                home_passing_accuracy = data_table.iloc[2, 0]
                away_passing_accuracy = data_table.iloc[2, 1]
                home_shot_on_target = data_table.iloc[4, 0]
                away_shot_on_target = data_table.iloc[4, 1]
                home_save = data_table.iloc[6, 0]
                away_save = data_table.iloc[6, 1]
                matchsummarymain_table=matchsummarymain_table._append({'home_possession': home_possession, 'away_possession': away_possession, 'home_passing_accuracy': home_passing_accuracy, 'away_passing_accuracy': away_passing_accuracy, 'home_shot_on_target': home_shot_on_target, 'away_shot_on_target': away_shot_on_target, 'home_save': home_save, 'away_save': away_save},ignore_index=True)
          
                  # matchsummary_table = pd.concat([matchsummary_table, pd.DataFrame({'home_possession': home_possession, 'away_possession': away_possession, 'home_passing_accuracy': home_passing_accuracy, 'away_passing_accuracy': away_passing_accuracy, 'home_shot_on_target': home_shot_on_target, 'away_shot_on_target': away_shot_on_target, 'home_save': home_save, 'away_save': away_save}, index=[0])], axis=1)                



        if x in [3,10]: #TeamSummary
            
            if x == 3: #HomeTeam #summary
                # Dropping a level down 
                    data_table.columns = data_table.columns.droplevel(0)
                    # Load Footer to footer table and drop footer from main table
                    teamsummaryfooter = data_table.tail(1)
                    data_table.drop(data_table.tail(1).index, inplace=True)
                    
                    #Footer Data insert
                    teamsummaryfooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                    teamsummaryfooter = teamsummaryfooter.reset_index(drop=True)
                    for (index,row) in teamsummaryfooter.iterrows():
                        teamsummaryfooter_table = teamsummaryfooter_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'gls':teamsummaryfooter.loc[index, 'Gls'],'ast':teamsummaryfooter.loc[index, 'Ast'],'pk':teamsummaryfooter.loc[index, 'PK'],'pkatt':teamsummaryfooter.loc[index, 'PKatt'],'sh':teamsummaryfooter.loc[index, 'Sh'],'sot':teamsummaryfooter.loc[index, 'SoT'],'crdy':teamsummaryfooter.loc[index, 'CrdY'],'crdr':teamsummaryfooter.loc[index, 'CrdR'],'touches':teamsummaryfooter.loc[index, 'Touches'],'tkl':teamsummaryfooter.loc[index, 'Tkl'],'int':teamsummaryfooter.loc[index, 'Int'],'blocks':teamsummaryfooter.loc[index, 'Blocks'],'xg':teamsummaryfooter.loc[index, 'xG'],'npxg':teamsummaryfooter.loc[index, 'npxG'],'xag':teamsummaryfooter.loc[index, 'xAG'],'sca':teamsummaryfooter.loc[index, 'SCA'],'gca':teamsummaryfooter.loc[index, 'GCA'],'cmp':teamsummaryfooter.loc[index, 'Cmp'],'passatt':teamsummaryfooter.iloc[index, 18],'cmp%':teamsummaryfooter.loc[index, 'Cmp%'],'prgp':teamsummaryfooter.loc[index, 'PrgP'],'carries':teamsummaryfooter.loc[index, 'Carries'],'prgc':teamsummaryfooter.loc[index, 'PrgC'],'takeonatt':teamsummaryfooter.iloc[index, 23],'succ':teamsummaryfooter.loc[index, 'Succ']}, ignore_index=True)

                    #Main Data insert
                    for (index,row) in data_table.iterrows():
                        # test=(dom.xpath(f'//*[@id="stats_47c64c55_summary"]/tbody/tr[1]/th/a').get('href'))


                        player_href=(dom.xpath(f'//*[@id="stats_{matchhomeid}_summary"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                        playerid=player_href.split('/')[3]
                        teamsummary_table = teamsummary_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'playerid': playerid,'player': data_table.loc[index, 'Player'],'no':data_table.loc[index, '#'],'nation':data_table.loc[index, 'Nation'],'pos':data_table.loc[index, 'Pos'],'age':data_table.loc[index, 'Age'],'min':data_table.loc[index, 'Min'],'gls':data_table.loc[index, 'Gls'],'ast':data_table.loc[index, 'Ast'],'pk':data_table.loc[index, 'PK'],'pkatt':data_table.loc[index, 'PKatt'],'sh':data_table.loc[index, 'Sh'],'sot':data_table.loc[index, 'SoT'],'crdy':data_table.loc[index, 'CrdY'],'crdr':data_table.loc[index, 'CrdR'],'touches':data_table.loc[index, 'Touches'],'tkl':data_table.loc[index, 'Tkl'],'int':data_table.loc[index, 'Int'],'blocks':data_table.loc[index, 'Blocks'],'xg':data_table.loc[index, 'xG'],'npxg':data_table.loc[index, 'npxG'],'xag':data_table.loc[index, 'xAG'],'sca':data_table.loc[index, 'SCA'],'gca':data_table.loc[index, 'GCA'],'cmp':data_table.loc[index, 'Cmp'],'passatt':data_table.iloc[index, 24],'cmp%':data_table.loc[index, 'Cmp%'],'prgp':data_table.loc[index, 'PrgP'],'carries':data_table.loc[index, 'Carries'],'prgc':data_table.loc[index, 'PrgC'],'takeonatt':data_table.iloc[index, 29],'succ':data_table.loc[index, 'Succ']}, ignore_index=True)

        
            if x == 10: #AwayTeam #summary
                 # Dropping a level down 
                    data_table.columns = data_table.columns.droplevel(0)
                    # Load Footer to footer table and drop footer from main table
                    teamsummaryfooter = data_table.tail(1)
                    data_table.drop(data_table.tail(1).index, inplace=True)
                    
                    #Footer Data insert
                    teamsummaryfooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                    teamsummaryfooter = teamsummaryfooter.reset_index(drop=True)
                    for (index,row) in teamsummaryfooter.iterrows():
                        teamsummaryfooter_table = teamsummaryfooter_table._append({'matchid':matchmatchid,'teamid':matchawayid,'gls':teamsummaryfooter.loc[index, 'Gls'],'ast':teamsummaryfooter.loc[index, 'Ast'],'pk':teamsummaryfooter.loc[index, 'PK'],'pkatt':teamsummaryfooter.loc[index, 'PKatt'],'sh':teamsummaryfooter.loc[index, 'Sh'],'sot':teamsummaryfooter.loc[index, 'SoT'],'crdy':teamsummaryfooter.loc[index, 'CrdY'],'crdr':teamsummaryfooter.loc[index, 'CrdR'],'touches':teamsummaryfooter.loc[index, 'Touches'],'tkl':teamsummaryfooter.loc[index, 'Tkl'],'int':teamsummaryfooter.loc[index, 'Int'],'blocks':teamsummaryfooter.loc[index, 'Blocks'],'xg':teamsummaryfooter.loc[index, 'xG'],'npxg':teamsummaryfooter.loc[index, 'npxG'],'xag':teamsummaryfooter.loc[index, 'xAG'],'sca':teamsummaryfooter.loc[index, 'SCA'],'gca':teamsummaryfooter.loc[index, 'GCA'],'cmp':teamsummaryfooter.loc[index, 'Cmp'],'passatt':teamsummaryfooter.iloc[index, 18],'cmp%':teamsummaryfooter.loc[index, 'Cmp%'],'prgp':teamsummaryfooter.loc[index, 'PrgP'],'carries':teamsummaryfooter.loc[index, 'Carries'],'prgc':teamsummaryfooter.loc[index, 'PrgC'],'takeonatt':teamsummaryfooter.iloc[index, 23],'succ':teamsummaryfooter.loc[index, 'Succ']}, ignore_index=True)
                       
                       
                    #Main Data insert
                    for (index,row) in data_table.iterrows():
                        player_href=(dom.xpath(f'//*[@id="stats_{matchawayid}_summary"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                        playerid=player_href.split('/')[3]
                        teamsummary_table = teamsummary_table._append({'matchid':matchmatchid,'teamid':matchawayid,'playerid': playerid,'player': data_table.loc[index, 'Player'],'no':data_table.loc[index, '#'],'nation':data_table.loc[index, 'Nation'],'pos':data_table.loc[index, 'Pos'],'age':data_table.loc[index, 'Age'],'min':data_table.loc[index, 'Min'],'gls':data_table.loc[index, 'Gls'],'ast':data_table.loc[index, 'Ast'],'pk':data_table.loc[index, 'PK'],'pkatt':data_table.loc[index, 'PKatt'],'sh':data_table.loc[index, 'Sh'],'sot':data_table.loc[index, 'SoT'],'crdy':data_table.loc[index, 'CrdY'],'crdr':data_table.loc[index, 'CrdR'],'touches':data_table.loc[index, 'Touches'],'tkl':data_table.loc[index, 'Tkl'],'int':data_table.loc[index, 'Int'],'blocks':data_table.loc[index, 'Blocks'],'xg':data_table.loc[index, 'xG'],'npxg':data_table.loc[index, 'npxG'],'xag':data_table.loc[index, 'xAG'],'sca':data_table.loc[index, 'SCA'],'gca':data_table.loc[index, 'GCA'],'cmp':data_table.loc[index, 'Cmp'],'passatt':data_table.iloc[index, 24],'cmp%':data_table.loc[index, 'Cmp%'],'prgp':data_table.loc[index, 'PrgP'],'carries':data_table.loc[index, 'Carries'],'prgc':data_table.loc[index, 'PrgC'],'takeonatt':data_table.iloc[index, 29],'succ':data_table.loc[index, 'Succ']}, ignore_index=True)

        if x in [4,11]: #HomeTeam #Passing

            if x == 4: #HomeTeam #passing
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                # Load Footer to footer table and drop footer from main table
                teampassingfooter = data_table.tail(1)
                data_table.drop(data_table.tail(1).index, inplace=True)
                #Footer Data insert
                teampassingfooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                teampassingfooter = teampassingfooter.reset_index(drop=True)
                teampassingfooter_table= teampassingfooter_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'totalcmp':teampassingfooter.iloc[0,0], 'totalatt':teampassingfooter.iloc[0,1], 'totalpasscompletionpct':teampassingfooter.iloc[0,2], 'totaltotdist':teampassingfooter.iloc[0,3], 'totalprgdist':teampassingfooter.iloc[0,4], 'shortcmp':teampassingfooter.iloc[0,5], 'shortatt':teampassingfooter.iloc[0,6], 'shortpasscompletionpct':teampassingfooter.iloc[0,7], 'mediumcmp':teampassingfooter.iloc[0,8], 'mediumatt':teampassingfooter.iloc[0,9], 'mediumpasscompletionpct':teampassingfooter.iloc[0,10], 'longcmp':teampassingfooter.iloc[0,11], 'longatt':teampassingfooter.iloc[0,12], 'longpasscompletionpct':teampassingfooter.iloc[0,13], 'ast':teampassingfooter.iloc[0,14], 'xag':teampassingfooter.iloc[0,15], 'xa':teampassingfooter.iloc[0,16], 'kp':teampassingfooter.iloc[0,17], 'passtofinalthird':teampassingfooter.iloc[0,18], 'PPA':teampassingfooter.iloc[0,19], 'crspa':teampassingfooter.iloc[0,20], 'prgp':teampassingfooter.iloc[0,21]}, ignore_index=True)

                 #Main Data insert
                for (index,row) in data_table.iterrows():

                    player_href=(dom.xpath(f'//*[@id="stats_{matchhomeid}_passing"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                    playerid=player_href.split('/')[3]

                    teampassing_table =teampassing_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'playerid': playerid,'player':data_table.iloc[index,0], 'no':data_table.iloc[index,1],'nation':data_table.iloc[index,2],'pos':data_table.iloc[index,3],'age':data_table.iloc[index,4],'min':data_table.iloc[index,5],'totalcmp':data_table.iloc[index,6], 'totalatt':data_table.iloc[index,7], 'totalpasscompletionpct':data_table.iloc[index,8], 'totaltotdist':data_table.iloc[index,9], 'totalprgdist':data_table.iloc[index,10], 'shortcmp':data_table.iloc[index,11], 'shortatt':data_table.iloc[index,12], 'shortpasscompletionpct':data_table.iloc[index,13], 'mediumcmp':data_table.iloc[index,14], 'mediumatt':data_table.iloc[index,15], 'mediumpasscompletionpct':data_table.iloc[index,16], 'longcmp':data_table.iloc[index,17], 'longatt':data_table.iloc[index,18], 'longpasscompletionpct':data_table.iloc[index,19], 'ast':data_table.iloc[index,20], 'xag':data_table.iloc[index,21], 'xa':data_table.iloc[index,22], 'kp':data_table.iloc[index,23], 'passtofinalthird':data_table.iloc[index,24], 'PPA':data_table.iloc[index,25], 'crspa':data_table.iloc[index,26], 'prgp':data_table.iloc[index,27]}, ignore_index=True)

                        

            if x == 11: #AwayTeam #passing
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                # Load Footer to footer table and drop footer from main table
                teampassingfooter = data_table.tail(1)
                data_table.drop(data_table.tail(1).index, inplace=True)
                #Footer Data insert
                teampassingfooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                teampassingfooter = teampassingfooter.reset_index(drop=True)
                teampassingfooter_table= teampassingfooter_table._append({'matchid':matchmatchid,'teamid':matchawayid,'totalcmp':teampassingfooter.iloc[0,0], 'totalatt':teampassingfooter.iloc[0,1], 'totalpasscompletionpct':teampassingfooter.iloc[0,2], 'totaltotdist':teampassingfooter.iloc[0,3], 'totalprgdist':teampassingfooter.iloc[0,4], 'shortcmp':teampassingfooter.iloc[0,5], 'shortatt':teampassingfooter.iloc[0,6], 'shortpasscompletionpct':teampassingfooter.iloc[0,7], 'mediumcmp':teampassingfooter.iloc[0,8], 'mediumatt':teampassingfooter.iloc[0,9], 'mediumpasscompletionpct':teampassingfooter.iloc[0,10], 'longcmp':teampassingfooter.iloc[0,11], 'longatt':teampassingfooter.iloc[0,12], 'longpasscompletionpct':teampassingfooter.iloc[0,13], 'ast':teampassingfooter.iloc[0,14], 'xag':teampassingfooter.iloc[0,15], 'xa':teampassingfooter.iloc[0,16], 'kp':teampassingfooter.iloc[0,17], 'passtofinalthird':teampassingfooter.iloc[0,18], 'PPA':teampassingfooter.iloc[0,19], 'crspa':teampassingfooter.iloc[0,20], 'prgp':teampassingfooter.iloc[0,21]}, ignore_index=True)
                for (index,row) in data_table.iterrows():

                    player_href=(dom.xpath(f'//*[@id="stats_{matchawayid}_passing"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                    playerid=player_href.split('/')[3]
                                    
                    teampassing_table =teampassing_table._append({'matchid':matchmatchid,'teamid':matchawayid,'playerid': playerid,'player':data_table.iloc[index,0], 'no':data_table.iloc[index,1],'nation':data_table.iloc[index,2],'pos':data_table.iloc[index,3],'age':data_table.iloc[index,4],'min':data_table.iloc[index,5],'totalcmp':data_table.iloc[index,6], 'totalatt':data_table.iloc[index,7], 'totalpasscompletionpct':data_table.iloc[index,8], 'totaltotdist':data_table.iloc[index,9], 'totalprgdist':data_table.iloc[index,10], 'shortcmp':data_table.iloc[index,11], 'shortatt':data_table.iloc[index,12], 'shortpasscompletionpct':data_table.iloc[index,13], 'mediumcmp':data_table.iloc[index,14], 'mediumatt':data_table.iloc[index,15], 'mediumpasscompletionpct':data_table.iloc[index,16], 'longcmp':data_table.iloc[index,17], 'longatt':data_table.iloc[index,18], 'longpasscompletionpct':data_table.iloc[index,19], 'ast':data_table.iloc[index,20], 'xag':data_table.iloc[index,21], 'xa':data_table.iloc[index,22], 'kp':data_table.iloc[index,23], 'passtofinalthird':data_table.iloc[index,24], 'PPA':data_table.iloc[index,25], 'crspa':data_table.iloc[index,26], 'prgp':data_table.iloc[index,27]}, ignore_index=True)
        
        if x in [5,12]: #Pass type
            if x ==5: #HomeTeam #Passtype
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                # Load Footer to footer table and drop footer from main table
                teampasstypefooter = data_table.tail(1)
                data_table.drop(data_table.tail(1).index, inplace=True)

                #Footer Data insert
                teampasstypefooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                teampasstypefooter = teampasstypefooter.reset_index(drop=True)
                teampasstypefooter_table =teampasstypefooter_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'Att':teampasstypefooter.iloc[0,0],'Live':teampasstypefooter.iloc[0,1],'Dead':teampasstypefooter.iloc[0,2],'FK':teampasstypefooter.iloc[0,3],'TB':teampasstypefooter.iloc[0,4],'Sw':teampasstypefooter.iloc[0,5],'Crs':teampasstypefooter.iloc[0,6],'TI':teampasstypefooter.iloc[0,7],'CK':teampasstypefooter.iloc[0,8],'In':teampasstypefooter.iloc[0,9],'Out':teampasstypefooter.iloc[0,10],'Str':teampasstypefooter.iloc[0,11],'Cmp':teampasstypefooter.iloc[0,12],'Off':teampasstypefooter.iloc[0,13],'Blocks':teampasstypefooter.iloc[0,14]}, ignore_index=True)
                # Main Data Insert
                for (index,row) in data_table.iterrows():
                        player_href=(dom.xpath(f'//*[@id="stats_{matchhomeid}_passing_types"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                        playerid=player_href.split('/')[3]

                        teampasstype_table = teampasstype_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'playerid':playerid,'Player':data_table.iloc[index,0],'no':data_table.iloc[index,1],'Nation':data_table.iloc[index,2],'Pos':data_table.iloc[index,3],'Age':data_table.iloc[index,4],'Min':data_table.iloc[index,5],'Att':data_table.iloc[index,6],'Live':data_table.iloc[index,7],'Dead':data_table.iloc[index,8],'FK':data_table.iloc[index,9],'TB':data_table.iloc[index,10],'Sw':data_table.iloc[index,11],'Crs':data_table.iloc[index,12],'TI':data_table.iloc[index,13],'CK':data_table.iloc[index,14],'In':data_table.iloc[index,15],'Out':data_table.iloc[index,16],'Str':data_table.iloc[index,17],'Cmp':data_table.iloc[index,18],'Off':data_table.iloc[index,19],'Blocks':data_table.iloc[index,20]},ignore_index=True)
                        
            if x ==12: #AwayTeam #Passtype
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                # Load Footer to footer table and drop footer from main table
                teampasstypefooter = data_table.tail(1)
                data_table.drop(data_table.tail(1).index, inplace=True)

                #Footer Data insert
                teampasstypefooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                teampasstypefooter = teampasstypefooter.reset_index(drop=True)
                teampasstypefooter_table =teampasstypefooter_table._append({'matchid':matchmatchid,'teamid':matchawayid,'Att':teampasstypefooter.iloc[0,0],'Live':teampasstypefooter.iloc[0,1],'Dead':teampasstypefooter.iloc[0,2],'FK':teampasstypefooter.iloc[0,3],'TB':teampasstypefooter.iloc[0,4],'Sw':teampasstypefooter.iloc[0,5],'Crs':teampasstypefooter.iloc[0,6],'TI':teampasstypefooter.iloc[0,7],'CK':teampasstypefooter.iloc[0,8],'In':teampasstypefooter.iloc[0,9],'Out':teampasstypefooter.iloc[0,10],'Str':teampasstypefooter.iloc[0,11],'Cmp':teampasstypefooter.iloc[0,12],'Off':teampasstypefooter.iloc[0,13],'Blocks':teampasstypefooter.iloc[0,14]}, ignore_index=True)
                # Main Data Insert
                for (index,row) in data_table.iterrows():
                        player_href=(dom.xpath(f'//*[@id="stats_{matchawayid}_passing_types"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                        playerid=player_href.split('/')[3]

                        teampasstype_table = teampasstype_table._append({'matchid':matchmatchid,'teamid':matchawayid,'playerid':playerid,'Player':data_table.iloc[index,0],'no':data_table.iloc[index,1],'Nation':data_table.iloc[index,2],'Pos':data_table.iloc[index,3],'Age':data_table.iloc[index,4],'Min':data_table.iloc[index,5],'Att':data_table.iloc[index,6],'Live':data_table.iloc[index,7],'Dead':data_table.iloc[index,8],'FK':data_table.iloc[index,9],'TB':data_table.iloc[index,10],'Sw':data_table.iloc[index,11],'Crs':data_table.iloc[index,12],'TI':data_table.iloc[index,13],'CK':data_table.iloc[index,14],'In':data_table.iloc[index,15],'Out':data_table.iloc[index,16],'Str':data_table.iloc[index,17],'Cmp':data_table.iloc[index,18],'Off':data_table.iloc[index,19],'Blocks':data_table.iloc[index,20]},ignore_index=True)

        if x in [6,13]: #HomeTeam #Defence Action
            if x==6:
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                # Load Footer to footer table and drop footer from main table
                teamdefencefooter = data_table.tail(1)
                data_table.drop(data_table.tail(1).index, inplace=True)

                #Footer Data insert
                teamdefencefooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                teamdefencefooter = teamdefencefooter.reset_index(drop=True)
                teamdefencefooter_table = teamdefencefooter_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'Tkl':teamdefencefooter.iloc[0,0],'TklW':teamdefencefooter.iloc[0,1],'Def3rd':teamdefencefooter.iloc[0,2],'Mid3rd':teamdefencefooter.iloc[0,3],'Att3rd':teamdefencefooter.iloc[0,4],'DribbleTkl':teamdefencefooter.iloc[0,5],'Att':teamdefencefooter.iloc[0,6],'Tkl%':teamdefencefooter.iloc[0,7],'Lost':teamdefencefooter.iloc[0,8],'Blocks':teamdefencefooter.iloc[0,9],'Sh':teamdefencefooter.iloc[0,10],'Pass':teamdefencefooter.iloc[0,11],'Int':teamdefencefooter.iloc[0,12],'Tkl+Int':teamdefencefooter.iloc[0,13],'Clr':teamdefencefooter.iloc[0,14],'Err':teamdefencefooter.iloc[0,15]}, ignore_index=True)
                for (index,row) in data_table.iterrows():
                    player_href=(dom.xpath(f'//*[@id="stats_{matchhomeid}_defense"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                    playerid=player_href.split('/')[3]
                    teamdefence_table = teamdefence_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'playerid':playerid,'Player':data_table.iloc[index,0],'no':data_table.iloc[index,1],'Nation':data_table.iloc[index,2],'Pos':data_table.iloc[index,3],'Age':data_table.iloc[index,4],'Min':data_table.iloc[index,5],'Tkl':data_table.iloc[index,6],'TklW':data_table.iloc[index,7],'Def3rd':data_table.iloc[index,8],'Mid3rd':data_table.iloc[index,9],'Att3rd':data_table.iloc[index,10],'DribbleTkl':data_table.iloc[index,11],'Att':data_table.iloc[index,12],'Tkl%':data_table.iloc[index,13],'Lost':data_table.iloc[index,14],'Blocks':data_table.iloc[index,15],'Sh':data_table.iloc[index,16],'Pass':data_table.iloc[index,17],'Int':data_table.iloc[index,18],'Tkl+Int':data_table.iloc[index,19],'Clr':data_table.iloc[index,20],'Err':data_table.iloc[index,21]}, ignore_index=True)

            if x==13:
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                # Load Footer to footer table and drop footer from main table
                teamdefencefooter = data_table.tail(1)
                data_table.drop(data_table.tail(1).index, inplace=True)

                #Footer Data insert
                teamdefencefooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                teamdefencefooter = teamdefencefooter.reset_index(drop=True)
                teamdefencefooter_table = teamdefencefooter_table._append({'matchid':matchmatchid,'teamid':matchawayid,'Tkl':teamdefencefooter.iloc[0,0],'TklW':teamdefencefooter.iloc[0,1],'Def3rd':teamdefencefooter.iloc[0,2],'Mid3rd':teamdefencefooter.iloc[0,3],'Att3rd':teamdefencefooter.iloc[0,4],'DribbleTkl':teamdefencefooter.iloc[0,5],'Att':teamdefencefooter.iloc[0,6],'Tkl%':teamdefencefooter.iloc[0,7],'Lost':teamdefencefooter.iloc[0,8],'Blocks':teamdefencefooter.iloc[0,9],'Sh':teamdefencefooter.iloc[0,10],'Pass':teamdefencefooter.iloc[0,11],'Int':teamdefencefooter.iloc[0,12],'Tkl+Int':teamdefencefooter.iloc[0,13],'Clr':teamdefencefooter.iloc[0,14],'Err':teamdefencefooter.iloc[0,15]}, ignore_index=True)
                for (index,row) in data_table.iterrows():
                    player_href=(dom.xpath(f'//*[@id="stats_{matchawayid}_defense"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                    playerid=player_href.split('/')[3]

                    teamdefence_table = teamdefence_table._append({'matchid':matchmatchid,'teamid':matchawayid,'playerid':playerid,'Player':data_table.iloc[index,0],'no':data_table.iloc[index,1],'Nation':data_table.iloc[index,2],'Pos':data_table.iloc[index,3],'Age':data_table.iloc[index,4],'Min':data_table.iloc[index,5],'Tkl':data_table.iloc[index,6],'TklW':data_table.iloc[index,7],'Def3rd':data_table.iloc[index,8],'Mid3rd':data_table.iloc[index,9],'Att3rd':data_table.iloc[index,10],'DribbleTkl':data_table.iloc[index,11],'Att':data_table.iloc[index,12],'Tkl%':data_table.iloc[index,13],'Lost':data_table.iloc[index,14],'Blocks':data_table.iloc[index,15],'Sh':data_table.iloc[index,16],'Pass':data_table.iloc[index,17],'Int':data_table.iloc[index,18],'Tkl+Int':data_table.iloc[index,19],'Clr':data_table.iloc[index,20],'Err':data_table.iloc[index,21]}, ignore_index=True)

        if x in [7,14]: #Posession
            if x==7: #HomeTeam
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                # Load Footer to footer table and drop footer from main table
                teamposessionfooter = data_table.tail(1)
                data_table.drop(data_table.tail(1).index, inplace=True)

                #Footer Data insert
                teamposessionfooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                teamposessionfooter = teamposessionfooter.reset_index(drop=True)

                teamposessionfooter_table =teamposessionfooter_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'Touches':teamposessionfooter.iloc[0,0],'DefPen':teamposessionfooter.iloc[0,1],'Def3rd':teamposessionfooter.iloc[0,2],'Mid3rd':teamposessionfooter.iloc[0,3],'Att3rd':teamposessionfooter.iloc[0,4],'AttPen':teamposessionfooter.iloc[0,5],'Live':teamposessionfooter.iloc[0,6],'Att':teamposessionfooter.iloc[0,7],'Succ':teamposessionfooter.iloc[0,8],'Succ%':teamposessionfooter.iloc[0,9],'Tkld':teamposessionfooter.iloc[0,10],'Tkld%':teamposessionfooter.iloc[0,11],'Carries':teamposessionfooter.iloc[0,12],'TotDist':teamposessionfooter.iloc[0,13],'PrgDist':teamposessionfooter.iloc[0,14],'PrgC':teamposessionfooter.iloc[0,15],'OneThird':teamposessionfooter.iloc[0,16],'CPA':teamposessionfooter.iloc[0,17],'Mis':teamposessionfooter.iloc[0,18],'Dis':teamposessionfooter.iloc[0,19],'Rec':teamposessionfooter.iloc[0,20],'PrgR':teamposessionfooter.iloc[0,21]},ignore_index=True)
                for (index,row) in data_table.iterrows():
                    player_href=(dom.xpath(f'//*[@id="stats_{matchhomeid}_summary"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                    playerid=player_href.split('/')[3]

                    teamposession_table = teamposession_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'playerid':playerid,'Player':data_table.iloc[index,0],'no':data_table.iloc[index,1],'Nation':data_table.iloc[index,2],'Pos':data_table.iloc[index,3],'Age':data_table.iloc[index,4],'Min':data_table.iloc[index,5],'Touches':data_table.iloc[index,6],'DefPen':data_table.iloc[index,7],'Def3rd':data_table.iloc[index,8],'Mid3rd':data_table.iloc[index,9],'Att3rd':data_table.iloc[index,10],'AttPen':data_table.iloc[index,11],'Live':data_table.iloc[index,12],'Att':data_table.iloc[index,13],'Succ':data_table.iloc[index,14],'Succ%':data_table.iloc[index,15],'Tkld':data_table.iloc[index,16],'Tkld%':data_table.iloc[index,17],'Carries':data_table.iloc[index,18],'TotDist':data_table.iloc[index,19],'PrgDist':data_table.iloc[index,20],'PrgC':data_table.iloc[index,21],'CarryIntoFinal3rd':data_table.iloc[index,22],'CPA':data_table.iloc[index,23],'Mis':data_table.iloc[index,24],'Dis':data_table.iloc[index,25],'Rec':data_table.iloc[index,26],'PrgR':data_table.iloc[index,27]},ignore_index=True)

            if x==14: #AwayTeam
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                # Load Footer to footer table and drop footer from main table
                teamposessionfooter = data_table.tail(1)
                data_table.drop(data_table.tail(1).index, inplace=True)

                #Footer Data insert
                teamposessionfooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                teamposessionfooter = teamposessionfooter.reset_index(drop=True)

                teamposessionfooter_table =teamposessionfooter_table._append({'matchid':matchmatchid,'teamid':matchawayid,'Touches':teamposessionfooter.iloc[0,0],'DefPen':teamposessionfooter.iloc[0,1],'Def3rd':teamposessionfooter.iloc[0,2],'Mid3rd':teamposessionfooter.iloc[0,3],'Att3rd':teamposessionfooter.iloc[0,4],'AttPen':teamposessionfooter.iloc[0,5],'Live':teamposessionfooter.iloc[0,6],'Att':teamposessionfooter.iloc[0,7],'Succ':teamposessionfooter.iloc[0,8],'Succ%':teamposessionfooter.iloc[0,9],'Tkld':teamposessionfooter.iloc[0,10],'Tkld%':teamposessionfooter.iloc[0,11],'Carries':teamposessionfooter.iloc[0,12],'TotDist':teamposessionfooter.iloc[0,13],'PrgDist':teamposessionfooter.iloc[0,14],'PrgC':teamposessionfooter.iloc[0,15],'OneThird':teamposessionfooter.iloc[0,16],'CPA':teamposessionfooter.iloc[0,17],'Mis':teamposessionfooter.iloc[0,18],'Dis':teamposessionfooter.iloc[0,19],'Rec':teamposessionfooter.iloc[0,20],'PrgR':teamposessionfooter.iloc[0,21]},ignore_index=True)
                for (index,row) in data_table.iterrows():
                    player_href=(dom.xpath(f'//*[@id="stats_{matchawayid}_summary"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                    playerid=player_href.split('/')[3]

                    teamposession_table = teamposession_table._append({'matchid':matchmatchid,'teamid':matchawayid,'playerid':playerid,'Player':data_table.iloc[index,0],'no':data_table.iloc[index,1],'Nation':data_table.iloc[index,2],'Pos':data_table.iloc[index,3],'Age':data_table.iloc[index,4],'Min':data_table.iloc[index,5],'Touches':data_table.iloc[index,6],'DefPen':data_table.iloc[index,7],'Def3rd':data_table.iloc[index,8],'Mid3rd':data_table.iloc[index,9],'Att3rd':data_table.iloc[index,10],'AttPen':data_table.iloc[index,11],'Live':data_table.iloc[index,12],'Att':data_table.iloc[index,13],'Succ':data_table.iloc[index,14],'Succ%':data_table.iloc[index,15],'Tkld':data_table.iloc[index,16],'Tkld%':data_table.iloc[index,17],'Carries':data_table.iloc[index,18],'TotDist':data_table.iloc[index,19],'PrgDist':data_table.iloc[index,20],'PrgC':data_table.iloc[index,21],'CarryIntoFinal3rd':data_table.iloc[index,22],'CPA':data_table.iloc[index,23],'Mis':data_table.iloc[index,24],'Dis':data_table.iloc[index,25],'Rec':data_table.iloc[index,26],'PrgR':data_table.iloc[index,27]},ignore_index=True)
      
            # print(teamdefence_table)

        if x in [8,15]: #misc
            if x == 8:
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                # Load Footer to footer table and drop footer from main table
                teammiscfooter = data_table.tail(1)
                data_table.drop(data_table.tail(1).index, inplace=True)

                #Footer Data insert
                teammiscfooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                teammiscfooter = teammiscfooter.reset_index(drop=True)
                teammiscfooter_table =teammiscfooter_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'CrdY':teammiscfooter.iloc[0,0],'CrdR':teammiscfooter.iloc[0,1],'2CrdY':teammiscfooter.iloc[0,2],'Fls':teammiscfooter.iloc[0,3],'Fld':teammiscfooter.iloc[0,4],'Off':teammiscfooter.iloc[0,5],'Crs':teammiscfooter.iloc[0,6],'Int':teammiscfooter.iloc[0,7],'TklW':teammiscfooter.iloc[0,8],'PKwon':teammiscfooter.iloc[0,9],'PKcon':teammiscfooter.iloc[0,10],'OG':teammiscfooter.iloc[0,11],'Recov':teammiscfooter.iloc[0,12],'Won':teammiscfooter.iloc[0,13],'Lost':teammiscfooter.iloc[0,14],'Won%':teammiscfooter.iloc[0,15]},ignore_index=True)
                for (index,row) in data_table.iterrows():
                    player_href=(dom.xpath(f'//*[@id="stats_{matchhomeid}_misc"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                    playerid=player_href.split('/')[3]
                    teammisc_table = teammisc_table._append({'matchid':matchmatchid,'teamid':matchhomeid,'playerid':playerid,'Player':data_table.iloc[index,0],'no':data_table.iloc[index,1],'Nation':data_table.iloc[index,2],'Pos':data_table.iloc[index,3],'Age':data_table.iloc[index,4],'Min':data_table.iloc[index,5],'CrdY':data_table.iloc[index,6],'CrdR':data_table.iloc[index,7],'2CrdY':data_table.iloc[index,8],'Fls':data_table.iloc[index,9],'Fld':data_table.iloc[index,10],'Off':data_table.iloc[index,11],'Crs':data_table.iloc[index,12],'Int':data_table.iloc[index,13],'TklW':data_table.iloc[index,14],'PKwon':data_table.iloc[index,15],'PKcon':data_table.iloc[index,16],'OG':data_table.iloc[index,17],'Recov':data_table.iloc[index,18],'Won':data_table.iloc[index,19],'Lost':data_table.iloc[index,20],'Won%':data_table.iloc[index,21]},ignore_index=True)
           
            if x == 15:
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                # Load Footer to footer table and drop footer from main table
                teammiscfooter = data_table.tail(1)
                data_table.drop(data_table.tail(1).index, inplace=True)

                #Footer Data insert
                teammiscfooter.drop(['Player','#','Nation','Pos','Age','Min'], axis=1, inplace=True)
                teammiscfooter = teammiscfooter.reset_index(drop=True)
                teammiscfooter_table =teammiscfooter_table._append({'matchid':matchmatchid,'teamid':matchawayid,'CrdY':teammiscfooter.iloc[0,0],'CrdR':teammiscfooter.iloc[0,1],'2CrdY':teammiscfooter.iloc[0,2],'Fls':teammiscfooter.iloc[0,3],'Fld':teammiscfooter.iloc[0,4],'Off':teammiscfooter.iloc[0,5],'Crs':teammiscfooter.iloc[0,6],'Int':teammiscfooter.iloc[0,7],'TklW':teammiscfooter.iloc[0,8],'PKwon':teammiscfooter.iloc[0,9],'PKcon':teammiscfooter.iloc[0,10],'OG':teammiscfooter.iloc[0,11],'Recov':teammiscfooter.iloc[0,12],'Won':teammiscfooter.iloc[0,13],'Lost':teammiscfooter.iloc[0,14],'Won%':teammiscfooter.iloc[0,15]},ignore_index=True)
                for (index,row) in data_table.iterrows():
                    player_href=(dom.xpath(f'//*[@id="stats_{matchawayid}_misc"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                    playerid=player_href.split('/')[3]
                    teammisc_table = teammisc_table._append({'matchid':matchmatchid,'teamid':matchawayid,'playerid':playerid,'Player':data_table.iloc[index,0],'no':data_table.iloc[index,1],'Nation':data_table.iloc[index,2],'Pos':data_table.iloc[index,3],'Age':data_table.iloc[index,4],'Min':data_table.iloc[index,5],'CrdY':data_table.iloc[index,6],'CrdR':data_table.iloc[index,7],'2CrdY':data_table.iloc[index,8],'Fls':data_table.iloc[index,9],'Fld':data_table.iloc[index,10],'Off':data_table.iloc[index,11],'Crs':data_table.iloc[index,12],'Int':data_table.iloc[index,13],'TklW':data_table.iloc[index,14],'PKwon':data_table.iloc[index,15],'PKcon':data_table.iloc[index,16],'OG':data_table.iloc[index,17],'Recov':data_table.iloc[index,18],'Won':data_table.iloc[index,19],'Lost':data_table.iloc[index,20],'Won%':data_table.iloc[index,21]},ignore_index=True)
        if x in [9,16]: #GoalKeeper Stats
            if x ==9: #HomeTeam
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                for (index,row) in data_table.iterrows():
                    player_href=(dom.xpath(f'//*[@id="keeper_stats_{matchhomeid}"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                    playerid=player_href.split('/')[3]
                    # Need to update line below and creating of table
                    goalkeeper_table = goalkeeper_table._append({'matchid':matchmatchid,'teamid':matchawayid,'playerid':playerid,'Player':data_table.iloc[index,0],'Nation':data_table.iloc[index,1],'Age':data_table.iloc[index,2],'Min':data_table.iloc[index,3],'SoTA':data_table.iloc[index,4],'GA':data_table.iloc[index,5],'Saves':data_table.iloc[index,6],'Save%':data_table.iloc[index,7],'PSxG':data_table.iloc[index,8],'LaunchedCmp':data_table.iloc[index,9],'LaunchedAtt':data_table.iloc[index,10],'LaunchedCmp%':data_table.iloc[index,11],'Att(GK)':data_table.iloc[index,12],'Thr':data_table.iloc[index,13],'PassesLaunch%':data_table.iloc[index,14],'PassesAvgLen':data_table.iloc[index,15],'GoalKicksAtt':data_table.iloc[index,16],'GoalKicksLaunch%':data_table.iloc[index,17],'GoalKicksAvgLen':data_table.iloc[index,18],'Opp':data_table.iloc[index,19],'Stp':data_table.iloc[index,20],'Stp%':data_table.iloc[index,21],'#OPA':data_table.iloc[index,22],'AvgDist':data_table.iloc[index,23]},ignore_index=True)
            if x ==16: #HomeTeam
                # Dropping a level down 
                data_table.columns = data_table.columns.droplevel(0)
                for (index,row) in data_table.iterrows():
                    player_href=(dom.xpath(f'//*[@id="keeper_stats_{matchawayid}"]/tbody/tr[{index+1}]/th/a')[0].get('href'))
                    playerid=player_href.split('/')[3]
                    # Need to update line below and creating of table
                    goalkeeper_table = goalkeeper_table._append({'matchid':matchmatchid,'teamid':matchawayid,'playerid':playerid,'Player':data_table.iloc[index,0],'Nation':data_table.iloc[index,1],'Age':data_table.iloc[index,2],'Min':data_table.iloc[index,3],'SoTA':data_table.iloc[index,4],'GA':data_table.iloc[index,5],'Saves':data_table.iloc[index,6],'Save%':data_table.iloc[index,7],'PSxG':data_table.iloc[index,8],'LaunchedCmp':data_table.iloc[index,9],'LaunchedAtt':data_table.iloc[index,10],'LaunchedCmp%':data_table.iloc[index,11],'Att(GK)':data_table.iloc[index,12],'Thr':data_table.iloc[index,13],'PassesLaunch%':data_table.iloc[index,14],'PassesAvgLen':data_table.iloc[index,15],'GoalKicksAtt':data_table.iloc[index,16],'GoalKicksLaunch%':data_table.iloc[index,17],'GoalKicksAvgLen':data_table.iloc[index,18],'Opp':data_table.iloc[index,19],'Stp':data_table.iloc[index,20],'Stp%':data_table.iloc[index,21],'#OPA':data_table.iloc[index,22],'AvgDist':data_table.iloc[index,23]},ignore_index=True)
        if x == 17: #Shots
            data_table.columns = data_table.columns.droplevel(0)

            # print(data_table.dtypes)

            for (index,row) in data_table.iterrows(): 
                # print(row['Minute'])
                # print(len(row['Minute']))
                player_row=(dom.xpath(f'//*[@id="shots_all"]/tbody/tr[{index+1}]/td[1]/a'))
                sca1_href=(dom.xpath(f'//*[@id="shots_all"]/tbody/tr[{index+1}]/td[9]/a'))
                sca2_href=(dom.xpath(f'//*[@id="shots_all"]/tbody/tr[{index+1}]/td[11]/a'))

                # print(player_href)
                if len(player_row) == 0:
                    continue
                else:
                    player_href=(dom.xpath(f'//*[@id="shots_all"]/tbody/tr[{index+1}]/td[1]/a')[0].get('href'))
                    playerid=player_href.split('/')[3]
                    team_href=(dom.xpath(f'//*[@id="shots_all"]/tbody/tr[{index+1}]/td[2]/a')[0].get('href'))
                    teamid=team_href.split('/')[3]
                    if len(sca1_href) == 0:
                        sca1player=''
                    else:
                        sca1_href=(dom.xpath(f'//*[@id="shots_all"]/tbody/tr[{index+1}]/td[9]/a')[0].get('href'))
                        sca1player=sca1_href.split('/')[3]
                    if len(sca2_href) == 0:
                        sca2player=''
                    else:
                        sca2_href=(dom.xpath(f'//*[@id="shots_all"]/tbody/tr[{index+1}]/td[11]/a')[0].get('href'))
                        sca2player=sca2_href.split('/')[3]
                shots_table = shots_table._append({'matchid':matchmatchid,'Minute':data_table.iloc[index,0],'playerid':playerid,'Player':data_table.iloc[index,1],'TeamId':teamid,'Team':data_table.iloc[index,2],'xG':data_table.iloc[index,3],'PSxG' :data_table.iloc[index,4],'Outcome':data_table.iloc[index,5], 'Distance':data_table.iloc[index,6],'Body Part':data_table.iloc[index,7],'Notes':data_table.iloc[index,8],'Sca1PlayerId':sca1player,'Sca1Player':data_table.iloc[index,9],'Sca1Event':data_table.iloc[index,10],'Sca2PlayerId':sca2player,'Sca2Player':data_table.iloc[index,11], 'Sca2Event':data_table.iloc[index,12]},ignore_index=True)
    # print(shots_table)
    # time.sleep(random.uniform(4, 5))
    time.sleep(1)

#Match Summary append to table
matchsummary_table =pd.concat([matchsummary_table,home_formation_table], axis=1)
matchsummary_table =pd.concat([matchsummary_table,away_formation_table], axis=1)
matchsummary_table =pd.concat([matchsummary_table,matchsummarymain_table], axis=1)


# Print all 0,1,2 table to match_summary.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/match_summary.txt'):
    matchsummary_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/match_summary.txt', sep='|',mode= 'a',index=False, header=False)
else:
    matchsummary_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/match_summary.txt', sep='|',index=False, header=True)

#Print all 3,10 table to teamsummary_footer.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teamsummary_footer.txt'):
    teamsummaryfooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamsummary_footer.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teamsummaryfooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamsummary_footer.txt', sep='|',index=False, header=True)

#Print all 3,10 table to teamsummary.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teamsummary.txt'):
    teamsummary_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamsummary.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teamsummary_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamsummary.txt', sep='|',index=False, header=True)

#Print all 4,11 table to teamsummary_footer.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teampassingfooter.txt'):
    teampassingfooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teampassingfooter.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teampassingfooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teampassingfooter.txt', sep='|',index=False, header=True)

#Print all 4,11 table to teamsummary.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teampassing.txt'):
    teampassing_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teampassing.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teampassing_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teampassing.txt', sep='|',index=False, header=True)

#Print all 5,12 table to teampasstype.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teampasstype.txt'):
    teampasstype_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teampasstype.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teampasstype_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teampasstype.txt', sep='|',index=False, header=True)

#Print all 5,12 table to teampasstypefooter.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teampasstypefooter.txt'):
    teampasstypefooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teampasstypefooter.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teampasstypefooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teampasstypefooter.txt', sep='|',index=False, header=True)

#Print all 6,13 table to teamdefence.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teamdefence.txt'):
    teamdefence_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamdefence.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teamdefence_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamdefence.txt', sep='|',index=False, header=True)

#Print all 6,13 table to teamdefencefooter.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teamdefencefooter.txt'):
    teamdefencefooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamdefencefooter.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teamdefencefooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamdefencefooter.txt', sep='|',index=False, header=True)

#Print all 7,14 table to teamposessionfooter.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teamposessionfooter.txt'):
    teamposessionfooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamposessionfooter.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teamposessionfooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamposessionfooter.txt', sep='|',index=False, header=True)

#Print all 7,14 table to teamposession.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teamposession.txt'):
    teamposession_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamposession.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teamposession_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teamposession.txt', sep='|',index=False, header=True)

#Print all 8,15 table to teammiscfooter.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teammiscfooter.txt'):
    teammiscfooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teammiscfooter.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teammiscfooter_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teammiscfooter.txt', sep='|',index=False, header=True)

#Print all 8,15 table to teammisc.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/teammisc.txt'):
    teammisc_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teammisc.txt', sep='|',mode= 'a',index=False, header=False)
else:
    teammisc_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/teammisc.txt', sep='|',index=False, header=True)

#Print all 9,16 table to keeper.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/keeper.txt'):
    goalkeeper_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/keeper.txt', sep='|',mode= 'a',index=False, header=False)
else:
    goalkeeper_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/keeper.txt', sep='|',index=False, header=True)

#Print 7 table to shots.txt
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/shots.txt'):
    shots_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/shots.txt', sep='|',mode= 'a',index=False, header=False)
else:
    shots_table.to_csv('C:/Users/User/Desktop/Code/scraping/data/shots.txt', sep='|',index=False, header=True)

# print match details
if os.path.exists('C:/Users/User/Desktop/Code/scraping/data/main.txt'):
    merged_df.to_csv('C:/Users/User/Desktop/Code/scraping/data/main.txt', sep='|',mode= 'a',index=False, header=False)
else:
    merged_df.to_csv('C:/Users/User/Desktop/Code/scraping/data/main.txt', sep='|',index=False, header=True)
