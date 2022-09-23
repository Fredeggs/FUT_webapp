"""Seed database with sample data from CSV Files."""

from csv import DictReader
from unicodedata import name
from app import db
from models import Likes, User, Nation, Team, Club, Player, RosterAssignment, Formation

# db.drop_all()
# db.create_all()

users = [
    User(id=2, email="test_email1@gmail.com", username="test_user1", password="test"),
    User(id=3, email="test_email2@gmail.com", username="test_user2", password="test"),
]

nations = [
    Nation(name="Albania"),
    Nation(name="Andorra"),
    Nation(name="Armenia"),
    Nation(name="Austria"),
    Nation(name="Azerbaijan"),
    Nation(name="Belarus"),
    Nation(name="Belgium"),
    Nation(name="Bosnia and Herzegovina"),
    Nation(name="Bulgaria"),
    Nation(name="Croatia"),
    Nation(name="Cyprus"),
    Nation(name="Czech Republic"),
    Nation(name="Denmark"),
    Nation(name="England"),
    Nation(name="Montenegro"),
    Nation(name="Faroe Islands"),
    Nation(name="Finland"),
    Nation(name="France"),
    Nation(name="FYR Macedonia"),
    Nation(name="Georgia"),
    Nation(name="Germany"),
    Nation(name="Greece"),
    Nation(name="Hungary"),
    Nation(name="Iceland"),
    Nation(name="Republic of Ireland"),
    Nation(name="Israel"),
    Nation(name="Italy"),
    Nation(name="Latvia"),
    Nation(name="Lithuania"),
    Nation(name="Luxembourg"),
    Nation(name="Malta"),
    Nation(name="Moldova"),
    Nation(name="Netherlands"),
    Nation(name="Northern Ireland"),
    Nation(name="Norway"),
    Nation(name="Poland"),
    Nation(name="Portugal"),
    Nation(name="Romania"),
    Nation(name="Russia"),
    Nation(name="Scotland"),
    Nation(name="Slovakia"),
    Nation(name="Slovenia"),
    Nation(name="Spain"),
    Nation(name="Sweden"),
    Nation(name="Switzerland"),
    Nation(name="Turkey"),
    Nation(name="Ukraine"),
    Nation(name="Wales"),
    Nation(name="Serbia"),
]

