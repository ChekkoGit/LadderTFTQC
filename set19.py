from api import Api
import json

def getRules():
    output = "---\nSources de tickets:\n"
    output += "---\nRank:\n1 ticket par tier.\n(Ex: Iron = 1, Gold = 4, Emerald = 6, etc.)\n"
    output += "---\nReferal:\n1 ticket par referral, au maximum de 3 tickets.\nLe referal se fait à l'inscription dans le champ correspondant du formulaire.\n"
    output += "---\nTag:\nChanger votre tag (#) pour mettre \"TFTQC\" vous accorde 2 tickets supplémentaires!\n(Ex: DavidAce#TFTQC au lieu de DavidAce#NA1)\nMerci de contacter Chekko si vous changez votre nom APRÈS votre inscription.\n---"
    return output

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

            tickets = getTicketsFromRank(profile['tier']) + player['referrals']
            if(player['tag'].lower() == 'tftqc'):
                tickets+=2

            leaderboard.append({
                "name": f'{player['name']}#{player['tag']}'.ljust(20),
                "rank": rank.ljust(18),
                "referrals": player['referrals'],
                "tickets": tickets
            })

        except Exception as e:
            print(f'Error fetching \"{player['name']}#{player['tag']}\", skipping')

    leaderboard.sort(key=lambda i: i['tickets'], reverse=True)
    output = ""
    for player in leaderboard:
        tickets = f'{player['tickets']} tickets'.ljust(12)
        output+= f'{player['name']} - {player['rank']} - {player['referrals']} referrals - {tickets}\n'
    return output