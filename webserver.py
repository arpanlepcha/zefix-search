# -*- coding: utf-8 -*-

import json

import marisa_trie
from tornado import web, ioloop
from tornado.escape import json_encode

from utils import file_path


class MainHandler(web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(MainHandler, self).__init__(*args, **kwargs)

        self.trie = marisa_trie.BytesTrie()
        self.trie.load(file_path('zefix.ds'))

    def get(self, params):
        args = self.get_argument('name')
        companies = self.trie.items(args.lower())
        companies = [json.loads(c[1], encoding='ISO-8859-1') for c in companies]

        self.write(json_encode(companies))
        self.set_header('Content-Type', 'application/json')

def make_app():
    return web.Application([
        (r"/(.*)", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()