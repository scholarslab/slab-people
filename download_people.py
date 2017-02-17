#!/usr/bin/env python3


import csv
import requests
from urllib.parse import urljoin
from collections import namedtuple


HOST = 'http://scholarslab.org/'
OUTPUT = 'people.csv'
FIELDS = ('date', 'name', 'category', 'description')

Person = namedtuple('Person', FIELDS)


def get_people(host=HOST):
    """Download all posts with post-type of people."""
    page = 1
    while True:
        resp = requests.get(
            urljoin(host, '/wp-json/posts'),
            params={
                'type': 'people',
                'page': page,
                },
            )

        chunk = resp.json()
        if not chunk:
            break
        yield from chunk

        page += 1


def to_person(p):
    """Extracts the information we want out of a WP people post-type."""
    try:
        return Person(
            p['date'],
            p['title'],
            ', '.join(cat['name'] for cat in p['terms']['people-category']),
            p['content'],
            )
    except:
        import pprint
        print('ERROR ON: {}'.format(pprint.pformat(p)))
        raise


def main():
    with open(OUTPUT, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(Person._fields)
        writer.writerows(to_person(p) for p in get_people())


if __name__ == '__main__':
    main()
