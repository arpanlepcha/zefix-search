import re
from ftplib import FTP
from threading import Thread

from utils import file_path


class FtpMixin():
    def _get_connection(self):
        client = FTP('ftp.zefix.ch')
        client.login()
        client.cwd('hrdata/vortag/')
        return client

class ZefixFetcher(object, FtpMixin):

    def __init__(self):
        self.client = self._get_connection()

    def fetch_records(self):
        files = self.client.nlst()
        threads = []
        downloaded_files = [file for file in files if self.match_file(file)]

        for file in downloaded_files:
            downloader = Async(file)
            threads.append(downloader)
            downloader.start()

        for thread in threads:
            thread.join()

        self.client.close()

        return sorted([file_path(file) for file in downloaded_files])

    def match_file(self, file):
        return re.match('f[bi]-\d+-\d+\.gz', file) is not None


class Async(Thread, FtpMixin):
    def __init__(self, file):
        super(Async, self).__init__()
        self.conn = self._get_connection()
        self.file  = file
        self.fp = open(file_path(file), 'wb+')

    def run(self):
        self.conn.voidcmd('TYPE I')
        socket = self.conn.transfercmd('RETR '+self.file)

        while True:
            data = socket.recv(8192)
            if not data:
                break
            self.fp.write(data)

        # send no-op to stop the hanging
        self.conn.voidcmd('NOOP')
        socket.close()
        self.conn.close()
        self.fp.close()