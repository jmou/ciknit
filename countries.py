from collections import defaultdict
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup


doc = urlopen('https://www.thebump.com/b/baby-name-origins')
soup = BeautifulSoup(doc, 'html.parser')
origins = [a['href'].removeprefix('/b/').removesuffix('-baby-names')
           for a in soup.select('.origins-name-list a')]

name_origins = defaultdict(list)
for origin in origins:
    try:
        doc = urlopen(f'https://www.thebump.com/b/{origin}-baby-girl-names')
    except HTTPError:
        doc = urlopen(f'https://www.thebump.com/b/{origin}-baby-names')
    soup = BeautifulSoup(doc, 'html.parser')
    for elem in soup.select('.name'):
        name_origins[elem.text].append(origin.capitalize())

print('name,origin')
for name, origins in name_origins.items():
    slashed_origins = '/'.join(origins)
    print(f"{name},{slashed_origins}")
