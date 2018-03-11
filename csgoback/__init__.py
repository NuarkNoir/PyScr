import jsonpickle
import requests, time
import datetime
from requests.cookies import cookiejar_from_dict


def read_config():
    config = {}
    with open("config.cfg", "r") as f:
        for x in f.readlines():
            name, value = x.strip().split("=")
            config[name] = value
    globals()["cfg"] = config
    globals()["timeformat"] = "%d.%m.%Y %H:%M"
    return config


def check_config(_config):
    config = _config
    if "cfduid" not in config.keys():
        exit("No cfduid found (__cfduid)!")
    if "bssid" not in config.keys():
        exit("No bssid found (BACKSESSID)!")
    print("Right config loaded!")


def configure_requestor(_config):
    config = _config
    requestor = requests.Session()
    requestor.cookies = cookiejar_from_dict({
        "__cfduid": config["cfduid"],
        "BACKSESSID": config["bssid"],
        "navigation": "min"
    })
    globals()["requestor"] = requestor
    print("Requestor configured")


def test_requestor():
    prof_url = globals()["cfg"]["prof_url"]
    requestor = globals()["requestor"]
    print("Testing connector...")
    if requestor.get(prof_url).url != "http://csgoback.net/profile":
        exit("Something wrong with connector! Maybe auth-system were updated.")
    print("Connector works normally!")


def gen_out(name, lf, op):
    A = lf['price']
    B = op['price']
    now = datetime.datetime.now()
    dtnow = now.strftime(globals()["timeformat"])
    out = f"[{dtnow}]\t{name}\n\t"
    out += "loot.farm\n\t\t" \
           f"price: {A}$\t" \
           f"updated: {datetime.date.fromtimestamp(lf['updated']).strftime(globals()['timeformat'])}\t" \
           f"count: {lf['count']}\t"
    out += "unavailable\n" if lf.get("unavailable") else f"acceptCount: {lf['acceptCount']}\n\t"
    out += "opskins.com\n\t\t" \
           f"price: {B}$\t" \
           f"updated: {datetime.date.fromtimestamp(op['updated']).strftime(globals()['timeformat'])}\t" \
           f"count: {op['count']}\n\t"
    out += f"profit: {round((B-A)/A*100, 2)}\n\t" \
           f"discount: {round((B-A)/B*100, 2)}\n"
    return out


def start_worker():
    requestor = globals()["requestor"]
    comparison_url = globals()["cfg"]["comparison_url"]
    payload = {
        "app": "730_2",
        "leftService": "loot.farm",
        "rightService": "opskins.com",
        "leftServiceMinCount": "",
        "rightServiceMinCount": "",
        "leftServiceMaxCount": "",
        "rightServiceMaxCount": "",
        "leftUpdateTime": "",
        "rightUpdateTime": "",
        "opskinsSales": "0"
    }
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.189 Safari/537.36 Vivaldi/1.95.1077.55",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "http://csgoback.net/comparison",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    while True:
        try:
            resp = requests.post(comparison_url, data=payload, cookies=requestor.cookies)
            rj = jsonpickle.decode(resp.content)
            if not rj["success"]:
                print("Something went wrong! Full response:", rj)
                input("Press any key to continue, press Alt+F4 to shutdown app.")
                continue
            print(f"Got {len(rj['result'])} positions")
            for item in rj["result"]:
                out = gen_out(item['name'], item["loot.farm"], item["opskins.com"])
                print(out)
            break
        except ConnectionError as e:
            print("Connection error happend! Error:", e)
        time.sleep(1)


def workflow():
    config = read_config()
    check_config(config)
    configure_requestor(config)
    test_requestor()
    start_worker()

if __name__ == "__main__":
    workflow()