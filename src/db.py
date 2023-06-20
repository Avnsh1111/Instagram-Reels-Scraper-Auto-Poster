from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, select, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import config
from datetime import datetime

# Create the database engine
engine = create_engine('sqlite:///'+config.DB_PATH)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Add `checkfirst=True` to only create the table if it doesn't exist
Base.metadata.create_all(engine, checkfirst=True)

# Define a Reels model
class Reel(Base):
    __tablename__ = 'reels'

    id = Column(Integer, primary_key=True)
    post_id = Column(String)
    code = Column(String)
    account = Column(String)
    file_name = Column(String)
    file_path = Column(String)
    caption = Column(String)
    data = Column(String)
    is_posted = Column(Boolean)
    posted_at = Column(DateTime)

class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# Create the database schema
Base.metadata.create_all(engine)


class ReelEncoder(json.JSONEncoder):
    def default(self, obj):
        return {
            'pk': obj.pk,
            'id': obj.id,
            'code': obj.code,
            'taken_at': obj.taken_at.isoformat(),
            'media_type': obj.media_type,
            'image_versions2': obj.image_versions2,
            'product_type': obj.product_type,
            'thumbnail_url': obj.thumbnail_url,
            'location': obj.location,
            'comment_count': obj.comment_count,
            'comments_disabled': obj.comments_disabled,
            'commenting_disabled_for_viewer': obj.commenting_disabled_for_viewer,
            'like_count': obj.like_count,
            'play_count': obj.play_count,
            'has_liked': obj.has_liked,
            'caption_text': obj.caption_text,
            'video_url': obj.video_url,
            'view_count' : obj.view_count
        }
