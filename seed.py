"""Seed file to make sample data for users db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
user1 = User(first_name='Jen', last_name="Smith")
user2 = User(first_name='Bob', last_name="Miller")
user3 = User(first_name='George', last_name="Jones", image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwUThv_MaRDc9rf7o3Ckckq3KOsCHtfk2kqA&usqp=CAU")
user4 = User(first_name='Molly', last_name="Fender", image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwsriUZaKXkW-8UMog-eES8TcqOsUd1YRt4w&usqp=CAU")


# Add posts
post1 = Post(title='Fun day', content="This is what I did", user_id = 1)
post2 = Post(title='Another Day', content="I did this too", user_id = 1)
post3 = Post(title='Flask is awesome', content="It lets you build cool things", user_id = 3)
post4 = Post(title='Another Post', content="Here is the content", user_id = 3)
post5 = Post(title='First Post', content="Here we go", user_id = 4)


# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)

# Commit--otherwise, this never gets saved!
db.session.commit()

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.add(post5)

# Commit--otherwise, this never gets saved!
db.session.commit()
