# coding=UTF-8
import glob
import os
import time

import jsonpickle
import requests
import vk_api
from PIL import Image, ImageFont, ImageDraw


def dbsher(db):
    blinks = ['mlp porn', 'mlp хуманизация', 'minor', 'my little pony', 'фэндомы', 'artist', 'секретные разделы', 'mlp OC', 'Equestria girls', 'mane 6', 'mlp песочница', 'mlp fallout', 'royal', 'mlp аугментация', 'mlp gif', 'mlp porn gif', 'gif r34', 'удалённое', 'mlp gryphon', 'mlp female porn', 'mlp комикс', 'mlp блоги', 'r34 gif', 'mlp porn comics', 'mlp милитаризм', 'mlp crossover', 'mlp баян', 'Кликабельно', 'princess cadance', 'mlp кентавры', 'mlp dakimakura', 'mlp язычок', 'mlp male porn', 'Gravity Falls porn', 'Gravity Falls', 'Disney Porn', 'GF Персонажи', 'mlp zebra', 'сделай сам mlp', 'пониеб', 'mlp дакимакура', 'Порно-комиксы без перевода', 'Порно-комиксы', 'конфета', '#Фуррятина', 'mlp сделай сам', 'mlp 3d', 'нарисовал сам', 'текст на картинке', 'Newhalf Furry', 'Newhalf Stockings', 'MLP Хеллоуин', 'Порно-комиксы без слов', 'mlp pets', 'mlp носочки', 'mlp комиксы', 'перевел сам mlp', 'mlp sphinx', 'mlp tentacles', 'длиннопост', 'mlp transformation', 'mlp sketch', 'mlp труселя', 'mlp чулочки', 'yiff skygracer', 'Gender bender', 'hypnosis', 'NSFW', 'Anal', 'Starbound', 'avian', 'atryl', 'tf-sential', 'xorza', 'NorthernSprint', 'Double Diamond', 'жесть', 'интернет', 'mlp понификация', 'gay zone', 'вроде не баян', 'фендомы', 'песочница', 'Пинки Пай', 'Песочница Порно', 'минум постит в меру упитанных коней', 'mlp foalcon', 'Zootopia porn', 'Gazelle (Zootopia)', 'Zootopia characters', 'Zootopia', 'в комментах ещё одна', 'под катом еще', 'mlp Art & Music', 'Я Ватник', 'rule 34', 'gay porn', 'gp art', 'gz nonHumans', 'yiff L', 'Yiff fetish', 'mlp r34', 'feel like a sir', 'мемы', '#Digimon', 'digimon porn', 'guilmon', 'digimon', '#nazi_pony', 'mlp butt', 'под катом еще одна', 'тег для блока', 'Mlp Antro', 'mlp драконофикация', 'драконофикация', 'mlp co', 'Порно-комиксы с переводом', 'mlp other', 'mlp video', 'моё', 'моё творчество', 'моё больное воображение', 'at crossover', 'помогите найти', 'личное', 'mlp urethral insertion', 'friendship games', 'Yuri Хентай', 'Toys хентай', 'Masturbation Хентай', 'рисунок', 'рисовал сам', 'скетчи', 'gay', 'mlp видео', 'mlp flash', 'nurse Sweetheart', 'автор?', 'don_ko', 'динозавры', 'флинстоуны', 'хрень', 'заминусовали', 'говно', 'суицид', 'перевел сам', '326', 'yiff G', 'yiff M', 'yiff F', 'Rule 63', 'mlp interspecies porn', "Marble's Rumbles", "Anon's pie adventures", 'комикс', '#Цветные кони', 'СПОЙЛЕР', 'Порно', "marble's rambles", 'технические посты секретных разделов', 'продолжение в комментариях', 'Порно гифки', 'Oral Porn', 'r 63', 'в комментах ещё', 'сделал сам', 'арт барышня', 'красивые картинки', 'Арт-клуб', 'Май литл пони', 'Рисовач', 'Принцесса Луна', 'рисованное', 'рисованная эротика', 'digital painting', 'digital art', 'cutie mark crusaders', 'S', 'mlp психоделия', 'yiff', 'My Little Sterelis', 'блинчики', 'носочки', 'ошейник', 'redheart', 'тортик', 'SFM Pony', 'арт', 'cup cake', 'sanders', 'mario porn', 'технический пост', 'mlp futа', 'порно комиксы с переводом', "Them's Fightin' Herds", 'Commander Shepard', 'ME персонажи', 'Siansaar', 'руководство к действию', 'продолжение в комментах', 'yiff feral', 'part 3', 'комиксы на русском', 'ms. cake', '#mlp sanctuary']
    k = []
    db.connect()
    s = "SELECT * FROM reactordb"
    posts = []
    import re
    from collections import Counter
    def clean(tg):
        return re.sub("\((.*?)\)", "", tg.replace("-", "_").replace(" ", "").replace("mlp", "").strip())
    for x in db.execute(s).fetchall():
        tags, pics = x[3:len(x)-2]
        pics = pics.split("|")
        tags = list(Counter([clean(tag) for tag in tags.split("|") if tag not in blinks]))
        text = " ".join([f"#{tag}@reachan" for tag in tags])
        post = {
            "text": text,
            "pics": pics
        }
        posts += [post]
    with open("posts.json", "w+") as f:
        f.write(jsonpickle.encode(posts, unpicklable=False))
    db.close()


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


def upload_photo(vk, post, date):
    print("Adding post for files", post["pics"], "on", date, "of unixtime")
    v = {'group_id': group_id}
    s = requests.Session()
    r = vk.photos.getWallUploadServer(group_id=group_id)
    ulink = r['upload_url']
    files = [open_files(file) for file in post["pics"]]
    r = s.post(ulink, files=files).json()
    print(r)
    exit()
    #close_files(file)
    v.update(r)
    v.update({'access_token': token['access_token']})
    epoint = f"https://api.vk.com/method/photos.saveWallPhoto"
    r = s.post(epoint, v).json()
    r = vk.wall.post(owner_id=-group_id, message=post["text"], attachments=r['response'][0]['id'], publish_date=ptime)
    if 'post_id' in r:
        print("Post added", r)
    else:
        raise Exception(r)


group_id = 147631144
v, tools, token = login()
ctime = int(time.time())
with open("reachan_posts.json") as f:
    json = f.readline()
posts = jsonpickle.decode(json)
for i in posts:
    print("Post:", i)
    ptime = ctime + 10
    upload_photo(v, i, ptime)
    time.sleep(10)
print("All posts added!")