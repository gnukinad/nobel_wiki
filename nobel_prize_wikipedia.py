import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import urllib.request
from pprint import pprint as pp
import re


# all functions are applicable to a specified link only, do not attempt to use these functions to your own custom web-page
def isNeededTable(a):

    t = 'Affiliations'

    aaa = a.contents[1]
    bbb = [xx.strip() for xx in aaa.text.split('\n') if xx != '']

    if t in bbb:
        return True
    else:
        return False


def get_aff_name(a):

    titles = a.contents[3].select('a')
    aff_name = titles[0].get_attribute_list('title')

    print(aff_name)


    return aff_name[0]


def find_aff(a):

    # which elements contain 'colspan'
    all_colspans = [x for x in a if x.has_attr('colspan')]

    # which colspan does not '<b>Notes</b>' in them
    all_affs = [x for x in all_colspans if len(x.select('b')) == 0]

    # remove <big>Break Records</big>
    all_affs = [x for x in all_affs if len(list(x.children)) != 0]

    # remove notes
    all_affs = [x for x in all_affs if 'Note:' not in x.text]

    return all_affs


def get_aff_table(a):

    # html_tables = [x.next.next.next.next.next.next for x in a]

    aaa = []

    for i, x in enumerate(a):
        # print('i, ', i, ' x ', x)
        aff_name = extract_aff_name(x)

        # version1 that worked for several tables
        # html_table = x.next.next.next.next.next.next

        tmp = x

        counter = 0
        while(counter < 3):

            # print('counter is ', counter)
            html_table = tmp.find_next('tr')
            

            '''
            # version2 which worked for all tables except the last
            if html_table.has_attr('valign'):
                print('breaking out')
                break
            else:
                print('getting deeper')
                tmp = html_table
                counter = counter + 1
            '''

            # version3 which works for all tables
            if len(html_table.select('td')) > 2:
                # print('breaking out')
                break
            else:
                # print('getting deeper')
                tmp = html_table
                counter = counter + 1

        aaa.append({'title_aff_name': aff_name['title_aff_name'],
                    'text_aff_name': aff_name['text_aff_name'],
                    'html_table': html_table})

    return aaa


def extract_aff_name(x):

    aff_name = {'title_aff_name': x.select('a')[0].get_attribute_list('title')[0], 
                'text_aff_name': x.select('a')[0].get_text()}

    return aff_name


def extract_data_from_col(a, aff_name):

    col = a.select('td')[1]
    lis = col.select('li')
    re_year = re.compile(r'\b\d{4}\b')
    re_phd = re.compile(r'\b(phd)\b', re.I)

    ress = []


    for i, x in enumerate(lis):

        # if PhD --> extract
        
        # print('i ', '\tx ', x)

        # if '(PhD)' in x.text:
        # print(x.text)
        # print(re_phd.match(x.text))
        # if re_phd.match(x.text):
        if 'phd' in x.text.lower():
            
            try:

                field = x.find('abbr').get_attribute_list('title')[0].lower()
                
                tmp = x.find_next('a')
                title_name = tmp.get_attribute_list('title')[0]
                name = tmp.text
                
                # print('title_name is ', title_name, '\tname is ', name)
                
                year = re_year.findall(x.text)[0]
                # print(year)
                
                res = {'title_aff_name': aff_name['title_aff_name'],
                       'text_aff_name': aff_name['text_aff_name'],
                       'year': year,
                       'field': field,
                       'name': name,
                       'title_name': title_name,
                       'degree': 'phd'}
                
                ress.append(res)

            except:
                pass

        
    if len(ress) == 0:

        res = {'title_aff_name': aff_name['title_aff_name'],
               'text_aff_name': aff_name['text_aff_name']}
        return [res]
    else:
        return ress



if __name__ == "__main__":


    fname = 'nobel_wiki.html'
    
    try:
        with open(fname, 'r') as f:
            soup = f.readlines()
    
        page = "\n".join(soup)

        print('reading page from local storage')

    except:

        link = 'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_university_affiliation'

        with urllib.request.urlopen(link) as response:
            page = response.read()

        print('reading page from web storage')


    soup = bs(page, 'html.parser')

    a = soup.select('table.wikitable')

    tables = [x for x in a if isNeededTable(x) is True]

    affs_in_table = []
    [affs_in_table.extend(find_aff(x.select('td'))) for x in tables]
    affs_in_dict = get_aff_table(affs_in_table)
    
    affs_data = []

    # for i in range(len(affs_in_dict[:5])):
    for i in range(len(affs_in_dict)):

        res = extract_data_from_col(affs_in_dict[i]['html_table'], 
                                    {'title_aff_name': affs_in_dict[i]['title_aff_name'],
                                     'text_aff_name': affs_in_dict[i]['text_aff_name']
                                     })
        affs_data.append(res)

    # putting everything into a single df
    df = pd.concat([pd.DataFrame(x) for x in affs_data], ignore_index=True).replace(np.nan, '')

    # removing empty entries
    df = df[df['field'] != '']
    
    df.to_excel('wikipedia_nobel_prize.xlsx')
