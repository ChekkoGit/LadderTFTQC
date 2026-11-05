import requests
import json
from time import sleep

class Api:
    def __init__(self):
        f = open("./config/config.json")
        apiKey = json.load(f)["riotApiKey"]

        self.headers =   {
            "Accept-Language": "en,en-US;q=0.5",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Riot-Token": f"{apiKey}"
        }

    def abstractApiCall(self, region, endpoint, params):
        url = f"https://{region}.api.riotgames.com/"
        return requests.get(f"{url}{endpoint}", headers=self.headers, params=params).json()

    def getSummonerId(self, puuid):
        return (self.abstractApiCall("na1", f"tft/summoner/v1/summoners/by-puuid/{puuid}", None))["id"]
    
    def getSummonerPuuid(self, name, tag):
        return (self.abstractApiCall("americas",f"riot/account/v1/accounts/by-riot-id/{name}/{tag}", None))["puuid"]
    
    def getTFTLeague(self, puuid):
        return (self.abstractApiCall("na1",f"tft/league/v1/by-puuid/{puuid}", None))