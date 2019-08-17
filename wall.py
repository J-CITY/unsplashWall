import urllib.request
import re
import random

TYPE_WALLPAPER = "wallpapers"
TYPE_TEXTURES = "textures-patterns"
TYPE_NATURE = "nature"
TYPE_EVENTS = "current-events"
TYPE_ARCHITECTURE = "architecture"
TYPE_BUSINESS = "business-work"
TYPE_FILM = "film"
TYPE_ANIMALS = "animals"
TYPE_TRAVEL = "travel"
TYPE_FASHION = "fashion"
TYPE_FOOD = "food-drink"
TYPE_SPIRITUAL = "spirituality"
TYPE_EXPERIMENTAL = "experimental"
TYPE_PEOPLE = "people"
TYPE_HEALTH = "health"
TYPE_ARTS = "arts-culture"

class Config:
    def __init__(self):
        pass

    TYPE = TYPE_ARTS
    
    TOP_ONE = True

    WALL_URL = "https://unsplash.com"

    NAME = "wall.jpg"

    TAG = "" # any string

config = Config()
lines = []
if config.TAG == "":
    lines = urllib.request.urlopen(config.WALL_URL + "/t/" + config.TYPE)
else:
    lines = urllib.request.urlopen(config.WALL_URL + "/search/photos/" + config.TAG)
txt = ""
for line in lines.readlines():
    txt += str(line)


finds = re.findall(r'<a title="View the photo by.{1,100} href=".{1,30}">', txt)

links = []

for f in finds:
    #print(f)
    hrefs = re.findall(r'href=".{1,40}"', f)
    for h in hrefs:
        pos = h.find('"')
        if pos > 0:
            links.append(h[pos+1:-1])

if links == []:
    print("Can not find images")
    exit()

link = ""
if config.TOP_ONE:
    link = config.WALL_URL + links[0]
else:
    link = config.WALL_URL + random.choice(links)

#GET CUR IMAGE
lines = urllib.request.urlopen(link)
txt = ""
for line in lines.readlines():
    txt += str(line)
finds = re.findall(r'<a title="Download photo" href=".{1,140}" rel', txt)

if finds == []:
    print("Can not find image block")
    exit()

href = re.findall(r'href=".{1,140}"', finds[0])
if href == []:
    print("Can not find image href block")
    exit()


imgLink = ""
pos = href[0].find('"')
if pos > 0:
    imgLink = href[0][pos+1:-1]

print("Load: ", imgLink)
if imgLink == "":
    print("Can not find image link")
    exit()
urllib.request.urlretrieve(imgLink, config.NAME)
