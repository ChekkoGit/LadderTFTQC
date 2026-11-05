from api import Api
from stats import Stats
import time
import json

def getProfiles():
    with open("config/players.txt", "r") as file:
        playerList = []
        for p in file:
            p = p.replace('\n','')
            playerList.append(p)

    config = json.load(open("./config/config.json"))
    startTime = config["startTime"]
    endTime = config["endTime"]
    
    api = Api(startTime, endTime) 
    output=[]
    for fullTag in playerList:
        name,tag = fullTag.split('#')
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - getMatches() {name}#{tag}")

        matches = api.getMatches(name, tag)
        if(len(matches)>0):
            puuid = api.getSummonerPuuid(name, tag)

            stats = Stats(puuid, matches)
            data = stats.getPlayerData()

            profile = api.getSummonerProfile(puuid)

            if(len(profile)>0):
                jsonProfile = {
                    "name": name,
                    "tag": tag,
                    "tier": profile[0]['tier'],
                    "rank": profile[0]['rank'],
                    "leaguePoints": profile[0]['leaguePoints'],
                    "gamesPlayed": len(matches),
                    "threeStars": stats.countThreeStarUnits(data)
                }
                output.append(jsonProfile)
    return output

### Featherknight
def sortByFeatherknight(jsonProfiles):
    sortedProfiles = sorted(jsonProfiles, key=lambda k: k['featherknight'],reverse=True)
    return sortedProfiles

def getFeatherknightLeaderboard(jsonProfiles):
    sortedProfiles = sortByFeatherknight(jsonProfiles)
    leaderboard = "Ladder de games en tant que Pengu:"
    for p in sortedProfiles:
        if(p["featherknight"] >0):
            leaderboard += f"\n{p['name']}#{p['tag']} - {p['featherknight']} games"

    if(leaderboard == "Ladder de games en tant que Pengu:"):
        leaderboard += "\nNone...\nPengu va pleurer ce soir se couchant...\n"
    return leaderboard

### Rank
def sortByRank(jsonProfiles):
    jsonProfiles = sorted(jsonProfiles, key=lambda k: k['leaguePoints'],reverse=True)
    sortedProfiles= []
    for tier in ["CHALLENGER", "GRANDMASTER", "MASTER", "DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]:
        for rank in ["I", "II", "III", "IV"]:
            for profile in jsonProfiles:
                if(profile['tier'] == tier and profile['rank'] == rank):
                    sortedProfiles.append(profile)
    return sortedProfiles

def getRankLeaderboard(jsonProfiles):
    sortedProfiles = sortByRank(jsonProfiles)
    leaderboard = "Ladder (rank):"
    for p in sortedProfiles:
        leaderboard += f"\n{p['name']}#{p['tag']} - {p['tier']} {p['rank']} {p['leaguePoints']} lp"
        
    if(leaderboard == "Ladder (rank):"):
        leaderboard += "\nNone...\nPersonne aime le set11...\n"
    return leaderboard

### ThreeStars (rerollers)
def sortByThreeStars(jsonProfiles):
    sortedProfiles = sorted(jsonProfiles, key=lambda k: k['threeStars'],reverse=True)
    return sortedProfiles

def getThreeStarsLeaderboard(jsonProfiles):
    sortedProfiles = sortByThreeStars(jsonProfiles)
    leaderboard = "Ladder des rerollers:"
    for p in sortedProfiles:
        if(p["threeStars"]>0):
            leaderboard += f"\n{p['name']}#{p['tag']} - {p['threeStars']} three stars units"

    if(leaderboard == "Ladder des rerollers:"):
        leaderboard += "\nNone...\nAppuyez dont sur D siboire...\n"
    return leaderboard

### TFTQC Tag
def getTagLeaderboard(jsonProfiles):
    leaderboard = "Tirage: Sellouts"
    for p in jsonProfiles:
        if(p["tag"]=="TFTQC" and p["gamesPlayed"]>=10):
            leaderboard += f"\n{p['name']}#{p['tag']}"

    if(leaderboard == "Tirage: Sellouts"):
        leaderboard += "\nNone...\nChekko n'est pas fier...\n"
    return leaderboard

### April Fools
def getFishedLeaderboard(jsonProfiles):
    leaderboard = "Tirage: Poissons"
    for p in jsonProfiles:
        with open("config/poissons.txt", "r") as file:
            fished = False
            for n in file:
                if((n.strip()) == f"{p['name']}#{p['tag']}"):
                    fished = True

        if(fished and p["gamesPlayed"]>=10):
            leaderboard += f"\n{p['name']}#{p['tag']}"

    if(leaderboard == "Tirage: Poissons"):
        leaderboard += "\nNone...\nChekko n'est pas fier...\n"
    return leaderboard