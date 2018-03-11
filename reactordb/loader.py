#encoding=utf-8
from collections import Counter

import jsonpickle
from lxml import etree

import lxml.html
import requests
import re

import queue
import idna.idnadata

try:
    from reactordb import db
except:
    import db

def element_exists(pid, link):
    db.connect()
    res = db.find_item(pid, link)
    db.close()
    return res


def put_post(pid, user, tags, pics, date, link):
    db.connect()
    db.put(pid, user, tags, pics, date, link)
    db.close()


sel_article = "div.postContainer"
sel_user = "div.uhead_nick a"
sel_tags = "h2.taglist b a"
sel_postcontent = "div.post_content"
sel_postimages = "img"
sel_date = "span.date span span"
sel_link = "span.link_wr a.link"
sel_lastpage = "div.pagination_expanded span.current"

full_pic = lambda link: link if "/post/full/" in link else link.replace("/post/", "/post/full/")
get_last_page_num = lambda link: int(lxml.html.fromstring(requests.get(link).text).cssselect(sel_lastpage)[0].text)

plink = "http://nuark.xyz/proxy.php?h&l="

def main(_link, start=-1, stop=1, max=0, offset=0):
    base = f"{_link.replace(plink, '').split('.cc/')[0]}.cc/"
    if start == -1:
        try:
            start = get_last_page_num(_link)
        except:
            print(1)
            html = requests.get(_link).text
            parse(base, html)
            return
    if max > 0:
        stop = start - max
        if offset:
            stop -= offset
    if offset and start - offset <= 0:
        raise Exception(f"Offset matches elements above zero")
    for i in range(start-offset, stop-1, -1):
        print(i)
        html = requests.get(f"{_link}/{i}").text
        parse(base, html)


def parse(base, html):
    root = lxml.html.fromstring(html)
    root.make_links_absolute(base)
    articles = root.cssselect(sel_article)
    for article in articles:
        pid = article.attrib["id"].replace("postContainer", "")
        link = article.cssselect(sel_link)[0].attrib["href"]
        ee = element_exists(pid, link)
        print(f"[{pid}]::> {link} <::[{'EXISTS' if ee else 'NOTEXISTS'}]")
        if ee:
            continue
        user = article.cssselect(sel_user)[0].text
        tags = [x.text for x in article.cssselect(sel_tags)]
        k = ",".join(tags)
        #if "mlp gay porn" in k or "futa" in k or "guro" in k or "гуро" in k or "stuff" in k or "песочница эротики" in k:
        #    continue
        try:
            post_content = article.cssselect(sel_postcontent)[0]
            pics = [full_pic(x.attrib["src"]) for x in post_content.cssselect(sel_postimages)]
            date = " ".join([x.text_content() for x in article.cssselect(sel_date)])
            put_post(pid, user, tags, pics, date, link)
        except Exception as e:
            print(e)
            continue

if __name__ == '__main__':
    link = plink + "http://anime.reactor.cc/tag/Oppai"
    link = plink + "http://pornreactor.cc/tag/photo+porn"
    link = plink + "http://joyreactor.cc/tag/шакальная+эротика"
    link = plink + "http://joyreactor.cc/tag/Ms_modestly_immodest"
    link = plink + "http://joyreactor.cc/tag/chickpeasyx"
    link = plink + "http://joyreactor.cc/tag/домашняя+эротика"
    link = plink + "http://joyreactor.cc/tag/эротический+пирсинг"
    link = plink + "http://joyreactor.cc/tag/blancnoir"
    link = plink + "http://joyreactor.cc/tag/Porn+Model"
    link = plink + "http://joyreactor.cc/tag/большая+грудь"
    link = plink + "http://joyreactor.cc/tag/попка"
    link = plink + "http://joyreactor.cc/tag/чулки"
    link = plink + "http://joyreactor.cc/tag/Moralhexx"
    link = plink + "http://joyreactor.cc/tag/Alathenia"
    link = plink + "http://joyreactor.cc/tag/Сиськи"
    link = plink + "http://joyreactor.cc/tag/Эротика"
    link = plink + "http://pornreactor.cc/tag/my+little+pony"
    link = plink + "http://pornreactor.cc/tag/mlp+porn"
    #main(link, -1)
    s = "SELECT * FROM reactordb"
    posts = []
    for x in db.execute(s).fetchall():
        print(x)
    db.close()
