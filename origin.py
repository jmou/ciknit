from collections import defaultdict
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup

# XXX narrow
ORIGINS = [
    'african',
    'american',
    'arabic',
    'aramaic',
    'armenian',
    'australian',
    'babylonian',
    'basque',
    'british',
    'bulgarian',
    'cambodian',
    'celtic',
    'chinese',
    'czech',
    'danish',
    'dutch',
    'egyptian',
    'finnish',
    'french',
    'gaelic',
    'german',
    'ghanaian',
    'greek',
    'hawaiian',
    'hebrew',
    'hungarian',
    'indian',
    'irish',
    'italian',
    'japanese',
    'korean',
    'latin',
    'mexican',
    'native-american',
    'nigerian',
    'norse',
    'norwegian',
    'persian',
    'polish',
    'portuguese',
    'russian',
    'sanskrit',
    'scandinavian',
    'scottish',
    'slavic',
    'spanish',
    'swahili',
    'swedish',
    'turkish',
    'ukrainian',
    'uncertain',
    'vietnamese',
    'welsh',
    'yiddish',
]

name_origins = defaultdict(list)
for origin in ORIGINS:
    try:
        # XXX generalize to boys?
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
