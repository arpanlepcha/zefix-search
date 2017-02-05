# -*- coding: utf-8 -*-
# this file should be ran as a cron once daily, or weekly depending upon the frequency
# of data changes

from loader import ZefixFetcher
from reader import Reader

def download_files():
    fetcher = ZefixFetcher()
    return fetcher.fetch_records()

def generate_trie(files):
    reader = Reader(*files)
    reader.run()

if __name__ == '__main__':
    files = download_files()
    generate_trie(files)
