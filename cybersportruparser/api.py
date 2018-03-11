from lxml import etree
import requests, lxml.html

class CybersportRuApi:

    def __init__(self):
        self.baseurl = "https://www.cybersport.ru"

    def get_teams(self, page=1, discipline="all", order="amount"):
        response = {
            "type": "teams",
            "current_page": page,
            "pages_count": None,
            "discipline": discipline,
            "order": order,
            "teams": None
        }
        endurl = f"{self.baseurl}/base/teams/list/disciplines/{discipline}/order/{order}/page/{page}/search"
        docum = requests.get(endurl)
        dtree = lxml.html.fromstring(docum.content)
        pag_is = dtree.cssselect(".pagination__item")
        tmp = pag_is[-1]
        if "pagination__item--next" in pag_is[-1].attrib["class"]:
            tmp = pag_is[-2]
        response["pages_count"] = int(tmp.text)
        teams = []
        tables_base_teams = dtree.cssselect(".tables-base--teams tr")[1:]
        for bt in tables_base_teams:
            team__id = bt.cssselect("td.tables-base__name a")[0].attrib["href"].replace("/base/teams/", "")
            team__place = bt.cssselect(".tables-base__place")[0].text.strip().rstrip(".")
            team__title = bt.cssselect("a.team .team__title strong")[0].text.strip()
            team__logo = bt.cssselect("a.team .team__logo img")[0].attrib["src"].strip()
            if "no-photo" in team__logo:
                team__logo = "https://www.cybersport.ru/assets/img/no-photo/no-photo-cs-go.png"
            else:
                team__logo = "https://" + team__logo.split("/https://").pop().split("?")[0]
            team__funds = bt.cssselect(".tables-base__fund")[0].text.strip()
            team__honors = bt.cssselect(".tables-base__winners .booty i")
            team__game = bt.cssselect(".tables-base__game i")[0].attrib["class"].split("--").pop()
            honors = {
                "first_place": team__honors[0].text.strip(),
                "second_place": team__honors[1].text.strip(),
                "third_place": team__honors[2].text.strip()
            }
            team = {
                "id": team__id,
                "place": int(team__place),
                "name": team__title,
                "logo": team__logo,
                "main_game": team__game,
                "funds": team__funds,
                "wins": honors
            }
            teams.append(team)
        response["teams"] = teams
        return response

    def get_gamers(self, page=1, discipline="all", order="amount"):
        response = {
            "type": "gamers",
            "current_page": page,
            "pages_count": None,
            "discipline": discipline,
            "order": order,
            "gamers": None
        }
        endurl = f"{self.baseurl}/base/gamers/list/disciplines/{discipline}/order/{order}/page/{page}/search"
        docum = requests.get(endurl)
        dtree = lxml.html.fromstring(docum.content)
        pag_is = dtree.cssselect(".pagination__item")
        tmp = pag_is[-1]
        if "pagination__item--next" in pag_is[-1].attrib["class"]:
            tmp = pag_is[-2]
        response["pages_count"] = int(tmp.text)
        gamers = []
        tables_base_teams = dtree.cssselect(".tables-base--players tr")[1:]
        for bt in tables_base_teams:
            gamer__place = bt.cssselect(".tables-base__place")[0].text.strip().rstrip(".")
            tmp = bt.cssselect(".tables-base__name .gamer")[0]
            gamer__id = tmp.cssselect(".gamer__title a")[0].attrib["href"].replace("/base/gamers/", "")
            gamer__nick = tmp.cssselect(".gamer__title p")[0].text_content()
            gamer__real_name = tmp.cssselect(".gamer__name")[0].text.strip()
            try:
                gamer__real_name = gamer__real_name.encode('raw-unicode-escape').decode('utf-8')
            except:
                try:
                    gamer__real_name = gamer__real_name[:len(gamer__real_name)-1].encode('raw-unicode-escape').decode('utf-8')
                except:
                    pass
            gamer__avatar = tmp.cssselect(".gamer__photo img")[0].attrib["src"]
            gamer__country = tmp.cssselect(".gamer__title p i")[0].attrib["class"].split().pop().split("-").pop()
            del tmp
            if "no-photo" in gamer__avatar:
                gamer__avatar = "https://www.cybersport.ru/assets/img/no-photo/no-photo-cs-go.png"
            else:
                gamer__avatar = "https://" + gamer__avatar.split("/https://").pop().split("?")[0]
            gamer__team = bt.cssselect("div.team__title span")[0].text if bt.cssselect("div.team__title span") else "><"
            gamer__game = bt.cssselect(".tables-base__game i")[0].attrib["class"].split("--").pop()
            gamer__funds = bt.cssselect(".tables-base__fund")[0].text.strip()
            gamer__honors = bt.cssselect(".tables-base__winners .booty i")
            honors = {
                "first_place": gamer__honors[0].text.strip(),
                "second_place": gamer__honors[1].text.strip(),
                "third_place": gamer__honors[2].text.strip()
            }
            gamer = {
                "id": gamer__id,
                "place": int(gamer__place),
                "nick": gamer__nick,
                "real_name": gamer__real_name,
                "country": gamer__country,
                "avatar": gamer__avatar,
                "main_game": gamer__game,
                "team": gamer__team,
                "funds": gamer__funds,
                "wins": honors
            }
            gamers.append(gamer)
        response["gamers"] = gamers
        return response




