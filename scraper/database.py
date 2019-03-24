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

    mydb = create_engine(db_url, echo=True)

    return mydb

def addTeamInfo(blue_team, red_team):
    positions = ['top', 'jungle', 'middle', 'bottom', 'support'] 

    #Database setup
    db = connectToDatabase(DB_INFO)
    metadata = MetaData()
    team_info = Table('team_info', metadata, autoload=True, autoload_with=db)
    
    #SQL expressions to be used later
    team_info_expr = select([team_info])
    add_player_expr = table_team_info.insert()

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

        if not blue_player_exists:
            add_player = add_player_expr.values(
                    team_name=blue_player_info[0],
                    player_name=blue_player_info[1],
                    player_role=blue_player_info[2],
                    split=blue_player_info[3]
                )
            result = conn.execute(add_player)

        if not red_player_exists:
            add_player = add_player_expr.values(
                    team_name=blue_player_info[0],
                    player_name=blue_player_info[1],
                    player_role=blue_player_info[2],
                    split=blue_player_info[3]
                )
            result = conn.execute(add_player)

        #close connection
        conn.close()
