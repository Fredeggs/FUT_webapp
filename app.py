from crypt import methods
import os
from tokenize import String
from unicodedata import name
from secrets import API_SECRET_KEY
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
import requests
import json

from forms import UserAddForm, LoginForm
from models import Formation, Player, Team, db, connect_db, User, Likes

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
API_BASE_URL = "https://futdb.app/api/players/search"
API_HEADERS = {"X-AUTH-TOKEN": API_SECRET_KEY}

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
    signupform = UserAddForm()

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

        # following_ids = [user.id for user in g.user.following]
        # messages = (
        #     Message.query.filter(
        #         (Message.user_id.in_(following_ids)) | (Message.user_id == g.user.id)
        #     )
        #     .order_by(Message.timestamp.desc())
        #     .limit(100)
        #     .all()
        # )

        # likes = Likes.query.filter(Likes.user_id == g.user.id).all()
        # like_ids = [like.message_id for like in likes]

        # return render_template("home.html", messages=messages, likes=like_ids)
        return render_template("players.html")


@app.route("/api/players", methods=["GET"])
def get_players():
    """Retrieve data from the Players model for the homepage"""
    if g.user:
        name = request.args.get("name")
        data = {
            "name": name,
        }

        response = requests.post(API_BASE_URL, headers=API_HEADERS, json=data).text
        resp_json = json.loads(response)
        items = resp_json.get("items")
        print(resp_json)
        names = [{"name": item.get("name")} for item in items]
        # [{"team": team[0].serialize(), "likes": team[1]} for team in teams]

        # following_ids = [user.id for user in g.user.following]
        # messages = (
        #     Message.query.filter(
        #         (Message.user_id.in_(following_ids)) | (Message.user_id == g.user.id)
        #     )
        #     .order_by(Message.timestamp.desc())
        #     .limit(100)
        #     .all()
        # )

        # likes = Likes.query.filter(Likes.user_id == g.user.id).all()
        # like_ids = [like.message_id for like in likes]

        # return render_template("home.html", messages=messages, likes=like_ids)
        return jsonify(names)
