"""
Programming an actual data-scraper application was new to me. Additionally, I have not worked extensively
with Pandas before this. Much of this code was based off of the following website:
    https://st2.ning.com/topology/rest/1.0/file/get/1483294544?profile=original
Though some parts of my code were directly lifted, I played around with this code for many hours and tried to
the best of my ability to understand everything it does.

Beautiful Soup is a library that makes it beautiful to scrape information soup from web pages.
It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.
"""

import os
import pandas as pd
import numpy as np
from requests import get
from contextlib import closing
from bs4 import BeautifulSoup
pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 18)


def simple_get(url):
    # Attempts to get the content at `url` by making an HTTP GET request. If the content-type of response
    # is some kind of HTML/XML, return the text content, otherwise return None.
    with closing(get(url, stream=True)) as resp:
        content_type = resp.headers['Content-Type'].lower()
        if resp.status_code == 200 and content_type is not None and content_type.find('html') > -1:
            return resp.content
        else:
            return None


def getKPommy():
    if os.path.exists('KenPom.csv'):
        print("Retrieving Saved KenPom Data...")
        KenPom = pd.read_csv('KenPom.csv')
    else:
        print("No local KenPom data found. Retrieving from the web...")
        dictionary = {}
        baseURL = "https://kenpom.com/index.php?y="
        for Season in range(2002, 2022):
            print("Collecting {} Data...".format(Season))
            URL = baseURL + str(Season)
            rawHTML = simple_get(URL)
            HTML = BeautifulSoup(rawHTML, 'html5lib')
            # "soupNugget.text" grabs the actually relevant info within each "td" group (see example below)
            data = [soupNugget.text for soupNugget in HTML.select("td")]      # (7413,)   type='list'
            dictionary[Season] = pd.DataFrame(np.array(data).reshape(int((len(data)/21)), 21))
            dictionary[Season].columns = ['rank', 'school', 'conference', 'w_l', 'adjem', 'adjo', 'adjoR', 'adjd', 'adjdR',
                                        'adjt', 'adjtR', 'luck', 'luckR', 'adjems', 'adjemsR', 'oppos', 'opposR', 'oppds',
                                        'oppdsR', 'adjemn', 'adjemnR']

        KenPom = pd.DataFrame(columns=['rank', 'school', 'conference', 'w_l', 'adjem', 'adjo', 'adjoR', 'adjd', 'adjdR',
                                           'adjt', 'adjtR', 'luck', 'luckR', 'adjems', 'adjemsR', 'oppos', 'opposR',
                                           'oppds', 'oppdsR', 'adjemn', 'adjemnR', 'seed', 'name'])
        for Season in reversed(list(dictionary.keys())):
            temp = dictionary[Season]
            temp['Season'] = Season
            KenPom = pd.concat([KenPom, temp], sort=False)

        KenPom.reset_index(inplace=True, drop=True)      # Resets lots of duplicated indices ---- very important!!

        # Create 'seed' and 'name' columns
        KenPom['name'] = KenPom['name'].str.replace('[*]', '')
        KenPom['school'] = KenPom['school'].str.replace('[*]', '')
        for idx, school in enumerate(KenPom['school']):
            if school.split()[-1].isdigit():
                KenPom.loc[idx, 'seed'] = int(school.split()[-1])
                KenPom.loc[idx, 'name'] = " ".join(school.split()[:-1])
                KenPom.loc[idx, 'school'] = " ".join(school.split()[:-1])
            else:
                KenPom.loc[idx, 'seed'] = 0
                KenPom.loc[idx, 'name'] = school

        # Add TeamID column
        spellings = pd.read_csv('Data\MTeamSpellings.csv', sep='\,', engine='python')
        KenPom['name'] = KenPom['name'].str.lower()
        KenPom = KenPom.merge(spellings, left_on=['name'], right_on=['TeamNameSpelling'], how='left')

        # Create 'win', 'loss', 'win%' columns
        KenPom['wins'] = [int(record.split("-")[0]) for record in KenPom['w_l']]
        KenPom['losses'] = [int(record.split("-")[1]) for record in KenPom['w_l']]
        KenPom['wpct'] = KenPom['wins'] / (KenPom['wins'] + KenPom['losses'])

        metaData = [['rank', 'int'], ['adjem', 'float'], ['adjo', 'float'], ['adjoR', 'int'], ['adjd', 'float'],
                    ['adjdR', 'int'], ['adjt', 'float'], ['adjtR', 'int'], ['luck', 'float'], ['luckR', 'int'],
                    ['adjems', 'float'], ['adjemsR', 'int'], ['oppos', 'float'], ['opposR', 'int'], ['oppds', 'float'],
                    ['oppdsR', 'int'], ['adjemn', 'float'], ['adjemnR', 'int'], ['seed', 'int'], ['name', 'str'],
                    ['Season', 'int'], ['TeamID', 'int']]

        for data in metaData:
            KenPom[data[0]] = KenPom[data[0]].astype(data[1])

        KenPom = KenPom[['Season', 'rank', 'school', 'TeamID', 'seed', 'conference', 'wins', 'losses', 'wpct', 'adjem',
                         'adjo', 'adjd', 'adjt', 'luck', 'adjems', 'oppos', 'oppds', 'adjemn', 'adjoR', 'adjdR', 'adjtR',
                         'luckR', 'adjemsR', 'opposR', 'oppdsR', 'adjemnR']]
        KenPom.to_csv("KenPom.csv", index=False)

    return KenPom

if __name__ == '__main__':
    KenPom = getKPommy()

    # Practice queries
    print("Prints Top and Bottom of file")
    print(pd.concat([KenPom.head(), KenPom.tail()], sort=False))
    print("Prints 5 random entries")
    print(KenPom.sample(5))
    print("Prints number of teams that played each Season")
    print(KenPom['Season'].value_counts())
    print("Prints B1G Conference for 2017-2018")
    print(KenPom.loc[(KenPom['conference'] == "B10") & (KenPom['Season'] < 2019) & (KenPom['Season'] > 2016)])
    print("Prints B1G Conference for 2017-2018, sorted by win%")
    print(KenPom.sort_values('wpct', ascending=False).loc[(KenPom['conference'] == "B10") & (KenPom['Season'] < 2019) & (KenPom['Season'] > 2016)])
    print("Prints the first 10 columns (except conference) of every Michigan season")
    print(KenPom.loc[KenPom['school'] == "Michigan", list(KenPom.columns)[:10]].drop(columns=['conference', 'TeamID']))
    print("Prints quick peek of top 2019 contenders")
    print(KenPom.loc[KenPom['Season'] == 2019].head(10))
    print("Prints the 15 2020 teams with the least losses")
    print(KenPom.sort_values(by=['losses', 'wins'], ascending=[True, False]).loc[KenPom['Season'] == 2020].head(15))

    # print(soupNugget, soupNugget.text)

'''
wpct: Winning Percentage
adjem: Adjusted Efficiency Margin
adjo: Adjusted offensive efficiency: points scored per 100 possessions (adjusted for opponent)
adjd: Adjusted defensive efficiency: points allowed per 100 possessions (adjusted for opponent)
adjt: Adjusted tempo: Possessions per 40 minutes
luck: Luck rating
oppos: Adjusted opposing offensive strength
oppds: Adjusted opposing defensive strength
adjemn: Adjusted Efficiency Margin (Non-conference)
"..."R: <that metric> Ranked
'''