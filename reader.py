# -*- coding: utf-8 -*-
import csv
import gzip
import json

import marisa_trie

from utils import file_path


class Reader(object):
    def __init__(self, fb_file, fi_file):
        self.fi_fieldnames = [
            'id', 'zefix', 'rechts_form_id', 'firma', 'regd_office_nr',
            'regd_office_name', 'commercial_regd_no', 'capital', 'currency_id',
            'status_id', 'close_date', 'open_date', 'shab_nr', 'shab_site', 'mutation_id',
            'mutation_date', 'shab_seq', 'address', 'care_of', 'strasse', 'house_no',
            'addr_additional', 'post_box', 'zip', 'place_name', 'purpose', 'uid'
        ]
        self.fb_fieldnames = ['id', 'i', 'j', 'lang', 'v', 'name', 'start', 'end']
        self.fi_file = fi_file
        self.fb_file = fb_file

    def run(self):
        data = {}
        keys = []
        values = []

        with gzip.open(self.fi_file, 'r') as fi:
            fi_reader = csv.DictReader(fi, fieldnames=self.fi_fieldnames, delimiter='\t')

            for row in fi_reader:
                data[row['id']] = {'zefix': row['zefix'].strip(), 'uid': row['uid'].strip()}

            with gzip.open(self.fb_file, 'r') as fb:
                fb_reader = csv.DictReader(fb, fieldnames=self.fb_fieldnames, delimiter='\t')

                for row in fb_reader:
                    zefix = data.get(row['id'])

                    if zefix is None:
                        continue

                    name = unicode(row['name'], 'ISO-8859-1')
                    keys.append(name.lower())

                    values.append(
                        json.dumps({'zefix': zefix['zefix'], 'name': name, 'uid': zefix['uid']})
                    )

                trie = marisa_trie.BytesTrie(zip(keys, values))
                trie.save(file_path('zefix.ds'))