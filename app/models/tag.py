from . import db, BaseMixin

# 关联表：视频与标签的多对多关系
video_tag = db.Table('video_tag',
    db.Column('video_id', db.Integer, db.ForeignKey('video.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(BaseMixin, db.Model):
    videos = db.relationship('Video', secondary=video_tag, back_populates='tags')
