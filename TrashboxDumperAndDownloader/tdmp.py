# coding:utf-8
# python3 tdmp.py
# I should stop on "CutTrack" for a while

from bs4 import BeautifulSoup as bs
import requests
import jsonpickle
import re
import os

global proxyurl
download_template = "https://trashbox.ru/files20/"
regex = r"(<script>)(show_landing_link2)(.*?)(\);)"


class AndroidApp:
    def __init__(self, name, tags, version, link):
        self.name = name.replace("/", "").replace("\\", "").replace("|", "")
        self.tags = tags
        self.version = version
        self.link = link
        self.download_link = ""
        self.filename = ""


def listGenerator():
    link = proxyurl + "https://trashbox.ru/apps/android/"
    proglist = []
    for pn in range(867, 0, -1):
        print("Page number", pn)
        resp = requests.get(link + str(pn))
        html = resp.content
        doc = bs(html, "lxml")
        catal = doc.select("div.div_topic_cat_content")
        for element in catal:
            name = element.select("span.div_topic_tcapt_content")[0].text
            version = element.select("span.div_topic_cat_tag_android")[0].text.replace("Android", "").replace("и выше",
                                                                                                              "").strip() + "+"
            tags = []
            for tag in element.select("div.div_topic_cat_tags a"):
                tags.append(tag.text)
            _link = element.select("a.a_topic_content")[0]["href"]
            proglist.append(AndroidApp(name, tags, version, _link))
    return proglist

def getDownloadLink(orig):
    resp = requests.get(proxyurl + orig)
    html = resp.content
    doc = bs(html, "lxml")
    newlink = doc.select("a.div_topic_top_download_button")[0]["href"]

    resp = requests.get(proxyurl + newlink)
    html = resp.content

    match = re.search(regex, str(html))
    downloadlink = match.group().strip().replace("<script>show_landing_link2(", "").replace(");", "").replace("\\'", "")
    el = downloadlink.split(", ")
    downloadlink = "{}{}_{}/{}".format(download_template, el[1], el[2], el[3])
    return downloadlink, el[3]

def serialize(_pl, name):
    with open(name, "w+") as f:
        f.write(jsonpickle.encode(_pl, unpicklable=False))

def serialize_picklable(_pl, name):
    with open(name, "w+") as f:
        f.write(jsonpickle.encode(_pl))

def file_exists(fname):
    fullname = "./downloads/" + fname + ".apk"
    return os.path.isfile(fullname)

def download_file(app):
    if file_exists(app.name):
        return
    d = "./downloads/" + app.name + ".apk"
    try:
        with open(d, 'wb') as out_stream:
            req = requests.get(proxyurl + app.download_link, stream=True)
            for chunk in req.iter_content(1024):
                out_stream.write(chunk)
    except:
        print("Something went wrong while downloading this file:", d)

def from_zero():
    print("\nLoading info...")
    pl = listGenerator()
    print("Got", len(pl), "apps")
    print("\nSerializindg...")
    serialize(pl, "TrashboxDump.json")
    serialize_picklable(pl, "TrashboxDumpPickle.json")
    npl = []
    print("\nGenerating download links...")
    for app in pl:
        print("Working on", app.name, "...")
        app.download_link, app.filename = getDownloadLink(app.link)
        npl.append(app)
        serialize(npl, "TrashboxDumpWithLinks.json")
    print("\nDownloading files...")
    for app in pl:
        print("Working on", app.name, "...")
        download_file(app)
    print("\nDone")

def from_file():
    act = int(input("1. Download files \n2. Generate links and and download\n[1/2]:\t"))
    if act == 1:
        with open("TrashboxDumpWithLinks.json", "r") as f:
            pl = jsonpickle.decode(str(f.read()))
            print("Got", len(pl), "apps")
            for app in pl:
                print("Working on", app.name, "...")
                download_file(app)
    elif act == 2:
        with open("TrashboxDumpPickle.json", "r") as f:
            pl = jsonpickle.decode(str(f.read()))
            print("Got", len(pl), "apps")
            npl = []
            print("\nGenerating download links...")
            for app in pl:
                if file_exists(app.name):
                    print("This file exists:", app.name, ". Skipping.")
                    continue
                _app = AndroidApp(app.name, app.tags, app.version, app.link)
                print("Working on", app.name, "...")
                if len(app.download_link) > 0:
                    continue
                _app.download_link, app.filename = getDownloadLink(app.link)
                npl.append(_app)
                serialize(npl, "TrashboxDumpWithLinks.json")
            print("\nDownloading files...")
            for app in npl:
                print("Working on", app.name, "...")
                download_file(app)

def gen_and_download():
    with open("TrashboxDumpPickle.json", "r") as f:
        pl = jsonpickle.decode(str(f.read()))
        print("Got", len(pl), "apps")
        npl = []
        print("\nGenerating download links and downloading...")
        for app in pl:
            if file_exists(app.name):
                print("This file exists:", app.name, ". Skipping.")
                continue
            print("Working on", app.name, "...")
            app.download_link, app.filename = getDownloadLink(app.link)
            npl.append(app)
            print("Downloading", app.name, "...")
            download_file(app)
        serialize(npl, "TrashboxDumpWithLinks.json")
        print("\nDownloading files...")
        for app in npl:
            print("Working on", app.name, "...")
            download_file(app)

def gen_and_send_to_yandex():
    with open("TrashboxDumpPickle.json", "r") as f:
        pl = jsonpickle.decode(str(f.read()))
        print("Got", len(pl), "apps")
        npl = []
        print("\nGenerating download links and downloading...")
        for id, app in enumerate(pl):
            print("Working on", app.name, "...")
            try:
                app.download_link, app.filename = getDownloadLink(app.link)
            except:
                print("Error happend while processing", app.name, ". Skipping.")
            npl.append(app)
            print("Sending to Yandex Disk", app.name, "...")
            code = requests.get(f"https://nuark-caffeine.herokuapp.com/acollection?mode=ubl&u={app.download_link}&f={app.name}.apk").text
        serialize(npl, "TrashboxDumpWithLinks.json")

def main():
    act = input("Proxy:\n1. Use nuark.xyz proxy \n2. Didn't use it \n[Y/n]:\t").lower()
    if act == "y" or not act:
        globals()["proxyurl"] = "http://nuark.xyz/proxy.php?h&l="
    elif act == "n":
        globals()["proxyurl"] = ""
    act = int(input("1. Load file \n2. Start from blank \n3. Gen and download \n4. Gen and send to Y.D \n[1/2/3/4]:\t"))
    if act == 1:
        from_file()
    elif act == 2:
        from_zero()
    elif act == 3:
        gen_and_download()
    elif act == 4:
        gen_and_send_to_yandex()
    else:
        exit("Unexpected input")


if __name__ == "__main__":
    main()