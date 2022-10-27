from crypt import methods
from email.mime import image
import os
from tokenize import String
from unicodedata import name
from secrets import API_SECRET_KEY
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
import requests
import json

from forms import UserAddForm, LoginForm
from models import Club, Formation, Nation, Player, Team, db, connect_db, User, Likes

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///fut_webapp_db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "it's a secret")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# toolbar = DebugToolbarExtension(app)

connect_db(app)
API_BASE_URL = "https://futdb.app/api/"
API_HEADERS = {
    "X-AUTH-TOKEN": API_SECRET_KEY,
    "accept": "image/png"

}

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    signupform = UserAddForm()
    loginform = LoginForm()

    if signupform.validate_on_submit():
        try:
            user = User.signup(
                username=signupform.username.data,
                password=signupform.password.data,
                email=signupform.email.data,
                image_url=signupform.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template(
                "landing.html", signupform=signupform, loginform=loginform
            )

        do_login(user)

        return redirect("/teams")

    else:
        return render_template(
            "landing.html", signupform=signupform, loginform=loginform
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    loginform = LoginForm()

    if loginform.validate_on_submit():
        user = User.authenticate(loginform.username.data, loginform.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", "danger")

    return redirect("/")


@app.route("/logout")
def logout():
    """Handle logout of user."""

    do_logout()
    flash("Successfully Logged Out")
    return redirect("/login")


##############################################################################
# Homepage and error pages


@app.route("/")
def homepage():
    """Show landing page or redirect to Teams page"""

    if g.user:

        return redirect("/teams")

    else:
        loginform = LoginForm()
        signupform = UserAddForm()

        return render_template(
            "landing.html", loginform=loginform, signupform=signupform
        )


@app.route("/teams")
def teams_page():
    if g.user:
        return render_template("teams.html")
    else:
        return redirect("/")


@app.route("/create-team")
def create_team():
    if g.user:
        return render_template("create-team.html")
    else:
        return redirect("/")


@app.route("/api/teams", methods=["GET"])
def get_teams():
    """Make a request to the Teams model to filter through Teams"""
    if g.user:

        price_min = request.args.get("price_min")
        price_max = request.args.get("price_max")
        rating_min = request.args.get("rating_min")
        rating_max = request.args.get("rating_max")
        formation = request.args.get("formation")
        sort = request.args.get("sort")

        queries = []

        try:
            queries.append(Team.price >= int(price_min))
        except:
            pass

        try:
            queries.append(Team.price <= int(price_max))
        except:
            pass

        try:
            queries.append(Team.rating >= int(rating_min))
        except:
            pass

        try:
            queries.append(Team.rating <= int(rating_max))
        except:
            pass

        try:
            if int(formation) != 0:
                queries.append(Team.formation_id == int(formation))
        except:
            pass

        if sort == "likes":
            # should return a list of the Teams in order of the # of likes
            print("sorted by likes")
            teams = (
                db.session.query(
                    Team,
                    func.count(Team.likes).label("total_likes"),
                )
                .join(Likes)
                .filter(*queries)
                .group_by(Team)
                .order_by("total_likes desc")
                .all()
            )
            json_list = [
                {"team": team[0].serialize(), "likes": team[1]} for team in teams
            ]
            return jsonify(json_list)

        if sort == "comments":
            # should return a list of the Teams in order of the # of comments
            print("sorted by comments")
            return jsonify()

        if sort == "rating":
            # should return a list of the Teams in order of ratings (highest to lowest)
            print("sorted by rating")
            teams = (
                db.session.query(
                    Team,
                    func.count(Team.likes).label("total_likes"),
                )
                .join(Likes)
                .filter(*queries)
                .group_by(Team)
                .order_by(Team.rating.desc())
                .all()
            )
            json_list = [
                {"team": team[0].serialize(), "likes": team[1]} for team in teams
            ]
            return jsonify(json_list)

        if sort == "newest":
            # should return a list of the Teams ordered by date (newest / most recent)
            print("sorted by date (newest)")
            teams = (
                db.session.query(
                    Team,
                    func.count(Team.likes).label("total_likes"),
                )
                .join(Likes)
                .filter(*queries)
                .group_by(Team)
                .order_by(Team.timestamp.desc())
                .all()
            )
            json_list = [
                {"team": team[0].serialize(), "likes": team[1]} for team in teams
            ]
            return jsonify(json_list)


@app.route("/players")
def players_page():
    """Display players page."""
    if g.user:

        return render_template("players.html")


@app.route("/api/players", methods=["GET"])
def get_players():
    """Retrieve data from the Players model for the homepage"""
    if g.user:
        name = request.args.get("name")
        data = {
            "name": name
        }

        image_resp = requests.get(url=f"{API_BASE_URL}players/2/image", headers=API_HEADERS)

        fp = open("static/images/players/2.png", "wb")
        fp.write(image_resp.content) #player.image is the binary data for the PNG returned by the api
        fp.close()
        print(fp.name)

        # Get raw player data from api
        response = requests.post(url=API_BASE_URL + "players/search", headers=API_HEADERS, json=data).text
        player_data = json.loads(response).get("items")

        new_players = []
        player_ids = []

        for player in player_data:
            player_ids.append(Player.id == int(player.get("id")))
            print(int(player.get("id")))
            # If a searched player does not exist in the database, add them to the database
            if db.session.query(Player).filter(Player.id == player.get("id")).first() == None:
                # If new player's Nation does not exist in the database, add it
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

                # Create the new player's image file
                image_data = requests.get(url=f"{API_BASE_URL}players/{player.get('id')}/image", headers=API_HEADERS).content
                player_image = open(f"static/images/players/{player.get('id')}.png", "wb")
                player_image.write(image_data)
                player_image.close()

                new_player = Player(
                    id=player.get("id"),
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

        players_list = db.session.query(Player).filter(or_(*player_ids)).all()

        return jsonify([player.serialize() for player in players_list])

@app.route("/player/<id>", methods=["GET"])
def show_player(id):
    """Display information for a specific Player id"""

    if g.user:
        player = db.session.query(Player).get_or_404(id)
        
        return render_template("player.html", player=player)

@app.route("/users/<id>", methods=["GET"])
def display_profile(id):
    """Display information for a specific User"""

    if g.user:
        user = db.session.query(User).get_or_404(id)
        
        return render_template("profile.html", user=user)

