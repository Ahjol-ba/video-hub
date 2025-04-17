from . import db, BaseMixin

# 关联表：视频与类别的多对多关系
video_category = db.Table('video_category',
    db.Column('video_id', db.Integer, db.ForeignKey('video.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Category(BaseMixin, db.Model):
    videos = db.relationship('Video', secondary=video_category, back_populates='categories')