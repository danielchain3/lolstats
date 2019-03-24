class Team:
    def __init__(self, team_name, result, gold, kills, towers, inhibs, barons, dragons, rift_herald):
        self.name = team_name
        self.win = result
        self.gold = gold
        self.kills = kills
        self.towers = towers
        self.inhibs = inhibs
        self.barons = barons
        self.dragons = dragons
        self.rift_herald = rift_herald
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
            Towers: %s
            Inhibitors: %s
            Barons: %s
            Dragons: %s
            Rift Herald: %s
            Players: %s
            """ % (self.name, self.win, self.gold, self.kills, self.towers, self.inhibs, \
                    self.barons, self.dragons, self.rift_herald, players)
        return s
