import pymongo

'''
Main assignment code
'''

dbClient = pymongo.MongoClient("mongodb://localhost:27017/")

db = dbClient["a3DataBase"]
playerCollection = db["players"]
teamsCollection = db["teams"]

# calculate goodness score using the player's preference
def calculateGoodnessScore(pref : int):
    goodnessScore = 0

    if pref == 1:
        goodnessScore += 5
    elif pref == 2:
        goodnessScore += 4
    elif pref == 3:
        goodnessScore += 3

    return goodnessScore

# calculate the goodness score of a team
def calculateTeamGoodnessScore(team : dict):
    teamGoodnessScore = 0

    teamName = team["name"]

    for teamPlayer in team["players"]:
        player = playerCollection.find_one({"lastName": teamPlayer[0], "firstName": teamPlayer[1]})
        teamPref = player["teamPref"]
        teamGoodnessScore += calculateGoodnessScore(teamPref.index(teamName) + 1)

    return teamGoodnessScore


# assign players to teams based on their preferences
def assignPlayersToTeams():
    players = playerCollection.find()

    for player in players:
        teamPref = player["teamPref"]

        for pref in teamPref:
            team = teamsCollection.find_one({"name": pref})
            # if the team has less than 2 players, add the player to the team and move onto the next
            # otherwise, move onto the next preference
            if len(team["players"]) < 2:
                team["players"].append((player["lastName"], player["firstName"]))
                teamsCollection.update_one({"name": pref}, {"$set": {"players": team["players"]}})
                break

# empty teams before assigning players to teams
def emptyTeams():
    teamsCollection.update_many({}, {"$set": {"players": []}})


if __name__ == "__main__":
    emptyTeams()
    assignPlayersToTeams()
    
    # output
    totalGoodnessScore = 0

    print("\nTeam Rosters:\n")
    teams = teamsCollection.find()
    for team in teams:
        print(team["name"] + ": " + str(team["players"]))
        goodnessScore = calculateTeamGoodnessScore(team)
        print("Goodness Score: " + str(goodnessScore))
        totalGoodnessScore += goodnessScore
        print()

    print("Total Goodness Score: " + str(totalGoodnessScore))
