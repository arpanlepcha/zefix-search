# zefix-search

Tornado powered zefix-search by company name, based on public data available at zefix.ch

# Usage

* Create virtual env
* Run requirements.txt file
* Run main.py, this will generate a trie file
* Run webserver.py, the server by default runs at port 8888, you can change the port at webserver.py.
* Search by company name using http://localhost:8888/?name=deep

# Notes
You can also put main.py as a cron so that latest changes are always updated in live server.
