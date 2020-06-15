from core import *
import sys

if len(sys.argv) < 2:

	exit("[!] python3 main.py {url} {cookie}")


url = sys.argv[1]
cookie = sys.argv[2]
parser = XSsearch(url=url,cookies=cookie)
parser.run()
