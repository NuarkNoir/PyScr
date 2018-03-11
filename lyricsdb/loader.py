from lxml import etree

import lxml.html
import requests
import re

from collections import Counter as C

import queue
import idna.idnadata

from exts.IDbDealer import LyricsDbDealer

try:
    from lyricsdb import db
except:
    import db


author_selector = ".main-page .row a"
song_selector = "div#listAlbum a[href][target]"
album_selector = "div.album-panel a"
text_selector = "div.text-center > div:nth-child(8)"
cats = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower())
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3360.0 Safari/537.36',
}
pruri = "http://nuark.xyz/proxy.php?h&l="

def main():
    database = db
    dbdealer = LyricsDbDealer(database)
    with dbdealer:
        for cat in cats:
            print("Processing of category '{cat}'".format(cat=cat))
            # Getting page of category
            try:
                html = requests.get(f"https://www.azlyrics.com/{cat}.html", headers=headers).text
            except:
                html = requests.get(f"{pruri}https://www.azlyrics.com/{cat}.html", headers=headers).text
            root = lxml.html.fromstring(html)
            els = root.cssselect(author_selector)
            for author, a_link in [(x.text.strip(), "https://www.azlyrics.com/" + x.attrib["href"]) for x in els]:
                print(f"\tProcessing songs of author '{author}'...")
                html = requests.get(pruri + a_link, headers=headers).text
                root = lxml.html.fromstring(html)
                els = root.cssselect(song_selector)
                for song, s_link in [(x.text.strip(), "https://www.azlyrics.com/" + x.attrib["href"][3:]) for x in els]:
                    print(f"\t\tProcessing song '{song}'...")
                    if dbdealer.element_exists(author, song):
                        print(f"\t\t\tSong exists.")
                        continue
                    try:
                        html = requests.get(s_link, headers=headers).text
                    except:
                        html = requests.get(pruri + s_link, headers=headers).text
                    root = lxml.html.fromstring(html)
                    els = root.cssselect(text_selector)
                    try:
                        text = els[0].text_content().strip()
                    except:
                        text = "No text found D:"
                    try:
                        album = root.cssselect(album_selector)[0].text.strip()
                    except:
                        album = "Other"
                    dbdealer.put_elements(author, album, song, text)
                    print(f"\t\t\tDone.")
                dbdealer.commit()


if __name__ == '__main__':
    main()
