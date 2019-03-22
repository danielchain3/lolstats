class Team:
    def __init__(self, team_name, result, gold, kills):
        self.name = team_name
        self.win = result
        self.gold = gold
        self.kills = kills
        self.players = []

    def __str__(self):
        players = ""
        for player in self.players:
            players += str(player) + ", "

        players = players[:-2]  #Removes the last unnecessary comma

        s = """
            Team Name: %s
            Win: %s
            Gold: %s
            Kills: %s
            Players: %s
            """ % (self.name, self.win, self.gold, self.kills, players)
        return s
