#!/usr/bin/env python3


import csv
import json
import os
import requests
from urllib.parse import urljoin
from collections import namedtuple


HOST = 'http://scholarslab.org/'
OUTPUT = 'people'
FIELDS = ('date', 'name', 'category', 'description')

class Person(namedtuple('Person', FIELDS)):
    __slot__ = ()

    @staticmethod
    def from_json(p):
        """Extracts the information we want out of a WP people post-type."""
        try:
            terms = p['terms']
            if terms:
                categories = ', '.join(
                    cat['name'] for cat in terms['people-category']
                    )
            else:
                categories = None

            return Person(p['date'], p['title'], categories, p['content'])
        except:
            import pprint
            print('ERROR ON: {}'.format(pprint.pformat(p)))
            raise


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


def main():
    people = list(get_people())

    csv_name = OUTPUT + '.csv'
    with open(csv_name, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(Person._fields)
        writer.writerows(Person.from_json(p) for p in people)

    json_name = OUTPUT + '.json'
    with open(json_name, 'w') as fout:
        json.dump(people, fout)


if __name__ == '__main__':
    main()
