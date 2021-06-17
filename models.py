"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User class """

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key = True, 
                   autoincrement = True)
    first_name = db.Column(db.String(50), 
                 nullable = False)
    last_name = db.Column(db.String(50), 
                nullable = False)
    image_url = db.Column(db.String, 
                nullable = True,
                default = "https://www.bsn.eu/wp-content/uploads/2016/12/user-icon-image-placeholder.jpg")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    posts = db.relationship('Post', backref="user", cascade="all, delete-orphan")



class Post(db.Model):
    """ Post class """

    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                   primary_key = True, 
                   autoincrement = True)
    title = db.Column(db.String(100), 
                 nullable = False)
    content = db.Column(db.String, 
                nullable = False)
    created_at = db.Column(db.DateTime, 
                nullable = False, 
                default = datetime.datetime.now())
    user_id = db.Column(db.Integer, 
              db.ForeignKey('users.id'), nullable = False)

    def get_date(self):
        days = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
        day_num = self.created_at.weekday()
        day = days[day_num]

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month = months[self.created_at.month]

        am_pm = 'AM' if self.created_at.hour < 12 else 'PM'
        hour =  self.created_at.hour - 12 if self.created_at.hour >= 12 else self.created_at.hour

        return f"{day} {month} {self.created_at.day}, {self.created_at.year}, {hour}:{self.created_at.minute} {am_pm}"

