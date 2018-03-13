import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import urllib.request
from pprint import pprint as pp


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
        html_table = x.next.next.next.next.next.next

        # print(aff_name)
        # print(aff_name)
        # print(html_table)

        # aaa.append({aff_name: html_table})
        aaa.append({'name': aff_name,
                    'html_table': html_table})

    return aaa


def extract_aff_name(x):

    aff_name = [x.select('a')[0].get_attribute_list('title')[0], 
                x.select('a')[0].get_text()]

    return aff_name



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
    
    aaa = affs_in_table[0]
    
    aaa2 = aaa.find_next('tr').find_next('tr')
    counter = 0
    while(counter < 5):
        aaa2 = aaa.find_next('tr')
        
        if aaa2.has_attr('valign'):
            break
        else:
            aaa = aaa2
            counter = counter + 1
    
    bbb = affs_in_table[-1]
    # bbb2 = affs_in_table[]

    # a = tables[-1]
    # affs_in_table = find_aff(a.select('td'))
    # qqq = get_aff_table(affs_in_table)

    # html_tables = affs_in_table[0].next.next.next.next.next.next
    # html_tables = [x.next.next.next.next.next.next for x in affs_in_table]

    # aaa = html_tables[0]


    # qqq = extract_aff_name(aaa)
