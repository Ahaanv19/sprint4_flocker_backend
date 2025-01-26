import logging
from sqlite3 import IntegrityError
from sqlalchemy import JSON
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.user import User
from model.channel import Channel

class Post(db.Model):
    """
    Post Model
    
    The Post class represents an individual contribution or discussion within a channel.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the post.
        _title (db.Column): A string representing the title of the post.
        _comment (db.Column): A string representing the comment of the post.
        _content (db.Column): A JSON blob representing the content of the post.
        _user_id (db.Column): An integer representing the user who created the post.
        _channel_id (db.Column): An integer representing the channel to which the post belongs.
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _comment = db.Column(db.String(255), nullable=False)
    _content = db.Column(JSON, nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)

    def __init__(self, title, comment, user_id=None, channel_id=None, content={}):
        self._title = title
        self._comment = comment
        self._user_id = user_id
        self._channel_id = channel_id
        self._content = content

    def __repr__(self):
        return f"Post(id={self.id}, title={self._title}, comment={self._comment}, content={self._content}, user_id={self._user_id}, channel_id={self._channel_id})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create post with title '{self._title}' due to {str(e)}.")
            return None
        return self
        
    def read(self):
        user = User.query.get(self._user_id)
        channel = Channel.query.get(self._channel_id)
        return {
            "id": self.id,
            "title": self._title,
            "comment": self._comment,
            "content": self._content,
            "user_name": user.name if user else None,
            "channel_name": channel.name if channel else None
        }
    
    def update(self, data):
        if 'title' in data:
            self._title = data['title']
        if 'comment' in data:
            self._comment = data['comment']
        if 'content' in data:
            self._content = data['content']
        if '_user_id' in data:
            self._user_id = data['_user_id']
        if '_channel_id' in data:
            self._channel_id = data['_channel_id']

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not update post with title '{self._title}' due to {str(e)}.")
            return None
        return self
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def restore(data, default_user_id=None, default_channel_id=None):
        """Restores posts from the provided data."""
        if not isinstance(data, list):
            logging.error("Provided data is not a list.")
            return
        
        for post_data in data:
            if not isinstance(post_data, dict):
                logging.warning("Post data is not a dictionary, skipping.")
                continue
            
            # Remove 'id' from post_data
            post_data.pop('id', None) 
            
            # Ensure required fields are present
            user_id = post_data.get("_user_id") or default_user_id
            channel_id = post_data.get("_channel_id") or default_channel_id
            title = post_data.get("_title")

            # Log missing fields with detailed post data
            if user_id is None:
                logging.warning(f"Missing _user_id in post data: {post_data}, skipping.")
                continue
            if channel_id is None:
                logging.warning(f"Missing _channel_id in post data: {post_data}, skipping.")
                continue
            if title is None:
                logging.warning(f"Missing title in post data: {post_data}, skipping.")
                continue
            
            # Create or update post
            post = Post.query.filter_by(_title=title).first()
            if post:
                post.update(post_data)
            else:
                post_data['_user_id'] = user_id  # Ensure _user_id is included
                post_data['_channel_id'] = channel_id  # Ensure _channel_id is included
                post = Post(**post_data)
                post.create()



def initPosts():
    with app.app_context():
        db.create_all()
        posts = [
            Post(title='Added Group and Channel Select', comment='The Home Page has a Section, on this page we can select Group and Channel to allow blog filtering', content={'type': 'announcement'}, _user_id=1, _channel_id=1),
            Post(title='JSON content saving through content field in database', comment='You could add other dialogs to a post that would allow custom data or even storing reference to uploaded images.', content={'type': 'announcement'}, _user_id=2, _channel_id=2),
            Post(title='Allows Post by different Users', comment='Different users seeing content is a key concept in social media.', content={'type': 'announcement'}, _user_id=3, _channel_id=3),
        ]
        
        for post in posts:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                db.session.rollback()
                print(f"Records exist, duplicate email, or error: {post._title}")
