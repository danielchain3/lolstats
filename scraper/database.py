import mysql.connector
from sqlalchemy import *
from sqlalchemy.sql import select
from player import PlayerInfo
from team import Team

DB_INFO = "DBInfo"      #name of file that stores db credentials
SPLIT = "2019 SPRING"   #current split

def connectToDatabase(file_name):
    DBinfo = []
    file = open(file_name, 'r')

    for line in file:
        DBinfo.append(line.rstrip("\n"))

    file.close()

    db_url = "mysql+mysqlconnector://%s:%s@%s/%s?charset=utf8mb4" \
            % (DBinfo[0], DBinfo[1], DBinfo[2], DBinfo[3])

    mydb = create_engine(db_url)    #echo=True) #include for debugging

    return mydb

def addTeamInfo(blue_team, red_team):
    positions = ['top', 'jungle', 'middle', 'bottom', 'support'] 

    #Database setup
    db = connectToDatabase(DB_INFO)
    metadata = MetaData()
    team_info = Table('team_info', metadata, autoload=True, autoload_with=db)
    
    #SQL expressions to be used later
    team_info_expr = select([team_info])
    add_player_expr = team_info.insert()

    for playerIndex in range(5):
        blue_player_info = (
            blue_team.name, blue_team.players[playerIndex].name, positions[playerIndex], SPLIT
            ) 
        red_player_info = (
            red_team.name, red_team.players[playerIndex].name, positions[playerIndex], SPLIT
            ) 

        #expressions to check if players exists
        check_blue_player = team_info_expr.where(and_(team_info.c.team_name==blue_player_info[0],
            team_info.c.player_name==blue_player_info[1],
            team_info.c.player_role==blue_player_info[2],
            team_info.c.split==blue_player_info[3]))

        check_red_player = team_info_expr.where(and_(team_info.c.team_name==red_player_info[0],
            team_info.c.player_name==red_player_info[1],
            team_info.c.player_role==red_player_info[2],
            team_info.c.split==red_player_info[3]))

        #creates connection to db
        conn = db.connect()

        #executes the expressions and stores results  
        blue_player = conn.execute(check_blue_player)
        red_player = conn.execute(check_red_player)

        blue_exists = blue_player.rowcount == 1
        red_exists = red_player.rowcount == 1

        #sends the result objects to the garbage collector
        blue_player.close()
        red_player.close()

        if not blue_exists:
            add_player = add_player_expr.values(
                    team_name=blue_player_info[0],
                    player_name=blue_player_info[1],
                    player_role=blue_player_info[2],
                    split=blue_player_info[3]
                )
            result = conn.execute(add_player)

        if not red_exists:
            add_player = add_player_expr.values(
                    team_name=red_player_info[0],
                    player_name=red_player_info[1],
                    player_role=red_player_info[2],
                    split=red_player_info[3]
                )
            result = conn.execute(add_player)

        #close connection
        conn.close()


def addTeamStats(blue_team, red_team, match_info):
    #Database setup
    db = connectToDatabase(DB_INFO)
    metadata = MetaData()
    team_stats = Table('team_stats', metadata, autoload=True, autoload_with=db)

    team_stats_expr = select([team_stats])
    add_stats_expr = team_stats.insert()

    #expressions to check if match info exists
    check_blue_team = team_stats_expr.where(and_(team_stats.c.match_id==match_info["match_id"],
        team_stats.c.team_name==blue_team.name))
    check_red_team = team_stats_expr.where(and_(team_stats.c.match_id==match_info["match_id"],
        team_stats.c.team_name==red_team.name))
    
    #creates connection to db
    conn = db.connect()

    #executes the expressions and stores results
    blue_team_exists = conn.execute(check_blue_team)
    red_team_exists = conn.execute(check_red_team)

    blue_exists = blue_team_exists.rowcount == 1
    red_exists = red_team_exists.rowcount == 1

    #sends the result objects to the garbage collector
    blue_team_exists.close()
    red_team_exists.close()

    if not blue_exists:
        add_stats = add_stats_expr.values(
            team_name=blue_team.name,
            win=blue_team.win,
            gold=blue_team.gold,
            kills=blue_team.kills, 
            towers=blue_team.towers,
            inhibitors=blue_team.inhibs,
            barons=blue_team.barons,
            dragons=blue_team.dragons,
            rift_herald=blue_team.rift_herald,
            match_id=match_info["match_id"],
            date_played=match_info["date"],
            match_duration=match_info["match_duration"]
            )
        result = conn.execute(add_stats)
    if not red_exists:
        add_stats = add_stats_expr.values(
            team_name=red_team.name,
            win=red_team.win,
            gold=red_team.gold,
            kills=red_team.kills, 
            towers=red_team.towers,
            inhibitors=red_team.inhibs,
            barons=red_team.barons,
            dragons=red_team.dragons,
            rift_herald=red_team.rift_herald,
            match_id=match_info["match_id"],
            date_played=match_info["date"],
            match_duration=match_info["match_duration"]
            )
        result = conn.execute(add_stats)

    #close connection
    conn.close()

