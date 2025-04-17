from . import db, BaseMixin

# 分辨率与视频呈一对多关系
class Resolution(BaseMixin, db.Model):
    videos = db.relationship('Video', back_populates='resolution', lazy='select')