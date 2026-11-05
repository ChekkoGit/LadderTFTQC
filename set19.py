from api import Api
import json

def getTicketsFromRank(tier):
    match tier:
        case "CHALLENGER":
            return 10
        case "GRANDMASTER":
            return 9
        case "MASTER":
            return 8
        case "DIAMOND":
            return 7
        case "EMERALD":
            return 6
        case "PLATINUM":
            return 5
        case "GOLD":
            return 4
        case "SILVER":
            return 3
        case "BRONZE":
            return 2
        case "IRON":
            return 1

def getLeaderboard():
    with open("config/players.json", "r") as file:
        player = json.load(file)

    api = Api()
    leaderboard = []
    for player in player:
        try:
            # Profile
            puuid = api.getSummonerPuuid(name=player['name'],tag=player['tag'])
            profile = api.getTFTLeague(puuid=puuid)[0]

            # Games played
            if(profile['wins'] + profile['losses'] < 10):
                print(f'{player['name']} has less than 10 games, skipping')

            # Rank
            if(profile['tier'] in {'CHALLENGER', 'GRANDMASTER', 'MASTER'}):
                rank = f'{profile['tier']} {profile['leaguePoints']} LP'
            else: 
                rank = f'{profile['tier']} {profile['rank']} {profile['leaguePoints']} LP'

            tickets = getTicketsFromRank(profile['tier']) + player['referals']
            if(player['tag'].lower() == 'tftqc'):
                tickets+=2

            leaderboard.append({
                "name": f'{player['name']}#{player['tag']}',
                "rank": rank,
                "referals": player['referals'],
                "tickets": tickets
            })

        except Exception as e:
            print(f'Error fetching \"{player['name']}#{player['tag']}\", skipping')

    leaderboard.sort(key=lambda i: i['tickets'], reverse=True)
    output = ""
    for player in leaderboard:
        output+= f'{player['name']} - {player['rank']} - {player['referals']} referals - {player['tickets']} tickets\n'
    return output