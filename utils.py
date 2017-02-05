# -*- coding: utf-8 -*-
import os

def root_path():
    return os.path.join(os.path.dirname(__file__))

def file_path(file):
    return os.path.join(root_path(), 'data', file)
