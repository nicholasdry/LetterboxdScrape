####################################
#
#   scraper.py
#   Nicholas Dry
#
####################################
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import threading

# Setup command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-user", help="User you want to scrape data for")
parser.add_argument("-info", help="Section of profile you want to scrape")
args = parser.parse_args()

# This list will allow the threads to simulateneously access it.
movies = []

# Global command line arguments.
username = ""
target = ""

if args.user:
    username = args.user
    if args.info:
        target = args.info
    else:
        raise Exception("Please input a target to scrape")
else:
    raise Exception("Please input a username.")

# Again, global output file for the threads.
output_file = open("{0}-watchlist.txt".format(username), "w")

# Class to maintain and implement the Threading Module.
class WatchlistThread(threading.Thread):
    def __init__(self, odd):
        # Super Constructor call
        threading.Thread.__init__(self)
        # Since we are running and odd page and even page thread, here is our flag.
        self.odd = odd
        if odd:
            self.name = "Odd Thread"
        else:
            self.name = "Even Thread"
    def run(self):
        # Executes when we call .start()
        print("Starting {0}".format(self.name))
        begin_scrape(self.odd)
        print("Exiting {0}".format(self.name))


def begin_scrape(odd):
    global movies

    if odd:
        ctr = 1
    else:
        ctr = 2

    while True:
        print("Viewing Page {0}".format(ctr))
        # All URLs are formatted the same way.
        base_url = "http://www.letterboxd.com/{0}/watchlist/page/{1}".format(username, ctr)
        url = urlopen(base_url)
        soup = BeautifulSoup(url, "html.parser")
        

        poster_containers = soup.findAll('li', {'class': 'poster-container'})
        if len(poster_containers) == 0:
            # We have reached the end of their watchlist, break.
            break

        for poster in poster_containers:
            # Requires some nice parsing here. 
            movie_title = str(poster).split("alt=\"")[1].split("\"")[0]
            output_file.write("{0}\n".format(movie_title))
        
        ctr += 2

# This looks at all potential options they wish to scrape, so far it's only watchlist.
if target == "watchlist":

    try:
        # Set thread objects.
        threads = [WatchlistThread(True), WatchlistThread(False)]
    except:
        raise Exception("Could not spawn threads.")
    
    # Fire off threads.
    for thread in threads:
        thread.start()
    # Wait for the to return and exit out.
    for thread in threads:
        thread.join()