def addPlayerStats(blue_team, red_team, match_info):
    db = connectToDatabase(DB_INFO)
    metadata = MetaData()
    player_stats = Table('player_stats', metadata, autoload=True, autoload_with=db)

    player_stats_expr = select([player_stats])
    add_player_expr = player_stats.insert()

    for player_index in range(5):
        blue_player_info = blue_team.players[player_index]
        red_player_info = red_team.players[player_index]

        check_blue_player = player_stats_expr.where(and_(
            player_stats.c.player_name==blue_player_info.name,
            player_stats.c.match_id==match_info['match_id']
            ))

        check_red_player = player_stats_expr.where(and_(
            player_stats.c.player_name==red_player_info.name,
            player_stats.c.match_id==match_info['match_id']
            ))

        conn = db.connect()

        blue_player = conn.execute(check_blue_player)
        red_player = conn.execute(check_red_player)

        blue_exists = blue_player.rowcount == 1
        red_exists = red_player.rowcount == 1

        blue_player.close()
        red_player.close()

        if not blue_exists:
            add_player = add_player_expr.values(
                player_name = blue_player_info.name,
                team_name = blue_team.name,
                match_id = match_info['match_id'],
                date_played = match_info['date'],
                split = SPLIT,
                champion = blue_player_info.info['champion'],
                kills = blue_player_info.info['kills'],
                deaths = blue_player_info.info['deaths'],
                assists = blue_player_info.info['assists'],
                largest_killing_spree = blue_player_info.info['largest killing spree'],
                largest_multi_kill = blue_player_info.info['largest multi kill'],
                first_blood = blue_player_info.info['first blood'],
                total_damage_to_champions = blue_player_info.info['total damage to champions'],
                physical_damage_to_champions=blue_player_info.info['physical damage to champions'],
                magic_damage_to_champions = blue_player_info.info['magic damage to champions'],
                true_damage_to_champions = blue_player_info.info['true damage to champions'],
                total_damage_dealt = blue_player_info.info['total damage dealt'],
                physical_damage_dealt = blue_player_info.info['physical damage dealt'],
                magic_damage_dealt = blue_player_info.info['magic damage dealt'],
                true_damage_dealt = blue_player_info.info['true damage dealt'],
                largest_critical_strike = blue_player_info.info['largest critical strike'],
                total_damage_to_objectives = blue_player_info.info['total damage to objectives'],
                total_damage_to_turrets = blue_player_info.info['total damage to turrets'],
                damage_healed = blue_player_info.info['damage healed'],
                damage_taken = blue_player_info.info['damage taken'],
                physical_damage_taken = blue_player_info.info['physical damage taken'],
                magic_damage_taken = blue_player_info.info['magic damage taken'],
                true_damage_taken = blue_player_info.info['true damage taken'],
                wards_placed = blue_player_info.info['wards placed'],
                wards_destroyed = blue_player_info.info['wards destroyed'],
                stealth_wards_purchased = blue_player_info.info['stealth wards purchased'],
                control_wards_purchased = blue_player_info.info['control wards purchased'],
                gold_earned = blue_player_info.info['gold earned'],
                gold_spent = blue_player_info.info['gold spent'],
                minions_killed = blue_player_info.info['minions killed'],
                neutral_minions_killed = blue_player_info.info['neutral minions killed'],
                neutral_minions_killed_in_team_jungle = \
                        blue_player_info.info["neutral minions killed in team's jungle"],
                neutral_minions_killed_in_enemy_jungle = \
                        blue_player_info.info['neutral minions killed in enemy jungle'])

            result = conn.execute(add_player)

        if not red_exists:
            add_player = add_player_expr.values(
                player_name = red_player_info.name,
                team_name = red_team.name,
                match_id = match_info['match_id'],
                date_played = match_info['date'],
                split = SPLIT,
                champion = red_player_info.info['champion'],
                kills = red_player_info.info['kills'],
                deaths = red_player_info.info['deaths'],
                assists = red_player_info.info['assists'],
                largest_killing_spree = red_player_info.info['largest killing spree'],
                largest_multi_kill = red_player_info.info['largest multi kill'],
                first_blood = red_player_info.info['first blood'],
                total_damage_to_champions = red_player_info.info['total damage to champions'],
                physical_damage_to_champions=red_player_info.info['physical damage to champions'],
                magic_damage_to_champions = red_player_info.info['magic damage to champions'],
                true_damage_to_champions = red_player_info.info['true damage to champions'],
                total_damage_dealt = red_player_info.info['total damage dealt'],
                physical_damage_dealt = red_player_info.info['physical damage dealt'],
                magic_damage_dealt = red_player_info.info['magic damage dealt'],
                true_damage_dealt = red_player_info.info['true damage dealt'],
                largest_critical_strike = red_player_info.info['largest critical strike'],
                total_damage_to_objectives = red_player_info.info['total damage to objectives'],
                total_damage_to_turrets = red_player_info.info['total damage to turrets'],
                damage_healed = red_player_info.info['damage healed'],
                damage_taken = red_player_info.info['damage taken'],
                physical_damage_taken = red_player_info.info['physical damage taken'],
                magic_damage_taken = red_player_info.info['magic damage taken'],
                true_damage_taken = red_player_info.info['true damage taken'],
                wards_placed = red_player_info.info['wards placed'],
                wards_destroyed = red_player_info.info['wards destroyed'],
                stealth_wards_purchased = red_player_info.info['stealth wards purchased'],
                control_wards_purchased = red_player_info.info['control wards purchased'],
                gold_earned = red_player_info.info['gold earned'],
                gold_spent = red_player_info.info['gold spent'],
                minions_killed = red_player_info.info['minions killed'],
                neutral_minions_killed = red_player_info.info['neutral minions killed'],
                neutral_minions_killed_in_team_jungle = \
                        red_player_info.info["neutral minions killed in team's jungle"],
                neutral_minions_killed_in_enemy_jungle = \
                        red_player_info.info['neutral minions killed in enemy jungle'])

            result = conn.execute(add_player)

        conn.close()