clubs = [
    Club(name="Arsenal"),
    Club(name="Aston Villa"),
    Club(name="Blackburn Rovers"),
    Club(name="Bolton"),
    Club(name="Chelsea"),
    Club(name="Everton"),
    Club(name="Leeds United"),
    Club(name="Liverpool"),
    Club(name="Manchester City"),
    Club(name="Manchester Utd"),
    Club(name="Middlesbrough"),
    Club(name="Newcastle Utd"),
    Club(name="Nott'm Forest"),
    Club(name="QPR"),
    Club(name="Southampton"),
    Club(name="Spurs"),
    Club(name="West Ham"),
    Club(name="FC Bayern"),
    Club(name="Dortmund"),
    Club(name="M'gladbach"),
    Club(name="SC Freiburg"),
    Club(name="Hansa Rostock"),
    Club(name="Hamburger SV"),
    Club(name="Kaiserslautern"),
    Club(name="1. FC Köln"),
    Club(name="Leverkusen"),
    Club(name="1860 München"),
    Club(name="FC Schalke 04"),
    Club(name="VfB Stuttgart"),
    Club(name="Werder Bremen"),
    Club(name="Inter"),
    Club(name="Milan"),
    Club(name="Napoli"),
    Club(name="Parma"),
    Club(name="Torino"),
    Club(name="Udinese"),
    Club(name="AJ Auxerre"),
    Club(name="SC Bastia"),
    Club(name="Bordeaux"),
    Club(name="EA Guingamp"),
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
db.session.add_all(nations)
db.session.add_all(clubs)
db.session.add_all(formations)
db.session.commit()

players = [
    Player(
        id=7,
        name="Bukayo Saka",
        nation_id=14,
        club_id=1,
        rating=80,
        pace=84,
        shooting=68,
        passing=76,
        dribbling=82,
        defending=65,
        physicality=64,
    ),
    Player(
        id=4,
        name="Martin Ødegaard",
        nation_id=36,
        club_id=1,
        rating=82,
        pace=77,
        shooting=74,
        passing=83,
        dribbling=84,
        defending=58,
        physicality=62,
    ),
    Player(
        id=23,
        name="Aaron Ramsdale",
        nation_id=14,
        club_id=1,
        rating=74,
        pace=48,
        shooting=22,
        passing=26,
        dribbling=43,
        defending=16,
        physicality=48,
    ),
    Player(
        id=13,
        name="Emile Smith Rowe",
        nation_id=14,
        club_id=1,
        rating=76,
        pace=78,
        shooting=64,
        passing=72,
        dribbling=78,
        defending=32,
        physicality=61,
    ),
    Player(
        id=10,
        name="Granit Xhaka",
        nation_id=47,
        club_id=1,
        rating=79,
        pace=50,
        shooting=64,
        passing=79,
        dribbling=69,
        defending=69,
        physicality=80,
    ),
    Player(
        id=8,
        name="Kieran Tierney",
        nation_id=42,
        club_id=1,
        rating=80,
        pace=84,
        shooting=60,
        passing=75,
        dribbling=77,
        defending=75,
        physicality=79,
    ),
    Player(
        id=17,
        name="Ben White",
        nation_id=14,
        club_id=1,
        rating=76,
        pace=69,
        shooting=27,
        passing=61,
        dribbling=67,
        defending=77,
        physicality=76,
    ),
    Player(
        id=11,
        name="Rob Holding",
        nation_id=14,
        club_id=1,
        rating=77,
        pace=57,
        shooting=34,
        passing=60,
        dribbling=65,
        defending=79,
        physicality=75,
    ),
    Player(
        id=16,
        name="Cédric",
        nation_id=38,
        club_id=1,
        rating=76,
        pace=76,
        shooting=63,
        passing=70,
        dribbling=75,
        defending=72,
        physicality=66,
    ),
    Player(
        id=5,
        name="Alexandre Lacazette",
        nation_id=18,
        club_id=1,
        rating=82,
        pace=75,
        shooting=82,
        passing=74,
        dribbling=82,
        defending=44,
        physicality=72,
    ),
    Player(
        id=25,
        name="Nuno Tavares",
        nation_id=38,
        club_id=1,
        rating=70,
        pace=86,
        shooting=52,
        passing=64,
        dribbling=72,
        defending=61,
        physicality=74,
    ),
]

db.session.add_all(players)
db.session.commit()

teams = [
    Team(
        name="test Team 1",
        formation_id=1,
        user_id=1,
        timestamp="2016-12-06 23:13:29.694274",
        price=123456789,
        rating=78,
    ),
    Team(
        name="test Team 2",
        formation_id=2,
        user_id=1,
        timestamp="2017-01-21 11:04:53.522807",
        price=12,
        rating=34,
    ),
]

db.session.add_all(teams)
db.session.commit()

roster_assignments = [
    RosterAssignment(player_id=7, team_id=1),
    RosterAssignment(player_id=4, team_id=1),
    RosterAssignment(player_id=23, team_id=1),
    RosterAssignment(player_id=13, team_id=1),
    RosterAssignment(player_id=10, team_id=1),
    RosterAssignment(player_id=8, team_id=1),
    RosterAssignment(player_id=17, team_id=1),
    RosterAssignment(player_id=11, team_id=1),
    RosterAssignment(player_id=16, team_id=1),
    RosterAssignment(player_id=5, team_id=1),
    RosterAssignment(player_id=25, team_id=1),
    RosterAssignment(player_id=7, team_id=2),
    RosterAssignment(player_id=4, team_id=2),
    RosterAssignment(player_id=23, team_id=2),
    RosterAssignment(player_id=13, team_id=2),
    RosterAssignment(player_id=10, team_id=2),
    RosterAssignment(player_id=8, team_id=2),
    RosterAssignment(player_id=17, team_id=2),
    RosterAssignment(player_id=11, team_id=2),
    RosterAssignment(player_id=16, team_id=2),
    RosterAssignment(player_id=5, team_id=2),
    RosterAssignment(player_id=25, team_id=2),
]

db.session.add_all(roster_assignments)
db.session.commit()

likes = [
    Likes(user_id=1, team_id=1),
    Likes(user_id=1, team_id=2),
    Likes(user_id=2, team_id=2),
    Likes(user_id=3, team_id=2),
]

db.session.add_all(likes)
db.session.commit()
