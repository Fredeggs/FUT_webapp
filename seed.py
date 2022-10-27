"""Seed database with sample data from CSV Files."""

from csv import DictReader
from unicodedata import name
from app import db
from models import Likes, User, Nation, Team, Club, Player, RosterAssignment, Formation
import requests
import json
from secrets import API_SECRET_KEY

API_BASE_URL = "https://futdb.app/api/"
API_HEADERS = {
    "X-AUTH-TOKEN": API_SECRET_KEY,
}

users = [
    User(id=2, email="test_email1@gmail.com", username="test_user1", password="test"),
    User(id=3, email="test_email2@gmail.com", username="test_user2", password="test"),
]

formations = [
    Formation(name="3-1-4-2"),
    Formation(name="3-4-1-2"),
    Formation(name="3-4-2-1"),
    Formation(name="3-4-3"),
    Formation(name="3-5-2"),
    Formation(name="4-1-2-1-2"),
    Formation(name="4-1-3-2"),
    Formation(name="4-1-4-1"),
    Formation(name="4-2-2-2"),
    Formation(name="4-2-3-1"),
    Formation(name="4-2-4"),
    Formation(name="4-3-1-2"),
    Formation(name="4-3-2-1"),
    Formation(name="4-3-3"),
    Formation(name="4-4-1-1"),
    Formation(name="4-4-2"),
    Formation(name="4-5-1"),
    Formation(name="5-2-1-2"),
    Formation(name="5-2-2-1"),
    Formation(name="5-3-2"),
    Formation(name="5-4-1"),
]

db.session.add_all(users)
db.session.add_all(formations)
db.session.commit()

new_players = []
for num in range(1,27):

    response = requests.get(url=f"{API_BASE_URL}players/{num}", headers=API_HEADERS)
    player = json.loads(response.text).get("player")

    # Create the new player's image file
    image_data = requests.get(url=f"{API_BASE_URL}players/{num}/image", headers=API_HEADERS).content
    player_image = open(f"static/images/players/{num}.png", "wb")
    player_image.write(image_data)
    player_image.close()

    if db.session.query(Nation).filter(Nation.id == player.get("nation")).first() == None:
        nation_resp = requests.get(url=f"{API_BASE_URL}nations/{player.get('nation')}", headers=API_HEADERS).text
        nation_name = json.loads(nation_resp).get("nation").get("name")
        new_nation = Nation(id=player.get("nation"), name=nation_name)
        db.session.add(new_nation)
        db.session.commit()
    # If new player's Club does not exist in the database, add it
    if db.session.query(Club).filter(Club.id == player.get("club")).first() == None:
        club_resp = requests.get(url=f"{API_BASE_URL}clubs/{player.get('club')}", headers=API_HEADERS).text
        club_name = json.loads(club_resp).get("club").get("name")
        new_club = Club(id=player.get("club"), name=club_name)
        db.session.add(new_club)
        db.session.commit()

    new_player = Player(
            id=num, 
            name=player.get("name"),
            nation_id=player.get("nation"),
            club_id=player.get("club"),
            rating=player.get("rating"),
            pace=player.get("pace"),
            shooting=player.get("shooting"),
            passing=player.get("passing"),
            dribbling=player.get("dribbling"),
            defending=player.get("defending"),
            physicality=player.get("physicality"),
            image = player_image.name
        )
    new_players.append(new_player)

db.session.add_all(new_players)
db.session.commit()

teams = [
    Team(
        name="test Team 1",
        formation_id=1,
        user_id=2,
        timestamp="2016-12-06 23:13:29.694274",
        price=123456789,
        rating=78,
    ),
    Team(
        name="test Team 2",
        formation_id=2,
        user_id=2,
        timestamp="2017-01-21 11:04:53.522807",
        price=12,
        rating=34,
    ),
]

db.session.add_all(teams)
db.session.commit()

roster_assignments = [
    RosterAssignment(player_id=1, team_id=1),
    RosterAssignment(player_id=2, team_id=1),
    RosterAssignment(player_id=3, team_id=1),
    RosterAssignment(player_id=4, team_id=1),
    RosterAssignment(player_id=5, team_id=1),
    RosterAssignment(player_id=6, team_id=1),
    RosterAssignment(player_id=7, team_id=1),
    RosterAssignment(player_id=8, team_id=1),
    RosterAssignment(player_id=9, team_id=1),
    RosterAssignment(player_id=10, team_id=1),
    RosterAssignment(player_id=11, team_id=1),
    RosterAssignment(player_id=12, team_id=2),
    RosterAssignment(player_id=13, team_id=2),
    RosterAssignment(player_id=14, team_id=2),
    RosterAssignment(player_id=15, team_id=2),
    RosterAssignment(player_id=16, team_id=2),
    RosterAssignment(player_id=17, team_id=2),
    RosterAssignment(player_id=18, team_id=2),
    RosterAssignment(player_id=19, team_id=2),
    RosterAssignment(player_id=20, team_id=2),
    RosterAssignment(player_id=21, team_id=2),
    RosterAssignment(player_id=22, team_id=2),
]

db.session.add_all(roster_assignments)
db.session.commit()

likes = [
    Likes(user_id=2, team_id=1),
    Likes(user_id=2, team_id=2),
    Likes(user_id=2, team_id=2),
    Likes(user_id=3, team_id=2),
]

db.session.add_all(likes)
db.session.commit()
