# coding=UTF-8
import glob
import os
import time

import requests
import vk_api
from PIL import Image, ImageFont, ImageDraw


def draw_with_contour(fn, text="Example text", where=(20, 20), size=81, c1=0, c2=255, border=2, meme=False):
    txt = Image.open(fn)
    if meme:
        px, py = txt.size
        height = size + size // 10
        width = 25 * len(text)
        if width > px:
            return draw_with_contour(fn, text, where, int(size / 2 * 1.6), c1, c2, border, meme)
        where = px // 2 - width // .8, py - (py // 6)
        if height > py // 8:
            where = where[0], where[1] - (10 * (size // 10)) // 2
    fnt = ImageFont.truetype("compact.ttf", size)
    ru, rd = (where[0] + border, where[1] + border), (where[0] + border, where[1] - border)
    lu, ld = (where[0] - border, where[1] + border), (where[0] - border, where[1] - border)
    d = ImageDraw.Draw(txt)
    d.text(ru, text, font=fnt, fill=(c1, c1, c1, 255))
    d = ImageDraw.Draw(txt)
    d.text(ld, text, font=fnt, fill=(c1, c1, c1, 255))
    d = ImageDraw.Draw(txt)
    d.text(rd, text, font=fnt, fill=(c1, c1, c1, 255))
    d = ImageDraw.Draw(txt)
    d.text(lu, text, font=fnt, fill=(c1, c1, c1, 255))
    d = ImageDraw.Draw(txt)
    d.text(where, text, font=fnt, fill=(c2, c2, c2, 255))
    del d
    txt.save(f"./ext/new_{fn.split('/').pop().split('.')[0]}.jpg", "JPEG")


def open_files(paths, key_format='file{}'):
    if not isinstance(paths, list):
        paths = [paths]

    files = []

    for x, file in enumerate(paths):
        if hasattr(file, 'read'):
            f = file

            if hasattr(file, 'name'):
                filename = file.name
            else:
                filename = '.jpg'
        else:
            filename = file
            f = open(filename, 'rb')

        ext = filename.split('.')[-1]
        files.append(
            (key_format.format(x), ('file{}.{}'.format(x, ext), f))
        )

    return files


def close_files(files):
    for f in files:
        f[1][1].close()


def login():
    app_id = 5882810

    login = "79659197391"
    password = "rossmoor11"

    vk_session = vk_api.VkApi(login=login, password=password, app_id=app_id)
    vk_session.auth()

    return vk_session.get_api(), vk_api.VkTools(vk_session), vk_session.token


def upload_photo(vk, file, date):
    print("Adding post for file", file, "on", date, "of unixtime")
    v = {'group_id': group_id}
    s = requests.Session()
    r = vk.photos.getWallUploadServer(group_id=group_id)
    ulink = r['upload_url']
    file = open_files(file)
    r = s.post(ulink, files=file).json()
    close_files(file)
    v.update(r)
    v.update({'access_token': token['access_token']})
    epoint = f"https://api.vk.com/method/photos.saveWallPhoto"
    r = s.post(epoint, v).json()
    r = vk.wall.post(owner_id=-group_id, attachments=r['response'][0]['id'], publish_date=ptime)
    if 'post_id' in r:
        print("Post added", r)
    else:
        raise Exception(r)


group_id = 158885847
v, tools, token = login()
ctime = int(time.time())
genlist =[]
for filename in glob.glob('./ext/*.jpg'):
    genlist.append(filename)
for i in range(25):
    print("Post:", i)
    ptime = ctime + 3600 * (i + 1)
    fname = genlist[i]
    upload_photo(v, fname, ptime)
    os.remove(fname)
    time.sleep(2)
print("All posts added!")