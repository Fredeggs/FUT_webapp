from unicodedata import name
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Likes(db.Model):
    """Mapping user likes to teams."""

    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))

    team_id = db.Column(
        db.Integer, db.ForeignKey("teams.id", ondelete="cascade"), unique=True
    )


class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    teams = db.relationship("Team")
    likes = db.relationship("Team", secondary="likes")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Team(db.Model):
    """A Team made up of Players."""

    __tablename__ = "teams"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )

    formation = db.Column(
        db.String(20),
        nullable=False,
        default="4-4-2",
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user = db.relationship("User")

    players = db.relationship("Player", secondary="roster_assignments")


class Player(db.Model):
    """A Player to be used in a Team. Data is obtained from FUT_db."""

    __tablename__ = "players"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )

    nation_id = db.Column(db.Integer, db.ForeignKey("nations.id"), nullable=False)
    nation = db.relationship("Nation")

    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False)
    club = db.relationship("Club")

    rating = db.Column(db.Integer)

    pace = db.Column(db.Integer)

    shooting = db.Column(db.Integer)

    passing = db.Column(db.Integer)

    dribbling = db.Column(db.Integer)

    defending = db.Column(db.Integer)

    physicality = db.Column(db.Integer)


class Nation(db.Model):
    """A Nation - used as an attribute on the Player model"""

    __tablename__ = "nations"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )


class Club(db.Model):
    """A football Club - used as an attribute on the Player model"""

    __tablename__ = "clubs"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )


class RosterAssignment(db.Model):
    """Mapping Players to Teams."""

    __tablename__ = "roster_assignments"

    id = db.Column(db.Integer, primary_key=True)

    player_id = db.Column(db.Integer, db.ForeignKey("players.id", ondelete="cascade"))

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id", ondelete="cascade"),
    )


class Comments(db.Model):
    """Mapping user likes to teams."""

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))

    team_id = db.Column(
        db.Integer, db.ForeignKey("teams.id", ondelete="cascade"), unique=True
    )


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
