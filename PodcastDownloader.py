#!/bin/env python3
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import os
import sys

podcastfolder = Path(os.getenv("PODCAST_FOLDER", "Podcasts"))

def getFeed(url):
    req = requests.get(url)
    return req.text

def getItemList(feed):
    soup = BeautifulSoup(feed, "xml");
    data = { "title": soup.rss.channel.title.contents[0],
            "items": list()}
    print("Fetched podcast: {}".format(data["title"]))
    for t in soup.rss.channel("item"):
        data["items"].append(
                { "title": t.title.contents[0],
                    "enclosure": t.enclosure["url"],
                    "type": t.enclosure["type"]
                }
                )
    return data

def downloadMissing(data):
    p = podcastfolder / data["title"]
    if not p.exists():
        p.mkdir(parents=True)
    for i in data["items"]:
        if not (i["type"] == "audio/mp3" or i["type"] == "audio/mpeg"):
            continue
        pi = p / (i["title"] + ".mp3")
        if pi.exists():
            continue
        try:
            with open(pi, "wb") as f:
                print("Downloading: Podcast: {} Title: {} URL: {}".format(data["title"], i["title"], i["enclosure"]))
                req = requests.get(i["enclosure"])
                f.write(req.content)
        except KeyboardInterrupt:
            print("Cancelled aborting and deleting the last file")
            pi.unlink()
            sys.exit(0)



f = getFeed(sys.argv[1])

if f is not None:
    f = getItemList(f)
if f is not None:
    downloadMissing(f)
