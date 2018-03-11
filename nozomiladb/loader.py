#encoding=utf-8
from collections import Counter

import jsonpickle
from lxml import etree

import lxml.html
import requests
import re

import queue
import idna.idnadata

from exts.IDbDealer import NozomiDbDealer
from exts.Downloader import Downloader

try:
    from nozomiladb import db
except:
    import db

plink = "http://nuark.xyz/proxy.php?h&l="


def main(tag=None):
    base = "https://nozomi.la"
    to = int(input("Сколько страниц грузим?\n>> "))
    dwn = False if input("Скачивать?[std: y/n]\n>> ").lower() == "n" else True
    ot = 1
    p = 0
    for i in range(ot, to+1):
        try:
            html = requests.get(f"{plink}{base}/{'index' if not tag else 'tag/' + tag}-{i}.html").text
            parse(base, html)
        except:
            if p == 5:
                break
            p += 1
            continue
    if dwn:
        download()


def parse(base, html):
    database = db
    ndealer = NozomiDbDealer(database)
    with ndealer:
        root = lxml.html.fromstring(html)
        root.make_links_absolute(base)
        posts = [x.attrib["href"] for x in root.cssselect("div.thumbnail-div a")]
        for post in posts:
            post = post.split("#")[0]
            try:
                print("Dealing with post: " + post)
                if ndealer.element_exists(post):
                    print("\tThis post exists")
                    continue
                html = requests.get(plink + post).text
                root = lxml.html.fromstring(html)
                root.make_links_absolute(base)
                image = root.cssselect("div.post img")[0].attrib["src"]
                sidebar = root.cssselect("div.sidebar")[0]
                chrs, series, artist, tags, uls = [], [], [], [], sidebar.cssselect("ul")
                for i, span in enumerate(sidebar.cssselect("span.title")):
                    title = span.text.strip()
                    if title == "Characters":
                        chrs = [x.text for x in uls[i].cssselect("li a")]
                    elif title == "Series":
                        series = [x.text for x in uls[i].cssselect("li a")]
                    elif title == "Artist":
                        artist = [x.text for x in uls[i].cssselect("li a")]
                    elif title == "Tags":
                        tags = [x.text for x in uls[i].cssselect("li a")]
                chrs = "|".join(chrs)
                series = "|".join(series)
                artist = "|".join(artist)
                tags = "|".join(tags)
                ndealer.put_elements(chrs, series, artist, tags, image, post)
                print("\tThis post done")
            except Exception as e:
                print("Error with post:", post, e)
                continue


def download():
    database = db
    ndealer = NozomiDbDealer(database)
    with ndealer:
        res = list(ndealer.db.get_all())
        for item in res:
            if item[7] == 1:
                print("File from post already downloaded: " + item[6])
                continue
            filename = str(str(item[0]) + " - " + item[1] + " - " + item[2])[:150] + "." + item[5].split(".").pop()
            d = Downloader()
            try:
                d.download(item[5], filename)
                ndealer.db.execute(f"UPDATE NozomiLa SET downloaded = 1 WHERE id = {item[0]}; COMMIT;")
            except Exception as e:
                print("Hmm, exception:", e)
                continue

if __name__ == '__main__':
    jdownload = True if input("Скачиваем DB?[y/std: n]\n>> ").strip() == "y" else False
    if jdownload:
        download()
    else:
        tag = input("Грузим тэг?\n(https://nozomi.la/tag/{ТЭГ}-1.html)\n(можно оставить пустым)\n>> ").strip()
        if len(tag.strip()) == 0:
            tag = None
        plink = plink if input("Проксируем?[y/std: n]\n(мб медленно, зато в обход блокировок)\n>> ").lower() == "y" else ""
        main(tag)
