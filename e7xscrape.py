import collections.abc
collections.Callable = collections.abc.Callable

import urllib.parse, urllib.error, urllib.request
from bs4 import BeautifulSoup
import ssl
import re
import pandas as pd

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://epic7x.com/characters/"
request_site = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(request_site, context=ctx).read()

soup = BeautifulSoup(html, "html.parser")

tags = soup("script")
counter = 0
for tag in tags:
    if counter == 8:
        new_tag = f'{tag}'
        break
    counter += 1

cleaned = new_tag[152:106439].rstrip()
result = re.findall("\{.*?\}", cleaned)

dict = {}
for res in result:   
    icon = res.index("icon")
    
    if res[9:icon-3] == "Support Model Brinus":
        continue 

    link = res.index('link')
    rar = res.index("rarity")
    cla = res.index("class")
    ele = res.index("element")
    hor = res.index("horoscope")
    max = res.index("max")
    att = res.index("attack")
    hea = res.index("health")
    defe =res.index("defense")
    spd = res.index("speed")
    link_end = res.index('","stats')
    dict[f"{res[9:icon-3]}"] = {}
    dict[f"{res[9:icon-3]}"]["link"] = res[link+7:link_end].replace("\/", "/")
    dict[f"{res[9:icon-3]}"]["info"] = {}
    dict[f"{res[9:icon-3]}"]["info"]["rarity"] = res[rar+9]
    dict[f"{res[9:icon-3]}"]["info"]["class"] = res[cla+8:ele-3]
    dict[f"{res[9:icon-3]}"]["info"]["horoscope"] = res[hor+12:link-3]  
    dict[f"{res[9:icon-3]}"]["info"]["attack"] = int(res[att+9:hea-3])
    dict[f"{res[9:icon-3]}"]["info"]["health"] = int(res[hea+9:defe-3])
    dict[f"{res[9:icon-3]}"]["info"]["defense"] = int(res[defe+10:spd-3])

for char in dict:
    char_link = dict[char]["link"]
    request_site = urllib.request.Request(char_link, headers={"User-Agent": "Mozilla/5.0"})

    html = urllib.request.urlopen(request_site, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    tags = soup("tr")
    i = 0

    if dict[char]["info"]["rarity"] == "5":
        for tag in tags:
            if i == 7:
                stat_table = tag
            i += 1
    elif dict[char]["info"]["rarity"] == "4":
        for tag in tags:
            if i == 9:
                stat_table = tag
            i += 1
    elif dict[char]["info"]["rarity"] == "3":
        for tag in tags:
            if i == 11:
                stat_table = tag
            i += 1

    stat = []
    try:
        for child in stat_table.children:
            try:
                for kid in child.children:
                    try:
                        for baby in kid.children:
                            if f"{baby}"[0] != " ":
                                try:
                                    new_baby = int(baby)
                                except:
                                    new_baby = int(baby[:-1])
                                stat.append(new_baby)
                            else:
                                start = baby.index("(") +1
                                try:
                                    end = baby.index("%")
                                except:
                                    end = baby.index(")")
                                stat[prev] += int(baby[start:end])
                            prev = len(stat) - 1 
                    except:
                        pass
            except:
                pass
    except:
        pass

    dict[char]["info"]["crit chance"] = stat[0]
    dict[char]["info"]["crit damage"] = stat[1]
    dict[char]["info"]["effectiveness"] = stat[2]
    dict[char]["info"]["effectiveness resistance"] = stat[3]
    dict[char]["info"]["speed"] = stat[4]

    if len(dict[char]["info"]) != 11:
        print(f"Len Mismatch for {char}, {dict[char]['info']}")
        break

    print(f"running................ {char}")

    print(stat)

new_dict = {}
for char in dict:
    try:
        new_dict["name"].append(char)
    except:
        new_dict["name"] = [char]
    
    for stuff in dict[char]["info"]:
        try:
            new_dict[f"{stuff}"].append(dict[char]["info"][stuff])
        except:
            new_dict[f"{stuff}"] = [dict[char]["info"][stuff]]

print(new_dict)

df = pd.DataFrame(new_dict)
df.to_csv(f"e7HeroData.csv")


