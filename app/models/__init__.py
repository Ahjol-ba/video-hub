from app.extensions import db
from .base import BaseMixin
from .category import Category, video_category
from .tag import Tag, video_tag
from .region import Region
from .era import Era
from .resolution import Resolution
from .video import Video





__all__ ={
    'db',
    'Category'
    'Region',
    'Era',
    'Resolution',
    'Video',
    'Tag',
    'video_category',
    'video_tag'
}