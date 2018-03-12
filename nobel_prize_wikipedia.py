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


if __name__ == "__main__":


    fname = 'nobel_wiki.html'
    
    try:
        with open(fname, 'r') as f:
            soup = f.readlines()
    
        page = "\n".join(soup)
    
    except:
    
        link = 'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_university_affiliation'
    
        with urllib.request.urlopen(link) as response:
            page = response.read()
    
    
    soup = bs(page, 'html.parser')
    
    
    a = soup.select('table.wikitable')
    
    tables = [x for x in a if isNeededTable(x) is True]
    
    a = tables[0]
    
    titles = a.contents[3].select('a')
    aff_name = titles[0].get_attribute_list('title')
    
    # aff_name = get_aff_name(a)
    
    # aff_names = ([{i: get_aff_name(x)} for i, x in enumerate(tables)])
