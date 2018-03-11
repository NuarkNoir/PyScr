# coding=UTF-8
import shutil

import requests, jsonpickle, re
import sys
from bs4 import BeautifulSoup as bs

def transform(link, size):
    return f"{link.replace('/wallpaper/', '/image/')}_{size}.jpg"


def give_back_image_struct(origlink, size):
    resp = {
        "orig": origlink,
        "fullimage": transform(origlink, size)
    }
    return resp


def parse_images_elements(domobject):
    resp = []
    for imageobj in domobject.select("li.wallpapers__item"):
        wi = imageobj.select_one("span.wallpapers__info")
        size = re.findall(r"(\d+x\d+)", wi.text.replace("\n", " ").strip()).pop()
        orlink = f"http:{imageobj.select_one('a.wallpapers__link').attrs['href']}"
        resp.append(give_back_image_struct(orlink, size))
    return resp


def get_all_walpapers(link, json=False, maxpage=0):
    fc = bs(requests.get(link).content, "html5lib")
    lp = int(fc.select("ul.pager__list a.pager__link").pop().text)
    print("Pages:", lp)
    resp = {
        "pagecout": lp,
        "link": link,
        "walpapers": []
    }
    resp["walpapers"] += parse_images_elements(fc)
    td = lp+1 if maxpage == 0 else int(maxpage)
    print("Will be parsed:", td)
    for i in range(2, td):
        fc = bs(requests.get(f"{link}/page{i}").content, "html5lib")
        resp["walpapers"] += parse_images_elements(fc)
    return jsonpickle.encode(resp, unpicklable=False) if json else resp

def serialize(string):
    if not string is str:
        string = jsonpickle.encode(string, unpicklable=False)
    with open("serialized_resp.json", "w") as f:
        f.write(string)


def download_files(serobj):
    print("Will be downloaded:", len(serobj["walpapers"]))
    for image in serobj["walpapers"]:
        try:
            lnk = image["fullimage"]
            filename = f"downloads/{lnk.split('/').pop()}"
            r = requests.get(lnk, stream=True)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        except KeyboardInterrupt:
            exit()
        except:
            continue


link = input("Walpaperscraft link:\n")
if len(link) < 10: exit("No walpaperscraft link found")
pages = int(input("How many pages to load(0 - inf.)?\n"))
print("Status: [------------------]   0% //Parsing...\r")
wlp = get_all_walpapers(link, False, pages)
print("Status: [######------------]  33% //Serializing...\r")
serialize(wlp)
print("Status: [############------]  67% //Downloading...\r")
download_files(wlp)
print("Status: [##################] 100% //Done!")